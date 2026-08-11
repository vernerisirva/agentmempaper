# Paper Scout Live Smoke Report - 2026-08-11

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 518
- **Unique papers:** 490
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 418
- Sample title: SHE: Trajectory-driven Safety Harness Evolution for LLM Agents
- Sample source ID: 2608.09885
- Sample URL: https://arxiv.org/abs/2608.09885v1
- Sample published date: 2026-08-10
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-08-09
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 29
- maybe: 41
- irrelevant: 420

## Top Relevant Or Maybe Papers

- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2607.29032
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032v1
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032
- **RING: Retrieval-Internalized Generation for Continual Large-Scale Knowledge Injection** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.01630v1
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2607.27080
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.27080
- **ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.48550/arxiv.2607.27773
- **ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2607.27773
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2608.07169v1
- **V-Mem: Modality-Routed Retrieval for Long-Term Multimodal Agentic Memory** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2608.01543

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.09885: arxiv:2608.09885, arxiv:2608.09885
- arxiv:2608.09507: arxiv:2608.09507, arxiv:2608.09507
- arxiv:2608.09380: arxiv:2608.09380, arxiv:2608.09380, arxiv:2608.09380
- arxiv:2608.09273: arxiv:2608.09273, arxiv:2608.09273, arxiv:2608.09273
- arxiv:2608.09184: arxiv:2608.09184, arxiv:2608.09184
- arxiv:2608.09119: arxiv:2608.09119, arxiv:2608.09119, arxiv:2608.09119
- arxiv:2608.08996: arxiv:2608.08996, arxiv:2608.08996
- arxiv:2608.08960: arxiv:2608.08960, arxiv:2608.08960, arxiv:2608.08960, arxiv:2608.08960
- arxiv:2608.08795: arxiv:2608.08795, arxiv:2608.08795
- arxiv:2608.04009: arxiv:2608.04009, arxiv:2608.04009
- doi:10.1145/3744916.3787762: arxiv:2608.03286, openalex:W7196981404
- arxiv:2608.09227: arxiv:2608.09227, arxiv:2608.09227, arxiv:2608.09227
- arxiv:2608.09819: arxiv:2608.09819, arxiv:2608.09819
- arxiv:2608.09568: arxiv:2608.09568, arxiv:2608.09568
- arxiv:2608.09555: arxiv:2608.09555, arxiv:2608.09555
- arxiv:2608.09140: arxiv:2608.09140, arxiv:2608.09140
- arxiv:2608.09128: arxiv:2608.09128, arxiv:2608.09128
- arxiv:2608.09109: arxiv:2608.09109, arxiv:2608.09109
- doi:10.1145/3831684: openalex:W4405562150, openalex:W4405562150
- openalex:W7171902691: openalex:W7171902691, openalex:W7171902691
- openalex:W7172474001: openalex:W7172474001, openalex:W7172474001
- doi:10.48550/arxiv.2607.29032: openalex:W7172337063, openalex:W7172337063
