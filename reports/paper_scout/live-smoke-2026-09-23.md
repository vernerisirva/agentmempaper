# Paper Scout Live Smoke Report - 2026-09-23

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 125
- **Candidates fetched:** 100
- **Unique papers:** 92
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-09-12
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 9
- maybe: 29
- irrelevant: 54

## Top Relevant Or Maybe Papers

- **PSD: Pseudo Self-Distillation of Memory Representation Capabilities for LLM Agents** (relevant, 100/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.48550/arxiv.2609.23449
- **Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.11060
- **DolphinBench: Mapping the Pareto Frontier of Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.48550/arxiv.2609.24971
- **Procedural Memory Under Change: Reuse and Interference in Controlled Web Tasks** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.09774
- **LSG: A Lightweight Supervised Gate for Sub-Millisecond Agentic Memory Novelty Filtering** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22889960
- **LSG: A Lightweight Supervised Gate for Sub-Millisecond Agentic Memory Novelty Filtering** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22889959
- **Cognitive Extensions for Dual-Process Language Agents: Memory and Self-Reflection in Interactive Environments** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.19128
- **Consolidation Without Weights: What the Complementary Learning Systems Analogy Licenses in LLM Agent Memory, and Why the Systems That Borrow Its Name Do Not Inherit Its Guarantee** (relevant, 90/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.5281/zenodo.22699102
- **Consolidation Without Weights: What the Complementary Learning Systems Analogy Licenses in LLM Agent Memory, and Why the Systems That Borrow Its Name Do Not Inherit Its Guarantee** (relevant, 90/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.5281/zenodo.22699101
- **fidelis: zero-LLM agent memory for Claude Code and AI agents** (maybe, 69/100): Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory. https://doi.org/10.5281/zenodo.22732418

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- doi:10.48550/arxiv.2609.19128: openalex:W7213516733, openalex:W7213516733
- doi:10.5281/zenodo.22699101: openalex:W7212154123, openalex:W7212154123
- doi:10.5281/zenodo.22699102: openalex:W7212131127, openalex:W7212131127
- doi:10.48550/arxiv.2609.19502: openalex:W7213596096, openalex:W7213596096
- doi:10.1145/3845797: openalex:W4390529182, openalex:W4390529182
- doi:10.1162/coli.a.652: openalex:W4403048355, openalex:W4403048355
- doi:10.1016/j.inffus.2026.104791: openalex:W4403882865, openalex:W4403882865
- openalex:W7213371194: openalex:W7213371194, openalex:W7213371194
