# Latest Paper Scout Digest

Latest daily digest: [2026-09-01](2026-09-01.md).

# Paper Scout Digest - 2026-09-01

## Run Summary

- **Run ID:** 106
- **Candidates fetched:** 949
- **New unique papers:** 831
- **Relevant:** 50
- **Maybe relevant:** 139
- **Irrelevant:** 760
- **Source summary:** arxiv: 546, openalex: 400, semantic_scholar: 3

## Source Warnings

- semantic_scholar failed for 'procedural memory language model': http error for https://api.semanticscholar.org/graph/v1/paper/search?query=procedural+memory+language+model&limit=100&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds%2CopenAccessPdf: request failed after 3 attempts: HTTP Error 500: Internal Server Error
- semantic_scholar failed for 'memory distillation': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar failed for 'parametric memory LLM': http error for https://api.semanticscholar.org/graph/v1/paper/search?query=parametric+memory+LLM&limit=100&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds%2CopenAccessPdf: request failed after 3 attempts: HTTP Error 500: Internal Server Error

## Highly Relevant

### [Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents](https://arxiv.org/abs/2608.29606v1)

- **Authors:** Ming Wu, Pengyuan Zhu
- **Date:** 2026-08-30
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, llm-agents, long-term-memory, memory-types, benchmark, memory-systems
- **Abstract summary:** Large language model (LLM) agents need durable, faithful memory of everything a user or organization has said and stored, yet most memory systems commit to a single organizing structure (a fact store, a vector index, or a knowledge graph) and inherit its blind spots. We present Agent Zero Memory, a provenance-aware...

### [UTILMEM: Benchmarking Evidence Utilization in Long-Term Conversational Memory](https://arxiv.org/abs/2608.30508v1)

- **Authors:** Peijun Qing, Fobo Shi, Soroush Vosoughi
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** long-term-memory, benchmark, evaluation, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Long-term memory is increasingly important for conversational agents, yet existing benchmarks primarily measure memory through pointwise factual recall: whether a system can recover isolated facts or event-level details from prior interactions. Real-world memory use, however, often requires a more demanding capabili...

### [Selective Forgetting: A Graph-Based Memory Framework for Long-Term LLM Agents](https://arxiv.org/abs/2608.28978v1)

- **Authors:** Theo Rusu, Sourena Khanzadeh, Manar Alalfi
- **Date:** 2026-08-29
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Studies governed shared memory or persistent memory protocols for LLM agents.
- **Tags:** agent-memory, llm-agents, benchmark, memory-systems
- **Abstract summary:** Knowledge graphs have been proposed as a structured alternative to flat retrieval-augmented generation for long-term agent memory, on the assumption that representing conversations as entities and relations improves recall. We evaluate that assumption directly. Our framework extracts each conversational turn into ty...

### [CGFM-Nav: Cognitive Graph-Field Memory for Semantic-Guided Lifelong Multimodal Embodied Navigation](https://arxiv.org/abs/2608.29114v1)

- **Authors:** Yuxiang Xiao, Xibei Chen, Xin Zhou, Jie Chen, Yifeng Zhang, Guillaume Sartoretti
- **Date:** 2026-08-29
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Vision-and-Language Navigation (VLN) requires agents to reason over accumulated observations while continuously exploring unseen regions. However, existing environment representations often struggle to jointly support explicit semantic memory and continuous exploration guidance. To address this challenge, we propose...

### [EMERGE-Policy: A Robot Mind Emerges Beyond a Single Policy](https://arxiv.org/abs/2608.29896v1)

- **Authors:** Zhirui Fang, Qingchi Yu, Ziyang Chen, Longfei Li, Haoran Ma, Keru Zhou, et al.
- **Date:** 2026-08-30
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory storage, retrieval, update, or consolidation for LLM agents.
- **Tags:** memory-policy, agent-memory, memory-systems, llm-agents
- **Abstract summary:** A robot's effective ``mind'' need not reside in a single policy. It can emerge when specialized components perceive, reason, predict, act, verify, and remember within a shared orchestration process. EMERGE-Policy turns this perspective into a graph-structured agentic framework that coordinates both capability invoca...

### [Memory-First Fact-Checking: A Knowledge-Graph-Grounded Multi-Agent System for Misinformation Detection](https://arxiv.org/abs/2608.29617v1)

- **Authors:** Amelia Petrenciuc, Alexandru Lecu, Adrian Groza
- **Date:** 2026-08-30
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, evaluation, agent-memory, memory-systems, llm-agents
- **Abstract summary:** This paper introduces a hybrid fact-checking framework that integrates Knowledge Graph-based semantic memory with adversarial multi-agent reasoning for explainable misinformation detection. The proposed system follows a memory-first, web-fallback architecture, in which input claims are initially evaluated against a...

### [Relational Reinforcement Learning with Semantic Memory](https://doi.org/10.5281/zenodo.22198408)

- **Authors:** Jincheng Zhang
- **Date:** 2026-08-31
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** This paper introduces a novel approach to relational reinforcement learning (RL) that integrates a semantic memory component. Existing relational RL methods often struggle with generalization, failing to adapt effectively to new environments. Our proposed system addresses this limitation by explicitly storing and re...

### [Relational Reinforcement Learning with Semantic Memory](https://doi.org/10.5281/zenodo.22198409)

- **Authors:** Jincheng Zhang
- **Date:** 2026-08-31
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** This paper introduces a novel approach to relational reinforcement learning (RL) that integrates a semantic memory component. Existing relational RL methods often struggle with generalization, failing to adapt effectively to new environments. Our proposed system addresses this limitation by explicitly storing and re...

### [Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory](https://arxiv.org/abs/2608.30177v1)

- **Authors:** Chuanchao Zang, Zijian Cao, Xiangtao Meng, Jianing Wang, Wenyu Chen, Xinyu Gao, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, llm-agents, memory-systems, long-term-memory, evaluation
- **Abstract summary:** Long-term memory is becoming a core capability of LLM agents, enabling personalization and long-horizon interaction. However, memory mechanisms that retain, transform, or expose more information can affect both benign utility and susceptibility to memory poisoning. Existing evaluations typically measure memory utili...

## Maybe Relevant

### [Thinking Beyond Videos: Unifying Video Reasoning and Deep Research for Open-World Video Agents](https://arxiv.org/abs/2608.23329)

- **Authors:** Wenqi Liu, Shijie Ma, Yunxiao Wang, Meng Liu, Qile Su, Han Liu, et al.
- **Date:** 2026-08-24
- **Source:** openalex
- **Relevance:** maybe (46/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** deep-research, parametric-memory
- **Abstract summary:** Open-world video understanding often requires a model to locate sparse visual evidence and acquire external knowledge that is absent from the video and its parametric memory. While Thinking-with-Videos enables active temporal perception and Deep Research supports multi-step information seeking, the two capabilities...

### [A Universal Context-Reuse Layer for Cross-Model KV Sharing](https://arxiv.org/abs/2608.30963v1)

- **Authors:** Yi Li, Dongming Jiang, Yi Zhao, Bingzhe Li
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Modern large language model (LLM) serving systems increasingly operate over repeated or shared context, yet each model typically performs its own prefill computation even when another model has already processed the same input. Existing KV-cache reuse mechanisms substantially reduce redundant computation within a si...

### [Adaptive KV Retention for LLM Agents at Human-Approval Timescales](https://arxiv.org/abs/2608.30830v1)

- **Authors:** Minseo Choi, Ananya Joshi
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Unlike the seconds-scale tool-call pauses targeted by prior agent-serving systems, agentic LLM requests can be suspended for minutes or hours while waiting for human approval. We study how suspension and resumption affect GPU serving performance and develop a retention policy that balances active-serving capacity ag...

### [Agents as Knowledge Integrator and Utilizer in Multimodal Recommendation](https://arxiv.org/abs/2608.29410v1)

- **Authors:** Jinfeng Xu, Zheyu Chen, Shuo Yang, Jinze Li, Puzhen Wu, Zewei Liu, et al.
- **Date:** 2026-08-29
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Online platforms increasingly rely on multimodal recommender systems to rank products, media, and other Web content. Existing methods usually inject visual and textual features into item representations or build homogeneous graphs from modality-level similarity, but the resulting signals can remain misaligned with t...

### [ATLAS: Dual-Horizon Diagnostic Evaluation for Industrial Tool-Use Agents](https://arxiv.org/abs/2608.30685v1)

- **Authors:** Wei Chen, Peilun Zhou, Zhaoyu Hu, Jiajun Chai, Zhongni Hou, Yufei Zhang, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Large language model (LLM) agents are increasingly deployed in user-facing services that require iterative tool use under dynamic business conditions. Reliable evaluation is essential for sustained improvement: it must reveal capability deficiencies, inform priorities, and assess interventions. Yet industrial agent...

### [Beacon: LLM Multi-Agent Driven Hardware Design Space Exploration for Heterogeneous Multi-Chiplet Deep Learning Accelerators](https://arxiv.org/abs/2608.30932v1)

- **Authors:** Boyu Li, Zongwei Zhu, Qianyue Cao, Xi Li, Xuehai Zhou
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Heterogeneous multi-chiplet accelerators allow chiplets to be configured independently to better match different operator characteristics and improve inference efficiency. However, heterogeneity makes simulator evaluation expensive, limiting the number of iterations affordable for hardware design space exploration (...

### [Beyond the Payload: How User Invocation Shapes Coding Agent Vulnerability to Repository Poisoning](https://arxiv.org/abs/2608.30686v1)

- **Authors:** Fukang Zhu, Binbin Zhao, Ruixiao Lin, Ping He, Tianyu Du, Shouling Ji
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Coding agents are increasingly used for software engineering tasks, including bootstrapping projects from third-party repositories whose integrity cannot be assumed. Prior work on repository poisoning largely focuses on attacker-controlled injection and disguise, but developers also shape risk through everyday invoc...

### [Building the Truman Show: A TrustZone-Based Framework for Lightweight Out-of-band Kernel Security Monitoring](https://arxiv.org/abs/2608.29758v1)

- **Authors:** Zhenling Duan, Pan Dong, Renshuang Jiang, Xiaoxiang Fang, Bao Li
- **Date:** 2026-08-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The increasing number of vulnerabilities in operating systems, together with sophisticated kernel-level threats (e.g., rootkits), has weakened the effectiveness of traditional in-kernel protection mechanisms. Since these defenses operate at the same privilege level as the kernel, they share the same attack surface a...

### [CAER: Causal Action Effect Reweighting for World Model Training](https://arxiv.org/abs/2608.30897v1)

- **Authors:** Jianjie Fang, Xvyuan Liu, Ziyou Wang, Rongze Tang, Zhaolu Wang, Zhuohang Li, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** World models are becoming core infrastructure for embodied intelligence, with action-conditioned video generation providing controllable predictions of how scenes evolve after agent interventions. Yet existing models are commonly trained with space-time-uniform mean squared error, allowing abundant background tokens...

### [CHASE: How Content Ecosystems Are Reshaped When Ranking Is the Only Target](https://arxiv.org/abs/2608.30466v1)

- **Authors:** Qianwen Gao, Zichang Su, Yiwen Hou, Arlen Kumar, Leanid Palkhouski
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Generative Engine Optimization (GEO) is increasingly used to improve content visibility in LLM-based retrieval systems, yet its population-level effects under repeated optimization remain poorly understood. We introduce Content Homogenization under rAnking Signal Exploitation (CHASE), a controlled simulation framewo...

### [CogEvol: Towards Efficient and Reliable Learning Environment Generation](https://arxiv.org/abs/2608.30968v1)

- **Authors:** Shangqing Tu, Daniel Zhang-Li, Yucheng Wang, Shiyu Gan, Yanpeng Wang, Huiqiang Rong, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We present CogEvol, a family of models trained specifically for Learning Environment Generation: turning a course brief into a finished learning artifact (structured-JSON slides or self-contained interactive HTML pages) in a single pass. Across 220k production requests, CogEvol completes a slide in a median of 17 se...

### [Decoupling Planning and Control for Instructable Agents](https://arxiv.org/abs/2608.26788)

- **Authors:** Zineng Tang, Kelsey R. Allen, Sjoerd van Steenkiste, Ishita Dasgupta, Alane Suhr
- **Date:** 2026-08-27
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Recent work shows that pre-trained, instruction-tuned vision-language models (VLMs) perform well at mapping from instructions and observations to high-level plans, but struggle to realize such plans as reliable low-latency action sequences in unfamiliar environments. At the same time, world-model controllers excel a...

### [Deploying DeepSeek 175B Locally on a Single Consumer-Grade RTX 4060 Laptop with 32GB RAM for 200k-Scale Protein-Ligand Virtual Screening](https://arxiv.org/abs/2608.30877v1)

- **Authors:** Rui Xiao, Yili Xu
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Recent advances in large language models (LLMs) have demonstrated exceptional performance in protein-ligand interaction prediction, but state-of-the-art pipelines for large-scale virtual screening almost exclusively rely on high-end GPU clusters with hundreds of gigabytes of memory, creating prohibitive hardware bar...

### [GarmentWeaver: Schema-Aware Structured Synthesis for Multimodal Sewing Patterns](https://arxiv.org/abs/2608.30550v1)

- **Authors:** Yinwen Lu, Weihao Luo, Yueqi Zhong
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Multimodal Sewing pattern generation aims to infer executable sewing patterns from design cues such as sketches and textual descriptions. As an interpretable and simulation-compatible representation, sewing patterns are particularly valuable for digital garment creation. However, existing methods often model garment...

### [LightNav-0: Eliciting VLM Spatial Intelligence for Generalist Embodied Navigation](https://arxiv.org/abs/2608.30935v1)

- **Authors:** Shaoan Wang, Aocheng Luo, Fei Huang, Jingyi Xu, Xiaoyang Wang, Yueyu Wang, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Embodied navigation requires agents to translate heterogeneous goals and visual observations into actions across tasks, environments, and robot embodiments. Modern vision-language models (VLMs) already encode spatial priors for visual grounding, spatial reasoning, and pointing, but these capabilities are rarely elic...

### [Matrix-Game 3.5: Enhancing Real-Time Streaming Interactive World Models with Patch Memory](https://arxiv.org/abs/2608.29910v1)

- **Authors:** Runjia Qian, Zile Wang, Jihai Zhang, Kai Zou, Wei Yu, Jiaxing Li, et al.
- **Date:** 2026-08-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Interactive world models extend video generation from offline clip synthesis toward persistent simulation of interactive virtual worlds, enabling applications in games, robotics, embodied agents, and XR. Achieving stable long-horizon interactive generation, however, remains challenging, as the model must simultaneou...

### [Measure Before You Manage: Evaluating Agent Working Memory in Coding Agents](https://arxiv.org/abs/2608.31057v1)

- **Authors:** Le Chen, Zishen Wan, Baixi Sun, Xiaolong Ma, Chih-Hsuan Yang, Feng Yan, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Agent working memory is heterogeneous. Objects such as instructions, artifacts, tool outputs, and agent-generated state play different semantic roles and exhibit different size, retention, and representation profiles. Recent work has begun to explore memory-management mechanisms that account for such heterogeneity....

### [Provably Safe Decentralized Contingency MPC under State-Only Information and Limited Sensing for Nonlinear Multi-agent Systems](https://arxiv.org/abs/2608.30874v1)

- **Authors:** Max Studt, Georg Schildbach
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** This paper considers decentralized contingency MPC for multi-agent control under a state-only information pattern, with particular focus on limited sensing and plug-and-play operation. The objective is to retain recursive feasibility, safety, and Lyapunov-type convergence while reducing conservatism in local interac...

### [SimCRAFT: Distilling Remote Sensing Agents via Synthetic Trajectories and Contextual Retrieval-Augmented Fine-Tuning](https://arxiv.org/abs/2608.30277v1)

- **Authors:** Haoran Wang, Jing Yao, Xu Yang, Zeqing Wang, Yang Zhang, Pedram Ghamisi, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The unprecedented surge in Earth observation data volume and diversity has exposed a critical bottleneck for traditional manual workflows, catalyzing the emergence of Remote Sensing (RS) Agents. However, the practical deployment of these advanced agents is severely hindered by their heavy reliance on large-scale gen...

### [SocialReasonBench: A Video-QA Benchmark for Social Reasoning with Counterfactual Narrative Videos](https://arxiv.org/abs/2608.30716v1)

- **Authors:** Zheyu Huang, Zijing Shi, Haozhe Luo, Huadong Tang, Mingyu Liu, Meng Fang, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Recent advances in Large Multimodal Models (LMMs) have greatly improved video understanding, yet their ability to reason about human-centered social situations remains limited. Existing benchmarks typically rely on videos with a single observed trajectory, making it difficult to determine whether models truly unders...

### [Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data](https://arxiv.org/abs/2608.31082v1)

- **Authors:** Milad Rezaei Hajidehi, Qitong Wang, Stratos Idreos
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Valuable data remains embedded in unstructured sources: web pages, reports, contracts, filings, earnings calls, and PDFs. The big bet in enterprise AI is deploying LLM agents that reason over this data to answer complex questions for every knowledge worker. Agents can do this today, but at prohibitive cost. Each que...

### [TrainSDC: Characterizing and Mitigating Silent Data Corruption in Large Language Model Training](https://arxiv.org/abs/2608.30769v1)

- **Authors:** Zhipeng Xia, Haotian Xu, Siyu Yun, Liqi Lin, Hu Liu, Yu Li, et al.
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** LLM training is increasingly vulnerable to silent data corruption (SDC), yet existing protection methods largely treat Transformer computations uniformly because their vulnerability remains poorly understood. We present the first systematic characterization of SDC vulnerability across major computation interfaces in...

### [TRIPPULSE: Multi-Agent Travel Planning with Review-Grounded Reasoning](https://arxiv.org/abs/2608.30924v1)

- **Authors:** Priyanshu Karmakar, Borru Vijay Sai, Shubhojit Mallick, Abhik Jana, Shreya Ghosh, Manish Gupta
- **Date:** 2026-08-31
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Travel itinerary generation requires balancing strict spatio-temporal constraints with human preferences. Existing LLM-based planners mainly rely on structured attributes and pre- defined traveler personas, but real travel deci- sions are often shaped by reviews that reveal experiential factors such as comfort, safe...

### [What Makes Agent Memory Useful for Reliable Unanswerable Question Handling?](https://doi.org/10.48550/arxiv.2608.27924)

- **Authors:** Chuanyuan Tan, Junjie Yu, Yuxin Wang, Yining Zheng, Xipeng Qiu, Wenliang Chen
- **Date:** 2026-08-28
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Reliable handling of unanswerable questions (UAQs) is critical for trustworthy LLM-based agents. Although memory is widely used in agent systems, its role in reliable UAQ handling remains unclear. We present a systematic study of agent memory for UAQ handling under a unified agentic RAG framework, evaluating four re...

### [Blind Men and the Elephant: Probing the Epistemic Myopia of LLMs under Long-Tail Divergent Knowledge](https://doi.org/10.48550/arxiv.2608.28478)

- **Authors:** Zhuoshi Pan, Junru Lu, Yan Qian, H. Vicky Zhao, Di Yin, Xing Sun
- **Date:** 2026-08-28
- **Source:** openalex
- **Relevance:** maybe (44/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** benchmark, parametric-memory
- **Abstract summary:** Factual question answering (QA) typically assumes a single canonical answer, obscuring whether large language models (LLMs) retain divergent accounts of long-tail facts. To address this gap, we introduce ElephantBench, a closed-book knowledge probe comprising 1,094 questions generated through an auditable graph-base...

### [MedCache: Efficient and Temporally Valid Memory for Longitudinal Clinical Agents](https://arxiv.org/abs/2608.29528v1)

- **Authors:** Hei Ting, Chan, Chenwei Wu, Xueshen Liu, Boyuan Zheng, Liyue Shen, et al.
- **Date:** 2026-08-30
- **Source:** arxiv
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Longitudinal clinical agents must maintain an evolving patient state from evidence distributed across visits, time points, and specialties. However, how agent memory should be designed for this setting remains unclear. We introduce a benchmark of multi-visit, multi-specialty patient records that evaluates long-conte...
