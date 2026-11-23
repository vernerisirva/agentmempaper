# Paper Scout Live Smoke Report - 2026-11-23

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 513
- **Unique papers:** 483
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 413
- Sample title: Do Alice and Bob Dream of the Oracle? Wishful Cryptanalysis
- Sample source ID: 2611.27729
- Sample URL: https://arxiv.org/abs/2611.27729v1
- Sample published date: 2026-11-20
- Abstract: yes

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
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 26
- maybe: 62
- irrelevant: 395

## Top Relevant Or Maybe Papers

- **Mem-X: A Memory-Dependent Cross-Episode Benchmark for Vision-and-Language Navigation** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.27166v1
- **MIRIX-2.0: Multi-Agent Memory System** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.12068v1
- **MIRIX-2.0: Multi-Agent Memory System** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.12068
- **Learning to remember: advances in memory mechanisms for large language models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.1007/s44336-026-00044-1
- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.20759v1
- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.20759
- **Agent Memory Integrity Benchmark (AMIB)** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.24227858
- **Agent Memory & State Management: A Unified Framework for Persistent Memory, Stateful Execution, and Reliable Autonomous AI Systems** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.24368985
- **SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.22017v1
- **LEDGER: Auditable Agent Memory Under Change** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2611.20927

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.27729: arxiv:2611.27729, arxiv:2611.27729
- arxiv:2611.27689: arxiv:2611.27689, arxiv:2611.27689, arxiv:2611.27689
- arxiv:2611.27499: arxiv:2611.27499, arxiv:2611.27499
- arxiv:2611.27381: arxiv:2611.27381, arxiv:2611.27381
- arxiv:2611.27219: arxiv:2611.27219, arxiv:2611.27219, arxiv:2611.27219
- arxiv:2611.27138: arxiv:2611.27138, arxiv:2611.27138
- arxiv:2611.27095: arxiv:2611.27095, arxiv:2611.27095
- arxiv:2611.27046: arxiv:2611.27046, arxiv:2611.27046
- arxiv:2611.26983: arxiv:2611.26983, arxiv:2611.26983
- arxiv:2611.26980: arxiv:2611.26980, arxiv:2611.26980
- arxiv:2611.26912: arxiv:2611.26912, arxiv:2611.26912
- arxiv:2611.26910: arxiv:2611.26910, arxiv:2611.26910
- arxiv:2611.26902: arxiv:2611.26902, arxiv:2611.26902
- arxiv:2611.26423: arxiv:2611.26423, arxiv:2611.26423
- arxiv:2611.26361: arxiv:2611.26361, arxiv:2611.26361, arxiv:2611.26361
- arxiv:2611.26615: arxiv:2611.26615, arxiv:2611.26615
- arxiv:2611.25889: arxiv:2611.25889, arxiv:2611.25889
- arxiv:2611.27500: arxiv:2611.27500, arxiv:2611.27500
- arxiv:2611.27365: arxiv:2611.27365, arxiv:2611.27365
- arxiv:2611.25433: arxiv:2611.25433, arxiv:2611.25433
- arxiv:2611.27353: arxiv:2611.27353, arxiv:2611.27353
- arxiv:2611.27317: arxiv:2611.27317, arxiv:2611.27317
- doi:10.48550/arxiv.2611.12068: openalex:W7225721830, openalex:W7225721830
- doi:10.1007/s44336-026-00044-1: openalex:W7223835807, openalex:W7223835807, openalex:W7223835807
- doi:10.48550/arxiv.2611.13127: openalex:W7225816720, openalex:W7225816720
- doi:10.21203/rs.3.rs-11495678/v1: openalex:W7212078144, openalex:W7212078144
