# Paper Scout Live Smoke Report - 2026-10-21

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 150
- **Candidates fetched:** 101
- **Unique papers:** 99
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Too Many Requests

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
- Converted candidates: 1
- Sample title: A Society of Researchers: Designing Institutions for Populations of Autonomous Research Agents
- Sample source ID: 5f55637d8707af3af30b52e9c0d431c5cd613a01
- Sample URL: https://www.semanticscholar.org/paper/5f55637d8707af3af30b52e9c0d431c5cd613a01
- Sample published date: 2026-10-07
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 21
- maybe: 7
- irrelevant: 71

## Top Relevant Or Maybe Papers

- **Triage-PiEvo: Evidence Admission for Principle-Evolving Scientific Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.14683
- **THE EL-RAKHAWI GLOBAL PROTOCOL FOR OPEN-SOURCE BIOLOGICAL DISCOVERY AND ANTI-BIOPIRACY From Monopolistic "AI Scientists" to Sovereign Science for Humanity A Groundbreaking Engineering and Legal Framework for Democratizing Autonomous Discovery, Advanced Therapies, and Climate-Resilient Agricultur** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23304572
- **Restricted materials (reference answers and raw agent session outputs) for: Autonomous AI scientists converge on estimates but diverge on uncertainty** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23300593
- **RIVO: Lightweight Adaptive Rerouting for Deep Research Agents** (relevant, 93/100): Studies research-agent memory or iterative research state. https://arxiv.org/abs/2610.15910
- **Mr.LHDR: A Benchmark for Multimodal Real-World Long-Horizon Deep Research Agents** (relevant, 93/100): Studies autonomous or deep research agents. https://doi.org/10.13140/rg.2.2.27194.15043
- **IAISS 2026 Project 10: ALS AI Scientist, run archives and results (pl-prod-014 to pl-prod-018)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23370542
- **DrugTargetWorld: A Synthetic Biobank for Training and Benchmarking AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.09558
- **Designing Human-AI Collaborative Science: The 9A Framework** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2610.22948
- **DataSense-Bench: The First Step Toward an AI Scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.12190
- **Code and public materials for: Autonomous AI scientists converge on estimates but diverge on uncertainty** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23300515

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- semantic_scholar (HTTP/API error) for `AI scientist`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- doi:10.48550/arxiv.2610.23299: openalex:W7222969410, openalex:W7222969410
- doi:10.3390/superintelligence1020008: openalex:W7164043397, openalex:W7164043397
