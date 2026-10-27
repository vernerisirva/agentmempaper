# Paper Scout Live Smoke Report - 2026-10-27

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 525
- **Unique papers:** 485
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 425
- Sample title: GEAR: Feature-Based Configuration and Code Generation for Agentic Systems
- Sample source ID: 2610.35592
- Sample URL: https://arxiv.org/abs/2610.35592v1
- Sample published date: 2026-10-26
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: MemoryTax: The Bitter Lesson of Agent Memory
- Sample source ID: W7223250543
- Sample URL: https://arxiv.org/abs/2610.29823
- Sample published date: 2026-10-21
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 37
- maybe: 59
- irrelevant: 389

## Top Relevant Or Maybe Papers

- **Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.19366v1
- **Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.19366
- **Recovery Budgets for Persistent AI-Agent Memory: Reproducibility Artifact** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.23623901
- **RL-Guided Temporal Localization for Dual-Channel Retrieval in Long-Horizon Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.23598
- **Multimodal Filesystem Memory For Long-Horizon Embodied Agents** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2610.22686
- **MemCode: Discrete Semantic Representations for Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.19472
- **Learning to Remember: Advances in Memory Mechanisms for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2610.35089v1
- **CreatorMemBench v1.0: A Lifecycle Benchmark for Mutable Creator-Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.23371367
- **BetaMem: Learning to Remember a Changing World for Embodied Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.26554v1
- **Agent Memory as Recommendation: Recommender-System Design for Long-Term Memory of LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.34673v1

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.35496: arxiv:2610.35496, arxiv:2610.35496
- arxiv:2610.35349: arxiv:2610.35349, arxiv:2610.35349
- arxiv:2610.35316: arxiv:2610.35316, arxiv:2610.35316, arxiv:2610.35316
- arxiv:2610.35272: arxiv:2610.35272, arxiv:2610.35272, arxiv:2610.35272
- arxiv:2610.35160: arxiv:2610.35160, arxiv:2610.35160, arxiv:2610.35160
- arxiv:2610.35089: arxiv:2610.35089, arxiv:2610.35089, arxiv:2610.35089
- arxiv:2610.35023: arxiv:2610.35023, arxiv:2610.35023
- arxiv:2610.34977: arxiv:2610.34977, arxiv:2610.34977, arxiv:2610.34977
- arxiv:2610.34724: arxiv:2610.34724, arxiv:2610.34724, arxiv:2610.34724, arxiv:2610.34724
- arxiv:2610.34450: arxiv:2610.34450, arxiv:2610.34450, arxiv:2610.34450
- arxiv:2610.34073: arxiv:2610.34073, arxiv:2610.34073
- arxiv:2610.35211: arxiv:2610.35211, arxiv:2610.35211
- arxiv:2610.32464: arxiv:2610.32464, arxiv:2610.32464
- arxiv:2610.26825: arxiv:2610.26825, arxiv:2610.26825
- arxiv:2610.25237: arxiv:2610.25237, arxiv:2610.25237
- arxiv:2610.34829: arxiv:2610.34829, arxiv:2610.34829
- arxiv:2610.31401: arxiv:2610.31401, arxiv:2610.31401
- doi:10.1109/igarss60577.2026.11730294: arxiv:2610.35175, arxiv:2610.35175
- arxiv:2610.34886: arxiv:2610.34886, arxiv:2610.34886
- arxiv:2610.35690: arxiv:2610.35690, arxiv:2610.35690
- arxiv:2610.35598: arxiv:2610.35598, arxiv:2610.35598
- arxiv:2610.35295: arxiv:2610.35295, arxiv:2610.35295
- arxiv:2610.34991: arxiv:2610.34991, arxiv:2610.34991
- arxiv:2610.34965: arxiv:2610.34965, arxiv:2610.34965
- arxiv:2610.34921: arxiv:2610.34921, arxiv:2610.34921
- arxiv:2610.34878: arxiv:2610.34878, arxiv:2610.34878
- arxiv:2610.34836: arxiv:2610.34836, arxiv:2610.34836
- doi:10.48550/arxiv.2610.21165: openalex:W7222470937, openalex:W7222470937, openalex:W7222470937
- doi:10.48550/arxiv.2610.22217: openalex:W7222625301, openalex:W7222625301
- doi:10.48550/arxiv.2610.19271: openalex:W7222006676, openalex:W7222006676
- doi:10.48550/arxiv.2610.25425: openalex:W7223000881, openalex:W7223000881
