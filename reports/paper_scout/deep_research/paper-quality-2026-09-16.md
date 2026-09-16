# Paper Scout scholarly-quality report - 2026-09-16

> Advisory automated assessment. Relevance and scholarly quality are independent, and human review remains necessary.

## Summary

- Papers assessed or reused: 10
- Scientific quality statuses: pass: 1, uncertain: 9
- Publication statuses: peer_reviewed: 2, preprint: 7, repository_only: 1
- Repository-only manuscripts inspected: 0
- Assessment scopes: full_text: 1, partial_full_text: 6, title_and_abstract: 3
- Confidence: high: 1, low: 3, medium: 6
- Recommendations: promising: 5, uncertain: 5
- Score distribution: 40-49: 3, 50-59: 1, 60-69: 1, 70-79: 5
- Assessor types: deterministic: 8, llm: 2
- Papers downranked: 0
- Papers hidden: 0
- Assessments with score caps: 0
- Assessment failures: 5
- Extraction failures: 7
- Cache hits / misses: 7 / 3
- Assessment version: `quality-v2`
- Rubric version: `scholarly-rubric-v1`

## Per-paper assessment

### `doi:10.1002/advs.76675`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: not recorded
- Automated score: 42
- Recommendation: uncertain
- Confidence / scope: low / title_and_abstract
- Paper type: empirical_research
- Summary: The available evidence is mixed or incomplete. Automated score 42/100, low confidence, based on title and abstract.
- Positive signals: User, expert, operational, or deployment evidence is described.; Limitations or threats to validity are acknowledged.

### `doi:10.48550/arxiv.2609.11243`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2609.11243
- Automated score: 76
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The available evidence suggests a credible contribution with some limitations. Automated score 76/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

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

### `doi:10.48550/arxiv.2609.10922`

- Scientific quality: uncertain
- Rationale: The proposed decision lacked sufficient located manuscript evidence; review is pending.
- Uncertainty: Full-text evidence is required for contribution, methods, validation, comparisons or their justified absence, claim alignment, and limitations.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.10922
- Automated score: 78
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: systems_or_application
- Summary: Auto-RecSys presents a well-motivated systems contribution for autonomous experimentation on industry-scale recommendation models, with a clear dual-loop architecture and a substantive 31-iteration reliability evaluation. The paper is candid about limitations and positions itself adequately against prior work. The main weaknesses are the observational nature of the evaluation and the lack of controlled comparisons or statistical testing.
- Main concerns: The evaluation is observational and lacks controlled comparisons or statistical significance testing for the reliability metrics.; The claim that human time per idea is reduced to minutes is supported by qualitative description rather than measured data.; No public code, data, or playbook artifacts are described as released, limiting independent reproduction.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.6082/mgmw1-gw451`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://knowledge.uchicago.edu/records/mgmw1-gw451/files/AI_Scientists_Need_a_Theory_of_Scientific_Value.pdf?download=1
- Automated score: 57
- Recommendation: uncertain
- Confidence / scope: high / full_text
- Paper type: survey_or_review
- Summary: The available evidence is mixed or incomplete. Automated score 57/100, high confidence, based on full text.
- Main concerns: Comparative claims were detected without a suitable baseline in the available text.
- Positive signals: The available text identifies data or a benchmark used by the work.; Quantitative evaluation signals were detected.

### `doi:10.48550/arxiv.2609.07611`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2609.07611
- Automated score: 77
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: survey_or_review
- Summary: The available evidence suggests a credible contribution with some limitations. Automated score 77/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.48550/arxiv.2609.07655`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2609.07655
- Automated score: 61
- Recommendation: uncertain
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The available evidence is mixed or incomplete. Automated score 61/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.64898/2026.09.03.749176`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://www.biorxiv.org/content/biorxiv/early/2026/09/07/2026.09.03.749176.full.pdf
- Automated score: 72
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: survey_or_review
- Summary: The available evidence suggests a credible contribution with some limitations. Automated score 72/100, medium confidence, based on partial full text.
- Positive signals: The available text identifies data or a benchmark used by the work.; A baseline or comparison system is described.

### `doi:10.17605/osf.io/qm2c3`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
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
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: not recorded
- Automated score: 43
- Recommendation: uncertain
- Confidence / scope: low / title_and_abstract
- Paper type: survey_or_review
- Summary: The available evidence is mixed or incomplete. Automated score 43/100, low confidence, based on title and abstract.
- Positive signals: The available text identifies data or a benchmark used by the work.; Limitations or threats to validity are acknowledged.

## Extraction failures

- Full-text enrichment unavailable for Closing the Empirical Loop: Autonomous AI Agents Conduct End‐to‐end Research With Human Participants via https://europepmc.org/articles/PMC13573717?pdf=render: full-text download failed: HTTP Error 403: Forbidden
- Full-text enrichment unavailable for Generative artificial intelligence for nanomaterial discovery and nanoengineering: From data-driven design to autonomous laboratories via https://api.elsevier.com/content/article/pii/S2949829526003670?httpAccept=application/pdf: full-text download failed: HTTP Error 406: Not Acceptable
- Full-text enrichment unavailable for Generative artificial intelligence for nanomaterial discovery and nanoengineering: From data-driven design to autonomous laboratories via https://www.sciencedirect.com/science/article/pii/S2949829526003670/pdf: full-text download failed: HTTP Error 403: Forbidden
- Full-text enrichment unavailable for Mr.LHDR: A Benchmark for Multimodal Real-World Long-Horizon Deep Research Agents via https://arxiv.org/pdf/2609.11318.pdf: full-text download failed: HTTP Error 406: Not Acceptable
- Full-text enrichment unavailable for Generative artificial intelligence for nanomaterial discovery and nanoengineering: From data-driven design to autonomous laboratories via https://www.sciencedirect.com/science/article/pii/S2949829526003670/pdf: full-text download failed: HTTP Error 403: Forbidden
- Full-text enrichment unavailable for Closing the Empirical Loop: Autonomous AI Agents Conduct End‐to‐end Research With Human Participants via https://pmc.ncbi.nlm.nih.gov/articles/PMC13573717/pdf/ADVS-9999-e76675.pdf: full-text response was not a plausible PDF
- Full-text enrichment unavailable for Generative artificial intelligence for nanomaterial discovery and nanoengineering: From data-driven design to autonomous laboratories via https://www.sciencedirect.com/science/article/pii/S2949829526003670/pdf: full-text download failed: HTTP Error 403: Forbidden
