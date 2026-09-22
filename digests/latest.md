# Latest Paper Scout Digest

Latest daily digest: [2026-09-22](2026-09-22.md).

# Paper Scout Digest - 2026-09-22

## Run Summary

- **Run ID:** 131
- **Candidates fetched:** 407
- **New unique papers:** 368
- **Relevant:** 34
- **Maybe relevant:** 60
- **Irrelevant:** 313
- **Source summary:** openalex: 400, semantic_scholar: 7

## Source Warnings

- arxiv failed for 'all:procedural and all:memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+and+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:parametric and all:memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aparametric+and+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'agent memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'memory distillation': http error for https://export.arxiv.org/api/query?search_query=all%3Amemory+AND+all%3Adistillation&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'self-improving language models': http error for https://export.arxiv.org/api/query?search_query=all%3Aself+AND+all%3Aimproving+AND+all%3Alanguage+AND+all%3Amodels&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'cs.AI,cs.CL,cs.LG': http error for https://export.arxiv.org/api/query?search_query=cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG&start=0&max_results=300&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex: incomplete discovery window for 'agent memory'; single-page record limit reached.
- openalex: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'memory distillation language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'parametric memory language model'; single-page record limit reached.
- semantic_scholar failed for 'agent memory': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'memory distillation'; single-page record limit reached.
- semantic_scholar failed for 'parametric memory LLM': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Highly Relevant

### [M-SQE: Multilingual Skill Quality Estimation for Enhancing Language Equality in Agentic Skill Use](https://arxiv.org/abs/2609.18445)

- **Authors:** Yilun Liu, Shimin Tao, Minggui He, Chenxin Liu, Li Zhang, Chen Liu, et al.
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Discusses Engram-style or parametric memory mechanisms for language models.
- **Tags:** llm-agents, parametric-memory, agent-memory, memory-systems
- **Abstract summary:** Agent skills, reusable procedural documents that extend LLM agents beyond their parametric memory, have become an important interface for deploying agents on real-world tasks. Community-maintained skill libraries built around this interface are growing rapidly. However, this ecosystem remains deeply English-centric:...

### [Mem-Forever: a Git-native persistent memory layer for AI agents](https://doi.org/10.5281/zenodo.22865161)

- **Authors:** Zhu Longquan
- **Date:** 2026-09-21
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Every AI tool forgets a user when the session closes. Mem-Forever keeps the memory in the user's own Git repository as compact I-Lang structures that a person can read and a machine can parse, so preferences, decisions and lessons survive across sessions, tools and models. It needs no installation and no configurati...

### [Mem-Forever: a Git-native persistent memory layer for AI agents](https://doi.org/10.5281/zenodo.22865160)

- **Authors:** Zhu Longquan
- **Date:** 2026-09-21
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Every AI tool forgets a user when the session closes. Mem-Forever keeps the memory in the user's own Git repository as compact I-Lang structures that a person can read and a machine can parse, so preferences, decisions and lessons survive across sessions, tools and models. It needs no installation and no configurati...

## Maybe Relevant

### [The Immutable Past: Formalizing State Mutability and Conflict Resolution in Mutable RAG](https://arxiv.org/abs/2609.16073)

- **Authors:** Hamed HaddadPajouh, Amir AmiriTabat
- **Date:** 2026-09-13
- **Source:** openalex
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation, llm-agents
- **Abstract summary:** Retrieval-Augmented Generation (RAG) serves as the primary memory architecture for long-horizon autonomous agents. However, treating shared memory as an append-only stream introduces \textit{Semantic Shadowing}, a critical failure mode where conflicting historical observations accumulate and statistically dominate v...

### [Benchmarking Factual Robustness of LLMs via Multi-conversation Persuasion](https://arxiv.org/abs/2609.16777)

- **Authors:** Zhuoang Cai
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** As Large Language Models (LLMs) increasingly serve as primary knowledge retrieval interfaces, their robustness against \textit{persuasion attacks}---attempts to inject misinformation or enforce counterfactuals---has become a critical safety concern. Existing red-teaming frameworks typically evaluate models in multi-...

### [CLEAR: Cross-Source Evidence Adjudication for Large Language Models in Medicine](https://arxiv.org/abs/2609.16301)

- **Authors:** Shuai Wang, Yize Zhao, Qingyu Chen
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Medical knowledge evolves continuously, whereas the parametric knowledge encoded in large language models (LLMs) is fixed at training time. External retrieval, including retrieval-augmented generation (RAG), can provide access to newly available evidence, but retrieved information may be irrelevant, incomplete, or c...

### [Knowledge-Graph Based Augmentation versus Retrieval Augmented Generation for Cultural-Related Question Answering](https://arxiv.org/abs/2609.18317)

- **Authors:** Pablo Poulenard, Yannis Karmim, Valentin Barrière
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language models (LLMs) suffer from a long-tail deficit: culturally specific facts, particularly those concerning underrepresented regions such as Latin America, appear too rarely in pretraining corpora to be reliably memorized. Retrieval-Augmented Generation (RAG) addresses this by grounding generation in exte...

### [Mechanistic control of large language models as simulated participants via linear representation](https://doi.org/10.1038/s44387-026-00160-9)

- **Authors:** Ruikang Zhang, Tong Xu, Derong Xu, Sirui Zhao, Yuzhan Hang, Wei Wu, et al.
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large Language Models (LLMs) have garnered significant attention within psychology due to their potential to simulate human participants. However, recent studies often rely on simple prompt engineering that elicits behavioral patterns without directly manipulating internal model states. We introduce a novel simulati...

### [Metacognitive Steering: Learning the Structure of Scientific Judgment](https://arxiv.org/abs/2609.16245)

- **Authors:** Vincent Karpf, Joseph Reth, Eike Gerhardt, Audrey Wang, Anna Butz, Jiehao Xing, et al.
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Long-horizon scientific discovery requires agents to alternate between exploration, disciplined execution, and critical reassessment as evidence changes. Current language models are trained primarily on the products of science and optimized using outcome-level signals, providing limited supervision for these process...

### [PVmatAgent: A Large Language Model (LLM) Agent for Perovskite Photovoltaic Material Design and Analysis](https://doi.org/10.1002/mgea.70102)

- **Authors:** Hangyuan Deng, Yuyan Wu, Youle Wang, Lei Zhang
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** ABSTRACT The rapid advancement of large language models (LLMs) has opened new opportunities for materials informatics. However, LLMs fall short in photovoltaic (PV) material design due to their lack of domain grounding, unreliable outputs, and inability to perform integrated computational tasks. To address these iss...

### [Risk-Calibrated Autonomy for Healthcare AI Agents: live-agent benchmark harness](https://doi.org/10.5281/zenodo.22851264)

- **Authors:** Senapati Lipsa
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Reproducibility materials for a live-agent benchmark of an independent action-safety gateway for healthcare AI agents. Contains the frozen synthetic episode generator, in-memory tool environment, Action Safety Gateway, Dynamic Autonomy Controller, condition-blinded adjudicator, agent adapters, prespecified analysis...

### [Risk-Calibrated Autonomy for Healthcare AI Agents: live-agent benchmark harness](https://doi.org/10.5281/zenodo.22851147)

- **Authors:** Senapati Lipsa
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Reproducibility materials for a live-agent benchmark of an independent action-safety gateway for healthcare AI agents. Contains the frozen synthetic episode generator, in-memory tool environment, Action Safety Gateway, Dynamic Autonomy Controller, condition-blinded adjudicator, agent adapters, prespecified analysis...

### [VERA: Reinforcement Learning for Dynamic Memory Scaling of HPC Workloads in Kubernetes](https://arxiv.org/abs/2609.19936)

- **Authors:** Ade Pramono, Jie Ren, Ivy Peng
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Memory over-provisioning results in resource underutilization when HPC workloads run on Kubernetes. The default Vertical Pod Autoscaler (VPA) cannot anticipate phase-driven memory spikes for first-run HPC jobs. In this work, we present a reinforcement learning (RL) recommender VERA that formulates vertical memory sc...

### [What happens next? The Long-Term Impact of Cancer Treatment on Memory and Affective Symptoms in Breast Cancer Survivors](http://hdl.handle.net/10393/52062)

- **Authors:** Meenakshie Bradley-Garcia
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Breast cancer is the most frequently diagnosed cancer worldwide, with increasing survival rates heightening awareness of long-term treatment-related effects on cognitive and mental health. Memory impairments are among the most commonly reported and functionally impactful complaints in survivors. However, most memory...

### [When Is Graph Structure Worth Its Cost? The Case for Structure Pricing in Retrieval-Augmented Generation](https://arxiv.org/abs/2609.18099)

- **Authors:** Yuzhong Zhang, Haoyang Ma, Chao Peng, Lionel Briand, Boxi Yu, Jialun Cao
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Graph-based retrieval-augmented generation (RAG) can help answer questions that require information from many documents. However, building a graph often requires many language-model calls during ingestion. It is therefore important to ask whether its quality gains justify the additional cost. We present EffiRAG, a g...

### [agmi: Agent Memory Integrity, a conformance test suite for tamper evidence in AI agent memory and checkpoint stores](https://doi.org/10.5281/zenodo.22860886)

- **Authors:** Khandelwal Yasha
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** First public release. Five at-rest tamper attacks measured against LangGraph SqliteSaver 3.1.1, Letta 0.16.8 and Mem0 2.0.20. All three accept all five attacks silently. Preprint: https://doi.org/10.5281/zenodo.22765627

### [agmi: Agent Memory Integrity, a conformance test suite for tamper evidence in AI agent memory and checkpoint stores](https://doi.org/10.5281/zenodo.22860887)

- **Authors:** Khandelwal Yasha
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** First public release. Five at-rest tamper attacks measured against LangGraph SqliteSaver 3.1.1, Letta 0.16.8 and Mem0 2.0.20. All three accept all five attacks silently. Preprint: https://doi.org/10.5281/zenodo.22765627

### [MBM-0: A Protocol for Measuring Agent Memory Self-Growth (v0)](https://doi.org/10.5281/zenodo.22853948)

- **Authors:** Fei Long Zai Tian
- **Date:** 2026-09-20
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** MBM-0 (Memory Birth Metric, v0) is the first open protocol for indirectly measuring whether an AI agent's stated belief actually 'lands' — becomes retrievable, citable, and reintegrated by its own memory system over time. It introduces a four-ring framework (publication, retrieval, integration, citation) and two cor...

### [MBM-0: A Protocol for Measuring Agent Memory Self-Growth (v0)](https://doi.org/10.5281/zenodo.22853949)

- **Authors:** Fei Long Zai Tian
- **Date:** 2026-09-20
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** MBM-0 (Memory Birth Metric, v0) is the first open protocol for indirectly measuring whether an AI agent's stated belief actually 'lands' — becomes retrievable, citable, and reintegrated by its own memory system over time. It introduces a four-ring framework (publication, retrieval, integration, citation) and two cor...
