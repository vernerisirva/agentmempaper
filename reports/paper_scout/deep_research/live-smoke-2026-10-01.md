# Paper Scout Live Smoke Report - 2026-10-01

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 275
- **Candidates fetched:** 144
- **Unique papers:** 134
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 44
- Sample title: DAGent: Evaluate-then-Grow Planning for Deep Research Agents
- Sample source ID: 2609.39154
- Sample URL: https://arxiv.org/abs/2609.39154v1
- Sample published date: 2026-09-30
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: DeepRewind: Predicting and Repairing Premature Commitments in Deep Research Agents
- Sample source ID: W7214903403
- Sample URL: https://doi.org/10.48550/arxiv.2609.36344
- Sample published date: 2026-09-28
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 25
- maybe: 15
- irrelevant: 94

## Top Relevant Or Maybe Papers

- **ScientistTwo Autonomous Research System Summary and Critical Assessment** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.70777/si.v3i3.18761
- **ReproBench: Benchmarking LLM Agents on Reproducing Vulnerability From Scratch** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2609.34450v1
- **LongCat-DeepResearch Technical Report** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2609.36071v1
- **Large-Scale Autonomous Discovery of Kissing Number Constructions** (relevant, 93/100): Studies multi-step planning, multi-agent workflows, or hypothesis and experiment-design agents for research. https://arxiv.org/abs/2609.35051v1
- **Large Knowledge Model: A Knowledge Foundation for Agentic Science at Scale** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.27297v2
- **Can AI Scientists Change Their Minds? Prior-Evidence Conflict in Synthetic Universes** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2609.36726
- **Can AI Scientists Change Their Minds? Prior-Evidence Conflict in Synthetic Universes** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.36726v1
- **AI Scientists for Building Virtual-Cell Models** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.21203/rs.3.rs-10954762/v1
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide · v2 (typography)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854691
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide · v2 (typography)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854690

## Source Failures

- semantic_scholar (HTTP/API error) for `automated literature review`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2609.33509: arxiv:2609.33509, arxiv:2609.33509
- arxiv:2609.32245: arxiv:2609.32245, arxiv:2609.32245
- doi:10.48550/arxiv.2609.23986: openalex:W7213995952, openalex:W7213995952
- doi:10.5281/zenodo.23051403: openalex:W7214961531, openalex:W7214961531
- doi:10.5281/zenodo.23051404: openalex:W7214949777, openalex:W7214949777
- doi:10.1136/jme-2026-112004: openalex:W7130572291, openalex:W7130572291
- doi:10.1038/s41598-026-72525-8: openalex:W7213672938, openalex:W7213672938
- doi:10.1117/1.ap.8.5.054003: openalex:W7214214533, openalex:W7214214533
- doi:10.1145/3829807.3829820: openalex:W4407091665, openalex:W4407091665
- doi:10.1016/j.respol.2026.105598: openalex:W7106159402, openalex:W7106159402
