# Paper Scout Live Smoke Report - 2026-10-20

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 125
- **Candidates fetched:** 100
- **Unique papers:** 93
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

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 14
- maybe: 22
- irrelevant: 57

## Top Relevant Or Maybe Papers

- **Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.19366
- **Recall What Is Missing: Composing Evidence from Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.15642
- **MemCode: Discrete Semantic Representations for Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.19472
- **MINDSET: Energy-based Schema Evolution for Long Conversational Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.08586
- **CreatorMemBench v1.0: A Lifecycle Benchmark for Mutable Creator-Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.23371367
- **Code and data for: Quantum Similarity Search for LLM-Agent Memory Retrieval under Bounded State Preparation** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.23306776
- **Beyond Downstream QA: Rethinking How We Evaluate Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2610.22209
- **SEPM: Self-Evolving Procedural Memory Grounded in Task Graphs for Multi-Agent Collaboration** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.14515
- **Persistent Agent Memory under the EU AI Act and NIS2: Misalignment, Emergent Behaviour and Regulatory Fit** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.1017/err.2026.10159
- **Memory Type Varies: Empowering LLM Agents for Long-Term Memory with Diverse Strategies** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.11573

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- doi:10.48550/arxiv.2610.08048: openalex:W7221062216, openalex:W7221062216
- doi:10.48550/arxiv.2610.10071: openalex:W7220906218, openalex:W7220906218
- doi:10.13140/rg.2.2.14834.06082: openalex:W7220733556, openalex:W7220733556
- doi:10.48550/arxiv.2610.21165: openalex:W7222470937, openalex:W7222470937
- doi:10.48550/arxiv.2610.22217: openalex:W7222625301, openalex:W7222625301
- doi:10.48550/arxiv.2610.19271: openalex:W7222006676, openalex:W7222006676
- doi:10.48550/arxiv.2610.11776: openalex:W7221160365, openalex:W7221160365
