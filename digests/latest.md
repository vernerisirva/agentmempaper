# Latest Paper Scout Digest

Latest daily digest: [2026-09-25](2026-09-25.md).

# Paper Scout Digest - 2026-09-25

## Run Summary

- **Run ID:** 134
- **Candidates fetched:** 418
- **New unique papers:** 375
- **Relevant:** 37
- **Maybe relevant:** 63
- **Irrelevant:** 318
- **Source summary:** openalex: 400, semantic_scholar: 18

## Source Warnings

- arxiv failed for 'agent memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'procedural memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+AND+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'parametric memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aparametric+AND+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'memory distillation': http error for https://export.arxiv.org/api/query?search_query=all%3Amemory+AND+all%3Adistillation&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'self-improving language models': http error for https://export.arxiv.org/api/query?search_query=all%3Aself+AND+all%3Aimproving+AND+all%3Alanguage+AND+all%3Amodels&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'cs.AI,cs.CL,cs.LG': http error for https://export.arxiv.org/api/query?search_query=cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG&start=0&max_results=300&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex: incomplete discovery window for 'agent memory'; single-page record limit reached.
- openalex: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'memory distillation language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'parametric memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'agent memory'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- semantic_scholar failed for 'memory distillation': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar: incomplete discovery window for 'parametric memory LLM'; single-page record limit reached.

## Highly Relevant

### [On the Turing Completeness of Transformers and Agents](https://arxiv.org/abs/2609.20335)

- **Authors:** Yimu Qiao, Lijia Yu, Ruichen Qiu, Xiao-Shan Gao
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, llm-agents
- **Abstract summary:** Transformers have emerged as the dominant architecture in sequence modeling, achieving remarkable success in natural language processing and reasoning tasks. While existing literature has established the Turing completeness of transformers under bounded input length, the reasoning power of a single transformer opera...

## Maybe Relevant

### [When Does Execution Provenance Help Agent Memory Retrieval?](https://doi.org/10.48550/arxiv.2609.25913)

- **Authors:** Yiqi Wang, jinqian ju, Jiaqi Zhang, Zequn Sun, Yiqun Duan, Mingkai Zheng, et al.
- **Date:** 2026-09-22
- **Source:** openalex
- **Relevance:** maybe (61/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, memory-policy, evaluation
- **Abstract summary:** A language agent's execution history can exceed its context window, requiring its memory system to retrieve complete supporting evidence under a hard token budget. Evidence may span multiple execution events, yet conventional retrievers use fixed token windows and fixed-k metrics that reward individual fragments wit...

### [Governing Agentic AI in Enterprise Workflows: A Bounded-Autonomy Framework for Delegated Authority and Controlled Execution](https://doi.org/10.3390/info17090923)

- **Authors:** Bo Nørregaard Jôrgensen, Zheng Ma
- **Date:** 2026-09-20
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agentic AI can interpret information, plan, make workflow decisions, and use enterprise tools. Yet technical capability does not establish authoritative meaning, legitimate process state, organisational permission, or accountable execution. The challenge is to preserve adaptability while ensuring that consequential...

### [PRISM-RAG: Multimodal Hypergraph Retrieval-Augmented Generation for Tobacco Product and Legislative Policy Reasoning](https://arxiv.org/abs/2609.23769)

- **Authors:** Manuel Serna-Aguilera, Raegan Anderes, Page Dobbs, Ky Luu
- **Date:** 2026-09-20
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The disambiguation of semantically similar statutory text across jurisdictions is a retrieval problem that existing methods do not solve. This inter-context conflict can steer generative models toward confidently produced answers grounded in topically relevant but jurisdictionally incorrect sources. Tobacco and nico...

### [Risk-Calibrated Autonomy for Healthcare AI Agents: live-agent benchmark harness](https://doi.org/10.5281/zenodo.22851148)

- **Authors:** Senapati Lipsa
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Reproducibility materials for a live-agent benchmark of an independent action-safety gateway for healthcare AI agents. Contains the frozen synthetic episode generator, in-memory tool environment, Action Safety Gateway, Dynamic Autonomy Controller, condition-blinded adjudicator, agent adapters, prespecified analysis...
