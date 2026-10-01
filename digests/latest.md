# Latest Paper Scout Digest

Latest daily digest: [2026-10-01](2026-10-01.md).

# Paper Scout Digest - 2026-10-01

## Run Summary

- **Run ID:** 140
- **Candidates fetched:** 1005
- **New unique papers:** 911
- **Relevant:** 76
- **Maybe relevant:** 99
- **Irrelevant:** 830
- **Source summary:** arxiv: 597, openalex: 400, semantic_scholar: 8

## Source Warnings

- arxiv: incomplete discovery window for 'agent memory'; single-page record limit reached.
- arxiv: incomplete discovery window for 'self-improving language models'; single-page record limit reached.
- arxiv: incomplete discovery window for 'cs.AI,cs.CL,cs.LG'; single-page record limit reached.
- openalex: incomplete discovery window for 'agent memory'; single-page record limit reached.
- openalex: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'memory distillation language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'parametric memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'agent memory'; single-page record limit reached.
- semantic_scholar failed for 'procedural memory language model': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar: incomplete discovery window for 'memory distillation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'parametric memory LLM'; single-page record limit reached.

## Highly Relevant

### [TAGGRAPH: Tag-Augmented Graphs for Graph Retrieval of Agent Persistent Histories](https://arxiv.org/abs/2609.38353v1)

- **Authors:** Yu-Su Chen, Yu-Jung Liang, Pengtao Xie
- **Date:** 2026-09-29
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, memory-systems, long-term-memory, benchmark, evaluation, agent-memory
- **Abstract summary:** Long-term memory lets LLM agents recall past interactions and remain consistent across sessions, but memory systems are hard to compare because they often vary in representation, indexing, retrieval, and evaluation. We present a controlled evaluation framework based on shared 5W-style conversational memories. Locali...

### [When Correct Memory Goes Wrong: Fuzzing Persistent Memory Use in LLM Agents](https://arxiv.org/abs/2609.38275v1)

- **Authors:** Yuqiao Meng, Luoxi Tang, Yingxue Zhang, Yuchen Yang, Zhaohan Xi
- **Date:** 2026-09-29
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, memory-systems, long-term-memory, memory-policy, evaluation, agent-memory
- **Abstract summary:** Persistent memory helps LLM agents carry information across long interactions, but correct memory can still be used incorrectly when queries change or memory states evolve. Existing work mainly studies memory content errors or evaluates fixed test cases, leaving memory-use failures hard to discover systematically. W...

### [When Context Changes: Understanding Update Failures in LLMs](https://arxiv.org/abs/2609.38866v1)

- **Authors:** Junyu Guo, Yuchen Fang, Shangding Gu, Costas Spanos, James Demmel, Javad Lavaei
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** llm-agents, benchmark, agent-memory, memory-systems
- **Abstract summary:** As preferences, goals, and facts change, LLM agents must use the current state while earlier versions remain in context. Yet they can answer with an old value of the same variable, a failure that we call stale binding. To study when models use outdated information and why, we introduce Controlled In-Context Memory (...

### [EngramBench: A Capability-Grounded Benchmark for Skill-Evolution Harnesses](https://arxiv.org/abs/2609.39284v1)

- **Authors:** Zhixuan Tan, Pengjie Gu, Zhao Li, Yihan Hu, Xu He, Dong Li, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** While large language models have achieved remarkable success in isolated code generation, authentic software engineering requires sustained reasoning, complex state management, and continuous cross-domain abstraction. However, current evaluations of skill evolution in autonomous agents suffer from a critical identif...

### [Memory Is a Derivation: The Distributed-Evidence Paradox in Long-Term Agents](https://doi.org/10.48550/arxiv.2609.36130)

- **Authors:** Hongjun Liu, Chen Zhao
- **Date:** 2026-09-28
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, long-term-memory, agent-memory, memory-systems
- **Abstract summary:** Long-running LLM agents compress past interactions into persistent memories that may be reused as premises for later tasks. This creates a distinct derivation problem: whether the memory actually follows from what the interaction history supports. Relevant evidence may be scattered across earlier interactions, while...

### [OmniSmartHome: A Multimodal Reasoning Benchmark for Smart-Home Agents](https://arxiv.org/abs/2609.32569)

- **Authors:** Jihoo Jung, Suho Yoo, Jeongsoo Choi, Hyebin Cho, Tae Wook Haam, Hyeonggon Ryu, et al.
- **Date:** 2026-09-26
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Smart-home assistants are expected to handle diverse, realistic requests that arise in daily life. In such interactions, users often rely on the surrounding multimodal context-pointing at objects or referring to what they see or hear, leaving their requests underspecified in language alone. Existing smart-home bench...

### [ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents](https://doi.org/10.48550/arxiv.2609.37311)

- **Authors:** Haohao Qu, Yongcheng Jing, Chun Hin Chan, Shanru Lin, Wenqi Fan, Dacheng Tao
- **Date:** 2026-09-29
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory storage, retrieval, update, or consolidation for LLM agents.
- **Tags:** memory-policy, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Recent Recommendation Agents (RecAgents) offer a promising alternative by shifting recommendation to an active, user-side paradigm, where generative agents autonomously perceive external platforms, reason over user preferences, and execute decisions. However, existing RecAgents still suffer from two critical limitat...

### [Salience, Ranking, and Metabolism: Three Conflated Signals in Long-Running Agent Memory Systems](https://doi.org/10.5281/zenodo.23068931)

- **Authors:** Baofeng Zhao
- **Date:** 2026-09-30
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, llm-agents
- **Abstract summary:** Who destroyed the LLM's memory? Not the model. Not RAG. Years of unexamined industry habit. A scoring formula written in 2023 for a simulation demo—relevance plus recency plus importance—moved into production hearts without a checkup, letting the three jobs of "importance" (sedimentation, ranking, retirement—which w...

### [Salience, Ranking, and Metabolism: Three Conflated Signals in Long-Running Agent Memory Systems](https://doi.org/10.5281/zenodo.23068930)

- **Authors:** Baofeng Zhao
- **Date:** 2026-09-30
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, llm-agents
- **Abstract summary:** Who destroyed the LLM's memory? Not the model. Not RAG. Years of unexamined industry habit. A scoring formula written in 2023 for a simulation demo—relevance plus recency plus importance—moved into production hearts without a checkup, letting the three jobs of "importance" (sedimentation, ranking, retirement—which w...

### [Salience, Ranking, and Metabolism: Three Conflated Signals in Long-Running Agent Memory Systems](https://doi.org/10.5281/zenodo.23070233)

- **Authors:** Baofeng Zhao
- **Date:** 2026-09-30
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, llm-agents
- **Abstract summary:** Who destroyed the LLM's memory? Not the model. Not RAG. Years of unexamined industry habit. A scoring formula written in 2023 for a simulation demo—relevance plus recency plus importance—moved into production hearts without a checkup, letting the three jobs of "importance" (sedimentation, ranking, retirement—which w...

### [Salience, Ranking, and Metabolism: Three Conflated Signals in Long-Running Agent Memory Systems](https://doi.org/10.5281/zenodo.23069906)

- **Authors:** Baofeng Zhao
- **Date:** 2026-09-30
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, llm-agents
- **Abstract summary:** Who destroyed the LLM's memory? Not the model. Not RAG. Years of unexamined industry habit. A scoring formula written in 2023 for a simulation demo—relevance plus recency plus importance—moved into production hearts without a checkup, letting the three jobs of "importance" (sedimentation, ranking, retirement—which w...

## Maybe Relevant

### [When Does Selection Replace Extraction? A Pre-Registered Test of Agent Memory with a Typed Decision Model](https://arxiv.org/abs/2609.34227)

- **Authors:** Rishabh Sharma, Rishika Lall
- **Date:** 2026-09-28
- **Source:** openalex
- **Relevance:** maybe (69/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, benchmark
- **Abstract summary:** Does conversational memory need LLM-extracted facts, or is selecting the right raw turns enough? Published results disagree. Extraction-based systems report gains from distilled facts. Recent studies find raw history with good ranking does as well, but disagree about whether ranking matters. We ran a pre-registered...

### [Beyond the Remembered World: Predictive 4D Belief for Persistent Navigation in Evolving Worlds](https://arxiv.org/abs/2609.39166v1)

- **Authors:** Mingjian Gao, Zhaocheng Li, Haoyang Huang, Wenqiao Zhang, Yingjie Niu, Hao Zhou, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Persistent spatial memory enables embodied agents to navigate familiar environments across repeated visits. However, targets may move while unobserved, including during navigation, making remembered locations unreliable by the time an agent arrives. Despite advances in memory retrieval and state prediction, accounti...

### [Deletion-Robust Memory for Long-Horizon Language Agents: A Neural–Symbolic Substrate with Exactly Addressable Hierarchical State Memory](https://doi.org/10.17605/osf.io/w9kbm)

- **Authors:** Yu-Xuan Liu
- **Date:** 2026-09-30
- **Source:** openalex
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation, llm-agents
- **Abstract summary:** This registration freezes, before execution, the complete confirmatory evaluation protocol for NSU-HSM (Hierarchical State Memory), a neural-symbolic memory substrate for long-horizon language agents, presented in a companion JAIR submission: "Deletion-Robust Memory for Long-Horizon Language Agents: A Neural–Symboli...

### [AIMS: An Agentic AI Framework for Sim-to-Real Multi-Modal ISAC](https://arxiv.org/abs/2609.39964v1)

- **Authors:** Yijie Bian, Kai Zhang, Wei Guo, Zixin Wang, Shenghui Song, Jun Zhang, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Multi-modal integrated sensing and communication (ISAC) enables environmental perception and reliable connectivity for intelligent wireless networks. Data-driven multi-modal ISAC models depend heavily on annotated real-world data to learn relationships across sensing and wireless observations, thereby constraining s...

### [AviGPT-250M-Instruct: Semi-Parametric Edge Intelligence with a Native NVMe Hardware Memory Bus](https://doi.org/10.5281/zenodo.23067633)

- **Authors:** Avinash Ricky Yadlapalli
- **Date:** 2026-09-30
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** AviGPT-250M-Instruct is a 250M-parameter autoregressive small language model (SLM) introducing a Semi-Parametric Decoupling paradigm for resource-constrained edge computing. Rather than overloading transformer weights with static encyclopedic memorization and floating-point arithmetic approximation, AviGPT-250M dele...

### [AviGPT-250M-Instruct: Semi-Parametric Edge Intelligence with a Native NVMe Hardware Memory Bus](https://doi.org/10.5281/zenodo.23067632)

- **Authors:** Avinash Ricky Yadlapalli
- **Date:** 2026-09-30
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** AviGPT-250M-Instruct is a 250M-parameter autoregressive small language model (SLM) introducing a Semi-Parametric Decoupling paradigm for resource-constrained edge computing. Rather than overloading transformer weights with static encyclopedic memorization and floating-point arithmetic approximation, AviGPT-250M dele...

### [Characterizing High Bandwidth Flash for LLM Serving](https://arxiv.org/abs/2609.39131v1)

- **Authors:** Zack Yu, Chloe Wong, Coleman Hooper, Minjae Lee, Wonjun Kang, Youngjin Cho, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language model (LLM) serving requires substantial memory to store model weights and KV caches. As models grow larger and contexts become longer, memory capacity and bandwidth increasingly become bottlenecks for serving performance. Agentic workloads compound this pressure through repeated interactions over gro...

### [cua-speedrun: Standardized Benchmarking of the Speed of Computer-Use Agents](https://arxiv.org/abs/2609.40284v1)

- **Authors:** Pranjal Aggarwal, Lawrence Keunho Jang, Sean Welleck, Daniel Fried, Ruslan Salakhutdinov, Jing Yu Koh
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Computer use agents (CUAs), which use graphical user interfaces (GUIs) to complete tasks on a computer, have recently surpassed human performance on many standard benchmarks, including difficult long-horizon tasks. Their capabilities are undoubtedly impressive, however, a key barrier to the widespread adoption and d...

### [DashVMC: Real-Time Discrete World Model Control in Geometry Dash](https://arxiv.org/abs/2609.40003v1)

- **Authors:** Florent Tariolle, Florian Yger
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** World-model agents are usually evaluated in simulators that can wait for the policy; live games impose the opposite constraint, requiring capture, prediction, and action before the next frame. We present DashVMC, which learns a compact, action-conditioned world model from approximately two hours of recorded Geometry...

### [Efficient Expert-Parallel Communication on PCIe-Connected Consumer GPUs](https://arxiv.org/abs/2609.40093v1)

- **Authors:** Jaehwan Lee, Sangmin Lee, Chaewon Kim, Junsik Shin, Jaejin Lee
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Expert parallelism (EP) enables inference of large Mixture-of-Experts (MoE) models by placing their experts across multiple GPUs, but requires substantial communication between GPUs at every MoE layer. As contemporary MoE models activate more experts per token, this communication accounts for a growing fraction of i...

### [Inference Auctions](https://arxiv.org/abs/2609.40070v1)

- **Authors:** Keegan Harris, Siddharth Prasad, Asher Trockman, Nika Haghtalab, Michael I. Jordan
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** When inference demand exceeds available compute capacity, model providers must decide which requests should be served first. Users have different tolerances for delay from an LLM API, but current priority pricing schemes compress these differences into coarse fixed-price service tiers. We design an inference auction...

### [OSWorld-Science: A Benchmark of Computer Use Agents for Learning and Using Scientific Software](https://arxiv.org/abs/2609.39903v1)

- **Authors:** Dingyuan Dai, Heli Qi, Lei Liu, Yinxi Li, Baiding Chen, Zijun Dou, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Scientific software presents a demanding test for computer-using agents based on visual language models (VLMs): completing a research workflow requires interpreting specialized interfaces, manipulating scientific objects, and producing verifiable results. We thus introduce OSWorld-Science, a benchmark and evaluation...

### [RankEvolve: A Reliable Multi-Agent Auto-Research Harness for Evolving Ranking Models](https://arxiv.org/abs/2609.39551v1)

- **Authors:** Zheng Chen, Linfeng Liu, Hong Li, Hong Yan
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Auto-research agents, LLM systems that propose, implement, train, and evaluate model changes across iterations, promise to automate applied ML's experimental loop. Over long horizons, execution accuracy is a binding constraint: a change can silently leak held-out data, omit normalization, disconnect a gradient, or l...

### [Recursive Organization Improvement: A Modeling Specification for Human--Agent Organizations](https://arxiv.org/abs/2609.38643v1)

- **Authors:** Zilong Wang
- **Date:** 2026-09-29
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Stronger AI agents do not automatically produce better organizations: teams must also learn which work arrangements to retain and when to reconsider them. We propose a modeling specification for recursive organization improvement and evaluate it through an executable checker, a public-record mapping, and controlled...

### [Self-Evolving Algorithm-Design Agents: Escaping In-Context Evolutionary Stagnation via Population-Curated Policy Optimization](https://arxiv.org/abs/2609.38757v1)

- **Authors:** Chen Lu, Ke Xue, Siyuan Xu, Mingxuan Yuan, Chao Qian
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language models are increasingly participating in complex real-world tasks in the form of algorithm-design agents, designing and refining algorithms. Many successful algorithm-design agents adopt pure in-context evolutionary frameworks, but they may quickly plateau in domains that require specialized knowledge...

### [SparseEngine: Sparse-First Inference Engine](https://arxiv.org/abs/2609.39068v1)

- **Authors:** Jitai Hao, Quansheng Gu, Qiang Huang, Jun Yu
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Long-context LLM agents accumulate interaction histories that strain KV-cache memory and attention computation. Although sparse attention reduces these costs, heterogeneous cache representations and workflows hinder integration with existing inference engines, while prior sparse-serving abstractions support only spe...

### [Speculative Safety Honeypot: Toward Proactive Defense Against Multi-turn Agent Attacks](https://arxiv.org/abs/2609.39549v1)

- **Authors:** Zezhong Wang, Xueyang Tang, Rui Lian, Yang Lou, Heqing Huang
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** As Large Language Model (LLM) agents are increasingly deployed in complex environments, multi-turn interaction attacks have become a significant security challenge. Existing detection methods typically rely on historical context. However, this retrospective logic struggles to identify deep malicious intents that are...

### [TACTIC: Temporal and Context-Aware LLM Tactical Planning for Roadside LiDAR Attacks](https://arxiv.org/abs/2609.39969v1)

- **Authors:** Yiming Gao, Shaocheng Luo
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Physical LiDAR attacks are often evaluated using fixed primitives and manually selected parameters, despite their strong dependence on surrounding traffic. We present TACTIC, a scene-aware framework that uses a multimodal large language model (MLLM) to coordinate state-adaptive roadside LiDAR attacks. Under a gray-b...

### [Towards Efficient HPC Systems for Agents: Challenges and Opportunities](https://arxiv.org/abs/2609.38723v1)

- **Authors:** Yunjia Zheng, Bintang Dwi Marthen, Zachary Pan, Minghao Li, Raminder Singh, Manasvita Joshi, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Coding agents have become real users of high-performance computing (HPC) systems, yet today's HPC abstractions, interfaces, and policies remain designed for human-driven workflows. In our measurement, users running coding agents are only 19.5% of the observed population, but account for 55.8% of job submissions, 29....

### [VirusCascade: Hijacking Collaborative Reflection in LLM-Powered Recommender Agents](https://arxiv.org/abs/2609.38270v1)

- **Authors:** Yurong Hao, Wen Zhou, Guowei Guan, Tiantong Wu, Fuyao Zhang, Wei Yang Bryan Lim
- **Date:** 2026-09-29
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Advancing beyond traditional static scoring models, LLM-powered agentic recommender systems (LLM-ARS) instantiate users and items as autonomous agents, whose semantic states are dynamically refined through a recurrent process known as collaborative reflection. While this mechanism improves recommendation quality, it...

### [What Limits Recursive Reasoning Models: Optimization, Architecture and Test-Time Scaling](https://arxiv.org/abs/2609.39967v1)

- **Authors:** Yuliana Shakhvalieva, Dmitrii Kharchev, Viacheslav Bezrukov, Inessa Fedorova, Dmitry Bocharov, Ivan Oseledets, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Recursive reasoning models apply a small shared Transformer block many times to refine a latent state. This gives them large effective depth with few parameters and makes them strong on algorithmic tasks. Such compact solvers are natural candidates for tools that an LLM can call on narrow algorithmic subproblems. Ho...

### [Working Around the Compute Ceiling: Byte-Exact Memory in Galahad Makes LLM Reading a One-Time Cost LLM Reading a One-Time Cost](https://arxiv.org/abs/2609.39358v1)

- **Authors:** Sietse Schelpe
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** A transformer language model performs a bounded amount of computation per token, and recent work by Vishal Sikka, former CEO of Infosys, argues that this bound limits which tasks a model can carry out or verify (arXiv:2507.07505). We ask how much of the budget beneath that ceiling is spent on work the model has alre...

### [Action Conditioned Bisimulation For GUI Agent Memory](https://arxiv.org/abs/2609.38778v1)

- **Authors:** Hongbo Zhang, Liuyang Song, Quanquan Li, Daqian Yang, Yan Wen, Zhengtao Yao
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** An agent that remembers what it did on a web page must decide when two pages count as the same. Memories built on observation similarity merge pages that look alike but behave differently, and GUIs are full of such pages: two tabs of one widget or two rows of one menu answer the same click differently. We define the...

### [How Can Recommendation Feedback Evolve Agent Memory?](https://doi.org/10.48550/arxiv.2609.37544)

- **Authors:** Shanwen Mao, Mingming Li, Hao Zhang, Zhiheng Li, Yige Wang, Penghua Yu, et al.
- **Date:** 2026-09-29
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Content-generation agents continuously receive impressions, clicks, conversions, and negative feedback from recommendation systems, providing real-world outcome signals for memory evolution. However, these signals are delayed and noisy, confounded by audience composition, placement, and recommendation policies, and...

### [MemCodex: Self-Programming Hierarchical Memory for Language Agents](https://arxiv.org/abs/2609.39765v1)

- **Authors:** Xiaoqiang Wang, Bang Liu
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Agent memory faces heterogeneous access needs: a single-hop question may require one piece of evidence, whereas a multi-hop question must combine evidence from multiple sources. Predefined memory workflows cannot adapt to these varying needs. Recent adaptive methods search or learn over memory components and their c...
