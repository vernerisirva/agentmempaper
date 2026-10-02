# Paper Scout Live Smoke Report - 2026-10-02

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 103
- **Unique papers:** 97
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents
- Sample source ID: W7213995952
- Sample URL: https://arxiv.org/abs/2609.23986
- Sample published date: 2026-09-21
- Abstract: yes

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 3
- Sample title: Designer-RSI: Evolving Procedural Memory from User Traffic for Agentic Graphic Design
- Sample source ID: 9c5233012d0a37e45f8e3a28beabe595c01d0bfd
- Sample URL: https://www.semanticscholar.org/paper/9c5233012d0a37e45f8e3a28beabe595c01d0bfd
- Sample published date: 2026-09-18
- Abstract: yes


## Decisions

- relevant: 19
- maybe: 18
- irrelevant: 60

## Top Relevant Or Maybe Papers

- **Revisit to Segment: Working Memory Distillation for Reasoning Segmentation** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://www.semanticscholar.org/paper/b14255a74a257c02d84c51a6fe10276ee2843f4e
- **Revisit to Segment: Working Memory Distillation for Reasoning Segmentation** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2609.34863
- **RPMem: Learning Long-Term Recurrent Parametric Memory Across Sessions for LLM Agents** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://www.semanticscholar.org/paper/d84232d26104a0f9ad8acce504a732c50f1cfe41
- **RPMem: Learning Long-Term Recurrent Parametric Memory Across Sessions for LLM Agents** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2609.23466
- **PSD: Pseudo Self-Distillation of Memory Representation Capabilities for LLM Agents** (relevant, 100/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.23449
- **DolphinBench: Mapping the Pareto Frontier of Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.24971
- **Tamper Evidence in AI Agent Memory Stores: A Method, a Taxonomy, and a Measurement** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22995111
- **Scope Before You Persist: Preventing Cross-Family Interference in Agent Memory** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2609.29144
- **Probing Stability-Plasticity Tradeoffs in Agent Memory through Cognitive Experimental Paradigms** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.30558
- **OmniSmartHome: A Multimodal Reasoning Benchmark for Smart-Home Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.32569

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- doi:10.48550/arxiv.2609.23986: openalex:W7213995952, openalex:W7213995952, openalex:W7213995952
- doi:10.1016/j.wpi.2026.102506: openalex:W7214490834, openalex:W7214490834
- doi:10.26434/chemrxiv.15009184/v1: openalex:W7213934344, openalex:W7213934344
- doi:10.1162/coli.a.652: openalex:W4403048355, openalex:W4403048355
- doi:10.1038/s41598-026-72525-8: openalex:W7213672938, openalex:W7213672938
