# Paper Scout Live Smoke Report - 2026-09-29

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 449
- **Unique papers:** 418
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 421
- Sample title: KV-streams for Efficient Compaction in Agentic Reinforcement Learning
- Sample source ID: 2609.35750
- Sample URL: https://arxiv.org/abs/2609.35750v1
- Sample published date: 2026-09-28
- Abstract: yes

### openalex

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 25
- Sample title: Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents
- Sample source ID: W7213995952
- Sample URL: https://arxiv.org/abs/2609.23986
- Sample published date: 2026-09-21
- Abstract: yes
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=procedural+memory+language+model&filter=from_publication_date%3A2026-09-15&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 3
- Sample title: ProMem-agent: Procedural memory-augmented large language model agents for clinical trajectory reasoning.
- Sample source ID: 1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
- Sample URL: https://www.semanticscholar.org/paper/1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
- Sample published date: 2026-09-17
- Abstract: no


## Decisions

- relevant: 23
- maybe: 30
- irrelevant: 365

## Top Relevant Or Maybe Papers

- **Revisit to Segment: Working Memory Distillation for Reasoning Segmentation** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2609.34863v1
- **RPMem: Learning Long-Term Recurrent Parametric Memory Across Sessions for LLM Agents** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2609.23466v2
- **DolphinBench: Mapping the Pareto Frontier of Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.24971
- **Separating Memory and Workflow Effects in Predicting Individual Answers** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.33321v1
- **WFM: Wiki Foundation Model for Complex Agentic Reasoning** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2609.18182v1
- **Tamper Evidence in AI Agent Memory Stores: A Method, a Taxonomy, and a Measurement** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22995111
- **Share-Borne AI Virus: Memory-Hopping Attacks Across LLM Agents** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.35576v1
- **Scope Before You Persist: Preventing Cross-Family Interference in Agent Memory** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2609.29144
- **ProMem-agent: Procedural memory-augmented large language model agents for clinical trajectory reasoning.** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://www.semanticscholar.org/paper/1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
- **OmniSmartHome: A Multimodal Reasoning Benchmark for Smart-Home Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.32569v1

## Source Failures

- openalex (HTTP/API error) for `procedural memory language model`: http error for https://api.openalex.org/works?search=procedural+memory+language+model&filter=from_publication_date%3A2026-09-15&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- arxiv:2609.35750: arxiv:2609.35750, arxiv:2609.35750
- arxiv:2609.35596: arxiv:2609.35596, arxiv:2609.35596
- arxiv:2609.35576: arxiv:2609.35576, arxiv:2609.35576
- arxiv:2609.35568: arxiv:2609.35568, arxiv:2609.35568
- arxiv:2609.35551: arxiv:2609.35551, arxiv:2609.35551
- arxiv:2609.35540: arxiv:2609.35540, arxiv:2609.35540, arxiv:2609.35540
- arxiv:2609.35432: arxiv:2609.35432, arxiv:2609.35432, arxiv:2609.35432
- arxiv:2609.35427: arxiv:2609.35427, arxiv:2609.35427
- arxiv:2609.35336: arxiv:2609.35336, arxiv:2609.35336
- arxiv:2609.35316: arxiv:2609.35316, arxiv:2609.35316
- arxiv:2609.35233: arxiv:2609.35233, arxiv:2609.35233
- arxiv:2609.35182: arxiv:2609.35182, arxiv:2609.35182
- arxiv:2609.34988: arxiv:2609.34988, arxiv:2609.34988
- arxiv:2609.34983: arxiv:2609.34983, arxiv:2609.34983
- arxiv:2609.33066: arxiv:2609.33066, arxiv:2609.33066
- arxiv:2609.28127: arxiv:2609.28127, arxiv:2609.28127
- arxiv:2609.22086: arxiv:2609.22086, semantic_scholar:9c5233012d0a37e45f8e3a28beabe595c01d0bfd
- arxiv:2609.35312: arxiv:2609.35312, arxiv:2609.35312
- arxiv:2609.23466: arxiv:2609.23466, semantic_scholar:d84232d26104a0f9ad8acce504a732c50f1cfe41
- arxiv:2609.35621: arxiv:2609.35621, arxiv:2609.35621
- arxiv:2609.35491: arxiv:2609.35491, arxiv:2609.35491
- arxiv:2609.35333: arxiv:2609.35333, arxiv:2609.35333
- arxiv:2609.35741: arxiv:2609.35741, arxiv:2609.35741
- arxiv:2609.35575: arxiv:2609.35575, arxiv:2609.35575
- arxiv:2609.35409: arxiv:2609.35409, arxiv:2609.35409
- arxiv:2609.35350: arxiv:2609.35350, arxiv:2609.35350
- arxiv:2609.35290: arxiv:2609.35290, arxiv:2609.35290
- arxiv:2609.35262: arxiv:2609.35262, arxiv:2609.35262
- arxiv:2609.35025: arxiv:2609.35025, arxiv:2609.35025
