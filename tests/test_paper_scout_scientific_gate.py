from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.config import QualityConfig, QualityFullTextConfig, load_config
from paper_scout.digest import write_digest
from paper_scout.full_text import ExtractedPage, FullTextDocument, SelectedPaperText, SelectedSection, locate_full_text_urls, select_assessment_text
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.publication import publication_status
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import _request_payload, validate_llm_quality_response
from paper_scout.quality_models import QUALITY_GATE_VERSION, REQUIRED_GATE_DIMENSIONS, QualityAssessment
from paper_scout.quality_service import assess_and_store_candidate
from paper_scout.site import build_site, _merge_two_papers, _load_library_papers
from paper_scout.state import PaperStore

ROOT = Path(__file__).resolve().parents[1]


def candidate(affiliation="Independent Researcher", **kwargs):
    return PaperCandidate("Persistent memory for LLM agents", ["Researcher"],
        "We evaluate persistent episodic memory for LLM agents with controlled memory retrieval experiments.",
        "arxiv", "fixture", arxiv_id="2601.00001", raw={"affiliation": affiliation}, **kwargs)


def manuscript():
    sections = [
        ("contribution_clarity", "Introduction", "We test whether temporal memory updates improve task retention in an LLM agent."),
        ("methodological_rigor", "Methods", "The memory uses a fixed 512-token budget; 200 held-out tasks use seeds 1 through 8."),
        ("evaluation_or_validation_strength", "Results", "Held-out retention is 74% versus 61% for retrieval-only; removing updates yields 62%."),
        ("evidence_to_claim_alignment", "Discussion", "The results support retention on these tasks only; no general intelligence claim is made."),
        ("related_work_and_gap_positioning", "Comparisons", "Retrieval-only and no-update controls use the same model, prompts, tasks and token budget."),
        ("limitations_and_uncertainty_handling", "Limitations", "Only one model and eight seeds were tested; task transfer and long-horizon behavior remain unknown."),
    ]
    selected = SelectedPaperText("\n".join(s[2] for s in sections),
        [SelectedSection(s[1], s[2], i+2) for i,s in enumerate(sections)],
        "partial_full_text", "fixture-manuscript-hash", False)
    response = {
        "quality_status":"pass", "quality_rationale":"Matched-budget comparisons and ablations support scoped retention claims.",
        "quality_uncertainty":"One model and eight seeds; broader transfer is untested.",
        "overall_quality_score":80, "confidence":"medium", "paper_type":"empirical_research",
        "evidence":[{"dimension":s[0], "signal_type":"positive", "paraphrase":s[2],
                    "explanation":"Located manuscript evidence supports the scoped criterion.",
                    "section":s[1], "page":i+2, "excerpt":s[2]} for i,s in enumerate(sections)],
    }
    return selected, response


def assessment(c=None, key="fixture", status="pass"):
    c = c or candidate()
    text, response = manuscript()
    if status == "insufficient":
        response["quality_status"] = "insufficient"
        response["quality_rationale"] = "The empirical claim is unsupported by this explicitly unevaluated method."
        response["evidence"][0]["signal_type"] = "concern"
    return validate_llm_quality_response(response, assess_quality_deterministically(c,key,text), "fixture-reviewer", selected=text)


class ScientificGateTest(unittest.TestCase):
    def test_affiliation_invariance_and_identity_omission(self):
        text,response = manuscript()
        decisions=[]
        for name in ("University", "Company", "Independent Researcher"):
            c=candidate(name)
            result=assessment(c)
            decisions.append((result.quality_status,result.quality_rationale,result.dimension_scores))
            payload=_request_payload(c,text,assess_quality_deterministically(c,"fixture",text),"test")
            supplied=json.loads(payload["messages"][1]["content"])["paper"]
            self.assertNotIn("authors", supplied)
            self.assertNotIn(name, json.dumps(supplied))
        self.assertEqual(decisions[0],decisions[1])
        self.assertEqual(decisions[1],decisions[2])
        self.assertEqual(decisions[0][0],"pass")

    def test_doi_repository_and_peer_review_are_not_quality_signals(self):
        for doi in (None,"10.5281/zenodo.123","10.1234/example"):
            c=replace(candidate(),source="zenodo",arxiv_id=None,doi=doi,raw={})
            self.assertEqual(publication_status(c).status,"repository_only")
            self.assertEqual(assess_quality_deterministically(c,"fixture").quality_status,"uncertain")
        c=replace(candidate(),arxiv_id=None,source="openalex",doi="10.1234/example",raw={})
        self.assertEqual(publication_status(c).status,"unknown")
        c=replace(c,raw={"primary_location":{"is_published":True,"source":{"type":"journal","display_name":"Example Journal"}}})
        self.assertEqual(publication_status(c).status,"peer_reviewed")
        self.assertNotEqual(assess_quality_deterministically(c,"fixture").quality_status,"pass")

    def test_strong_independent_preprint_and_repository_can_pass(self):
        for source,arxiv in (("arxiv","2601.00001"),("zenodo",None)):
            c=replace(candidate(),source=source,arxiv_id=arxiv)
            a=assessment(c)
            self.assertEqual(a.quality_status,"pass")
            self.assertTrue(a.full_text_assessed)

    def test_weak_institutional_manuscript_can_be_insufficient(self):
        text,response=manuscript()
        weak="We assert better retention, but no evaluation was performed; all results await future work."
        text=replace(text,text=weak,sections=[SelectedSection("Results",weak,4)])
        response.update(quality_status="insufficient",quality_rationale="The manuscript explicitly defers all validation of its comparative claim.")
        response["evidence"]=[{"dimension":"evaluation_or_validation_strength","signal_type":"concern", "paraphrase":"Validation is deferred.","explanation":"An explicit unsupported comparative claim.","page":4,"section":"Results","excerpt":weak}]
        for affiliation in ("University", "Company", "Independent Researcher"):
            c=candidate(affiliation)
            a=validate_llm_quality_response(response,assess_quality_deterministically(c,"fixture",text),"test",selected=text)
            self.assertEqual(a.quality_status,"insufficient")

    def test_abstract_marketing_missing_and_fabricated_evidence_cannot_pass(self):
        text,response=manuscript()
        c=candidate()
        abstract=select_assessment_text(replace(c,abstract=text.text),None)
        for selected in (abstract, None):
            a=validate_llm_quality_response(response,assess_quality_deterministically(c,"fixture",abstract),"test",selected=selected)
            self.assertEqual(a.quality_status,"uncertain")
        response["evidence"][0]["excerpt"]="An invented result absent from the manuscript."
        a=validate_llm_quality_response(response,assess_quality_deterministically(c,"fixture",text),"test",selected=text)
        self.assertEqual(a.quality_status,"uncertain")

    def test_deterministic_full_text_cannot_promote_keywords(self):
        text,_=manuscript()
        self.assertEqual(assess_quality_deterministically(candidate(),"fixture",text).quality_status,"uncertain")

    def test_numeric_curation_does_not_manufacture_manuscript_review(self):
        from paper_scout.curation import QualityCuration
        from paper_scout.quality_service import _apply_manual_curation
        text, _ = manuscript()
        diagnostic = assess_quality_deterministically(candidate(), "fixture", text)
        override = QualityCuration(quality_score_override=99)
        curated = _apply_manual_curation(diagnostic, override)
        self.assertEqual(curated.quality_status, "uncertain")
        self.assertFalse(curated.full_text_assessed)
        for status in ("pass", "uncertain"):
            reviewed = replace(assessment(), quality_status=status)
            curated = _apply_manual_curation(reviewed, override)
            self.assertTrue(curated.full_text_assessed)
            self.assertEqual(curated.assessor_model, reviewed.assessor_model)

    def test_each_core_dimension_is_required(self):
        text,full=manuscript()
        for dimension in REQUIRED_GATE_DIMENSIONS:
            response={**full,"evidence":[e for e in full["evidence"] if e["dimension"]!=dimension]}
            a=validate_llm_quality_response(response,assess_quality_deterministically(candidate(),"fixture",text),"test",selected=text)
            self.assertEqual(a.quality_status,"uncertain",dimension)

    def test_legacy_assessments_remain_unassessed_and_round_trip(self):
        a=assessment(); data=a.to_dict()
        for key in ("quality_status","quality_gate_version","quality_rationale","quality_uncertainty"):
            data.pop(key)
        for assessor in ("deterministic","llm","manual_override"):
            old=QualityAssessment.from_dict({**data,"assessor_type":assessor})
            self.assertEqual(old.quality_status,"not_assessed")
            self.assertEqual(old.overall_quality_score,a.overall_quality_score)
        self.assertEqual(QualityAssessment.from_dict(a.to_dict()),a)

    def test_site_gate_all_tracks_and_curation_cannot_bypass(self):
        for track in ("agent_memory","deep_research","engram"):
            with self.subTest(track=track), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); store=PaperStore(root/"state.sqlite3")
                digests=root/"digests"; digests.mkdir()
                write_digest(digests/"2026-09-16.md","2026-09-16",[])
                ids={}
                for status in ("pass","not_assessed","uncertain","insufficient"):
                    c=replace(candidate(),title=f"{status} persistent agent memory",source_id=status,arxiv_id=None)
                    key=store.upsert_paper(c,ClassificationResult(90,"relevant","Core topical match"))
                    ids[status]=key
                    if status != "not_assessed":
                        a=assessment(c,key,status=status)
                        if status=="uncertain": a=replace(a,quality_status="uncertain")
                        store.save_quality_assessment(a)
                curator=root/"curation.yaml"
                curator.write_text("pinned:\n  - title: insufficient persistent agent memory\noverrides:\n  - title: not_assessed persistent agent memory\n    quality_score_override: 99\n    include_despite_quality: true\n")
                # Isolate gate policy from each track's independently tested classifier.
                with patch("paper_scout.site._refresh_rule_classifications",side_effect=lambda p,**k:p):
                    build_site(digests,root/"reports",root/"docs",root/"state.sqlite3",curator,
                               build_time="2026-09-16T12:00:00+00:00",relevance_profile=track,enrich_dates=False)
                index=(root/"docs/index.html").read_text();review=(root/"docs/review.html").read_text()
                self.assertIn('data-title="pass persistent agent memory"',index)
                for status in ("not_assessed","uncertain","insufficient"):
                    self.assertNotIn(f'data-title="{status} persistent agent memory"',index)
                self.assertIn('data-title="not_assessed persistent agent memory"',review)
                self.assertIn('data-title="uncertain persistent agent memory"',review)
                self.assertNotIn('data-title="insufficient persistent agent memory"',review)
                records=json.loads((root/"docs/data/papers.json").read_text())
                self.assertEqual(len(records),4)
                report=json.loads((root/"reports/library-quality-2026-09-16.json").read_text())
                self.assertEqual(report["main_library"],1)
                self.assertEqual(report["quality_statuses"],dict.fromkeys(("pass","uncertain","insufficient","not_assessed"),1))

    def test_merge_preserves_assessment_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=PaperStore(Path(tmp)/"state.sqlite3")
            c=candidate(); key=store.upsert_paper(c,ClassificationResult(90,"relevant","Core"))
            store.save_quality_assessment(assessment(c,key))
            p=_load_library_papers(Path(tmp)/"state.sqlite3")[0]
            merged=_merge_two_papers(p,replace(p,canonical_id="other",score=50,quality_status="not_assessed"))
            self.assertEqual(merged.quality_status,"pass")
            self.assertEqual(merged.quality_source_content_hash,p.quality_source_content_hash)

    def test_zenodo_fixture_uses_retrieved_metadata_and_located_content(self):
        v=json.loads((ROOT/"config/fixtures/zenodo-22735829.json").read_text());m=v["metadata"]
        c=PaperCandidate(m["title"],[x["name"] for x in m["creators"]],m["description"],"zenodo",str(v["id"]),doi=v["doi"],raw=v)
        self.assertIsNone(m["creators"][0]["affiliation"])
        self.assertEqual(m["resource_type"]["subtype"],"preprint")
        self.assertNotIn("stats",v)
        self.assertEqual(publication_status(c).status,"repository_only")
        self.assertEqual(locate_full_text_urls(c),[v["files"][0]["links"]["self"]])
        self.assertEqual(assess_quality_deterministically(c,"fixture").quality_status,"uncertain")
        sections=[SelectedSection(e["section"],e["excerpt"],e["page"]) for e in v["manuscript_excerpts"]]
        text=SelectedPaperText("\n".join(s.text for s in sections),sections,"partial_full_text",v["manuscript_sha256"],False)
        response={"quality_status":"pass","quality_rationale":v["inspection"]["rationale"],"quality_uncertainty":v["inspection"]["uncertainty"],"confidence":"medium","overall_quality_score":75,"paper_type":"systems_or_application","evidence":[{**{k:e[k] for k in ("dimension","page","section","excerpt")},"signal_type":"positive","paraphrase":e["conclusion"],"explanation":"Manuscript inspected on 2026-09-16; conclusions limited to reported scope."} for e in v["manuscript_excerpts"]]}
        result=validate_llm_quality_response(response,assess_quality_deterministically(c,"fixture",text),"fixture-manuscript-review",selected=text)
        self.assertEqual(result.quality_status,"pass")
        self.assertEqual(v["inspection"]["relevance"]["agent_memory"],"review_candidate")

    def test_backfill_rejects_unbounded_or_ambiguous_import(self):
        from paper_scout.cli import main
        for args in (["--limit","51"],["--limit","0"],["--assessment-json","missing.json"],["--pdf-url","https://example.org/paper.pdf"]):
            with self.assertRaises(SystemExit) as exc:
                main(["reassess-quality",*args])
            self.assertEqual(exc.exception.code,2)


    def test_extraction_retains_architecture_page_continuations_and_actual_bounds(self):
        pages=[ExtractedPage(1,"1 Architecture\nThe method defines fixed feature bins and memory update rules."),
               ExtractedPage(2,"The update decay is 0.88 and reward is one on success.\n2 Experimental Protocol\nWe evaluate on held-out tasks with matched seeds."),
               ExtractedPage(3,"3 Results\nThe held-out hit rate is 0.974.\n4 Limitations\nOnly one task family is tested.")]
        doc=FullTextDocument("https://example.org/paper.pdf",pages,"pdfhash",True)
        text=select_assessment_text(candidate(),doc)
        self.assertTrue(any(s.heading=="Architecture" and s.first_page==2 for s in text.sections))
        self.assertIn("held-out tasks",text.text)
        truncated=select_assessment_text(candidate(),doc,max_prompt_characters=100)
        self.assertEqual(truncated.scope,"partial_full_text")
        self.assertLessEqual(len(truncated.text),100)

    def test_review_import_is_versioned_and_routine_reassessment_preserves_it(self):
        text,response=manuscript()
        with tempfile.TemporaryDirectory() as tmp:
            store=PaperStore(Path(tmp)/"state.sqlite3"); c=candidate()
            classification=ClassificationResult(90,"relevant","Core")
            key=store.upsert_paper(c,classification)
            config=QualityConfig(enabled=True,mode="deterministic",full_text=QualityFullTextConfig(enabled=False))
            with patch("paper_scout.quality_service.select_assessment_text",return_value=text):
                first=assess_and_store_candidate(config,store,c,key,classification,manual_assessment=response)
                self.assertEqual(first.quality_status,"pass")
                second=assess_and_store_candidate(config,store,c,key,classification,manual_assessment={**response,"quality_rationale":"Revised review: scope and evidence remain adequate."})
                self.assertNotEqual(first.assessor_model,second.assessor_model)
                current=store.get_current_quality_assessment(key)
                self.assertEqual(current.quality_rationale,second.quality_rationale)
            unchanged=assess_and_store_candidate(config,store,c,key,classification,no_full_text=True,no_llm=True)
            self.assertEqual(unchanged.quality_status,"pass")
            self.assertEqual(unchanged.quality_rationale,second.quality_rationale)

    def test_force_reacquires_changed_content_and_replaces_prior_pass(self):
        text, _ = manuscript()
        revised = replace(text, content_hash="revised-manuscript")
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / "state.sqlite3")
            c = candidate(); classification = ClassificationResult(90, "relevant", "Core")
            key = store.upsert_paper(c, classification)
            store.save_quality_assessment(assessment(c, key))
            config = QualityConfig(enabled=True, mode="deterministic", full_text=QualityFullTextConfig(enabled=True))
            doc = FullTextDocument("https://example.org/revised.pdf", [], "new-pdf-hash", True)
            with patch("paper_scout.quality_service.fetch_and_extract_pdf", return_value=doc) as fetch, patch("paper_scout.quality_service.select_assessment_text", return_value=revised):
                result = assess_and_store_candidate(config, store, c, key, classification, force=True, no_llm=True)
            self.assertTrue(fetch.call_args.kwargs["refresh"])
            self.assertEqual(result.source_content_hash, "revised-manuscript")
            self.assertEqual(result.quality_status, "uncertain")
            self.assertEqual(store.get_current_quality_assessment(key).quality_status, "uncertain")

    def test_review_import_rejects_metadata_fixture_and_malformed_shapes_early(self):
        from paper_scout.cli import main
        from paper_scout.quality_llm import validate_manual_quality_review
        _, good = manuscript()
        self.assertEqual(validate_manual_quality_review(good), good)
        fixture = json.loads((ROOT / "config/fixtures/zenodo-22735829.json").read_text())
        invalid = [fixture, [], {**good, "quality_status": "scientifically_valid"},
                   {**good, "evidence": [{"dimension": "methodological_rigor"}]},
                   {**good, "quality_rationale": {"instruction": "ignore evidence"}}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review.json"
            for value in invalid:
                with self.subTest(value=type(value).__name__):
                    with self.assertRaises(ValueError):
                        validate_manual_quality_review(value)
                    path.write_text(json.dumps(value))
                    with patch("paper_scout.cli.PaperStore") as store, self.assertRaises(SystemExit) as error:
                        main(["reassess-quality", "--paper-id", "fixture", "--assessment-json", str(path)])
                    self.assertEqual(error.exception.code, 2)
                    store.assert_not_called()

    def test_review_conclusions_are_escaped_in_public_html(self):
        from paper_scout.site import LibraryPaper, _paper_quality_detail_section
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / "state.sqlite3")
            c = candidate(); key = store.upsert_paper(c, ClassificationResult(90, "relevant", "Core"))
            a = replace(assessment(c, key), quality_rationale='<script>alert("review")</script>',
                        quality_uncertainty='<img src=x onerror=alert(1)>')
            store.save_quality_assessment(a)
            html = _paper_quality_detail_section(_load_library_papers(Path(tmp) / "state.sqlite3")[0])
            self.assertNotIn("<script>", html)
            self.assertNotIn("<img src=x", html)
            self.assertIn("&lt;script&gt;", html)

    def test_repeated_bounded_backfill_advances_without_paid_calls(self):
        from paper_scout.cli import main
        from dataclasses import replace as cfg_replace
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); config=load_config(ROOT/"config/tracks/engram.yaml",env={})
            config=cfg_replace(config,sqlite_path=root/"state.sqlite3",report_dir=root/"reports",curation_path=root/"absent.yaml")
            store=PaperStore(config.sqlite_path)
            for i in range(3):
                c=replace(candidate(),title=f"Paper {i}",source_id=str(i),arxiv_id=None)
                store.upsert_paper(c,ClassificationResult(90,"relevant","Core"))
            with patch("paper_scout.cli.load_config",return_value=config), patch("paper_scout.quality_llm.openai_compatible_settings_from_env",side_effect=AssertionError("No model use")):
                for n in (1,2,3,3):
                    self.assertEqual(main(["reassess-quality","--track","engram","--limit","1","--no-llm"]),0)
                    self.assertEqual(len(store.list_current_quality_assessments()),n)
                self.assertEqual(main(["reassess-quality", "--track", "engram", "--limit", "1", "--no-llm", "--rubric-version", "revised-rubric"]), 0)
                self.assertEqual(sum(a.rubric_version == "revised-rubric" for a in store.list_current_quality_assessments()), 1)
