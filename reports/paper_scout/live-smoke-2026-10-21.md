# Paper Scout Live Smoke Report - 2026-10-21

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 102
- **Unique papers:** 97
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory
- Sample source ID: W7222038340
- Sample URL: https://arxiv.org/abs/2610.19366
- Sample published date: 2026-10-14
- Abstract: yes

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 2
- Sample title: TAM: Task-Aware Memory Distillation for Efficient Spatiotemporal Prediction
- Sample source ID: 27f95babe0a49454413d0115e45ca32abd9d4053
- Sample URL: https://www.semanticscholar.org/paper/27f95babe0a49454413d0115e45ca32abd9d4053
- Sample published date: 2026-10-08
- Abstract: yes


## Decisions

- relevant: 17
- maybe: 23
- irrelevant: 57

## Top Relevant Or Maybe Papers

- **Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.19366
- **SAFE-Mem: Secure Agentic Memory with Fine-Grained Authority and Governance-Aware Retrieval** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2610.22959
- **Recall What Is Missing: Composing Evidence from Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.15642
- **RL-Guided Temporal Localization for Dual-Channel Retrieval in Long-Horizon Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2610.23598
- **MemCode: Discrete Semantic Representations for Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.19472
- **CreatorMemBench v1.0: A Lifecycle Benchmark for Mutable Creator-Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.23371367
- **Code and data for: Quantum Similarity Search for LLM-Agent Memory Retrieval under Bounded State Preparation** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.23306776
- **Beyond Downstream QA: Rethinking How We Evaluate Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2610.22209
- **SEPM: Self-Evolving Procedural Memory Grounded in Task Graphs for Multi-Agent Collaboration** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.14515
- **Persistent Agent Memory under the EU AI Act and NIS2: Misalignment, Emergent Behaviour and Regulatory Fit** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.1017/err.2026.10159

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- doi:10.48550/arxiv.2610.10071: openalex:W7220906218, openalex:W7220906218
- doi:10.48550/arxiv.2610.21165: openalex:W7222470937, openalex:W7222470937
- doi:10.48550/arxiv.2610.22217: openalex:W7222625301, openalex:W7222625301
- doi:10.48550/arxiv.2610.19271: openalex:W7222006676, openalex:W7222006676
- doi:10.48550/arxiv.2610.11776: openalex:W7221160365, openalex:W7221160365
