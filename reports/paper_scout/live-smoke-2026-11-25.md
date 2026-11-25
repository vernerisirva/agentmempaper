# Paper Scout Live Smoke Report - 2026-11-25

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 600
- **Candidates fetched:** 512
- **Unique papers:** 484
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 412
- Sample title: AIChipBench: Benchmarking LLM Agents for Automated AI Accelerator Design
- Sample source ID: 2611.33093
- Sample URL: https://arxiv.org/abs/2611.33093v1
- Sample published date: 2026-11-24
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Agent Memory
- Sample source ID: W7238877371
- Sample URL: https://doi.org/10.1002/9781394324613.ch6
- Sample published date: 2026-11-23
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 19
- maybe: 75
- irrelevant: 390

## Top Relevant Or Maybe Papers

- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.20759v1
- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.20759
- **DISCERN: Preserve at Write, Resolve at Read for Persistent LLM-Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.15729
- **Agent Memory Integrity Benchmark (AMIB)** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.24227858
- **Agent Memory & State Management: A Unified Framework for Persistent Memory, Stateful Execution, and Reliable Autonomous AI Systems** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.24368985
- **SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.22017v2
- **SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.22017
- **LEDGER: Auditable Agent Memory Under Change** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2611.20927
- **HEAMS: Holistic Evaluation of Agent Memory Systems** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.20144
- **enron-memory-replay: an agent memory replayed week by week through one mailbox of the Enron corpus** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.24241955

## Source Failures

- semantic_scholar (HTTP/API error) for `parametric memory LLM`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.33093: arxiv:2611.33093, arxiv:2611.33093
- arxiv:2611.33005: arxiv:2611.33005, arxiv:2611.33005
- arxiv:2611.32954: arxiv:2611.32954, arxiv:2611.32954
- arxiv:2611.32811: arxiv:2611.32811, arxiv:2611.32811
- arxiv:2611.32218: arxiv:2611.32218, arxiv:2611.32218
- arxiv:2611.32209: arxiv:2611.32209, arxiv:2611.32209
- arxiv:2611.32203: arxiv:2611.32203, arxiv:2611.32203
- arxiv:2611.32119: arxiv:2611.32119, arxiv:2611.32119
- arxiv:2611.31173: arxiv:2611.31173, arxiv:2611.31173
- arxiv:2611.31117: arxiv:2611.31117, arxiv:2611.31117
- arxiv:2611.26615: arxiv:2611.26615, arxiv:2611.26615
- arxiv:2611.26361: arxiv:2611.26361, arxiv:2611.26361
- arxiv:2611.30287: arxiv:2611.30287, arxiv:2611.30287, arxiv:2611.30287
- arxiv:2611.33119: arxiv:2611.33119, arxiv:2611.33119
- arxiv:2611.32660: arxiv:2611.32660, arxiv:2611.32660
- arxiv:2611.32564: arxiv:2611.32564, arxiv:2611.32564
- arxiv:2611.32508: arxiv:2611.32508, arxiv:2611.32508
- arxiv:2611.32472: arxiv:2611.32472, arxiv:2611.32472
- arxiv:2611.32390: arxiv:2611.32390, arxiv:2611.32390
- arxiv:2611.32347: arxiv:2611.32347, arxiv:2611.32347
- arxiv:2611.32292: arxiv:2611.32292, arxiv:2611.32292
- doi:10.1109/swc69865.2026.11763986: arxiv:2611.32266, arxiv:2611.32266
- arxiv:2611.32238: arxiv:2611.32238, arxiv:2611.32238
- doi:10.1145/3863973: openalex:W4393942320, openalex:W4393942320
- doi:10.21203/rs.3.rs-11495678/v1: openalex:W7212078144, openalex:W7212078144, openalex:W7212078144
- doi:10.48550/arxiv.2611.18113: openalex:W7233989087, openalex:W7233989087
