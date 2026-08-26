# Paper Scout Live Smoke Report - 2026-08-26

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 225
- **Candidates fetched:** 126
- **Unique papers:** 116
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 25
- Sample title: Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses
- Sample source ID: 2608.24876
- Sample URL: https://arxiv.org/abs/2608.24876v1
- Sample published date: 2026-08-25
- Abstract: yes
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-08-20
- Abstract: yes

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 1
- Sample title: Gaming with AI: A Hybrid Reinforcement Learning, Large Language Model, and Procedural Content Generation Framework for Enhancing Player Engagement and User Experience
- Sample source ID: bef526c86452cbe462b7c6957f86ecb893f8c6d5
- Sample URL: https://www.semanticscholar.org/paper/bef526c86452cbe462b7c6957f86ecb893f8c6d5
- Sample published date: 2026-08-21
- Abstract: yes


## Decisions

- relevant: 11
- maybe: 35
- irrelevant: 70

## Top Relevant Or Maybe Papers

- **The Judgment Layer: Turning Agent Memory into Wisdom** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://dhare.com.au
- **The Judgment Layer: Turning Agent Memory into Wisdom** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://dhare.com.au
- **RippleMem: From Isolated Retrieval to Associative Recollection for Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.13334
- **RAF-LLM: A retrieval-augmented large language model framework for remaining useful life prediction of rotating machinery** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.1088/1361-6501/ae989d
- **Mitigating Identity Essentialism in LLM Agents with Longitudinal Life Trajectories** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2608.19621
- **CONTRAMEM: Learning Self-Evolving Procedural Memory from Contrasting Multi-Model Trajectories** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2608.22533v1
- **What Does Each Memory Feature Buy? A Measured Audit of an Agent Memory System** (relevant, 90/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.5281/zenodo.22002654
- **What Does Each Memory Feature Buy? A Measured Audit of an Agent Memory System** (relevant, 90/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.5281/zenodo.22002653
- **InjecMEM: Memory Injection Attack on LLM Agent Memory Systems** (relevant, 90/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2608.23471v1
- **Can an Agent Memory System Track an Evolving State?** (relevant, 90/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.13140/rg.2.2.33735.87208

## Source Failures

- arxiv (HTTP/API error) for `procedural memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- doi:10.5281/zenodo.22025638: openalex:W7203917275, openalex:W7203917275
- doi:10.48550/arxiv.2608.11654: openalex:W7202382037, openalex:W7202382037
- doi:10.48175/ijarsct-38105: openalex:W7203824408, semantic_scholar:bef526c86452cbe462b7c6957f86ecb893f8c6d5
- doi:10.1007/s00146-026-03283-4: openalex:W4417529023, openalex:W4417529023
- doi:10.48550/arxiv.2608.11671: openalex:W7202415437, openalex:W7202415437
- doi:10.48550/arxiv.2608.13787: openalex:W7203604614, openalex:W7203604614
- doi:10.48550/arxiv.2608.12626: openalex:W7203452646, openalex:W7203452646
- doi:10.5281/zenodo.21966214: openalex:W7203585882, openalex:W7203585882
- doi:10.5281/zenodo.21966215: openalex:W7203574771, openalex:W7203574771
- doi:10.1007/s11042-026-21853-y: openalex:W7202290456, openalex:W7202290456
