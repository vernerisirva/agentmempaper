# Paper Scout scholarly-quality report - 2026-09-16

> Advisory automated assessment. Relevance and scholarly quality are independent, and human review remains necessary.

## Summary

- Papers assessed or reused: 10
- Scientific quality statuses: insufficient: 1, pass: 2, uncertain: 7
- Publication statuses: peer_reviewed: 1, preprint: 3, repository_only: 6
- Repository-only manuscripts inspected: 5
- Assessment scopes: full_text: 4, partial_full_text: 5, title_and_abstract: 1
- Confidence: high: 4, low: 1, medium: 5
- Recommendations: promising: 3, uncertain: 5, unknown: 1, weak: 1
- Score distribution: 30-39: 1, 40-49: 1, 50-59: 1, 60-69: 3, 70-79: 2, 80-89: 1, unknown: 1
- Assessor types: deterministic: 1, llm: 8, manual_override: 1
- Papers downranked: 0
- Papers hidden: 0
- Assessments with score caps: 0
- Assessment failures: 0
- Extraction failures: 0
- Cache hits / misses: 9 / 1
- Assessment version: `quality-recovery-v1`
- Rubric version: `scholarly-rubric-v1`

## Per-paper assessment

### `doi:10.1007/s44206-026-00290-2`

- Scientific quality: uncertain
- Rationale: The paper is a philosophical position/conceptual argument rather than an empirical study. It develops a clear central thesis about misrecognition of non-agentive AI and supports it with conceptual distinctions, cited philosophical work, and empirical studies of AI use. However, the supplied text is partial and omits some sections, including parts of the argumentative center and any explicit limitations discussion. The central claims are largely aligned with the presented evidence, but the absence of a visible limitations section and the incomplete text prevent a full pass.
- Uncertainty: The assessment is based on partial full text. Several sections appear truncated, and no explicit limitations or uncertainty-handling section is visible in the supplied material. The paper's philosophical argument is coherent and well-supported in the available text, but the missing portions could contain qualifications, objections, or limitations that would affect the evaluation.
- Full text inspected: True; source: https://link.springer.com/content/pdf/10.1007/s44206-026-00290-2.pdf
- Automated score: 68
- Recommendation: uncertain
- Confidence / scope: medium / partial_full_text
- Paper type: position_or_conceptual
- Summary: This is a philosophical position paper arguing that current AI systems are widely treated as epistemic agents but lack episodic memory and the first-personal, diachronic standpoint required for robust epistemic agency. The author develops a distinction between thin reliability-based authority and stronger answerable epistemic standing, supports the claim with cognitive science literature on episodic and semantic memory, and cites empirical studies showing AI is treated as an authority in medicine, education, and everyday life. The argument is clear and well-structured, but the supplied text is partial and lacks an explicit limitations discussion.
- Main concerns: The supplied text does not include an explicit limitations section or sustained discussion of objections to the central argument.; The paper relies heavily on the assumption that episodic memory is necessary for robust epistemic agency, but the defense of this necessity claim is not fully developed in the available text.; The empirical evidence cited is used to show that AI is treated as an authority, but the paper does not systematically assess the strength or representativeness of that evidence.
- Positive signals: The available text identifies data or a benchmark used by the work.; A baseline or comparison system is described.

### `doi:10.5281/zenodo.22750153`

- Scientific quality: uncertain
- Rationale: The paper is a coherent position piece with a clearly stated central claim and a structured conceptual framework. However, it lacks empirical validation, formal modeling, or worked examples to support its causal assertions about drift gradients and intransitability. Related work is limited to two prior HibriMind formulations, and limitations of the central claim are not addressed. The paper is internally consistent but remains at the level of conceptual assertion rather than demonstrated or tested claims.
- Uncertainty: The paper's conceptual contribution is clear, but the absence of empirical or formal validation, limited related work, and unaddressed limitations make it difficult to assess the scientific substance of the claims. The paper may be valuable as a position piece, but its claims are not yet supported by evidence.
- Full text inspected: True; source: https://zenodo.org/records/22750153/files/The_Intransitability_of_Hybrid_Agents_HibriMind_v0.1.pdf
- Automated score: 55
- Recommendation: uncertain
- Confidence / scope: high / full_text
- Paper type: position_or_conceptual
- Summary: The paper is a position/conceptual piece proposing the HibriMind principle of hybrid-agent intransitability. It argues that long-horizon hybrid human-AI agents cannot be fully transferred between biological operators because accumulated operational history becomes a causal drift gradient. The central claim is clearly stated and consistently developed, with supporting conceptual distinctions (biological operator, algorithmic substrate, authorized object, accumulated coupling history) and practical safety mechanisms. However, the paper lacks empirical validation, formal modeling, or worked examples demonstrating the claimed causal effects. Related work is limited to two prior HibriMind formulations, with no engagement with broader literature on agent memory, continual learning, or human-AI interaction. Limitations are not explicitly addressed. The paper is internally coherent but remains at the level of conceptual assertion rather than demonstrated or tested claims.
- Positive signals: The available text identifies data or a benchmark used by the work.; The paper clearly states its central principle and defines key concepts.

### `doi:10.48550/arxiv.2609.12320`

- Scientific quality: uncertain
- Rationale: The proposed decision lacked sufficient located manuscript evidence; review is pending.
- Uncertainty: Full-text evidence is required for contribution, methods, validation, comparisons or their justified absence, claim alignment, and limitations.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.12320
- Automated score: 73
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The available evidence suggests a credible contribution with some limitations. Automated score 73/100, medium confidence, based on partial full text.
- Positive signals: The contribution is stated explicitly.; A baseline or comparison system is described.

### `doi:10.5281/zenodo.22661593`

- Scientific quality: insufficient
- Rationale: The manuscript asserts that human supervision guarantees attractor stabilization, but provides no worked case, formal derivation or operational evaluation establishing that guarantee. Its concepts and ten-step protocol are explicit, yet the central evidence-to-claim link remains unsupported. This is a scientific support problem in the available complete manuscript.
- Uncertainty: This is a conceptual contribution, so conventional empirical baselines are not required. The protocol and supervision-risk table are acknowledged; the concern is the unqualified guarantee without a supporting argument or demonstration, not absence of every procedure or limitation.
- Full text inspected: True; source: https://zenodo.org/records/22661593/files/Human_Supervision_as_Attractor_Stabilization_HibriMind.pdf
- Automated score: 35
- Recommendation: weak
- Confidence / scope: high / full_text
- Paper type: position_or_conceptual
- Summary: The manuscript asserts that human supervision guarantees attractor stabilization, but provides no worked case, formal derivation or operational evaluation establishing that guarantee. Its concepts and ten-step protocol are explicit, yet the central evidence-to-claim link remains unsupported. This is a scientific support problem in the available complete manuscript.
- Positive signals: The available text identifies data or a benchmark used by the work.; A baseline or comparison system is described.

### `doi:10.5281/zenodo.22699102`

- Scientific quality: pass
- Rationale: The paper is a theoretical audit with a clearly stated contribution, a well-defined methodological framework (four commitments), and careful alignment of evidence to claims. It grounds its central dis-analogy in a controlled study and explicitly addresses its own limitations, including the weakness of literature-search absence claims and reliance on preprints. The argument is well-structured and the paper type (theoretical) is appropriate for the absence of empirical experiments.
- Uncertainty: The assessment is based on partial full text. Several load-bearing claims rest on literature-search absence assertions and unrefereed preprints, which the paper itself acknowledges. The parametric branch sample is small (four systems) and recent, so the generalisation about isolation may not hold as the field evolves.
- Full text inspected: True; source: https://zenodo.org/records/22699102/files/consolidation-without-weights.pdf
- Automated score: 78
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: theoretical
- Summary: The paper is a theoretical audit of the term 'consolidation' in LLM agent memory systems against four commitments derived from complementary learning systems theory. It argues that neither the textual nor the parametric branch instantiates the mechanism, and identifies one published configuration that does. The contribution is clearly stated, the argument is well-structured, and limitations are explicitly addressed. The main weakness is that several load-bearing claims rest on literature-search absence assertions and unrefereed preprints, which the paper itself acknowledges.
- Main concerns: Comparative claims were detected without a suitable baseline in the available text.
- Positive signals: The available text identifies data or a benchmark used by the work.; An ablation analysis is reported.

### `doi:10.48550/arxiv.2609.11060`

- Scientific quality: uncertain
- Rationale: The proposed decision lacked sufficient located manuscript evidence; review is pending.
- Uncertainty: Full-text evidence is required for contribution, methods, validation, comparisons or their justified absence, claim alignment, and limitations.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.11060
- Automated score: 84
- Recommendation: promising
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The available evidence suggests a credible contribution with some limitations. Automated score 84/100, medium confidence, based on partial full text.
- Main concerns: Comparative claims were detected without a suitable baseline in the available text.
- Positive signals: The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### `doi:10.5281/zenodo.22682679`

- Scientific quality: pass
- Rationale: The paper is a well-scoped position/conceptual architecture paper. It clearly articulates its contribution, grounds its gap analysis in prior work, defines evaluation criteria, and handles limitations transparently. The absence of empirical validation is appropriate for the stated paper type and is explicitly acknowledged as future work.
- Uncertainty: The assessment is based on the supplied full text, which is internally consistent and clearly scoped. The main uncertainty is whether the proposed architecture will ultimately demonstrate the runtime behavior required to justify its operating-system terminology, which the paper itself acknowledges as an open question.
- Full text inspected: True; source: https://zenodo.org/records/22682680/files/AIVORIX_Beyond_Agentic_Operating_Systems_Zenodo_Upload.pdf
- Automated score: 68
- Recommendation: uncertain
- Confidence / scope: high / full_text
- Paper type: position_or_conceptual
- Summary: The paper is a position/conceptual architecture paper proposing AIVORIX OS as a governance-centric enterprise AI operating system. It clearly scopes itself as research-stage, presents a ten-layer architecture and runtime cycle, and grounds its gap analysis in prior academic and commercial work. The main limitation is the absence of empirical validation, which the paper explicitly acknowledges and frames as future work.
- Positive signals: The available text identifies data or a benchmark used by the work.; Quantitative evaluation signals were detected.

### `arxiv:2609.11225`

- Scientific quality: uncertain
- Rationale: The paper presents a systems/application contribution: a unified embodied-agent runtime (HROS) and its Argos quadruped inspection realization. The architecture, component integration, and operational closed loop are described in substantial detail, and the paper reports quantitative field results for navigation, hazard detection, and enterprise delivery. However, the central cognitive-runtime claims—voice interaction, hierarchical memory, and safety-gated self-evolution—are explicitly deferred: the text states that numerical values for these controlled trials are reported only after the corresponding trials are completed, and the conclusion says future work will quantify the contribution of each cognitive component. This means the paper's most distinctive architectural claims are not yet validated by the supplied evidence. The navigation and inspection results are plausible and internally consistent, but the manuscript lacks sample sizes, trial counts, repetitions, confidence intervals, and detailed experimental conditions for the reported metrics. The paper is therefore a credible integrated field-system report with a clear contribution, but its validation is incomplete for the claims that distinguish it from a conventional navigation stack.
- Uncertainty: The main uncertainty is whether the cognitive-runtime components (voice grounding, hierarchical memory, governed self-evolution) have any empirical support beyond design description. The supplied text repeatedly defers these evaluations to future work or to controlled trials whose numerical values are not yet reported. Additionally, the field metrics in Table 1 are presented without trial counts, repetitions, noise conditions, or statistical intervals, so the strength of the navigation and inspection validation cannot be fully assessed from the available text. The paper type is best classified as systems_or_application rather than survey_or_review, because it describes and evaluates a deployed prototype system.
- Full text inspected: True; source: https://arxiv.org/pdf/2609.11225
- Automated score: 69
- Recommendation: uncertain
- Confidence / scope: high / full_text
- Paper type: systems_or_application
- Summary: The paper presents HROS, a unified embodied-agent runtime, and Argos, its quadruped inspection realization, with detailed architecture and quantitative field results for navigation, hazard detection, and enterprise delivery. The contribution is clear and the system design is thoughtful, particularly the safety-gated self-evolution loop. However, the most distinctive cognitive-runtime claims—voice grounding, hierarchical memory, and governed adaptation—are explicitly deferred to future evaluation, and the reported field metrics lack sample sizes and statistical detail. The paper is a credible integrated field-system report but its validation is incomplete for the claims that distinguish it from a conventional navigation stack.
- Main concerns: Meaningful evaluation appears to be deferred to future work in the available text.; The central cognitive-runtime claims (voice interaction, hierarchical memory, safety-gated self-evolution) are not empirically validated in the supplied text; numerical results for these controlled trials are explicitly deferred.; The field metrics in Table 1 are reported without sample sizes, trial counts, independent repetitions, or statistical intervals, limiting the strength of the quantitative validation.
- Positive signals: The contribution is stated explicitly.; A baseline or comparison system is described.

### `doi:10.5281/zenodo.22685081`

- Scientific quality: uncertain
- Rationale: The proposed decision lacked sufficient located manuscript evidence; review is pending.
- Uncertainty: Full-text evidence is required for contribution, methods, validation, comparisons or their justified absence, claim alignment, and limitations.
- Full text inspected: True; source: https://zenodo.org/records/22685081/files/rank-bounded-memory-v1.3.pdf
- Automated score: not enough evidence
- Recommendation: unknown
- Confidence / scope: medium / partial_full_text
- Paper type: empirical_research
- Summary: The paper presents a novel rank-bounded memory schema for LLM agents with quantitative claims about self-poisoning and attack resistance. The supplied text includes the abstract, threat model, and related work sections, but omits the core methodological and results sections needed to validate the central empirical claims. The paper is classified as insufficient due to missing evidence for its quantitative assertions.
- Main concerns: The core empirical sections (Sections 3-7) are missing from the supplied text, so the central quantitative claims cannot be verified.; The paper relies on a single annotator (the author) for the primary label computability measurement, which is a methodological limitation acknowledged in the text.; The paper's abstract makes strong claims about attack resistance (1 of 128 tasks) but the supplied text does not include the experimental details to support this.
- Positive signals: Code, data, or research artifacts are described as available.; Formal definitions or proof-oriented evidence is present.

### `doi:10.5281/zenodo.22682633`

- Scientific quality: uncertain
- Rationale: Scientific quality could not be assessed because manuscript-level evidence was unavailable.
- Uncertainty: No semantic quality assessment has established methods, evidence and claim alignment.
- Full text inspected: False; source: not recorded
- Automated score: 42
- Recommendation: uncertain
- Confidence / scope: low / title_and_abstract
- Paper type: unclear
- Summary: The available evidence is mixed or incomplete. Automated score 42/100, low confidence, based on title and abstract.

## Unknown quality

- `doi:10.5281/zenodo.22685081`: The paper presents a novel rank-bounded memory schema for LLM agents with quantitative claims about self-poisoning and attack resistance. The supplied text includes the abstract, threat model, and related work sections, but omits the core methodological and results sections needed to validate the central empirical claims. The paper is classified as insufficient due to missing evidence for its quantitative assertions.
