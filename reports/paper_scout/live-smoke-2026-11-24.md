# Paper Scout Live Smoke Report - 2026-11-24

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 150
- **Candidates fetched:** 100
- **Unique papers:** 98
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
- Sample title: The Agent Memory Wall
- Sample source ID: W7225828643
- Sample URL: https://doi.org/10.5281/zenodo.24146465
- Sample published date: 2026-11-11
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 17
- maybe: 24
- irrelevant: 57

## Top Relevant Or Maybe Papers

- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.20759
- **DISCERN: Preserve at Write, Resolve at Read for Persistent LLM-Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.15729
- **Agent Memory Integrity Benchmark (AMIB)** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.24227858
- **Agent Memory & State Management: A Unified Framework for Persistent Memory, Stateful Execution, and Reliable Autonomous AI Systems** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.24368985
- **SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.22017
- **LEDGER: Auditable Agent Memory Under Change** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2611.20927
- **HEAMS: Holistic Evaluation of Agent Memory Systems** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.20144
- **Coding Agent Memory Benchmark: LongMemEval-S, LoCoMo, and 19,195-Session Day-Zero Evaluation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.24416711
- **enron-memory-replay: an agent memory replayed week by week through one mailbox of the Enron corpus** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.24241955
- **Memory index in the weights: a proposal for agent memory whose contents stay in files** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.24184983

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- doi:10.21203/rs.3.rs-11495678/v1: openalex:W7212078144, openalex:W7212078144
- doi:10.48550/arxiv.2611.18113: openalex:W7233989087, openalex:W7233989087
