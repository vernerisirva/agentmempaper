import json
import unittest

from paper_scout.enrichment import (
    DateEnrichmentDiagnostics,
    enrich_candidate_publication_date,
    extract_ssrn_id,
    infer_ssrn_doi,
)
from paper_scout.http import HttpRequestError
from paper_scout.models import PaperCandidate


SSRN_HTML = """
<html>
  <head>
    <meta name="citation_title" content="Toward Fully Autonomous and Scalable AI Agent Systems">
    <meta name="citation_publication_date" content="2026/04/15">
  </head>
  <body>
    <h1>Toward Fully Autonomous and Scalable AI Agent Systems</h1>
    <p>Date Written: April 15, 2026</p>
    <a href="https://doi.org/10.2139/ssrn.6584998">DOI</a>
  </body>
</html>
"""


class FakeHttp:
    def __init__(self, responses=None, errors=None):
        self.responses = responses or {}
        self.errors = errors or {}
        self.calls = []

    def get_text(self, url, params=None, headers=None):
        self.calls.append((url, params, headers))
        key = url if params is None else f"{url}?{json.dumps(params, sort_keys=True)}"
        if key in self.errors:
            raise self.errors[key]
        if url in self.errors:
            raise self.errors[url]
        if key in self.responses:
            return self.responses[key]
        return self.responses[url]


class PaperScoutEnrichmentTest(unittest.TestCase):
    def test_extracts_ssrn_id_from_url_and_doi(self):
        self.assertEqual(extract_ssrn_id("https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6584998"), "6584998")
        self.assertEqual(extract_ssrn_id("10.2139/ssrn.6584998"), "6584998")

    def test_infers_ssrn_doi_from_landing_page_url(self):
        self.assertEqual(infer_ssrn_doi("https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6584998"), "10.2139/ssrn.6584998")

    def test_ssrn_html_date_written_beats_year_only_metadata(self):
        candidate = PaperCandidate(
            title="Toward Fully Autonomous and Scalable AI Agent Systems",
            authors=["Agent Author"],
            abstract="Autonomous AI agent systems.",
            source="semantic_scholar",
            source_id="ssrn-year",
            url="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6584998",
            published_date="2026",
            publication_year="2026",
            publication_date_precision="year",
            publication_date_source="semantic_scholar",
        )
        diagnostics = DateEnrichmentDiagnostics()
        enriched = enrich_candidate_publication_date(
            candidate,
            http=FakeHttp({"https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6584998": SSRN_HTML}),
            diagnostics=diagnostics,
        )

        self.assertEqual(enriched.published_date, "2026-04-15")
        self.assertEqual(enriched.publication_year, "2026")
        self.assertEqual(enriched.publication_date_precision, "day")
        self.assertEqual(enriched.publication_date_source, "ssrn")
        self.assertEqual(enriched.publication_date_confidence, "high")
        self.assertEqual(enriched.doi, "10.2139/ssrn.6584998")
        self.assertEqual(enriched.raw["ssrn_id"], "6584998")
        self.assertEqual(diagnostics.warnings, [])

    def test_ssrn_403_does_not_fail_and_records_warning(self):
        candidate = PaperCandidate(
            title="Toward Fully Autonomous and Scalable AI Agent Systems",
            authors=[],
            abstract="",
            source="openalex",
            source_id="ssrn-blocked",
            url="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6584998",
            published_date="2026",
            publication_year="2026",
            publication_date_precision="year",
            publication_date_source="openalex",
        )
        diagnostics = DateEnrichmentDiagnostics()
        enriched = enrich_candidate_publication_date(
            candidate,
            http=FakeHttp(errors={"https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6584998": HttpRequestError("http", candidate.url or "", "HTTP Error 403: Forbidden")}),
            diagnostics=diagnostics,
        )

        self.assertEqual(enriched.published_date, "2026")
        self.assertTrue(any("SSRN enrichment failed" in warning and "6584998" in warning for warning in diagnostics.warnings))

    def test_crossref_published_date_fallback(self):
        candidate = PaperCandidate(
            title="Crossref Agent Memory Paper",
            authors=[],
            abstract="",
            source="openalex",
            source_id="crossref",
            doi="10.2139/ssrn.6584998",
            published_date="2026",
            publication_year="2026",
            publication_date_precision="year",
            publication_date_source="openalex",
        )
        payload = json.dumps({"message": {"published-online": {"date-parts": [[2026, 4, 16]]}}})
        enriched = enrich_candidate_publication_date(
            candidate,
            http=FakeHttp({"https://api.crossref.org/works/10.2139%2Fssrn.6584998": payload}),
            diagnostics=DateEnrichmentDiagnostics(),
        )

        self.assertEqual(enriched.published_date, "2026-04-16")
        self.assertEqual(enriched.publication_date_precision, "day")
        self.assertEqual(enriched.publication_date_source, "crossref-published-online")
        self.assertEqual(enriched.publication_date_confidence, "medium")

    def test_crossref_created_date_is_lower_confidence(self):
        candidate = PaperCandidate(
            title="Crossref Created Agent Memory Paper",
            authors=[],
            abstract="",
            source="openalex",
            source_id="crossref-created",
            doi="10.1000/example",
            published_date=None,
        )
        payload = json.dumps({"message": {"created": {"date-parts": [[2026, 5, 2]]}}})
        enriched = enrich_candidate_publication_date(
            candidate,
            http=FakeHttp({"https://api.crossref.org/works/10.1000%2Fexample": payload}),
            diagnostics=DateEnrichmentDiagnostics(),
        )

        self.assertEqual(enriched.published_date, "2026-05-02")
        self.assertEqual(enriched.publication_date_source, "crossref-created")
        self.assertEqual(enriched.publication_date_confidence, "low")


if __name__ == "__main__":
    unittest.main()
