# Paper Scout scholarly-quality report - 2026-09-16

> Advisory automated assessment. Relevance and scholarly quality are independent, and human review remains necessary.

## Summary

- Papers assessed or reused: 10
- Scientific quality statuses: pass: 4, uncertain: 6
- Publication statuses: peer_reviewed: 2, preprint: 7, repository_only: 1
- Repository-only manuscripts inspected: 0
- Assessment scopes: full_text: 2, partial_full_text: 6, title_and_abstract: 2
- Confidence: high: 2, low: 2, medium: 6
- Recommendations: promising: 5, strong: 1, uncertain: 3, weak: 1
- Score distribution: 40-49: 2, 50-59: 2, 70-79: 5, 80-89: 1
- Assessor types: deterministic: 2, llm: 5, manual_override: 3
- Papers downranked: 0
- Papers hidden: 0
- Assessments with score caps: 0
- Assessment failures: 0
- Extraction failures: 0
- Cache hits / misses: 8 / 2
- Assessment version: `quality-recovery-v1`
- Rubric version: `scholarly-rubric-v1`

## Per-paper assessment

### `doi:10.1002/advs.76675`

- Scientific quality: uncertain
- Rationale: Scientific quality remains uncertain because the supplied assessment excerpts truncate key Methods, Results and Discussion passages. The original model insufficient proposal relied on that missing input and is not a valid adverse scientific decision.
- Uncertainty: The public Europe PMC manuscript XML was acquired, but the bounded context does not expose enough detail to resolve the scientific judgment. Logical XML section numbers are not PDF pages.
- Full text inspected: True; source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13573717/fullTextXML
- Automated score: 54
- Recommendation: weak
- Confidence / scope: medium / partial_full_text
- Paper type: systems_or_application
- Summary: Scientific quality remains uncertain because the supplied assessment excerpts truncate key Methods, Results and Discussion passages. The original model insufficient proposal relied on that missing input and is not a valid adverse scientific decision.
- Main concerns: The available results appear to demonstrate functionality rather than comparative effectiveness.
- Positive signals: The available text identifies data or a benchmark used by the work.; A baseline or comparison system is described.

### `doi:10.48550/arxiv.2609.11243`

- Scientific quality: uncertain
- Rationale: The proposed decision lacked sufficient located manuscript evidence; review is pending.
- Uncertainty: Full-text evidence is required for contribution, methods, validation, comparisons or their justified absence, claim alignment, and limitations.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.11243
- Automated score: 85
- Recommendation: strong
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The available evidence suggests a clearly supported scholarly contribution. Automated score 85/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.48550/arxiv.2609.10922`

- Scientific quality: pass
- Rationale: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. Auto-RecSys presents a well-motivated systems contribution for autonomous experimentation on industry-scale recommendation models. The architecture is clearly described, and the evaluation provides quantitative evidence of improved execution reliability and qualitative evidence of robust recovery. However, the evaluation is limited in scale and lacks statistical rigor, and the scientific value of generated ideas is not directly validated. Overall, the paper is a credible systems contribution with clear limitations.
- Uncertainty: Limited 31-iteration systems evidence, no statistical causal estimate, no direct validation of generated research ideas, and no formal playbook-update validation gate. The original rejected proposal rationale was not retained by the prior validator; this audit uses its preserved summary, explanations and exact quotes, and is explicitly a manual override rather than a new model assessment.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.10922
- Automated score: 78
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: systems_or_application
- Summary: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. Auto-RecSys presents a well-motivated systems contribution for autonomous experimentation on industry-scale recommendation models. The architecture is clearly described, and the evaluation provides quantitative evidence of improved execution reliability and qualitative evidence of robust recovery. However, the evaluation is limited in scale and lacks statistical rigor, and the scientific value of generated ideas is not directly validated. Overall, the paper is a credible systems contribution with clear limitations.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.6082/mgmw1-gw451`

- Scientific quality: uncertain
- Rationale: The paper is a position/conceptual argument for making a theory of scientific value foundational to AI-for-science. It develops a substantive conceptual framework with formal illustrations (Bell-test loophole closure, Blackwell comparisons, potential-based rewards) and engages alternative views, but it does not empirically validate the proposed theory or demonstrate that the framework can be operationalized in AI systems. The central claims are argued rather than tested, and the paper explicitly frames the work as a research agenda, so the contribution is plausible and well-articulated but not yet established.
- Uncertainty: The manuscript is a preprint and the extracted text appears to omit some sections or tables (e.g., Table 1 is truncated, some section transitions are abrupt), so the assessment may not reflect the complete argument. Because the paper is a position piece, the absence of empirical validation is expected, but the strength of the contribution depends on whether the proposed formal apparatus can be made checkable and useful in practice, which the paper only sketches.
- Full text inspected: True; source: https://knowledge.uchicago.edu/records/mgmw1-gw451/files/AI_Scientists_Need_a_Theory_of_Scientific_Value.pdf?download=1
- Automated score: 56
- Recommendation: uncertain
- Confidence / scope: high / full_text
- Paper type: position_or_conceptual
- Summary: This position paper argues that AI-for-science should treat a theory of scientific value as a foundational research task. It offers a clear conceptual framework, formal illustrations, and engagement with alternative views, but it does not empirically validate the proposal or demonstrate operational feasibility. The contribution is plausible and well-articulated but remains a research agenda rather than an established result.
- Main concerns: Comparative claims were detected without a suitable baseline in the available text.; The paper does not empirically test or implement the proposed theory of scientific value, leaving the practical feasibility of checkable value judgments unvalidated.; The formal apparatus is presented as a sketch; no complete derivation or worked end-to-end example is provided for the proposed judgment form.
- Positive signals: The available text identifies data or a benchmark used by the work.; Quantitative evaluation signals were detected.

### `doi:10.48550/arxiv.2609.07611`

- Scientific quality: pass
- Rationale: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. The available evidence suggests a credible contribution with some limitations. Automated score 77/100, medium confidence, based on partial full text.
- Uncertainty: All dimension scores are LLM judgments; expert novelty validation is absent. Active mode bundles retrieval, turns and tool competence; the exploratory generation-time result is unconfirmed. The original rejected proposal rationale was not retained by the prior validator; this audit uses its preserved summary, explanations and exact quotes, and is explicitly a manual override rather than a new model assessment.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.07611
- Automated score: 77
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: dataset_or_benchmark
- Summary: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. The available evidence suggests a credible contribution with some limitations. Automated score 77/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.48550/arxiv.2609.07655`

- Scientific quality: pass
- Rationale: The paper presents a clearly formulated contribution (online surrogate repair) with explicit claims, a well-defined problem setting, and a systematic experimental design across static, synthetic, and MADE benchmark settings. The central claims are supported by quantitative results, including comparisons against multiple baselines and ablations, and the manuscript includes a limitations section. Methodological choices are described in sufficient detail to assess the validity of the main claims, and related work is positioned adequately for the stated scope.
- Uncertainty: Some uncertainty remains because the paper is a preprint and the full text includes only partial sections; however, the supplied material contains enough substantive evidence across all six required dimensions to support a pass.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.07655
- Automated score: 78
- Recommendation: promising
- Confidence / scope: high / full_text
- Paper type: empirical_research
- Summary: The paper presents online surrogate repair (OSR), a closed-loop algorithm that uses sparse high-fidelity evaluations to update a surrogate during a longer agent search. The contribution is clearly stated, the methodology is described in detail, and the evaluation includes controlled synthetic worlds and the MADE benchmark with multiple baselines. The claims are supported by quantitative results, and limitations are acknowledged.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.64898/2026.09.03.749176`

- Scientific quality: uncertain
- Rationale: The manuscript reports a multi-case evaluation of five AI research frameworks on two biopharmaceutical tasks, with explicit comparisons to reference studies and detailed qualitative and quantitative observations. The available partial text supports a credible empirical evaluation, but several central claims depend on intermediate files, full results tables, and appendices that are not fully supplied, so the strength of validation and reproducibility cannot be fully established from the extracted material alone.
- Uncertainty: The supplied text is partial full text with missing portions of the Results, Methods, and Appendix. Claims about fabricated datasets, hallucinated citations, and numerical irreproducibility are asserted but the underlying evidence is only partially visible. The absence of complete results tables and intermediate-file documentation limits confidence in the evaluation's completeness.
- Full text inspected: True; source: https://www.biorxiv.org/content/biorxiv/early/2026/09/07/2026.09.03.749176.full.pdf
- Automated score: 72
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: This empirical study evaluates five AI research frameworks on antibody developability prediction and lipid-RNA MD simulation tasks, finding partial successes but severe failures, narrower scope, and irreproducibility compared with published reference studies. The available text supports a credible comparative evaluation, though incomplete results and intermediate evidence limit full verification.
- Main concerns: The extracted text does not include complete results tables or intermediate-file evidence supporting all claims of hallucination and fabrication.; The paper relies on qualitative judgments about scope and depth that are only partially quantified in the supplied text.; The reproducibility of the evaluation itself is limited by the absence of full prompts and complete run-level data in the extracted material.
- Positive signals: The available text identifies data or a benchmark used by the work.; A baseline or comparison system is described.

### `doi:10.17605/osf.io/qm2c3`

- Scientific quality: uncertain
- Rationale: Scientific quality could not be assessed because manuscript-level evidence was unavailable.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: not recorded
- Automated score: 42
- Recommendation: uncertain
- Confidence / scope: low / title_and_abstract
- Paper type: replication
- Summary: The available evidence is mixed or incomplete. Automated score 42/100, low confidence, based on title and abstract.
- Positive signals: The available text identifies data or a benchmark used by the work.

### `doi:10.1016/j.nxnano.2026.100728`

- Scientific quality: uncertain
- Rationale: Scientific quality could not be assessed because manuscript-level evidence was unavailable.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: not recorded
- Automated score: 43
- Recommendation: uncertain
- Confidence / scope: low / title_and_abstract
- Paper type: survey_or_review
- Summary: The available evidence is mixed or incomplete. Automated score 43/100, low confidence, based on title and abstract.
- Positive signals: The available text identifies data or a benchmark used by the work.; Limitations or threats to validity are acknowledged.

### `doi:10.48550/arxiv.2609.11318`

- Scientific quality: pass
- Rationale: The paper presents a clearly scoped benchmark contribution with explicit construction principles, a defined evaluation protocol, and empirical results across 25 systems. The central claims are supported by quantitative evidence in the supplied text, including main results, an image ablation with bootstrap confidence intervals, checklist-length analysis, and failure-mode diagnostics. The authors explicitly distinguish what the metrics do and do not measure, and limitations are acknowledged. The related-work section positions Mr.LHDR against representative benchmarks and explains the gap it addresses. The available partial text is sufficient to establish substantive manuscript evidence for the six required dimensions.
- Uncertainty: The assessment is based on partial full text limited to 120,000 characters, so some appendix-level details, complete judge robustness analyses, and full split-level results are not available. Confidence intervals for many system comparisons overlap, and the authors themselves note that most per-model differences are not statistically separable. These factors limit the strength of ranking claims but do not undermine the benchmark contribution itself.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.11318
- Automated score: 77
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: dataset_or_benchmark
- Summary: The paper introduces Mr.LHDR, a benchmark for long-horizon multimodal deep research with 102 items constructed from hidden Node-Relation graphs. It defines OA, SA, CS, and DACS metrics and evaluates 25 systems, finding that final-answer accuracy overstates dependency-consistent task success. The contribution is clearly scoped, the methodology is described with validation gates, and the central claims are supported by quantitative evidence including an image ablation and failure-mode analysis. Limitations are acknowledged, and the related-work positioning is adequate for the benchmark's claims.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.
