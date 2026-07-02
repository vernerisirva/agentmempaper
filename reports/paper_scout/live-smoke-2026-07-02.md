# Paper Scout Live Smoke Report - 2026-07-02

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 0
- **Sources failed:** 3
- **Raw records:** 575
- **Candidates fetched:** 38
- **Unique papers:** 23
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22agent+memory%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-06-18&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable

### semantic_scholar

- Status: Failed
- Queries attempted: 24
- Raw records: 575
- Converted candidates: 38
- Sample title: Always-OnAgents:A Survey of Persistent Memory, State, and Governance in LLMAgents
- Sample source ID: 87e2041b525cecfb9d6aa6908100faf9e7545587
- Sample URL: https://www.semanticscholar.org/paper/87e2041b525cecfb9d6aa6908100faf9e7545587
- Sample published date: 2026-06-29
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 12
- maybe: 3
- irrelevant: 8

## Top Relevant Or Maybe Papers

- **TRUSTMEM: Learning Trustworthy Memory Consolidation for LLM Agents with Long-Term Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://www.semanticscholar.org/paper/1d3d2f04270110888af84b9222c8a6a41a791b54
- **Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://www.semanticscholar.org/paper/8f901170b067c63db1d2067885926954e7441ccb
- **AtomMem: Building Simple and Effective Memory System for LLM Agents via Atomic Facts** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://www.semanticscholar.org/paper/e4c62633ee5b54b3c6db5434d228067b8e50f76e
- **Are We Ready For An Agent-Native Memory System?** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://www.semanticscholar.org/paper/ac2c86ea6117ff3ca422923ea51a5de19a391099
- **AdaMem: Learning What to Remember for Personalized Long-Horizon LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://www.semanticscholar.org/paper/ea0a600b90c61e5348f9d2e64ab6065d5def9139
- **Mandol: An Agglomerative Agent Memory System for Long-Term Conversations** (relevant, 99/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://www.semanticscholar.org/paper/7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8
- **ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://www.semanticscholar.org/paper/57563394951aebb6d7f5611808eac0ba14a5bb87
- **Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://www.semanticscholar.org/paper/05c11d86a4b91c94b0178c1b5f80340720a5bfec
- **Agent-Native Immune System: Architecture, Taxonomy, and Engineering** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://www.semanticscholar.org/paper/1f663e73091d3b776bde5d6d13520434cfc3fcf0
- **Memory Contagion: Cross-Temporal Propagation of Evaluator Bias via Agent Memory** (relevant, 90/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://www.semanticscholar.org/paper/74d393a345e6fb29308dde0940b7f6b2c8976afe

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22agent+memory%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- openalex (HTTP/API error) for `agent memory`: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-06-18&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable
- semantic_scholar (HTTP/API error) for `agent memory benchmark`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2606.30639: semantic_scholar:4a397b42a1352f4a67938b84d3332382b0c7bdea, semantic_scholar:4a397b42a1352f4a67938b84d3332382b0c7bdea
- doi:10.48550/arxiv.2602.01869: semantic_scholar:57563394951aebb6d7f5611808eac0ba14a5bb87, semantic_scholar:57563394951aebb6d7f5611808eac0ba14a5bb87
- semantic_scholar:16086f872f1c52a6a5ea2c7ce7ac79b026c2b3c7: semantic_scholar:16086f872f1c52a6a5ea2c7ce7ac79b026c2b3c7, semantic_scholar:16086f872f1c52a6a5ea2c7ce7ac79b026c2b3c7
- arxiv:2606.24535: semantic_scholar:d04271d7fe5d097d9dd60bc5c20fe520ca1a9cc6, semantic_scholar:d04271d7fe5d097d9dd60bc5c20fe520ca1a9cc6
- arxiv:2606.24775: semantic_scholar:ac2c86ea6117ff3ca422923ea51a5de19a391099, semantic_scholar:ac2c86ea6117ff3ca422923ea51a5de19a391099, semantic_scholar:ac2c86ea6117ff3ca422923ea51a5de19a391099
- arxiv:2606.28270: semantic_scholar:1f663e73091d3b776bde5d6d13520434cfc3fcf0, semantic_scholar:1f663e73091d3b776bde5d6d13520434cfc3fcf0
- arxiv:2606.22142: semantic_scholar:bff079bde674971a2e3f9d9125f1a3e065a5142d, semantic_scholar:bff079bde674971a2e3f9d9125f1a3e065a5142d
- arxiv:2606.23743: semantic_scholar:6c8180090511a0c30e74bf6e0add3a42812fd28b, semantic_scholar:6c8180090511a0c30e74bf6e0add3a42812fd28b
- arxiv:2606.28781: semantic_scholar:2f7ee6adc9ba9c7345bdd550b461a773ba70dbc6, semantic_scholar:2f7ee6adc9ba9c7345bdd550b461a773ba70dbc6
- arxiv:2606.29778: semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8
- arxiv:2606.24322: semantic_scholar:8f901170b067c63db1d2067885926954e7441ccb, semantic_scholar:8f901170b067c63db1d2067885926954e7441ccb
