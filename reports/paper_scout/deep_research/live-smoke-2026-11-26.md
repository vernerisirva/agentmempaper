# Paper Scout Live Smoke Report - 2026-11-26

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 275
- **Candidates fetched:** 147
- **Unique papers:** 144
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 47
- Sample title: DRBench Pro: A Knowledge-Centric Benchmark for Professional Deep Research Agents
- Sample source ID: 2611.34852
- Sample URL: https://arxiv.org/abs/2611.34852v1
- Sample published date: 2026-11-25
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: DRAgNEt: Deep Research Agent Network for Etymology
- Sample source ID: W7239728678
- Sample URL: https://doi.org/10.5281/zenodo.24540588
- Sample published date: 2026-11-25
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 25
- maybe: 6
- irrelevant: 113

## Top Relevant Or Maybe Papers

- **DRBench Pro: A Knowledge-Centric Benchmark for Professional Deep Research Agents** (relevant, 98/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2611.34852v1
- **DRAgNEt: Deep Research Agent Network for Etymology** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.5281/zenodo.24540588
- **TwinLab-Bench: Evaluating AI Scientists in Agentic Twins of Real Labs** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.26248v1
- **TwinLab-Bench: Evaluating AI Scientists in Agentic Twins of Real Labs** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.26248
- **The AI scientist in the mirror: Shared flaws, joint remedies** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1073/pnas.2633303123
- **SEA-Lab: Experiment-grounded recursive self-improvement in an automated laboratory** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.64898/2026.11.12.766090
- **Inventa: Decentralized Self-Improving Agents for Autonomous Scientific Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.21847v1
- **Inventa: Decentralized Self-Improving Agents for Autonomous Scientific Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.21847
- **Ground, Iterate, Trace: Decomposing AI Research Ideation** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.24887v1
- **Eliciting Research Taste in LLMs through Future Research Direction Choice** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.19794v1

## Source Failures

- semantic_scholar (HTTP/API error) for `automated literature review`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.21950: arxiv:2611.21950, arxiv:2611.21950
- arxiv:2611.26343: arxiv:2611.26343, arxiv:2611.26343
- doi:10.48550/arxiv.2611.23323: openalex:W7236692867, openalex:W7236692867
