# Paper Scout scholarly-quality report - 2026-09-16

> Advisory automated assessment. Relevance and scholarly quality are independent, and human review remains necessary.

## Summary

- Papers assessed or reused: 8
- Scientific quality statuses: pass: 3, uncertain: 5
- Publication statuses: preprint: 8
- Repository-only manuscripts inspected: 0
- Assessment scopes: full_text: 2, partial_full_text: 6
- Confidence: medium: 8
- Recommendations: promising: 3, uncertain: 4, weak: 1
- Score distribution: 50-59: 2, 60-69: 3, 70-79: 2, 80-89: 1
- Assessor types: llm: 4, manual_override: 4
- Papers downranked: 0
- Papers hidden: 0
- Assessments with score caps: 1
- Assessment failures: 0
- Extraction failures: 0
- Cache hits / misses: 8 / 0
- Assessment version: `quality-recovery-v1`
- Rubric version: `scholarly-rubric-v1`

## Per-paper assessment

### `arxiv:2609.04793`

- Scientific quality: uncertain
- Rationale: The paper presents a clear contribution with explicit implementation details, quantitative evaluations against baselines, ablations, and acknowledged limitations. The available text supports the central claims of competitive performance and parameter efficiency, though the partial full text limits assessment of some methodological details and reproducibility.
- Uncertainty: The assessment is based on partial full text, and some sections such as complete training details, full results tables, and code availability statements may be incomplete or absent from the supplied material.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.04793
- Automated score: 68
- Recommendation: uncertain
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: ProtLingo augments a pretrained ESM2-150M backbone with centered latent N-gram memory and sparse MoE upcycling. The paper reports competitive ProteinGym, FLIP, and CASP15 contact prediction results with 153M active parameters, supported by ablations and biological specialization analyses. The available text is partial but contains substantive implementation, evaluation, and limitation details.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.48550/arxiv.2609.03426`

- Scientific quality: pass
- Rationale: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. Lngram v2 is a well-specified architectural extension that decouples memory capacity from backbone width, validated through controlled comparisons, ablations, statistical testing, and semantic analysis of discrete IDs. The evidence supports the central claims of parameter efficiency, scalability, and semantic preservation, though reproducibility is limited by absent code and partially deferred implementation details.
- Uncertainty: Code and implementation detail are incomplete in supplied excerpts; some baselines are single-run and 30B comparisons do not repeat all controls. Early-training address instability limits applicability. The original rejected proposal rationale was not retained by the prior validator; this audit uses its preserved summary, explanations and exact quotes, and is explicitly a manual override rather than a new model assessment.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.03426
- Automated score: 78
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. Lngram v2 is a well-specified architectural extension that decouples memory capacity from backbone width, validated through controlled comparisons, ablations, statistical testing, and semantic analysis of discrete IDs. The evidence supports the central claims of parameter efficiency, scalability, and semantic preservation, though reproducibility is limited by absent code and partially deferred implementation details.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `arxiv:2608.29327`

- Scientific quality: pass
- Rationale: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. The paper proposes Engram Adapter, a conditional-memory PEFT method that repurposes DeepSeek Engram's hash-based n-gram lookup as a post-hoc adapter with occupancy-tracked joint masking and a learned scalar gate. The central claim is that conditional activation preserves OOD capabilities better than always-on PEFT while improving in-domain accuracy. The manuscript provides quantitative results on Qwen3-4B and Qwen3-8B across AG-News, MedMCQA, ARC-Challenge, FLORES, MBPP, and LegalBench, plus mechanistic residual and output-distribution analyses. The contribution is clearly stated, the method is described in sufficient architectural detail, and the empirical evidence generally supports the retention claim. However, the related-work positioning is somewhat thin for the actual claims, and reproducibility is limited by the absence of code or full implementation details in the supplied text.
- Uncertainty: The 8B table uses one seed; evidence covers two model scales and limited domains. The adapter trades some in-domain accuracy and inference overhead for retention; broader generality is not established. The original rejected proposal rationale was not retained by the prior validator; this audit uses its preserved summary, explanations and exact quotes, and is explicitly a manual override rather than a new model assessment.
- Full text inspected: True; source: https://arxiv.org/pdf/2608.29327
- Automated score: 78
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. The paper proposes Engram Adapter, a conditional-memory PEFT method that repurposes DeepSeek Engram's hash-based n-gram lookup as a post-hoc adapter with occupancy-tracked joint masking and a learned scalar gate. The central claim is that conditional activation preserves OOD capabilities better than always-on PEFT while improving in-domain accuracy. The manuscript provides quantitative results on Qwen3-4B and Qwen3-8B across AG-News, MedMCQA, ARC-Challenge, FLORES, MBPP, and LegalBench, plus mechanistic residual and output-distribution analyses. The contribution is clearly stated, the method is described in sufficient architectural detail, and the empirical evidence generally supports the retention claim. However, the related-work positioning is somewhat thin for the actual claims, and reproducibility is limited by the absence of code or full implementation details in the supplied text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `arxiv:2608.23982`

- Scientific quality: pass
- Rationale: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. The paper systematically studies conditional memory in scientific reasoning and proposes a Knowledge Boundary-Aware Router that selectively activates memory based on pre-inference input proxies. The central claim that memory utility is input- and computation-dependent is supported by boundary-cohort ablations, layer-stage interventions, and comparisons against static and activation-rate-matched random routing across biological and chemical benchmarks. The work is methodologically grounded and clearly positioned, though internal router validation is limited to offline replay and some reproducibility details are absent from the supplied text.
- Uncertainty: Internal-router evidence is same-cohort offline replay, not independent generalization. Some implementation details are absent from the bounded supplied text. The original rejected proposal rationale was not retained by the prior validator; this audit uses its preserved summary, explanations and exact quotes, and is explicitly a manual override rather than a new model assessment.
- Full text inspected: True; source: https://arxiv.org/pdf/2608.23982
- Automated score: 82
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: Codex evidence audit of the saved DeepSeek proposed pass, following the reviewed literal line-wrap correction. The paper systematically studies conditional memory in scientific reasoning and proposes a Knowledge Boundary-Aware Router that selectively activates memory based on pre-inference input proxies. The central claim that memory utility is input- and computation-dependent is supported by boundary-cohort ablations, layer-stage interventions, and comparisons against static and activation-rate-matched random routing across biological and chemical benchmarks. The work is methodologically grounded and clearly positioned, though internal router validation is limited to offline replay and some reproducibility details are absent from the supplied text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.48550/arxiv.2608.17050`

- Scientific quality: uncertain
- Rationale: The model returned schema-valid JSON but repeated the deterministic seed assessment, including its statement that no semantic scientific assessment had occurred. Scientific quality remains unassessed pending a substantive response.
- Uncertainty: This is a model-response problem, not evidence of poor science. The original response provenance and billed usage remain in assessment history; no additional call was made.
- Full text inspected: True; source: https://arxiv.org/pdf/2608.17050
- Automated score: 54
- Recommendation: weak
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The model returned schema-valid JSON but repeated the deterministic seed assessment, including its statement that no semantic scientific assessment had occurred. Scientific quality remains unassessed pending a substantive response.
- Main concerns: Comparative claims were detected without a suitable baseline in the available text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `openalex:W7172473936`

- Scientific quality: uncertain
- Rationale: The paper presents a clear technical contribution—replacing XOR hashing with polynomial hashing to achieve tokenizer-agnostic Engram embeddings—and provides quantitative experiments, ablations, and code availability. However, the evidence for the central cross-tokenizer transfer claim is mixed: the transferred Engram embeddings produce only marginal gains over the base model (mean 0.560 to 0.584, with several benchmark scores below the base), and the paper does not clearly establish that the observed improvements are attributable to byte-equivalent N-gram lookups rather than other factors. The methodological description is detailed but the validation of the core claim is weak, and limitations are not explicitly discussed.
- Uncertainty: The paper's central claim of tokenizer-agnosticism is supported by a single cross-tokenizer transfer experiment with modest and mixed results. The absence of explicit limitations, the small performance differences, and the lack of a direct comparison against a tokenizer-locked baseline for the transfer scenario leave the strength of the contribution uncertain.
- Full text inspected: True; source: https://arxiv.org/pdf/2607.29065
- Automated score: 55
- Recommendation: uncertain
- Confidence / scope: medium / full_text
- Paper type: methods_or_algorithm
- Summary: The paper proposes a polynomial hashing replacement for DeepSeek's Engram module to achieve tokenizer-agnosticism. The method is clearly described and the experiments show comparable performance to XOR hashing, but the central cross-tokenizer transfer claim is supported by only one experiment with modest and mixed results, and limitations are not discussed.
- Main concerns: Comparative claims were detected without a suitable baseline in the available text.; The central cross-tokenizer transfer claim is supported by only one experiment with mixed results.; The paper does not explicitly discuss limitations or uncertainty in the transfer results.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `arxiv:2605.20948`

- Scientific quality: uncertain
- Rationale: The paper presents a clear method, Memory Grafting, with matched baselines, quantitative benchmark results, ablations, efficiency analysis, and a limitations section. However, several scientific quality dimensions are only partially supported: related work is discussed but not systematically compared against the actual claims, reproducibility is limited by the absence of code or detailed hyperparameters in the supplied text, and some evaluation claims rely on figures and tables whose full statistical context is not provided. The work is substantive but not fully validated as a scholarly contribution from the available manuscript evidence.
- Uncertainty: The assessment is limited by the supplied text, which includes tables and figures but not all implementation details, statistical significance tests, or code. Some claims about efficiency and memory use are reported without full measurement methodology. The absence of a knowledge distillation comparison is acknowledged but leaves the relative value of the method partially unresolved.
- Full text inspected: True; source: https://arxiv.org/pdf/2605.20948
- Automated score: 66
- Recommendation: uncertain
- Confidence / scope: medium / full_text
- Paper type: empirical_research
- Summary: Memory Grafting proposes using frozen hidden states from a pretrained grafting model as conditional n-gram memory for a smaller recipient model. The paper reports benchmark gains over MoE and vanilla Engram baselines, ablations, efficiency results, and representational analyses. The contribution is clear and the evaluation is substantive, but related-work positioning, reproducibility, and statistical rigor are only partially supported in the available text.
- Main concerns: Related work is summarized but not systematically compared against the actual claims or evaluated for how Memory Grafting differs in measured performance.; Reproducibility is limited because the supplied text does not include code, full hyperparameter details, or exact evaluation procedures.; Benchmark improvements are reported without statistical significance tests or confidence intervals.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `arxiv:2601.07372`

- Scientific quality: uncertain
- Rationale: The manuscript presents a clearly articulated architectural contribution (Engram as conditional memory) with substantial quantitative evaluation, ablations, and mechanistic analyses. However, the supplied text is partial and omits several sections that would be needed to fully verify methodological details, statistical rigor, and limitations. The available evidence supports a credible but not fully established scholarly contribution.
- Uncertainty: The assessment is based on partial full text. Several sections, including detailed hyperparameters, full ablation tables, and a dedicated limitations discussion, are not present in the supplied material. This prevents a definitive judgment on methodological completeness and uncertainty handling.
- Full text inspected: True; source: https://arxiv.org/pdf/2601.07372
- Automated score: 65
- Recommendation: uncertain
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The paper introduces Engram, a conditional memory module that modernizes N-gram embeddings for O(1) lookup, and evaluates it against iso-parameter and iso-FLOPs MoE baselines. The available text shows clear contribution framing, extensive benchmark results, ablations, and mechanistic analyses supporting the claimed benefits. However, the partial text lacks a dedicated limitations section and statistical uncertainty reporting, leaving methodological completeness uncertain.
- Main concerns: The supplied text does not include a dedicated limitations section, and the discussion of limitations is limited to brief remarks about under-training and benchmark noise.; Statistical significance or variance estimates are not reported for the benchmark improvements.; The paper relies on a single training run per configuration, and no evidence of repeated runs or uncertainty quantification is provided.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.
