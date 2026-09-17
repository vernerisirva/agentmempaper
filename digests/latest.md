# Latest Paper Scout Digest

Latest daily digest: [2026-09-17](2026-09-17.md).

# Paper Scout Digest - 2026-09-17

## Run Summary

- **Run ID:** 124
- **Candidates fetched:** 411
- **New unique papers:** 380
- **Relevant:** 56
- **Maybe relevant:** 95
- **Irrelevant:** 260
- **Source summary:** openalex: 400, semantic_scholar: 11

## Source Warnings

- arxiv failed for 'all:self and all:improving and all:language and all:models': http error for https://export.arxiv.org/api/query?search_query=all%3Aself+and+all%3Aimproving+and+all%3Alanguage+and+all%3Amodels&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:procedural and all:memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+and+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:parametric and all:memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aparametric+and+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:memory and all:distillation': http error for https://export.arxiv.org/api/query?search_query=all%3Amemory+and+all%3Adistillation&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:agent and all:memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+and+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'cat:cs.ai or cat:cs.cl or cat:cs.lg': http error for https://export.arxiv.org/api/query?search_query=cat%3Acs.ai+or+cat%3Acs.cl+or+cat%3Acs.lg&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex: incomplete discovery window for 'agent memory'; single-page record limit reached.
- openalex: incomplete discovery window for 'memory distillation language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'parametric memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- semantic_scholar failed for 'agent memory': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'memory distillation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'parametric memory LLM'; single-page record limit reached.

## Highly Relevant

### [Causal Path Alignment: Anchoring the Optimization Trajectory for Controllable In-Parameter Knowledge Editing](https://doi.org/10.24963/ijcai.2026/655)

- **Authors:** Xiyu Liu, Zhengxiao Liu, Naibin Gu, Zheng Lin, Weiping Wang
- **Date:** 2026-09-01
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Discusses Engram-style or parametric memory mechanisms for language models.
- **Tags:** parametric-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Knowledge editing is pivotal for efficiently updating the parametric memory of Large Language Models (LLMs), enabling them to function as evolving agents in dynamic environments. However, mainstream in-parameter knowledge editing approaches suffer from Subject-Dominant Memory Interference: modifying a specific fact...

### [WFM: Wiki Foundation Model for Complex Agentic Reasoning](https://www.semanticscholar.org/paper/4132309227a569c215f7924a16be922e2afdda08)

- **Authors:** Jun-Nan Dong, Lin-Hao Luo, Sen-Lei Zhang, Gong Chen, Taian Guo, Yi-Fei Yu, et al.
- **Date:** 2026-09-16
- **Source:** semantic_scholar
- **Relevance:** relevant (91/100)
- **Reason:** Studies governed shared memory or persistent memory protocols for LLM agents.
- **Tags:** agent-memory, long-term-memory, memory-systems, llm-agents
- **Abstract summary:** Real-world agents fundamentally require persistent non-parametric knowledge for dynamic reasoning, i.e., long-term memory and retrieval-augmented generation. While graphs have shown reliable advantages in providing structured evidence, the sparse graph representations naturally restrict machine readability and seman...
- **Automated evidence-based assessment:** 68/100 · Uncertain · Medium confidence · full text
- **Positive signals:** The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

## Maybe Relevant

### [An empirical study of retrieval-augmented diffusion language models for generative commonsense reasoning](https://doi.org/10.1016/j.ins.2026.124147)

- **Authors:** YUBO FANG, Hai-Tao Yu, Hideo Joho, Sumio Fujita, Yan Ge, Chao Lei
- **Date:** 2026-09-11
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Generative commonsense reasoning (GCR) remains challenging for intelligent systems, as large language models (LLMs) rely primarily on parametric knowledge and often lack sufficient commonsense information. Although retrieval-augmented generation (RAG) alleviates this limitation by incorporating external knowledge, i...

### [BadEngram: Backdoor Attack on Gated Memory Components in LLMs](https://arxiv.org/abs/2609.13478)

- **Authors:** Ariel Fogel, Omer Hofman, Eilon Cohen, Roman Vainshtein
- **Date:** 2026-09-11
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** To expand open-weight models' capacity without proportionally increasing computation, recent language models incorporate gated parametric memories that retrieve learned values and inject them into intermediate representations. Despite these efficiency benefits, such modules create a distinct attack surface: their pa...

### [BadEngram: Backdoor Attack on Gated Memory Components in LLMs](https://doi.org/10.48550/arxiv.2609.13478)

- **Authors:** Ariel Fogel, Omer Hofman, Eilon Cohen, Roman Vainshtein
- **Date:** 2026-09-11
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** To expand open-weight models' capacity without proportionally increasing computation, recent language models incorporate gated parametric memories that retrieve learned values and inject them into intermediate representations. Despite these efficiency benefits, such modules create a distinct attack surface: their pa...

### [Distillation of a Locally Deployable 8B Language Model for Lung Histology Abstraction: A 33-Report Proof-of-Concept Study](https://doi.org/10.2147/jmdh.s619855)

- **Authors:** Dian Tri Wiyanti, Min-Huei Hsu, Daniel CA Nugroho
- **Date:** 2026-09-01
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Background: The manual data abstraction process for lung cancer registries is a labor-intensive undertaking that often results in registry lag. While cloud-based Large Language Models (LLMs) exhibit high reasoning acuity, their reliance on third-party APIs poses significant data privacy risks and conflicts with inst...

### [Mind2Dialogue: Training Human-Aware Language Models by Simulating User Mental States](https://arxiv.org/abs/2609.15972)

- **Authors:** Zixuan Wang, Yufan Zhou, Jinzhou Tang, Xinle Yu, Chengjun Wu, Lyumanshan Ye, et al.
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** As language models become more capable, long-term collaboration in learning, reasoning, and decision-making calls for a deeper understanding of the people they serve. Yet training such human-aware language models faces a fundamental supervision gap because current datasets for LLM assistant training contain few if a...

### [Salesforce Koa: An Enterprise Language Model for Agentic Tool Use](https://arxiv.org/abs/2609.15066)

- **Authors:** Zixiang Chen, Sufeng Niu, Yingchi Liu, Wenting Zhao, Akshara Prabhakar, Shubham Mehrotra, et al.
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We present Salesforce Koa, an enterprise language model built by post-training the open-weight Nemotron-3-Super-120B foundation model with reinforcement learning using Group Relative Policy Optimization (GRPO). Salesforce Koa is trained on public and synthetically generated data, with no customer data, to improve to...

### [URCHIN: A Horizontal Spiking Language Model for Data-Constrained Pretraining](https://arxiv.org/abs/2609.13899)

- **Authors:** Po‐Han Chiang
- **Date:** 2026-09-12
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The BabyLM challenge measures how much language a model can learn from developmentally-plausible, child-scale data rather than internet-scale corpora, yet prior language models forgo the biological constraints of the neural circuitry that acquires human language: spiking neurons separated into excitatory and inhibit...

### [Agent Memory Sync: Default to Operation-Based Sync for 32 Nodes](https://doi.org/10.5281/zenodo.22768443)

- **Authors:** Colton Ramsey
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Default to operation-based sync for 32-node agent memory to cut bandwidth, ensure deterministic convergence and use commutative merge semantics. Independent technical note mirroring the canonical version: https://tryinterlock.com/blog/agent-memory-sync-default-to-operation-based-sync-for-32-nodes.php

### [Agent Memory Sync: Default to Operation-Based Sync for 32 Nodes](https://doi.org/10.5281/zenodo.22768442)

- **Authors:** Colton Ramsey
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Default to operation-based sync for 32-node agent memory to cut bandwidth, ensure deterministic convergence and use commutative merge semantics. Independent technical note mirroring the canonical version: https://tryinterlock.com/blog/agent-memory-sync-default-to-operation-based-sync-for-32-nodes.php
