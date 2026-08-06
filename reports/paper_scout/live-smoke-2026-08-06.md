# Paper Scout Live Smoke Report - 2026-08-06

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 518
- **Unique papers:** 477
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 416
- Sample title: Argus: A General-Purpose Agentic Runtime for Long-Horizon Reasoning
- Sample source ID: 2608.05144
- Sample URL: https://arxiv.org/abs/2608.05144v1
- Sample published date: 2026-08-05
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Exploring Large Language Model‐Based Intelligent Agents: Definitions, Methods, and Prospects
- Sample source ID: W4390730779
- Sample URL: https://doi.org/10.1002/widm.70111
- Sample published date: 2026-07-24
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 2
- Sample title: MemVLN: Episodic and Procedural Memory for Vision-and-Language Navigation
- Sample source ID: 1af8b9812d954832d00ab7091f9dbd028dec41d8
- Sample URL: https://www.semanticscholar.org/paper/1af8b9812d954832d00ab7091f9dbd028dec41d8
- Sample published date: 2026-07-26
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 29
- maybe: 42
- irrelevant: 406

## Top Relevant Or Maybe Papers

- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2607.29032
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032v1
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032
- **Stop When Memory Suffices: Evidence-Conditioned Progressive Execution for LLM Agents** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2608.01285v1
- **RING: Retrieval-Internalized Generation for Continual Large-Scale Knowledge Injection** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.01630v1
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2607.27080
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.27080
- **ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2607.27773
- **MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2608.04843v1
- **FinPerMA: A Theory-Informed, Event-Grounded Personalized-Memory Benchmark for LLM Agents** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2608.04095v1

## Source Failures

- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.05144: arxiv:2608.05144, arxiv:2608.05144, arxiv:2608.05144
- arxiv:2608.05111: arxiv:2608.05111, arxiv:2608.05111
- arxiv:2608.05095: arxiv:2608.05095, arxiv:2608.05095
- arxiv:2608.04872: arxiv:2608.04872, arxiv:2608.04872, arxiv:2608.04872
- arxiv:2608.04843: arxiv:2608.04843, arxiv:2608.04843
- arxiv:2608.04830: arxiv:2608.04830, arxiv:2608.04830
- arxiv:2608.04746: arxiv:2608.04746, arxiv:2608.04746
- arxiv:2608.04574: arxiv:2608.04574, arxiv:2608.04574
- arxiv:2608.04458: arxiv:2608.04458, arxiv:2608.04458
- arxiv:2608.04289: arxiv:2608.04289, arxiv:2608.04289
- arxiv:2608.04278: arxiv:2608.04278, arxiv:2608.04278
- arxiv:2608.04095: arxiv:2608.04095, arxiv:2608.04095
- arxiv:2608.04009: arxiv:2608.04009, arxiv:2608.04009, arxiv:2608.04009, arxiv:2608.04009
- arxiv:2608.04003: arxiv:2608.04003, arxiv:2608.04003, arxiv:2608.04003, arxiv:2608.04003
- arxiv:2608.05013: arxiv:2608.05013, arxiv:2608.05013
- arxiv:2608.03979: arxiv:2608.03979, arxiv:2608.03979, arxiv:2608.03979
- arxiv:2608.03700: arxiv:2608.03700, arxiv:2608.03700
- arxiv:2608.03067: arxiv:2608.03067, semantic_scholar:b5233936e6221a748c0bb73139ed33cb35a84580
- arxiv:2607.29468: arxiv:2607.29468, arxiv:2607.29468
- arxiv:2607.28156: arxiv:2607.28156, arxiv:2607.28156
- arxiv:2608.01315: arxiv:2608.01315, arxiv:2608.01315
- arxiv:2607.29032: arxiv:2607.29032, arxiv:2607.29032
- arxiv:2608.05141: arxiv:2608.05141, arxiv:2608.05141
- arxiv:2608.05131: arxiv:2608.05131, arxiv:2608.05131
- arxiv:2608.04926: arxiv:2608.04926, arxiv:2608.04926
- arxiv:2608.04761: arxiv:2608.04761, arxiv:2608.04761
- doi:10.1145/3832783.3837445: arxiv:2608.04439, arxiv:2608.04439
- arxiv:2608.04405: arxiv:2608.04405, arxiv:2608.04405
- arxiv:2608.04374: arxiv:2608.04374, arxiv:2608.04374
- doi:10.1002/widm.70111: openalex:W4390730779, openalex:W4390730779
- doi:10.1145/3831684: openalex:W4405562150, openalex:W4405562150
- openalex:W7171902691: openalex:W7171902691, openalex:W7171902691
- doi:10.48550/arxiv.2607.29032: openalex:W7172337063, openalex:W7172337063
- openalex:W7172474001: openalex:W7172474001, openalex:W7172474001
