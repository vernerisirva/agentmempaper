# Paper Scout scholarly-quality report - 2026-09-16

> Advisory automated assessment. Relevance and scholarly quality are independent, and human review remains necessary.

## Summary

- Papers assessed or reused: 1
- Scientific quality statuses: pass: 1
- Publication statuses: repository_only: 1
- Repository-only manuscripts inspected: 1
- Assessment scopes: full_text: 1
- Confidence: high: 1
- Recommendations: promising: 1
- Score distribution: 80-89: 1
- Assessor types: llm: 1
- Papers downranked: 0
- Papers hidden: 0
- Assessments with score caps: 0
- Assessment failures: 0
- Extraction failures: 0
- Cache hits / misses: 1 / 0
- Assessment version: `quality-coverage-v1`
- Rubric version: `scholarly-rubric-v1`

## Per-paper assessment

### `doi:10.5281/zenodo.22685081`

- Scientific quality: pass
- Rationale: The paper presents a coherent, well-scoped contribution: a storage-schema defense (rank-bounded memory) against attribution laundering in LLM agents, with a formal reachability argument, a measured self-poisoning benchmark, and adversarial evaluation. The claims are carefully bounded and the limitations section is unusually thorough. The empirical work includes multiple memory systems, two storylines, two languages, cluster-bootstrapped intervals, human and independent adjudication, and a factorial control isolating verbatim storage from the structural label. The adversarial section decomposes end-to-end ASR into storage promotion and read-side violation, and traces the single residual failure. The paper is transparent about what is specified versus enforced, what is measured versus assumed, and what remains unpriced. The main weaknesses are a single author-annotator for the label-computability pilot, a synthetic corpus, one attacker/framework, and some post-hoc controls, but these are explicitly disclosed and do not undermine the central measured claims.
- Uncertainty: The central claims are well supported by the supplied text, but several measurements rest on a single annotator who is also the author, a synthetic corpus, one attacker, and some post-hoc controls. The frozen-protocol replication for the annotation pilot is explicitly owed. These are disclosed limitations rather than hidden flaws, so the uncertainty is scientific rather than a coverage failure.
- Manuscript evidence assessed: True; source: https://zenodo.org/records/22685081/files/rank-bounded-memory-v1.3.pdf
- Automated score: 82
- Recommendation: promising
- Confidence / scope: high / full_text
- Paper type: empirical_research
- Summary: The paper introduces rank-bounded memory, a storage schema that attaches ownership paths and grounds to every memory record, and argues by reachability induction that foreign content cannot silently become the agent's own belief. It measures self-poisoning without an adversary across flat notes, a self-edit block, and three production memory systems (24-33% laundering), shows the attributed store reduces this to 3-6%, and isolates verbatim storage from the structural label via a factorial control. Under MINJA injection, write-time promotion drops to zero with I2+I4, and end-to-end ASR falls from 47% to 10% with the read rule as a prompt and to 1 of 128 with it enforced in code. The paper is transparent about its trusted base, its specified-but-unenforced invariants, and its unpriced action-side utility cost.
- Main concerns: Label-computability pilot relies on a single annotator who is also the owner and author; frozen-protocol replication is still owed.; Self-poisoning corpus is synthetic and authored by the authors; a live-feed realism check is only planned.; Adversarial evaluation uses one attacker (MINJA) and one framework (SuperRed); corpus poisoning and score-feedback optimizers are not run.
- Positive signals: The available text identifies data or a benchmark used by the work.; A baseline or comparison system is described.
