# Paper Scout Live Smoke Report - 2026-07-20

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 275
- **Candidates fetched:** 148
- **Unique papers:** 141
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 48
- Sample title: Learning Reach-Avoid Task with Reinforcement Learning: Vectorized Simulation and Benchmark
- Sample source ID: 2607.15935
- Sample URL: https://arxiv.org/abs/2607.15935v1
- Sample published date: 2026-07-17
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Total Recall QA: A Verifiable Evaluation Suite for Deep Research Agents
- Sample source ID: W7168405860
- Sample URL: https://doi.org/10.1145/3805712.3808629
- Sample published date: 2026-07-15
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 32
- maybe: 8
- irrelevant: 101

## Top Relevant Or Maybe Papers

- **Which ‘AI scientist’ suits your lab? A guide for the perplexed** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1038/d41586-026-02091-6
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **Toward Auditable AI Scientists: A Hypothesis Evolution Protocol for LLM Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2607.09195
- **Toward Auditable AI Scientists: A Hypothesis Evolution Protocol for LLM Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.09195v1
- **Toward Auditable AI Scientists: A Hypothesis Evolution Protocol for LLM Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.09195
- **Recent Advances in AI for Automated ICD Coding: A Systematic Literature Review** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.1007/s10916-026-02429-7
- **NVAITC AI Scientist: A Governed End-to-End Research System -- A Hypertension GWAS Case Study** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2607.11084
- **NVAITC AI Scientist: A Governed End-to-End Research System -- A Hypertension GWAS Case Study** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.11084v1
- **NVAITC AI Scientist: A Governed End-to-End Research System -- A Hypertension GWAS Case Study** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.11084

## Source Failures

- semantic_scholar (HTTP/API error) for `automated literature review`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2607.14582: arxiv:2607.14582, arxiv:2607.14582
- arxiv:2607.10712: arxiv:2607.10712, arxiv:2607.10712
- arxiv:2607.10309: arxiv:2607.10309, arxiv:2607.10309
- arxiv:2607.14178: arxiv:2607.14178, arxiv:2607.14178
- arxiv:2607.09195: arxiv:2607.09195, arxiv:2607.09195
- doi:10.1038/s41524-026-02205-8: openalex:W7167678561, openalex:W7167678561
- doi:10.1017/psrm.2026.10110: openalex:W4411728625, openalex:W4411728625
