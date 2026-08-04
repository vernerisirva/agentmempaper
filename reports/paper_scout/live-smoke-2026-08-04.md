# Paper Scout Live Smoke Report - 2026-08-04

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 514
- **Unique papers:** 469
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 414
- Sample title: A Taxonomy of Cognitive Capability Gaps in Generative and Agentic AI
- Sample source ID: 2608.02553
- Sample URL: https://arxiv.org/abs/2608.02553v1
- Sample published date: 2026-08-03
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
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 27
- maybe: 58
- irrelevant: 384

## Top Relevant Or Maybe Papers

- **When Memory Becomes Authority: Benchmarking Authority Collapse at the Memory Consolidation Boundary** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.01679v1
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032v1
- **Stop When Memory Suffices: Evidence-Conditioned Progressive Execution for LLM Agents** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2608.01285v1
- **RING: Retrieval-Internalized Generation for Continual Large-Scale Knowledge Injection** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.01630v1
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2607.27080
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.27080
- **MemSIF: From Structured Interactions to Dual-Track Fact Memory for LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.01742v1
- **MNC: Scope-Bound Semantic Declassification for Private LLM-Agent Communication** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.01719v1
- **ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2607.27773
- **Dimension Reduction for Quantum Adaptive Agents** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2607.19156v1

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.02553: arxiv:2608.02553, arxiv:2608.02553
- arxiv:2608.02515: arxiv:2608.02515, arxiv:2608.02515
- arxiv:2608.02508: arxiv:2608.02508, arxiv:2608.02508, arxiv:2608.02508
- arxiv:2608.02505: arxiv:2608.02505, arxiv:2608.02505
- arxiv:2608.02391: arxiv:2608.02391, arxiv:2608.02391
- arxiv:2608.02358: arxiv:2608.02358, arxiv:2608.02358
- arxiv:2608.02351: arxiv:2608.02351, arxiv:2608.02351
- arxiv:2608.02113: arxiv:2608.02113, arxiv:2608.02113
- arxiv:2608.01995: arxiv:2608.01995, arxiv:2608.01995
- arxiv:2608.01904: arxiv:2608.01904, arxiv:2608.01904, arxiv:2608.01904
- arxiv:2608.01851: arxiv:2608.01851, arxiv:2608.01851, arxiv:2608.01851
- arxiv:2608.01805: arxiv:2608.01805, arxiv:2608.01805
- arxiv:2608.01802: arxiv:2608.01802, arxiv:2608.01802, arxiv:2608.01802
- arxiv:2608.01759: arxiv:2608.01759, arxiv:2608.01759, arxiv:2608.01759
- arxiv:2608.01742: arxiv:2608.01742, arxiv:2608.01742
- arxiv:2608.01739: arxiv:2608.01739, arxiv:2608.01739
- arxiv:2608.01719: arxiv:2608.01719, arxiv:2608.01719
- arxiv:2608.01708: arxiv:2608.01708, arxiv:2608.01708
- arxiv:2608.01679: arxiv:2608.01679, arxiv:2608.01679
- arxiv:2608.01651: arxiv:2608.01651, arxiv:2608.01651
- arxiv:2608.01637: arxiv:2608.01637, arxiv:2608.01637, arxiv:2608.01637
- arxiv:2608.01619: arxiv:2608.01619, arxiv:2608.01619
- arxiv:2607.29468: arxiv:2607.29468, arxiv:2607.29468
- arxiv:2607.28156: arxiv:2607.28156, arxiv:2607.28156
- arxiv:2608.02347: arxiv:2608.02347, arxiv:2608.02347
- arxiv:2608.01630: arxiv:2608.01630, arxiv:2608.01630
- arxiv:2608.01315: arxiv:2608.01315, arxiv:2608.01315
- arxiv:2607.29032: arxiv:2607.29032, arxiv:2607.29032
- arxiv:2608.01672: arxiv:2608.01672, arxiv:2608.01672
- arxiv:2608.01662: arxiv:2608.01662, arxiv:2608.01662
- arxiv:2608.02585: arxiv:2608.02585, arxiv:2608.02585
- arxiv:2608.02520: arxiv:2608.02520, arxiv:2608.02520
- arxiv:2608.02139: arxiv:2608.02139, arxiv:2608.02139
- arxiv:2608.02087: arxiv:2608.02087, arxiv:2608.02087
- arxiv:2608.01724: arxiv:2608.01724, arxiv:2608.01724
- doi:10.1002/widm.70111: openalex:W4390730779, openalex:W4390730779
- doi:10.1145/3831684: openalex:W4405562150, openalex:W4405562150
- openalex:W7171902691: openalex:W7171902691, openalex:W7171902691
- openalex:W7172173145: openalex:W7172173145, openalex:W7172173145
