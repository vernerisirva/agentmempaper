# Paper Scout Live Smoke Report - 2026-10-22

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 520
- **Unique papers:** 489
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 420
- Sample title: Multimodal Embodied Agents: A Unified Capability-centric Perspective from Computer-Use to Robot-Use
- Sample source ID: 2610.30108
- Sample URL: https://arxiv.org/abs/2610.30108v1
- Sample published date: 2026-10-21
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory
- Sample source ID: W7222038340
- Sample URL: https://arxiv.org/abs/2610.19366
- Sample published date: 2026-10-14
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 37
- maybe: 48
- irrelevant: 404

## Top Relevant Or Maybe Papers

- **Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.19366v1
- **Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.19366
- **Recall What Is Missing: Composing Evidence from Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.15642
- **RL-Guided Temporal Localization for Dual-Channel Retrieval in Long-Horizon Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.23598
- **PreCoMem: Predictive Cognitive Memory for Self-Evolving Long-Term Dialogue Agents** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.29467v1
- **Multimodal Filesystem Memory For Long-Horizon Embodied Agents** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2610.22686v1
- **Memory Internalization via Test-Time Training for Long-Video Understanding** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2610.26910v1
- **MemCode: Discrete Semantic Representations for Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.19472
- **CreatorMemBench v1.0: A Lifecycle Benchmark for Mutable Creator-Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.23371367
- **Code and data for: Quantum Similarity Search for LLM-Agent Memory Retrieval under Bounded State Preparation** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.23306776

## Source Failures

- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.30108: arxiv:2610.30108, arxiv:2610.30108
- arxiv:2610.29995: arxiv:2610.29995, arxiv:2610.29995
- arxiv:2610.29823: arxiv:2610.29823, arxiv:2610.29823
- arxiv:2610.29671: arxiv:2610.29671, arxiv:2610.29671
- arxiv:2610.29560: arxiv:2610.29560, arxiv:2610.29560
- arxiv:2610.29467: arxiv:2610.29467, arxiv:2610.29467
- arxiv:2610.29357: arxiv:2610.29357, arxiv:2610.29357, arxiv:2610.29357, arxiv:2610.29357
- arxiv:2610.29327: arxiv:2610.29327, arxiv:2610.29327
- arxiv:2610.29249: arxiv:2610.29249, arxiv:2610.29249
- arxiv:2610.28945: arxiv:2610.28945, arxiv:2610.28945
- arxiv:2610.29845: arxiv:2610.29845, arxiv:2610.29845
- arxiv:2610.29329: arxiv:2610.29329, arxiv:2610.29329
- arxiv:2610.29317: arxiv:2610.29317, arxiv:2610.29317
- arxiv:2610.26825: arxiv:2610.26825, arxiv:2610.26825
- arxiv:2610.25237: arxiv:2610.25237, arxiv:2610.25237
- arxiv:2610.20399: arxiv:2610.20399, arxiv:2610.20399
- arxiv:2610.29302: arxiv:2610.29302, arxiv:2610.29302
- arxiv:2610.30132: arxiv:2610.30132, arxiv:2610.30132
- arxiv:2610.30068: arxiv:2610.30068, arxiv:2610.30068
- arxiv:2610.29832: arxiv:2610.29832, arxiv:2610.29832
- arxiv:2610.29784: arxiv:2610.29784, arxiv:2610.29784
- arxiv:2610.29641: arxiv:2610.29641, arxiv:2610.29641
- arxiv:2610.29472: arxiv:2610.29472, arxiv:2610.29472
- arxiv:2610.29378: arxiv:2610.29378, arxiv:2610.29378
- arxiv:2610.29167: arxiv:2610.29167, arxiv:2610.29167
- doi:10.48550/arxiv.2610.21165: openalex:W7222470937, openalex:W7222470937
- doi:10.48550/arxiv.2610.22217: openalex:W7222625301, openalex:W7222625301
- doi:10.48550/arxiv.2610.19271: openalex:W7222006676, openalex:W7222006676
- doi:10.48550/arxiv.2610.11776: openalex:W7221160365, openalex:W7221160365
