# Paper Scout Live Smoke Report - 2026-10-26

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 157
- **Unique papers:** 149
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 57
- Sample title: Beyond Watching and Searching: Benchmarking Agents for Video-centered Deep Research Reports
- Sample source ID: 2610.31158
- Sample URL: https://arxiv.org/abs/2610.31158v1
- Sample published date: 2026-10-22
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: OpenSaC: A Python Library for Search as Code in Deep Research Agents
- Sample source ID: W7223039332
- Sample URL: https://arxiv.org/abs/2610.25779
- Sample published date: 2026-10-19
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 33
- maybe: 12
- irrelevant: 104

## Top Relevant Or Maybe Papers

- **Auto-MD-bench: Evaluating Autoresearch Agents for Real-World Medical Tasks** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.25069v1
- **Auto-MD-bench: Evaluating Autoresearch Agents for Real-World Medical Tasks** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.25069
- **Research Copilot: An Autonomous AI Research Engineering Platform for Automated Literature Discovery, Evidence Grounding, and Novelty Analysis** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.5281/zenodo.23589708
- **IAISS 2026 Project 10: ALS AI Scientist, run archives and results (pl-prod-014 to pl-prod-018)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23370542
- **From Robots to Organizations: The Role of the AI Scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.2196/114408
- **ExpEvolve: Structuring and Reusing Experience for Open-Ended Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.29303v1
- **ExpEvolve: Structuring and Reusing Experience for Open-Ended Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.29303
- **EL-RAKHAWI BIO-QUANTUM COMPUTING FRAMEWORK INTEGRATING CEREBRAL ORGANOIDS, QUANTUM NEUROMORPHIC ARCHITECTURES, AND AUTONOMOUS AI SCIENTIST AGENTS A Unified Paradigm for Next-Generation Computational Intelligence and Autonomous Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23527960
- **Designing Human-AI Collaborative Science: The 9A Framework** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.22948v1
- **Designing Human-AI Collaborative Science: The 9A Framework** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.22948

## Source Failures

- semantic_scholar (HTTP/API error) for `deep research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.29346: arxiv:2610.29346, arxiv:2610.29346
- doi:10.1016/j.sysarc.2026.103874: arxiv:2610.28699, arxiv:2610.28699
- arxiv:2610.30181: arxiv:2610.30181, arxiv:2610.30181
- arxiv:2610.23299: arxiv:2610.23299, arxiv:2610.23299
- arxiv:2610.21042: arxiv:2610.21042, arxiv:2610.21042
- arxiv:2610.29895: arxiv:2610.29895, arxiv:2610.29895
- doi:10.48550/arxiv.2610.23299: openalex:W7222969410, openalex:W7222969410
- doi:10.3390/superintelligence1020008: openalex:W7164043397, openalex:W7164043397
