# Paper Scout Live Smoke Report - 2026-10-26

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 600
- **Candidates fetched:** 518
- **Unique papers:** 486
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 418
- Sample title: ActionRAG: Evidence-Refining Graph Diffusion for Long-Term Memory in LLM Agents
- Sample source ID: 2610.32752
- Sample URL: https://arxiv.org/abs/2610.32752v1
- Sample published date: 2026-10-23
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
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 31
- maybe: 51
- irrelevant: 404

## Top Relevant Or Maybe Papers

- **Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.19366v1
- **Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.19366
- **SAFE-Mem: Secure Agentic Memory with Fine-Grained Authority and Governance-Aware Retrieval** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.22959
- **Recovery Budgets for Persistent AI-Agent Memory: Reproducibility Artifact** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.23623901
- **RL-Guided Temporal Localization for Dual-Channel Retrieval in Long-Horizon Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.23598
- **Multimodal Filesystem Memory For Long-Horizon Embodied Agents** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2610.22686
- **Memory Internalization via Test-Time Training for Long-Video Understanding** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2610.26910v1
- **MemCode: Discrete Semantic Representations for Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.19472
- **CreatorMemBench v1.0: A Lifecycle Benchmark for Mutable Creator-Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.23371367
- **BetaMem: Learning to Remember a Changing World for Embodied Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.26554v1

## Source Failures

- semantic_scholar (HTTP/API error) for `parametric memory LLM`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.32752: arxiv:2610.32752, arxiv:2610.32752
- arxiv:2610.32477: arxiv:2610.32477, arxiv:2610.32477
- arxiv:2610.32464: arxiv:2610.32464, arxiv:2610.32464, arxiv:2610.32464
- arxiv:2610.32370: arxiv:2610.32370, arxiv:2610.32370, arxiv:2610.32370
- arxiv:2610.32332: arxiv:2610.32332, arxiv:2610.32332
- arxiv:2610.32295: arxiv:2610.32295, arxiv:2610.32295, arxiv:2610.32295
- arxiv:2610.32002: arxiv:2610.32002, arxiv:2610.32002
- arxiv:2610.31789: arxiv:2610.31789, arxiv:2610.31789
- arxiv:2610.31307: arxiv:2610.31307, arxiv:2610.31307
- arxiv:2610.32265: arxiv:2610.32265, arxiv:2610.32265
- arxiv:2610.26825: arxiv:2610.26825, arxiv:2610.26825
- arxiv:2610.25237: arxiv:2610.25237, arxiv:2610.25237
- arxiv:2610.31401: arxiv:2610.31401, arxiv:2610.31401
- arxiv:2610.32046: arxiv:2610.32046, arxiv:2610.32046
- arxiv:2610.32891: arxiv:2610.32891, arxiv:2610.32891
- arxiv:2610.32881: arxiv:2610.32881, arxiv:2610.32881
- arxiv:2610.32770: arxiv:2610.32770, arxiv:2610.32770
- arxiv:2610.32481: arxiv:2610.32481, arxiv:2610.32481
- arxiv:2610.32474: arxiv:2610.32474, arxiv:2610.32474
- arxiv:2610.32423: arxiv:2610.32423, arxiv:2610.32423
- arxiv:2610.32326: arxiv:2610.32326, arxiv:2610.32326
- arxiv:2610.32103: arxiv:2610.32103, arxiv:2610.32103
- arxiv:2610.32101: arxiv:2610.32101, arxiv:2610.32101
- arxiv:2610.31946: arxiv:2610.31946, arxiv:2610.31946
- doi:10.48550/arxiv.2610.21165: openalex:W7222470937, openalex:W7222470937, openalex:W7222470937
- doi:10.48550/arxiv.2610.22217: openalex:W7222625301, openalex:W7222625301
- doi:10.48550/arxiv.2610.19271: openalex:W7222006676, openalex:W7222006676
- doi:10.48550/arxiv.2610.25425: openalex:W7223000881, openalex:W7223000881
