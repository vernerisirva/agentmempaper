# Paper Scout Live Smoke Report - 2026-10-29

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 522
- **Unique papers:** 488
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 421
- Sample title: Rare, Relevant, and Still Wrong: How Memory Fails LLM Group Decisions
- Sample source ID: 2610.37624
- Sample URL: https://arxiv.org/abs/2610.37624v1
- Sample published date: 2026-10-27
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
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 1
- Sample title: Learning to Remember: Advances in Memory Mechanisms for Large Language Models
- Sample source ID: 70c1c4f061c15e7ae74fcd369d07e073eedd4225
- Sample URL: https://www.semanticscholar.org/paper/70c1c4f061c15e7ae74fcd369d07e073eedd4225
- Sample published date: 2026-10-26
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 31
- maybe: 54
- irrelevant: 403

## Top Relevant Or Maybe Papers

- **Recovery Budgets for Persistent AI-Agent Memory: Reproducibility Artifact** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.23623901
- **RL-Guided Temporal Localization for Dual-Channel Retrieval in Long-Horizon Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.23598
- **Multimodal Filesystem Memory For Long-Horizon Embodied Agents** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2610.22686
- **Learning to Remember: Advances in Memory Mechanisms for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2610.35089
- **Learning to Remember: Advances in Memory Mechanisms for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2610.35089v1
- **BetaMem: Learning to Remember a Changing World for Embodied Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.26554v1
- **Agent Memory as Recommendation: Recommender-System Design for Long-Term Memory of LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2610.34673
- **TrawMem: Reframing Agent Memory as Task-Oriented Role-Adaptive Workspaces** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.36918v1
- **MemoryTax: The Bitter Lesson of Agent Memory** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.29823
- **From Voiceprints to User Entities: Online Speaker-Memory Construction for Multi-User Spoken Agents** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2610.36713v1

## Source Failures

- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.37624: arxiv:2610.37624, arxiv:2610.37624
- arxiv:2610.37482: arxiv:2610.37482, arxiv:2610.37482
- arxiv:2610.37443: arxiv:2610.37443, arxiv:2610.37443
- arxiv:2610.36967: arxiv:2610.36967, arxiv:2610.36967
- arxiv:2610.36918: arxiv:2610.36918, arxiv:2610.36918
- arxiv:2610.36877: arxiv:2610.36877, arxiv:2610.36877
- arxiv:2610.36826: arxiv:2610.36826, arxiv:2610.36826, arxiv:2610.36826
- arxiv:2610.36794: arxiv:2610.36794, arxiv:2610.36794
- arxiv:2610.36713: arxiv:2610.36713, arxiv:2610.36713
- arxiv:2610.36652: arxiv:2610.36652, arxiv:2610.36652
- arxiv:2610.36589: arxiv:2610.36589, arxiv:2610.36589
- arxiv:2610.36523: arxiv:2610.36523, arxiv:2610.36523
- arxiv:2610.35089: arxiv:2610.35089, arxiv:2610.35089, semantic_scholar:70c1c4f061c15e7ae74fcd369d07e073eedd4225
- arxiv:2610.34724: arxiv:2610.34724, arxiv:2610.34724, arxiv:2610.34724
- arxiv:2610.32464: arxiv:2610.32464, arxiv:2610.32464
- arxiv:2610.26825: arxiv:2610.26825, arxiv:2610.26825
- arxiv:2610.37019: arxiv:2610.37019, arxiv:2610.37019
- arxiv:2610.31401: arxiv:2610.31401, arxiv:2610.31401
- arxiv:2610.34450: arxiv:2610.34450, arxiv:2610.34450
- arxiv:2610.37651: arxiv:2610.37651, arxiv:2610.37651
- arxiv:2610.37645: arxiv:2610.37645, arxiv:2610.37645
- arxiv:2610.37553: arxiv:2610.37553, arxiv:2610.37553
- arxiv:2610.37211: arxiv:2610.37211, arxiv:2610.37211
- arxiv:2610.37115: arxiv:2610.37115, arxiv:2610.37115
- arxiv:2610.36901: arxiv:2610.36901, arxiv:2610.36901
- arxiv:2610.36767: arxiv:2610.36767, arxiv:2610.36767
- doi:10.48550/arxiv.2610.35089: openalex:W7223835807, openalex:W7223835807
- doi:10.48550/arxiv.2610.21165: openalex:W7222470937, openalex:W7222470937, openalex:W7222470937
- doi:10.48550/arxiv.2610.22217: openalex:W7222625301, openalex:W7222625301
- doi:10.48550/arxiv.2610.25425: openalex:W7223000881, openalex:W7223000881
