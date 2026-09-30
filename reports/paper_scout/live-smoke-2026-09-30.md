# Paper Scout Live Smoke Report - 2026-09-30

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 476
- **Unique papers:** 442
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 422
- Sample title: Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning
- Sample source ID: 2609.38147
- Sample URL: https://arxiv.org/abs/2609.38147v1
- Sample published date: 2026-09-29
- Abstract: yes

### openalex

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 50
- Sample title: Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents
- Sample source ID: W7213995952
- Sample URL: https://arxiv.org/abs/2609.23986
- Sample published date: 2026-09-21
- Abstract: yes
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=memory+distillation+language+model&filter=from_publication_date%3A2026-09-16&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 4
- Sample title: ProMem-agent: Procedural memory-augmented large language model agents for clinical trajectory reasoning.
- Sample source ID: 1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
- Sample URL: https://www.semanticscholar.org/paper/1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
- Sample published date: 2026-09-17
- Abstract: no


## Decisions

- relevant: 24
- maybe: 41
- irrelevant: 377

## Top Relevant Or Maybe Papers

- **Revisit to Segment: Working Memory Distillation for Reasoning Segmentation** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2609.34863v1
- **RPMem: Learning Long-Term Recurrent Parametric Memory Across Sessions for LLM Agents** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2609.23466v2
- **DolphinBench: Mapping the Pareto Frontier of Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.24971
- **Separating Memory and Workflow Effects in Predicting Individual Answers** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.33321v1
- **WFM: Wiki Foundation Model for Complex Agentic Reasoning** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2609.18182v1
- **Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.38147v1
- **Tamper Evidence in AI Agent Memory Stores: A Method, a Taxonomy, and a Measurement** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22995111
- **Scope Before You Persist: Preventing Cross-Family Interference in Agent Memory** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2609.29144
- **ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2609.37311v1
- **Probing Stability-Plasticity Tradeoffs in Agent Memory through Cognitive Experimental Paradigms** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.30558

## Source Failures

- openalex (HTTP/API error) for `memory distillation language model`: http error for https://api.openalex.org/works?search=memory+distillation+language+model&filter=from_publication_date%3A2026-09-16&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- arxiv:2609.38147: arxiv:2609.38147, arxiv:2609.38147
- arxiv:2609.38081: arxiv:2609.38081, arxiv:2609.38081
- arxiv:2609.38021: arxiv:2609.38021, arxiv:2609.38021
- arxiv:2609.37953: arxiv:2609.37953, arxiv:2609.37953
- arxiv:2609.37626: arxiv:2609.37626, arxiv:2609.37626
- arxiv:2609.37544: arxiv:2609.37544, arxiv:2609.37544
- arxiv:2609.37311: arxiv:2609.37311, arxiv:2609.37311
- arxiv:2609.37125: arxiv:2609.37125, arxiv:2609.37125
- arxiv:2609.36892: arxiv:2609.36892, arxiv:2609.36892
- arxiv:2609.36746: arxiv:2609.36746, arxiv:2609.36746
- arxiv:2609.36739: arxiv:2609.36739, arxiv:2609.36739
- arxiv:2609.36722: arxiv:2609.36722, arxiv:2609.36722
- arxiv:2609.36675: arxiv:2609.36675, arxiv:2609.36675, arxiv:2609.36675
- arxiv:2609.33066: arxiv:2609.33066, arxiv:2609.33066
- arxiv:2609.28127: arxiv:2609.28127, arxiv:2609.28127
- arxiv:2609.23466: arxiv:2609.23466, semantic_scholar:d84232d26104a0f9ad8acce504a732c50f1cfe41
- arxiv:2609.37702: arxiv:2609.37702, arxiv:2609.37702
- arxiv:2609.34863: arxiv:2609.34863, semantic_scholar:b14255a74a257c02d84c51a6fe10276ee2843f4e
- arxiv:2609.38143: arxiv:2609.38143, arxiv:2609.38143
- arxiv:2609.38142: arxiv:2609.38142, arxiv:2609.38142
- arxiv:2609.37968: arxiv:2609.37968, arxiv:2609.37968
- arxiv:2609.37950: arxiv:2609.37950, arxiv:2609.37950
- arxiv:2609.37924: arxiv:2609.37924, arxiv:2609.37924
- arxiv:2609.37915: arxiv:2609.37915, arxiv:2609.37915
- arxiv:2609.37868: arxiv:2609.37868, arxiv:2609.37868
- arxiv:2609.37837: arxiv:2609.37837, arxiv:2609.37837
- arxiv:2609.37825: arxiv:2609.37825, arxiv:2609.37825
- arxiv:2609.37633: arxiv:2609.37633, arxiv:2609.37633
- arxiv:2609.37631: arxiv:2609.37631, arxiv:2609.37631
- arxiv:2609.37356: arxiv:2609.37356, arxiv:2609.37356
- doi:10.48550/arxiv.2609.23986: openalex:W7213995952, openalex:W7213995952
- doi:10.48550/arxiv.2609.19128: openalex:W7213516733, openalex:W7213516733
- doi:10.1016/j.ijmedinf.2026.106727: openalex:W7213526976, semantic_scholar:1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
