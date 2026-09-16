# Paper Scout scholarly-quality report - 2026-09-16

> Advisory automated assessment. Relevance and scholarly quality are independent, and human review remains necessary.

## Summary

- Papers assessed or reused: 8
- Scientific quality statuses: uncertain: 8
- Publication statuses: preprint: 8
- Repository-only manuscripts inspected: 0
- Assessment scopes: full_text: 2, partial_full_text: 6
- Confidence: high: 2, medium: 6
- Recommendations: promising: 4, uncertain: 3, weak: 1
- Score distribution: 50-59: 1, 60-69: 3, 70-79: 3, 80-89: 1
- Assessor types: deterministic: 6, llm: 2
- Papers downranked: 0
- Papers hidden: 0
- Assessments with score caps: 1
- Assessment failures: 6
- Extraction failures: 5
- Cache hits / misses: 8 / 0
- Assessment version: `quality-v2`
- Rubric version: `scholarly-rubric-v1`

## Per-paper assessment

### `arxiv:2609.04793`

- Scientific quality: uncertain
- Rationale: The proposed decision lacked sufficient located manuscript evidence; review is pending.
- Uncertainty: Full-text evidence is required for contribution, methods, validation, comparisons or their justified absence, claim alignment, and limitations.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.04793
- Automated score: 72
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: ProtLingo augments a pretrained ESM2-150M backbone with centered latent N-gram memory and sparse MoE routing. The paper provides clear architectural details, training configuration, and evaluation protocols. Quantitative results on ProteinGym, FLIP, and CASP15 contact prediction, plus ablations and biological analyses, support the claims of parameter-efficient mutation-sensitive modeling and preserved structural representations. Limitations are acknowledged, including bounded gains and unvalidated sampling choices.
- Main concerns: Some baseline comparisons are literature-reported rather than controlled head-to-head.; The 80/20 sampling strategy is acknowledged as not fully validated through controlled ablation.; The paper is a preprint and has not undergone external peer review.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.48550/arxiv.2609.03426`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2609.03426
- Automated score: 75
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: replication
- Summary: The available evidence suggests a credible contribution with some limitations. Automated score 75/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `arxiv:2608.29327`

- Scientific quality: uncertain
- Rationale: The proposed decision lacked sufficient located manuscript evidence; review is pending.
- Uncertainty: Full-text evidence is required for contribution, methods, validation, comparisons or their justified absence, claim alignment, and limitations.
- Full text inspected: True; source: https://arxiv.org/pdf/2608.29327
- Automated score: 84
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The available evidence suggests a credible contribution with some limitations. Automated score 84/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `arxiv:2608.23982`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2608.23982
- Automated score: 74
- Recommendation: promising
- Confidence / scope: high / full_text
- Paper type: survey_or_review
- Summary: The available evidence suggests a credible contribution with some limitations. Automated score 74/100, high confidence, based on full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.48550/arxiv.2608.17050`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2608.17050
- Automated score: 54
- Recommendation: weak
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The available evidence suggests weak or incomplete scholarly validation. Automated score 54/100, medium confidence, based on partial full text.
- Main concerns: Comparative claims were detected without a suitable baseline in the available text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `openalex:W7172473936`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2607.29065
- Automated score: 64
- Recommendation: uncertain
- Confidence / scope: high / full_text
- Paper type: position_or_conceptual
- Summary: The available evidence is mixed or incomplete. Automated score 64/100, high confidence, based on full text.
- Main concerns: Comparative claims were detected without a suitable baseline in the available text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `arxiv:2605.20948`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2605.20948
- Automated score: 67
- Recommendation: uncertain
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The available evidence is mixed or incomplete. Automated score 67/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `arxiv:2601.07372`

- Scientific quality: uncertain
- Rationale: Text-pattern signals are available, but scientific substance requires manuscript review.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: https://arxiv.org/pdf/2601.07372
- Automated score: 65
- Recommendation: uncertain
- Confidence / scope: medium / partial_full_text
- Paper type: position_or_conceptual
- Summary: The available evidence is mixed or incomplete. Automated score 65/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

## Extraction failures

- Full-text enrichment unavailable for Memory Is Not Always Needed: Characterizing Conditional Memory in Scientific Reasoning via https://arxiv.org/pdf/2608.23982.pdf: full-text download failed: HTTP Error 406: Not Acceptable
- Full-text enrichment unavailable for Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory via https://arxiv.org/pdf/2605.20948.pdf: full-text download failed: HTTP Error 406: Not Acceptable
- Full-text enrichment unavailable for When to Adapt: Conditional Memory Adapters for Retention-Preserving Domain Specialization via https://arxiv.org/pdf/2608.29327.pdf: full-text download failed: HTTP Error 406: Not Acceptable
- Full-text enrichment unavailable for ProtLingo: Efficient Protein Language Modeling via Conditional Memory and Expert Routing via https://arxiv.org/pdf/2609.04793.pdf: full-text download failed: HTTP Error 406: Not Acceptable
- Full-text enrichment unavailable for Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models via https://arxiv.org/pdf/2601.07372.pdf: full-text download failed: HTTP Error 406: Not Acceptable
