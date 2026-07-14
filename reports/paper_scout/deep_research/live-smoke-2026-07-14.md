# Paper Scout Live Smoke Report - 2026-07-14

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 155
- **Unique papers:** 147
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 55
- Sample title: Can LLMs Perform Deep Technical Comprehension of Computer Architecture Papers?
- Sample source ID: 2607.11859
- Sample URL: https://arxiv.org/abs/2607.11859v1
- Sample published date: 2026-07-13
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: FORGE: Research-Trajectory Hijacking Attacks on Deep Research Agents
- Sample source ID: W7167747000
- Sample URL: https://arxiv.org/abs/2607.04718
- Sample published date: 2026-07-06
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 24
- maybe: 9
- irrelevant: 114

## Top Relevant Or Maybe Papers

- **One Reflection Is Not Enough: Self-Correcting Autonomous Research via Multi-Hypothesis Failure Attribution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2606.31478v1
- **Which ‘AI scientist’ suits your lab? A guide for the perplexed** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1038/d41586-026-02091-6
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **Toward Auditable AI Scientists: A Hypothesis Evolution Protocol for LLM Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2607.09195
- **Toward Auditable AI Scientists: A Hypothesis Evolution Protocol for LLM Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.09195v1
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.31273
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.31273v1
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.31273
- **NVAITC AI Scientist: A Governed End-to-End Research System -- A Hypertension GWAS Case Study** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.11084v1

## Source Failures

- semantic_scholar (HTTP/API error) for `deep research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2607.10712: arxiv:2607.10712, arxiv:2607.10712
- arxiv:2607.10309: arxiv:2607.10309, arxiv:2607.10309
- arxiv:2607.05456: arxiv:2607.05456, arxiv:2607.05456, arxiv:2607.05456
- arxiv:2607.09195: arxiv:2607.09195, arxiv:2607.09195
- doi:10.21203/rs.3.rs-9701113/v1: openalex:W4391556095, openalex:W4391556095
- doi:10.1098/rsos.251988: openalex:W4417090127, openalex:W4417090127
- doi:10.1038/s41524-026-02205-8: openalex:W7167678561, openalex:W7167678561
