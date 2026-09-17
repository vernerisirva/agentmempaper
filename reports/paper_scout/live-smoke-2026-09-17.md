# Paper Scout Live Smoke Report - 2026-09-17

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 101
- **Unique papers:** 93
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

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 1
- Sample title: ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents
- Sample source ID: 57563394951aebb6d7f5611808eac0ba14a5bb87
- Sample URL: https://www.semanticscholar.org/paper/57563394951aebb6d7f5611808eac0ba14a5bb87
- Sample published date: 2026
- Abstract: no


## Decisions

- relevant: 11
- maybe: 28
- irrelevant: 54

## Top Relevant Or Maybe Papers

- **Personalizing LLM Agent Memory Using Biometrics** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2609.08558
- **Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.11060
- **What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.08279
- **MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.08273
- **Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.08258
- **Procedural Memory Under Change: Reuse and Interference in Controlled Web Tasks** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.09774
- **ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://www.semanticscholar.org/paper/57563394951aebb6d7f5611808eac0ba14a5bb87
- **Delete Names Five Operations: Erasure Semantics for Derived Agent Memory, and Why a State-Level Definition Cannot Be the Auditable One** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.22425281
- **Delete Names Five Operations: Erasure Semantics for Derived Agent Memory, and Why a State-Level Definition Cannot Be the Auditable One** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.22425280
- **Consolidation Without Weights: What the Complementary Learning Systems Analogy Licenses in LLM Agent Memory, and Why the Systems That Borrow Its Name Do Not Inherit Its Guarantee** (relevant, 90/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.5281/zenodo.22699102

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable

## Deduplication Examples

- doi:10.5281/zenodo.22425281: openalex:W7210261900, openalex:W7210261900
- doi:10.5281/zenodo.22425280: openalex:W7210278398, openalex:W7210278398
- doi:10.5281/zenodo.22699102: openalex:W7212131127, openalex:W7212131127
- doi:10.5281/zenodo.22699101: openalex:W7212154123, openalex:W7212154123
- doi:10.48550/arxiv.2609.06006: openalex:W7212078144, openalex:W7212078144
- openalex:W7211978768: openalex:W7211978768, openalex:W7211978768
- doi:10.1145/3845797: openalex:W4390529182, openalex:W4390529182
- doi:10.1145/3844947: openalex:W4417515043, openalex:W4417515043
