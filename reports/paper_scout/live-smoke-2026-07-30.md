# Paper Scout Live Smoke Report - 2026-07-30

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 525
- **Candidates fetched:** 506
- **Unique papers:** 472
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 406
- Sample title: Minimal Markovization via Stable Quotients in Holonomy-Cover Decision Processes
- Sample source ID: 2607.27132
- Sample URL: https://arxiv.org/abs/2607.27132v1
- Sample published date: 2026-07-29
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Provenance Is Not Independence: The False-Corroboration Exclusion Rule for Multi-Agent Memory
- Sample source ID: W7169678469
- Sample URL: https://doi.org/10.5281/zenodo.21431717
- Sample published date: 2026-07-18
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 15
- maybe: 77
- irrelevant: 380

## Top Relevant Or Maybe Papers

- **Retain or Consolidate? Budget-Dependent Operator Selection for Language Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2607.17545
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.27080v1
- **Autoresearch with Coding Agents: Generalizers and Metric-Maximizers on Quran Recitation Data** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.18064v1
- **From Memory to Skills: Evidence-Grounded Co-Evolution Governance for Long-Horizon LLM Agents** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2607.16621v1
- **From Memory to Skills: Evidence-Grounded Co-Evolution Governance for Long-Horizon LLM Agents** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2607.16621
- **Dimension Reduction for Quantum Adaptive Agents** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2607.19156v1
- **Metis: Memory Foundation Model** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2607.26760v1
- **MemVLN: Episodic and Procedural Memory for Vision-and-Language Navigation** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.48550/arxiv.2607.23504
- **MemVLN: Episodic and Procedural Memory for Vision-and-Language Navigation** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2607.23504v1
- **MemTX: Transactional Belief Commit for Stateful Agent Memory** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.48550/arxiv.2607.23929

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2607.27132: arxiv:2607.27132, arxiv:2607.27132
- arxiv:2607.27080: arxiv:2607.27080, arxiv:2607.27080
- arxiv:2607.27056: arxiv:2607.27056, arxiv:2607.27056
- arxiv:2607.26760: arxiv:2607.26760, arxiv:2607.26760, arxiv:2607.26760
- arxiv:2607.26724: arxiv:2607.26724, arxiv:2607.26724
- arxiv:2607.26637: arxiv:2607.26637, arxiv:2607.26637, arxiv:2607.26637
- arxiv:2607.26598: arxiv:2607.26598, arxiv:2607.26598, arxiv:2607.26598, arxiv:2607.26598
- arxiv:2607.26587: arxiv:2607.26587, arxiv:2607.26587
- arxiv:2607.26520: arxiv:2607.26520, arxiv:2607.26520
- arxiv:2607.26490: arxiv:2607.26490, arxiv:2607.26490
- arxiv:2607.26473: arxiv:2607.26473, arxiv:2607.26473
- arxiv:2607.26410: arxiv:2607.26410, arxiv:2607.26410
- arxiv:2607.26212: arxiv:2607.26212, arxiv:2607.26212
- arxiv:2607.26017: arxiv:2607.26017, arxiv:2607.26017, arxiv:2607.26017
- arxiv:2607.25992: arxiv:2607.25992, arxiv:2607.25992
- arxiv:2607.23702: arxiv:2607.23702, arxiv:2607.23702
- arxiv:2607.26946: arxiv:2607.26946, arxiv:2607.26946
- arxiv:2607.26455: arxiv:2607.26455, arxiv:2607.26455
- arxiv:2607.24434: arxiv:2607.24434, arxiv:2607.24434
- arxiv:2607.26873: arxiv:2607.26873, arxiv:2607.26873
- arxiv:2607.26722: arxiv:2607.26722, arxiv:2607.26722
- arxiv:2607.26643: arxiv:2607.26643, arxiv:2607.26643
- doi:10.1002/widm.70111: openalex:W4390730779, openalex:W4390730779
- openalex:W7170112036: openalex:W7170112036, openalex:W7170112036
- openalex:W7171268892: openalex:W7171268892, openalex:W7171268892
- openalex:W7171268587: openalex:W7171268587, openalex:W7171268587
- openalex:W7170224623: openalex:W7170224623, openalex:W7170224623
- openalex:W7170113022: openalex:W7170113022, openalex:W7170113022
- doi:10.5282/edoc.37293: openalex:W7170310497, openalex:W7170310497
