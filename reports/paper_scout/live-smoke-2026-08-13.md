# Paper Scout Live Smoke Report - 2026-08-13

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 514
- **Unique papers:** 473
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 414
- Sample title: DreamFly: Causal Memory and Receding-Horizon Diffusion Planning for Aerial Vision-Language Navigation
- Sample source ID: 2608.12308
- Sample URL: https://arxiv.org/abs/2608.12308v1
- Sample published date: 2026-08-12
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

- relevant: 27
- maybe: 36
- irrelevant: 410

## Top Relevant Or Maybe Papers

- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2607.29032
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032v1
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032
- **The Sleeping Agent: What Gist-Based Context Compression Loses and Why** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.11775v1
- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775v1
- **RING: Retrieval-Internalized Generation for Continual Large-Scale Knowledge Injection** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.01630v1
- **From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.10502v1
- **ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.48550/arxiv.2607.27773
- **ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2607.27773
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://doi.org/10.48550/arxiv.2608.07169

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.12308: arxiv:2608.12308, arxiv:2608.12308
- arxiv:2608.11977: arxiv:2608.11977, arxiv:2608.11977
- arxiv:2608.11967: arxiv:2608.11967, arxiv:2608.11967, arxiv:2608.11967, arxiv:2608.11967
- arxiv:2608.11879: arxiv:2608.11879, arxiv:2608.11879
- arxiv:2608.11775: arxiv:2608.11775, arxiv:2608.11775
- arxiv:2608.11654: arxiv:2608.11654, arxiv:2608.11654
- arxiv:2608.11632: arxiv:2608.11632, arxiv:2608.11632
- arxiv:2608.10775: arxiv:2608.10775, arxiv:2608.10775, arxiv:2608.10775
- arxiv:2608.10676: arxiv:2608.10676, arxiv:2608.10676
- arxiv:2608.10494: arxiv:2608.10494, arxiv:2608.10494, arxiv:2608.10494, arxiv:2608.10494
- arxiv:2608.10178: arxiv:2608.10178, arxiv:2608.10178, arxiv:2608.10178
- arxiv:2608.04009: arxiv:2608.04009, arxiv:2608.04009
- doi:10.1145/3744916.3787762: arxiv:2608.03286, openalex:W7196981404
- arxiv:2608.09227: arxiv:2608.09227, arxiv:2608.09227
- arxiv:2608.12099: arxiv:2608.12099, arxiv:2608.12099
- arxiv:2608.12290: arxiv:2608.12290, arxiv:2608.12290
- arxiv:2608.11994: arxiv:2608.11994, arxiv:2608.11994
- arxiv:2608.11924: arxiv:2608.11924, arxiv:2608.11924
- arxiv:2608.11843: arxiv:2608.11843, arxiv:2608.11843
- arxiv:2608.11705: arxiv:2608.11705, arxiv:2608.11705
- arxiv:2608.11660: arxiv:2608.11660, arxiv:2608.11660
- arxiv:2608.11650: arxiv:2608.11650, arxiv:2608.11650
- arxiv:2608.11587: arxiv:2608.11587, arxiv:2608.11587
- arxiv:2608.11573: arxiv:2608.11573, arxiv:2608.11573
- arxiv:2608.11350: arxiv:2608.11350, arxiv:2608.11350
- openalex:W7202230549: openalex:W7202230549, openalex:W7202230549
- doi:10.48550/arxiv.2608.07169: openalex:W7202132500, openalex:W7202132500
- openalex:W7201914503: openalex:W7201914503, openalex:W7201914503
- doi:10.1145/3831684: openalex:W4405562150, openalex:W4405562150
- openalex:W7197053160: openalex:W7197053160, openalex:W7197053160
- openalex:W7172172188: openalex:W7172172188, openalex:W7172172188
- openalex:W7202005914: openalex:W7202005914, openalex:W7202005914
- openalex:W7172474001: openalex:W7172474001, openalex:W7172474001
- doi:10.48550/arxiv.2607.29032: openalex:W7172337063, openalex:W7172337063
- doi:10.48550/arxiv.2608.09227: openalex:W7202157015, openalex:W7202157015
