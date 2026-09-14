# Paper Scout Live Smoke Report - 2026-09-14

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 125
- **Candidates fetched:** 27
- **Unique papers:** 27
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: Timeout/network error: timeout error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out

### openalex

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 25
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-09-12
- Abstract: yes
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=procedural+memory+language+model&filter=from_publication_date%3A2026-08-31&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 2
- Sample title: Modality Disentangled Learning for Incomplete Multimodal Emotion Recognition: A Primitive Memory Distillation Perspective
- Sample source ID: 50b458d018f8452a620325eb4a6f80652a52e215
- Sample URL: https://www.semanticscholar.org/paper/50b458d018f8452a620325eb4a6f80652a52e215
- Sample published date: 2026-08-31
- Abstract: yes


## Decisions

- relevant: 10
- maybe: 15
- irrelevant: 2

## Top Relevant Or Maybe Papers

- **Personalizing LLM Agent Memory Using Biometrics** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2609.08558
- **Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.11060
- **What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.08279
- **MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.08273
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260019
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260018
- **Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.30177
- **Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.08258
- **ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://www.semanticscholar.org/paper/57563394951aebb6d7f5611808eac0ba14a5bb87
- **Memory as Infrastructure: Reliability Engineering for Persistent Agent Memory in Months-Long LLM-Assisted Development** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2609.05510

## Source Failures

- arxiv (Timeout/network error) for `agent memory`: timeout error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out
- openalex (HTTP/API error) for `procedural memory language model`: http error for https://api.openalex.org/works?search=procedural+memory+language+model&filter=from_publication_date%3A2026-08-31&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- No duplicates found.
