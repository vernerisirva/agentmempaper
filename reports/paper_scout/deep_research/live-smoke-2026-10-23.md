# Paper Scout Live Smoke Report - 2026-10-23

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 250
- **Candidates fetched:** 158
- **Unique papers:** 150
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 58
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
- Sample title: RIVO: Lightweight Adaptive Rerouting for Deep Research Agents
- Sample source ID: W7221819642
- Sample URL: https://arxiv.org/abs/2610.15910
- Sample published date: 2026-10-11
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 35
- maybe: 15
- irrelevant: 100

## Top Relevant Or Maybe Papers

- **Auto-MD-bench: Evaluating Autoresearch Agents for Real-World Medical Tasks** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.25069v1
- **Auto-MD-bench: Evaluating Autoresearch Agents for Real-World Medical Tasks** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.25069
- **Triage-PiEvo: Evidence Admission for Principle-Evolving Scientific Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.14683v1
- **Triage-PiEvo: Evidence Admission for Principle-Evolving Scientific Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.14683
- **THE EL-RAKHAWI GLOBAL PROTOCOL FOR OPEN-SOURCE BIOLOGICAL DISCOVERY AND ANTI-BIOPIRACY From Monopolistic "AI Scientists" to Sovereign Science for Humanity A Groundbreaking Engineering and Legal Framework for Democratizing Autonomous Discovery, Advanced Therapies, and Climate-Resilient Agricultur** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23304572
- **Restricted materials (reference answers and raw agent session outputs) for: Autonomous AI scientists converge on estimates but diverge on uncertainty** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23300593
- **RIVO: Lightweight Adaptive Rerouting for Deep Research Agents** (relevant, 93/100): Studies research-agent memory or iterative research state. https://arxiv.org/abs/2610.15910
- **Mr.LHDR: A Benchmark for Multimodal Real-World Long-Horizon Deep Research Agents** (relevant, 93/100): Studies autonomous or deep research agents. https://doi.org/10.13140/rg.2.2.27194.15043
- **IAISS 2026 Project 10: ALS AI Scientist, run archives and results (pl-prod-014 to pl-prod-018)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23370542
- **ExpEvolve: Structuring and Reusing Experience for Open-Ended Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.29303v1

## Source Failures

- semantic_scholar (HTTP/API error) for `AI scientist`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.29346: arxiv:2610.29346, arxiv:2610.29346
- doi:10.1016/j.sysarc.2026.103874: arxiv:2610.28699, arxiv:2610.28699
- arxiv:2610.30181: arxiv:2610.30181, arxiv:2610.30181
- arxiv:2610.23299: arxiv:2610.23299, arxiv:2610.23299
- arxiv:2610.21042: arxiv:2610.21042, arxiv:2610.21042
- arxiv:2610.29895: arxiv:2610.29895, arxiv:2610.29895
- doi:10.48550/arxiv.2610.23299: openalex:W7222969410, openalex:W7222969410
- doi:10.3390/superintelligence1020008: openalex:W7164043397, openalex:W7164043397
