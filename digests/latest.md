# Latest Paper Scout Digest

Latest daily digest: [2026-08-02](2026-08-02.md).

# Paper Scout Digest - 2026-08-02

## Run Summary

- **Run ID:** 72
- **Candidates fetched:** 895
- **New unique papers:** 812
- **Relevant:** 62
- **Maybe relevant:** 150
- **Irrelevant:** 683
- **Source summary:** arxiv: 481, openalex: 400, semantic_scholar: 14

## Highly Relevant

### [ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory](https://doi.org/10.48550/arxiv.2607.27773)

- **Authors:** Yongye Su, Wujiang Xu, Chaoji Zuo, Elisa Bertino
- **Date:** 2026-07-30
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Studies memory storage, retrieval, update, or consolidation for LLM agents.
- **Tags:** agent-memory, llm-agents, memory-systems, long-term-memory, memory-policy
- **Abstract summary:** LLM agents increasingly rely on long-term memory to support multi-session interaction and personalization. However, existing agent memory systems are designed around forward-only evolution, continuously accumulating, consolidating, and overwriting knowledge, with no principled mechanism to inspect, version, or rever...

### [MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory](https://doi.org/10.48550/arxiv.2607.27834)

- **Authors:** Hanshuai Cui, Zhiqing Tang, Zhi Yao, Fanshuai Meng, Qianli Ma, Weijia Jia
- **Date:** 2026-07-30
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, llm-agents, long-term-memory, benchmark, memory-systems
- **Abstract summary:** Persistent memory lets long-running large language model agents reuse information across sessions and tasks. Yet errors in writable memory can persist and corrupt future behavior. Existing systems improve storage and retrieval, but they do not provide a transaction boundary for reliable updates and recovery. We ther...

### [MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair](https://arxiv.org/abs/2607.27080)

- **Authors:** Xuanze Chen, Xukang Xie, Wentao Fu, Jiajun Zhou, Shanqing Yu, Qi Xuan
- **Date:** 2026-07-29
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, memory-systems, long-term-memory, memory-policy, evaluation, llm-agents
- **Abstract summary:** Memory systems allow agents to retain and reuse information from past interactions, but they can also let malicious content persist. A malicious instruction crafted by an attacker may be stored in long-term memory, recalled much later, and quietly shape a real action. Recent benchmarks increasingly examine agent mem...

### [Living-Harness Is an Interactive-Agent Evolver](https://arxiv.org/abs/2607.26598)

- **Authors:** Yuetian Du, Yucheng Wang, He Xu, Jiexu Xu, Shanwen Tan, Bing Zhao, et al.
- **Date:** 2026-07-29
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** llm-agents, memory-types, agent-memory, memory-systems
- **Abstract summary:** Large language model (LLM) agents may recover from a failure within an episode or after a retry, yet the same execution failure can recur in later tasks because post-episode feedback rarely revises the persistent harness that guides future interactions. Static harnesses improve reliability through fixed tools, conte...

### [Filesystem-Based Memory for LLM Agents: Organization, Evolution, and Sustainability](https://arxiv.org/abs/2607.26637)

- **Authors:** Sizhe Zhou, Shuying Yu, Hui Wei, Junda Wu, Siru Ouyang, Yizhu Jiao, et al.
- **Date:** 2026-07-29
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, llm-agents, long-term-memory, memory-systems
- **Abstract summary:** Deployed LLM agents increasingly keep their long-term memory as a filesystem: a directory tree of markdown files that the agent itself reads, writes, and reorganizes through generic file tools. Yet research has largely passed over this medium: prior systems design bespoke memory representations and study retrieval o...

### [$Σ$-Mem: An Online Reliability Memory for LLM-based Multi-Agent Systems](https://doi.org/10.48550/arxiv.2607.27958)

- **Authors:** Peilin Feng, Suorong Yang, Soujanya Poria
- **Date:** 2026-07-30
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** llm-agents, memory-systems, agent-memory
- **Abstract summary:** Memory is central to long-horizon LLM agents, yet existing memory systems primarily preserve interaction content rather than modeling which agents can be trusted and under what conditions. This limitation is particularly important in multi-agent systems, where a central model may be unable to directly verify plausib...

## Maybe Relevant

### [A Graph-Native Bitemporal Memory Store for Conversational AI Agents](https://arxiv.org/abs/2607.26520)

- **Authors:** Alp Niksarli, Gopesh Baheti
- **Date:** 2026-07-29
- **Source:** openalex
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Conversational AI agents commonly lack persistent memory across sessions. The obvious fixes like injecting full chat histories into the context window, or delegating to a third-party memory service, either exhaust the model's context budget or send personal data through infrastructure the user does not control. We d...

### [A Unified Framework for Human–AI Collaboration in Security Operations Centers with Trusted Autonomy](https://doi.org/10.1145/3837073)

- **Authors:** Ahmad Mohsin, Helge Janicke, Ahmed Ibrahim, Iqbal H. Sarker, Seyit Camtepe
- **Date:** 2026-07-30
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** This article presents a structured framework for Human-AI collaboration in Security Operations Centers (SOCs), integrating AI autonomy, trust calibration, and Human-in-the-Loop decision making. Existing frameworks in SOCs often focus narrowly on automation, lacking systematic structures to manage human oversight, tr...

### [Explainable Recognition of Complex Flight Maneuvers via Retrieval-Augmented Large Language Models](https://doi.org/10.3390/e28080850)

- **Authors:** Liqiang Ren, Haipeng Wang, Xinlong Pan, Tiantian Tang, Hongdong Wan
- **Date:** 2026-07-30
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Complex flight maneuver recognition (FMR) underpins intelligent flight training, including training assessment, pilot skill profiling, and flight safety monitoring. Existing FMR methods typically require large labeled datasets, generalize poorly across aircraft, and provide limited decision transparency. We propose...

### [Retrieval-Augmented Generation for Trustworthy Enterprise LLM Assistants](https://doi.org/10.63090/ijitrs/3139.3209.0033)

- **Authors:** B Bini
- **Date:** 2026-07-30
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language models (LLMs) have changed enterprise knowledge work. Their value, however, is capped by three failures: they hallucinate, their parametric memory is frozen and grows stale, and they cannot read the proprietary data that holds most business answers. Retrieval-Augmented Generation (RAG) targets all thr...

### [CoRenew: A large language model agent-based policy simulation platform for multifamily residential redevelopment](https://arxiv.org/abs/2607.25447)

- **Authors:** Yudi Zhang, Yuming Lin, Li Tian, Yu Wang, Jianghao Yu
- **Date:** 2026-07-28
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** The difficulty of collective action remains a central challenge in the design of policies for multifamily residential redevelopment. Stakeholders continually adjust their decisions in response to evolving negotiation contexts and the reactions of others, meaning that when a policy intervenes and which stakeholders i...

### [The Disruptive Impact of Large Language Models on Capture the Flag Competitions and the Path Toward Fair Play](https://arxiv.org/abs/2607.25425)

- **Authors:** Michael Macaulay, Harmony Bouabid, Guo Gen Ang, Sasha Shaw
- **Date:** 2026-07-28
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Capture the Flag (CTF) competitions are among cybersecurity's most effective training grounds, developing practical skill across cryptography, web exploitation, and binary exploitation. Large language models (LLMs) can now solve a growing share of challenges with minimal human input, raising urgent questions about f...

### [The Case Against Generation for Retrieval: Discriminative Language Models as Effective Retrievers](https://arxiv.org/abs/2607.25346)

- **Authors:** Zhe Xu, Prachi Agrawal, Kavosh Asadi, Tianyi Chen, Carl Hu, Justin Johnson, et al.
- **Date:** 2026-07-28
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large Language Models (LLMs) have emerged as powerful assets for recommender systems. However, deploying them as generative recommenders or zero-shot rankers at web-scale remains bottlenecked by prohibitive computational overhead and grounding challenges. In this paper, we revitalize the classic, highly efficient tw...

### [Hypothesis-Driven Shelf Generation for Personalised Recommendation](https://arxiv.org/abs/2607.25823)

- **Authors:** Aleksandr Petrov, Tarun Chillara, Matthew D. Moellman, Lucas van de Haas, Yabai Song, Alina Susoykina, et al.
- **Date:** 2026-07-28
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Modern recommendation interfaces organise content into shelves: themed rows such as "More of What You Like" or "New Releases for You." In production systems, these shelves are typically defined through hand-crafted templates coupled with dedicated retrieval logic. While effective for broad recommendation intents, th...

### [Domain-Prior-Regularized Graph Modeling for Anomaly Detection in Cyber-Physical Systems](https://arxiv.org/abs/2607.23197)

- **Authors:** Youngseok Hwang, Joonsung Kwon, Geonwoo Lee, Hyunwoo Park
- **Date:** 2026-07-25
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Anomaly detection on multivariate sensor time series is critical for industrial monitoring of cyber-physical systems (CPS), where even subtle deviations from normal behavior can indicate process disruption. Recent graph-based approaches have made significant progress, but they often struggle in small-scale physical...

### [RELIC: Revealed Principles for Learning Interpretable Composable Skills in Multi-Agent Planning](https://arxiv.org/abs/2607.16745v2)

- **Authors:** Nguyen Viet Tuan Kiet, Bui Dinh Pham, Duong Quoc Chinh, Dao Van Tung, Tran Cong Dao, Huynh Thi Thanh Binh
- **Date:** 2026-07-18
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Multi-agent planning becomes substantially harder when agents must improve specialized decision-making skills while keeping their executable implementations private. This setting arises when independently developed agents expose heterogeneous interfaces, observations, and capabilities, yet must coordinate under a sh...

### [Retrieval-Augmented Generation in LLMs for Mental Health: Quantifying the Incremental Contribution of Retrieval Within a Layered Safety Architecture](https://arxiv.org/abs/2607.24817v1)

- **Authors:** Anand Gupta, Akshat Surolia, Shubham Mishra, Shakil Imtiaz, Chaitali Sinha
- **Date:** 2026-07-17
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Digital mental health interventions (DMHIs) offer scalable support, but ensuring they accurately detect users' intent during volatile situations can be challenging. Pure parametric Large Language models (LLMs) do not contain specific safety critical architecture, and can miss critical cues, or hallucinate, undermini...

### [Masked Distillation: Internalizing the Chain-of-Thought in Language Models](https://arxiv.org/abs/2607.22629v1)

- **Authors:** Durgesh Kalwar, Vardhan Palod, Subbarao Kambhampati
- **Date:** 2026-06-18
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large Reasoning Models (LRMs) produce long, explicit chains of intermediate steps before generating a final answer at inference time. These intermediate traces dominate latency, memory usage, and serving cost, even though the final answer correctness is not causally related to the trace correctness and the trace len...

### [Masked Distillation: Internalizing the Chain-of-Thought in Language Models](https://arxiv.org/abs/2607.22629)

- **Authors:** Durgesh Kalwar, Vardhan Palod, Subbarao Kambhampati
- **Date:** 2026-06-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large Reasoning Models (LRMs) produce long, explicit chains of intermediate steps before generating a final answer at inference time. These intermediate traces dominate latency, memory usage, and serving cost, even though the final answer correctness is not causally related to the trace correctness and the trace len...

### [Masked Distillation: Internalizing the Chain-of-Thought in Language Models](https://doi.org/10.48550/arxiv.2607.22629)

- **Authors:** Durgesh Kalwar, Vardhan Palod, Subbarao Kambhampati
- **Date:** 2026-06-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large Reasoning Models (LRMs) produce long, explicit chains of intermediate steps before generating a final answer at inference time. These intermediate traces dominate latency, memory usage, and serving cost, even though the final answer correctness is not causally related to the trace correctness and the trace len...
