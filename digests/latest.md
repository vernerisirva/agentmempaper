# Latest Paper Scout Digest

Latest daily digest: [2026-11-17](2026-11-17.md).

# Paper Scout Digest - 2026-11-17

## Run Summary

- **Run ID:** 182
- **Candidates fetched:** 929
- **New unique papers:** 828
- **Relevant:** 75
- **Maybe relevant:** 119
- **Irrelevant:** 735
- **Source summary:** arxiv: 517, openalex: 400, semantic_scholar: 12

## Source Warnings

- arxiv: incomplete discovery window for 'agent memory'; single-page record limit reached.
- arxiv: incomplete discovery window for 'cs.AI,cs.CL,cs.LG'; single-page record limit reached.
- openalex: incomplete discovery window for 'agent memory'; single-page record limit reached.
- openalex: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'memory distillation language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'parametric memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'agent memory'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'memory distillation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'parametric memory LLM'; single-page record limit reached.

## Highly Relevant

### [Instant Weight-Space Consolidation for Long-Term Memory in LLMs](https://arxiv.org/abs/2611.20759v1)

- **Authors:** Manan Suri, Dinesh Manocha
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Discusses Engram-style or parametric memory mechanisms for language models.
- **Tags:** agent-memory, long-term-memory, benchmark, parametric-memory, memory-systems, llm-agents
- **Abstract summary:** Agentic memory systems give LLMs persistent memory by extracting experience into text and retrieving it at query time, but the model itself does not evolve: however many interactions it has had, it starts each query the same. Extraction errors compound, implicit cross-session patterns that no single fragment states...

### [Compositional Exploits in Autonomous Coding Agents: Attack Mechanics and Ephemeral Defense](https://arxiv.org/abs/2611.19764v1)

- **Authors:** Deep Shah, Nehal Kathrotia
- **Date:** 2026-11-15
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** benchmark, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Autonomous coding agents (such as Antigravity, Claude Code, Cursor, and OpenHands) rely on third-party tools to inspect files, run commands, and call external APIs. Today's security auditors evaluate these tools almost entirely in isolation: static linters and AST checkers verify that each individual tool contains n...

### [HEAMS: Holistic Evaluation of Agent Memory Systems](https://arxiv.org/abs/2611.20144v1)

- **Authors:** Chirag Goel, Jacob Lavoie, Amirhossein Naghshzan, Jordan Bannister, Marzia Nouri, Mehar Bhatia, et al.
- **Date:** 2026-11-15
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** agent-memory, memory-systems, benchmark, evaluation, llm-agents
- **Abstract summary:** Memory systems allow AI agents to persist information across interactions, making them more personalized and more capable on long-horizon tasks. This persistence introduces new risks: stored information can be disclosed in inappropriate contexts, resist correction or deletion, be retained beyond what users desire, o...

### [LEDGER: Auditable Agent Memory Under Change](https://arxiv.org/abs/2611.20927v1)

- **Authors:** Md Aidul Islam, Md Nasir Uddin Shuvo, Muhammad Waseem, Pekka Abrahamsson
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, benchmark, evaluation, llm-agents
- **Abstract summary:** Agent memory systems are mostly evaluated on fixed histories, and only their final answers are scored. In real use, facts change, sources differ in reliability, and users ask the agent to forget things. We present LEDGER, a memory layer in which a language model proposes facts and explicit rules decide which value i...

### [AdMem: Expectation-Grounded Procedural Memory for Long-Horizon Task-Solving Agents](https://arxiv.org/abs/2611.20605v1)

- **Authors:** Runzhe Wang, Huilin Lu, Shengjie Liu, Li Dong, Zhihuai Zhu
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** An agent that carries memory across tasks is only as good as the entries it keeps. We begin from an observation that is easy to reproduce and uncomfortable for the field: naively accumulating cross-task experience can make an agent \emph{worse} than one with no memory at all. On AgentBoard, a workflow-induction memo...

### [Agentic Computational Algebra](https://arxiv.org/abs/2611.16073)

- **Authors:** Ryan A. Anderson, Matthew Trager, B. Bowman, Wei Xia, Stefano Soatto
- **Date:** 2026-11-11
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** We explore the use of AI agents for solving computational problems in algebra. For the problems we consider, the main challenge is not correctness but \emph{time}: general-purpose algorithms are guaranteed to provide correct solutions but can be prohibitively slow, while reformulations that exploit special structure...

### [enron-memory-replay: an agent memory replayed week by week through one mailbox of the Enron corpus](https://doi.org/10.5281/zenodo.24241955)

- **Authors:** Emre Akadal
- **Date:** 2026-11-15
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, long-term-memory, memory-systems, llm-agents
- **Abstract summary:** An AI assistant's long-term memory, built week by week from one real mailbox, with every intermediate layer kept. One Enron employee's email (the kaminski-v mailbox of the public CMU Enron corpus: 11,523 messages, 30 November 1999 to 3 February 2002) is replayed in the order it arrived into a file-based agent memory...

## Maybe Relevant

### [A Matrix with Steps: An Episodic and Procedural Memory Method for Tool-Using Agents and Robots](https://arxiv.org/abs/2611.20230v1)

- **Authors:** Jürgen Paulhart, Peter Schüller
- **Date:** 2026-11-15
- **Source:** arxiv
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Agents that call tools and robots that execute tasks are challenged by two shortcomings: they repeat what failed before, and they learn from runs that they only believe succeeded. We describe the construction of a memory that addresses both, built for a production agent platform. Every run is recorded as an episode,...

### [CRAFT: A Robot-Agent Harness with Scope-Aware Adaptation](https://arxiv.org/abs/2611.19952v1)

- **Authors:** Peng Zhang, Jiawen Wang, Cheng Xue, Jochen Renz
- **Date:** 2026-11-15
- **Source:** arxiv
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** A robot may know how to move an object yet still need to learn where it belongs. When a person rejects a placement, the robot must decide whether the correction applies only to that situation or expresses a broader rule. We study this problem in CRAFT (Contextual Requirement Adaptation with Frozen Tools), a framewor...

### [Digital Resources to Long-Term Agent Memory: Evaluating Memory Formation and Retrieval Across Heterogeneous Personal Knowledge](https://doi.org/10.5281/zenodo.24241304)

- **Authors:** kishore sabavath, vansh, devansh
- **Date:** 2026-11-15
- **Source:** openalex
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation, llm-agents
- **Abstract summary:** The ability to retain and retrieve information from heterogeneous digital resources is an important requirement for long-term memory in intelligent agents. This paper evaluates different memory representation and retrieval approaches for organizing personal knowledge collected from multiple digital sources. The eval...

### [Jetriever: Shifting Agent Memory Retrieval from Similarity to Utility](https://arxiv.org/abs/2611.21478v1)

- **Authors:** Ruizhe Li, Licheng Zhang, Mingxuan Du, Zhendong Mao
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (61/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, memory-policy
- **Abstract summary:** A useful memory need not resemble the question it helps answer. Jetriever ranks each stored memory by Jev's decision score for its usefulness to the current question, replacing similarity search with full-pool utility scoring. On InMind's 125 indirect-query tasks, it places the gold exchange first in 84.8% of cases;...

### [StaleBench: Isolating Stale Retrieval in Agent Memory, and Pricing the Fix](https://arxiv.org/abs/2611.19752v1)

- **Authors:** S M Mahbub Murshed
- **Date:** 2026-11-15
- **Source:** arxiv
- **Relevance:** maybe (61/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, memory-policy
- **Abstract summary:** An agent that stores facts over time eventually stores several versions of the same fact. Asked a value-agnostic question - "which team does X play for now?" - a similarity retriever cannot prefer the current version, because every version matches the entity the query names. StaleBench isolates this stale-retrieval...

### [Agent-Guided Configuration Tuning for SMT Solvers](https://arxiv.org/abs/2611.20484v1)

- **Authors:** Cong Wang, Qiaoyi Zheng, Zhaoguo Wang, Fan Long
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** SMT solvers expose many configuration choices that determine how well their existing algorithms perform on a workload. We present, to our knowledge, the first workflow that uses general-purpose LLM agents to tune SMT solver configurations. Agents read solver documentation, source code, and persistent experiment reco...

### [AgenticJevNav: Agentic Object Search and Navigation via Event-Driven Verification](https://arxiv.org/abs/2611.19912v1)

- **Authors:** Shuning Zhang, Shuli Zhang, Yunheng Wang, Wei Lu, Jiaxi Zhang, Yihang Kang, et al.
- **Date:** 2026-11-15
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agentic navigation must maintain goals and adapt actions from incomplete evidence despite execution failures and delayed inference. We present AgenticJevNav, which links goal-directed planning, evidence memory, event-triggered verification, and bounded execution. The Agent plans from RGB, odometry, memory, and feedb...

### [B2G-Agent: An LLM-Based Multi-Agent Tool for End-to-End Building-Grid Interactions](https://arxiv.org/abs/2611.19036v1)

- **Authors:** Xueyuan Cui, Qian Zhang, Xiaochen Liu, Yi Wang
- **Date:** 2026-11-14
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Buildings are major electricity consumers and can interact with distribution network dispatch through flexible power scheduling. These interactions require distribution network operators (DNOs) and building energy managers (BEMs) to reconcile their operational constraints and perform complex cross-field computations...

### [CAE-Bench: Benchmarking AI Agents for Reusable CAE Solver Development](https://arxiv.org/abs/2611.21273v1)

- **Authors:** Zhiyu Zhou, Tianyou Liu, Xinping Yang, Yiyao Liu, Jiayi Dong, Yihan Lin, et al.
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We developed CAE-Bench, a benchmark to evaluate AI agents on Computer-Aided Engineering (CAE) solver development. A CAE solver is more than a PDE solver; it must be able to generalize across various inputs, such as different boundary conditions, geometries, and material properties. CAE-Bench evaluates the generaliza...

### [Contrastive Activation-Guided Zeroth-Order Preference Optimisation for Memory-Efficient LLM Alignment](https://arxiv.org/abs/2611.20635v1)

- **Authors:** Weiyun Huang, Alessio Galatolo
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Direct Preference Optimisation (DPO) simplifies reinforcement learning from human feedback, but still relies on traditional backpropagation and its associated activation-memory cost. Zeroth-order (ZO) optimisation avoids backpropagation, yet isotropic perturbations can produce noisy updates for preference objectives...

### [Conversing with a Conversational Agent: A Real Conversation, Not a Simulated One](https://arxiv.org/abs/2611.20826v1)

- **Authors:** Christophe Denis
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The claim that interactions with artificial conversational agents merely simulate human conversation rests on a philosophical distinction between reproducing the observable features of an activity and actually performing it. Although this distinction is appropriate for certain physical phenomena, its application to...

### [Evaluating Authorization and Trust Boundaries in Agentic Orchestration Frameworks](https://arxiv.org/abs/2611.21259v1)

- **Authors:** Sahaya Jestus Lazer, Kshitiz Aryal, Maanak Gupta, Elisa Bertino
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agentic AI systems extend large language models with tools, memory, and multi-agent collaboration, introducing security risks at orchestration boundaries. These risks depend on how identities are represented, operations are authorized, and instructions or information propagate between components. We evaluate LangCha...

### [GranularGPT: Natural-Language-Driven End-to-End Discrete Element Method Simulations](https://arxiv.org/abs/2611.20551v1)

- **Authors:** Erlei Li, Sirui Tang, Ai Wang, Mingwei Hu, Yuchen Dai, Geoff Wang
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Discrete element method (DEM) simulations are widely used to investigate granular and particulate systems, but their application often requires specialized expertise in particle physics, numerical modelling, and simulation post-processing. Large language models (LLMs) offer new opportunities to simplify these workfl...

### [How Developer Personality Shapes the Use of AI Coding Assistants](https://arxiv.org/abs/2611.21240v1)

- **Authors:** Annemarie Wittig, Alina Mailach, Norbert Siegmund
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Developers differ in personality traits that shape how they approach software development tasks, yet AI coding assistants either behave uniformly or offer personalization features whose fit with individual developers must be found through trial and error. This is because it remains unclear how personality shapes dev...

### [K2-Horizon: A Frontier Fleet of Open Source Language Models](https://arxiv.org/abs/2611.21003v1)

- **Authors:** K2 Team, Zhengzhong Liu, Haonan Li, Xuezhe Ma, Alexander Moreno, Subham Sekhar Sahoo, et al.
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We present K2-Horizon, a fleet of six fully open language models, from a 0.9B dense model to a 375B-A23B MoE, built for general-purpose reasoning and agentic work across math and science, software engineering, deep research, office automation, and beyond. The models lead or are competitive with strong open models of...

### [Language Models Meet Vibration Testing for LEO Constellation Satellites with Calibrated Response Prediction from Few-show Sweeps](https://arxiv.org/abs/2611.20579v1)

- **Authors:** Jun Wu, Deming Li, Zhenming Zheng, Honghao Yue, Fei Yang, Hao Sun
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language models (LLMs) increasingly drive engineering analysis end to end, turning textual records into the inputs of numerical programs, but a plausible and wrong value can pass silently into a decision. We propose deterministic validation gates for LLM-driven engineering analysis, a general paradigm in which...

### [Memory-On-Demand: Bounded-Context Recall of Unbounded Interaction History via RAG in Multi-agent LLM Systems](https://doi.org/10.1007/978-3-032-44237-6_13)

- **Authors:** Mirza Riyasat Ali, Prajoona Valsalan, Rida Maamoor
- **Date:** 2026-11-15
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** No abstract available.

### [Multi-LLM Agentic AI at the Edge: Joint Agent Scheduling and Resource Allocation](https://arxiv.org/abs/2611.20915v1)

- **Authors:** Yuanyan Song, Kezhi Wang, Xinmian Xu, Yongmin Li
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** In this paper, an edge-enabled multi-large language model (LLM) agentic AI architecture is proposed, where one supervisor AI agent and multiple worker AI agents cooperatively execute users' requests at the edge. The supervisor AI agent decouples the user request into a series of sub-tasks and dynamically dispatches...

### [ProcReverser: Multi-Agent Black-Box Microarchitectural Reverse Engineering for Processor Vulnerability Analysis](https://arxiv.org/abs/2611.20827v1)

- **Authors:** Guanqi Lyu, Decheng Qiu, Guangyang Zhang, Fei Zhao, Zhaojun Lu, Jiaji He, et al.
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** When processor implementation details are unavailable, black-box microarchitectural reverse engineering helps security researchers identify hardware conditions related to security vulnerabilities. However, this process requires substantial manual effort to design experiments, develop test programs, and analyze resul...

### [RoCoMark: Robust Code Watermarking Against LLM-Based Functionality-Preserving Rewriting Attacks](https://arxiv.org/abs/2611.11399)

- **Authors:** Hongjie Zhang, Xingcheng Li, Hanzhou Wu, Zhihua Xia, Xinpeng Zhang
- **Date:** 2026-11-08
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large Language Models (LLMs) present significant challenges to source tracing of generated code, as LLM rewriting can substantially alter the syntactic and structural characteristics of watermarked code. However, existing watermarking methods often suffer severe performance degradation under LLM-based functionality-...

### [ShadowBench: Exposing Lexical Anchoring and the Illusion of Forgetting in Large Language Models](https://arxiv.org/abs/2611.15925)

- **Authors:** Sujan Maharjan, Lu Liu
- **Date:** 2026-11-11
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large Language Models (LLMs) have emerged as primary interfaces for factual retrieval, yet current evaluation paradigms rely almost exclusively on explicit entity names. In this work, we demonstrate that LLM knowledge is fundamentally lexically anchored: models possess extensive factual information but find it signi...

### [Sim-to-Real Powertrain Vibration Control via Model-Based Assisted Domain-Randomized Reinforcement Learning](https://arxiv.org/abs/2611.15133)

- **Authors:** Heisei Yonezawa, Ansei Yonezawa, Itsuro KAJIWARA
- **Date:** 2026-11-11
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Controllers designed from nominal models often degrade on mechanical systems with nonlinearities and parametric variations, such as automotive powertrains with backlash. Deep reinforcement learning (DRL) with domain randomization can acquire robustness to such model discrepancies, but wide randomization destabilizes...

### [SliceWise: Traffic-Aware Multi-Agent RL with Temporal Encoding for Joint Slice Admission and Resource Orchestration in O-RAN](https://arxiv.org/abs/2611.19357v1)

- **Authors:** Xingqi Wu, Yuhui Wang, Junaid Farooq, Hakim Ghazzai, Gianluca Setti
- **Date:** 2026-11-14
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Ultra-reliable low-latency communication (URLLC) services in mission-critical applications such as industrial automation, remote healthcare, and autonomous systems demand stringent quality-of-service (QoS) guarantees under dynamic, resource-constrained wireless conditions. Open radio access networks (O-RAN) offer a...

### [StyleJudge: A Human-Validated, In-Context-Learning Vision-Language Evaluator for Artistic Style Transfer](https://arxiv.org/abs/2611.19475v1)

- **Authors:** Lokesh, Pramukto Mandal, Somanshu Juneja, Jashnoor Singh, Amit Kumar, Pranav Adlinge, et al.
- **Date:** 2026-11-14
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Automatic evaluation of artistic style transfer remains an open problem: existing metrics score an image pair in isolation, without seeing an example of the intended style transformation, and correlate poorly with human judgment. We introduce StyleJudge, a compact vision-language evaluator conditioned on a small set...

### [SWE-OPD: On-Policy Distillation for Agentic Coding](https://arxiv.org/abs/2611.21020v1)

- **Authors:** Yuhang He, Yanyu Chen, Chuanzhe Guo, Jie Zhu, Zichen Tian, Hongyu Ge, et al.
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** In this work, we study on-policy distillation (OPD) for transferring agentic coding capabilities from a large teacher model to a smaller student model. Prior work has focused primarily on reasoning and short-horizon agentic tasks. We present SWE-OPD, a minimal OPD study for software engineering, where the student in...

### [System 1 agents: a method for local, reliable and fast agentic AI](https://arxiv.org/abs/2611.21053v1)

- **Authors:** Eleftherios Tzanis, Michail E. Klontzas
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agentic artificial intelligence could automate analyses of sensitive clinical data, but current agents depend on large language models (LLMs). Cloud LLMs expose patient data. Local LLMs hallucinate, and an invented value in a tool call propagates through every later step. Here we present a method to build System 1 a...

### [The Anatomy of Inference in Agentic Systems — from memory buses to the agent loop, step by step](https://doi.org/10.5281/zenodo.24245958)

- **Authors:** Yuri Ostrozhnykh
- **Date:** 2026-11-13
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Local agent inference on consumer hardware is usually judged by tokens per second on a short prompt. This work measures the agent loop instead: a session of ~100 steps in which context grows monotonically and every step pays for both incremental prefill and generation. Four experiments (E1–E4) on two RTX 5060 Ti 16...

### [VISTA: A Framework for Vision-Informed Semantic Traffic Awareness](https://arxiv.org/abs/2611.20458v1)

- **Authors:** Murat Arda Onsu, Poonam Lohan, Burak Kantarci, Aisha Syed, Matthew Andrews, Sean Kennedy
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The Internet of Things (IoT) is transforming intelligent transportation systems by connecting roadside cameras, edge computing units, vehicles, and traffic infrastructure into a shared sensing and decision-making ecosystem. However, transmitting raw traffic video over vehicle-to-everything (V2X) links is bandwidth-i...

### [When the Bill Falls: Reusing the Old Index Defers,Never Avoids, Re-encoding in Complete Embedding-Model Migration](https://arxiv.org/abs/2611.20702v1)

- **Authors:** Nannan Zhao, Jiameng Zhang, Taoyu Zhong, Hao Wang, Bo Wang
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Upgrading the embedding model behind a vector index requires re-encoding the corpus. Recent work reuses the old index through adapters or window re-ranking. Across sixteen model pairs on passage and code corpora, plus eleven on Natural Questions (NQ), we find three results. First, reuse never avoids re-encoding: if...

### [MIGRO: A Decoupled and Portable Long-Term Memory System for Language Models](https://arxiv.org/abs/2611.15315)

- **Authors:** Mingxi Zou, Yinghui Xu, Jiaxiang Chen, Langzhang Liang, Wei Zhu, Peng Ye, et al.
- **Date:** 2026-11-11
- **Source:** openalex
- **Relevance:** maybe (44/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** long-term-memory, benchmark
- **Abstract summary:** Language models evolve, but the observations, revisions, and context accumulated through user interactions should remain usable. Each new model must be able to retrieve past evidence, track revisions, and add new observations. We present MIGRO, a decoupled long-term memory system that treats experience as a persiste...

### [Measuring AI agent memory returns: 30% repeat errors vs MTTR in SaaS support 2026](https://doi.org/10.5281/zenodo.24242274)

- **Authors:** Sofia Lindström
- **Date:** 2026-11-15
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** AI memory ROI requires paired gains: ≥20% fewer repeat errors and ≥10% faster MTTR on the same issue class. A standalone 30% drop isn't enough. Independent technical note mirroring the canonical version: https://bteanalytics.co/blog/measuring-ai-agent-memory-returns-30-repeat-errors-vs-mttr-in-saas-support-2026.php

### [MemDoctor: Stage-wise Error Attribution and Repair for MLLM Agent Memory](https://arxiv.org/abs/2611.21019v1)

- **Authors:** Ruiyang Jiang, Xinyang Liao, Weikai Huang, Yuqi Niu, Junjie Zhou, Yubin Zheng
- **Date:** 2026-11-16
- **Source:** arxiv
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Multimodal large language models (MLLMs) now assist users across sessions of images and text, carried by an external memory of what was said and shown. When such an assistant answers wrongly, the failure usually began earlier, in how a record was written, updated or retrieved, and the answer alone does not say where...

### [Read Boundaries in Agent Memory: Consistency, Completeness, and Repair](https://arxiv.org/abs/2611.19264v1)

- **Authors:** Haoting Qiu, Qibai Chen
- **Date:** 2026-11-14
- **Source:** arxiv
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Agent-memory services assemble evidence through several reads across connections or stores. An update between those reads can pair an assertion with source content from another revision. We protect the complete recall, including enrichment and materialization, and evaluate the resulting evidence and service behavior...
