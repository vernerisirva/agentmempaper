# Paper Scout Live Smoke Report - 2026-11-27

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 513
- **Unique papers:** 480
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 413
- Sample title: Agentic LongLive: Asynchronous Agentic Memory for Long Video Generation
- Sample source ID: 2611.34907
- Sample URL: https://arxiv.org/abs/2611.34907v1
- Sample published date: 2026-11-25
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
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 22
- maybe: 49
- irrelevant: 409

## Top Relevant Or Maybe Papers

- **Mem-X: A Memory-Dependent Cross-Episode Benchmark for Vision-and-Language Navigation** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.27166
- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.20759v1
- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.20759
- **Failure Broadens, Success Sharpens: Continual Adaptation of Tool-Use Agents Across Diverse Tasks with Dual-Polarity Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.48550/arxiv.2611.33612
- **Failure Broadens, Success Sharpens: Continual Adaptation of Tool-Use Agents Across Diverse Tasks with Dual-Polarity Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2611.33612v1
- **Agent Memory Integrity Benchmark (AMIB)** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.24227858
- **Agent Memory & State Management: A Unified Framework for Persistent Memory, Stateful Execution, and Reliable Autonomous AI Systems** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.24368985
- **LEDGER: Auditable Agent Memory Under Change** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2611.20927
- **HEAMS: Holistic Evaluation of Agent Memory Systems** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.20144
- **enron-memory-replay: an agent memory replayed week by week through one mailbox of the Enron corpus** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.24241955

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.34776: arxiv:2611.34776, arxiv:2611.34776
- arxiv:2611.34762: arxiv:2611.34762, arxiv:2611.34762, arxiv:2611.34762
- arxiv:2611.34675: arxiv:2611.34675, arxiv:2611.34675, arxiv:2611.34675, arxiv:2611.34675
- arxiv:2611.34290: arxiv:2611.34290, arxiv:2611.34290
- arxiv:2611.34249: arxiv:2611.34249, arxiv:2611.34249, arxiv:2611.34249, arxiv:2611.34249
- arxiv:2611.34215: arxiv:2611.34215, arxiv:2611.34215
- arxiv:2611.33897: arxiv:2611.33897, arxiv:2611.33897, arxiv:2611.33897
- arxiv:2611.33822: arxiv:2611.33822, arxiv:2611.33822, arxiv:2611.33822
- arxiv:2611.33612: arxiv:2611.33612, arxiv:2611.33612, arxiv:2611.33612
- arxiv:2611.34576: arxiv:2611.34576, arxiv:2611.34576
- arxiv:2611.26615: arxiv:2611.26615, arxiv:2611.26615
- arxiv:2611.26361: arxiv:2611.26361, arxiv:2611.26361
- arxiv:2611.33875: arxiv:2611.33875, arxiv:2611.33875
- arxiv:2611.30287: arxiv:2611.30287, arxiv:2611.30287
- arxiv:2611.34881: arxiv:2611.34881, arxiv:2611.34881
- arxiv:2611.34420: arxiv:2611.34420, arxiv:2611.34420
- arxiv:2611.34400: arxiv:2611.34400, arxiv:2611.34400
- arxiv:2611.34398: arxiv:2611.34398, arxiv:2611.34398
- arxiv:2611.33836: arxiv:2611.33836, arxiv:2611.33836
- doi:10.1145/3863973: openalex:W4393942320, openalex:W4393942320
- doi:10.21203/rs.3.rs-11495678/v1: openalex:W7212078144, openalex:W7212078144, openalex:W7212078144
- doi:10.48550/arxiv.2611.18113: openalex:W7233989087, openalex:W7233989087
- doi:10.48550/arxiv.2611.28298: openalex:W7239400910, openalex:W7239400910
- doi:10.48550/arxiv.2611.27973: openalex:W7238834291, openalex:W7238834291
