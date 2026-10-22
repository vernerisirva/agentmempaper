# Latest Paper Scout Digest

Latest daily digest: [2026-10-22](2026-10-22.md).

# Paper Scout Digest - 2026-10-22

## Run Summary

- **Run ID:** 160
- **Candidates fetched:** 1001
- **New unique papers:** 898
- **Relevant:** 106
- **Maybe relevant:** 130
- **Irrelevant:** 765
- **Source summary:** arxiv: 586, openalex: 400, semantic_scholar: 15

## Source Warnings

- arxiv: incomplete discovery window for 'agent memory'; single-page record limit reached.
- arxiv: incomplete discovery window for 'self-improving language models'; single-page record limit reached.
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

### [Memory Internalization via Test-Time Training for Long-Video Understanding](https://arxiv.org/abs/2610.26910v1)

- **Authors:** Haonan Zhao, Jiaxuan Chen, Qingyang Liu, Shuochen Chang, Siyu Sun, Jiangtong Li, et al.
- **Date:** 2026-10-17
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights.
- **Tags:** agent-memory, memory-systems, llm-agents, procedural-memory, parametric-memory, memory-distillation, self-improvement, language-model-memory, cross-episode-learning
- **Abstract summary:** Long-video understanding often requires answering many questions about a single video whose evidence is distributed across extended temporal contexts. Conventional video-language models repeatedly encode frames or retrieve visual evidence for every question. Parameterized video memory offers a write-once alternative...

### [PreCoMem: Predictive Cognitive Memory for Self-Evolving Long-Term Dialogue Agents](https://arxiv.org/abs/2610.29467v1)

- **Authors:** Jian Zhong, Zeyu Liu, Pingchuan Cao, Rongduo Han, Shunye Tang, Guohuan Xie, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Studies memory storage, retrieval, update, or consolidation for LLM agents.
- **Tags:** memory-policy, benchmark, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Long-horizon dialogue agents need to keep user memories stable enough for personalization while adapting when the user genuinely changes. Existing memory systems often append every observation or overwrite old entries by heuristic rules, which makes transient noise hard to distinguish from real belief drift. We intr...

### [Let Them Sleep: Recursive Self-Pruning Memory for Long-Horizon LLM Agents](https://doi.org/10.48550/arxiv.2610.25561)

- **Authors:** Kargi Chauhan, Sadiba Nusrat Nur, Pratibha Revankar, Kyle Montgomery, Chenguang Wang
- **Date:** 2026-10-18
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** agent-memory, llm-agents, benchmark, memory-systems
- **Abstract summary:** Agents that run for a long time have a memory problem, and it is not the one most systems optimize for. Storing every trace and retrieving the nearest neighbors works early and quietly stops working later: the store fills up with failures the agent then repeats, and with facts that were true fifty turns ago. RSPM (R...

### [MemoryTax: The Bitter Lesson of Agent Memory](https://arxiv.org/abs/2610.29823v1)

- **Authors:** Zedong Peng
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, benchmark, llm-agents
- **Abstract summary:** Agent memory systems such as Mem0 and Zep decide what to keep before any question arrives; coding agents keep the raw history and let the model search it with its own tools. We ask whether designed memory still helps once the model is strong enough to search for itself. On one LoCoMo conversation (419 turns, 152 que...

### [MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents](https://doi.org/10.48550/arxiv.2610.24955)

- **Authors:** Yiming Zong, Shiyuan Piao, Jiashuo Jiang, Fugee Tsung
- **Date:** 2026-10-18
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** llm-agents, benchmark, evaluation, agent-memory, memory-systems
- **Abstract summary:** Long-horizon LLM agents face a fundamental allocation problem as interaction histories grow: which information to retain, how much context to devote to it, and at what granularity. Existing memory mechanisms largely focus on relevance, retrieval, or compression, leaving this allocation trade-off implicit. We introdu...

### [Episodic Memory for AI Agents: A Persistent Experience Store](https://doi.org/10.5281/zenodo.23489659)

- **Authors:** CE-1 Research Programme
- **Date:** 2026-10-20
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** A persistent episodic memory system for AI agents. Stores experiences (what happened, when, in what context, what was decided, what was learned) not just facts. Uses ChromaDB + sentence-transformers for semantic retrieval. Includes MCP server for tool integration. 10 tests. Based on Tulving (1972, 1985) episodic mem...

### [MEMORA: A Memory-Enhanced Multimodal Committee Reranking Agent for Reasoning-Intensive Retrieval](https://doi.org/10.48550/arxiv.2610.25282)

- **Authors:** Mohamed Mahmoud, Mostafa Farouk Senussi, Mahmoud Abdalla, Mahmoud SalahEldin Kasem, Abdelrahman Abdallah, Hyun Soo Kang
- **Date:** 2026-10-18
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Reasoning-intensive retrieval is fundamentally challenged when queries demand deep semantic inference and arrive in multimodal form. Existing systems treat each query in isolation, rely on monolithic rerankers, and lack retrievers trained for cross-modal reasoning. We introduce MEMORA, a Memory-Enhanced Multimodal O...

### [Memory, Know Your PLACE: Governing Lifecycle State and Query-Time Eligibility in Persistent-Memory Agents](https://doi.org/10.48550/arxiv.2610.25179)

- **Authors:** Chen-Fang Hu, Hong-Han Shuai, Woan-Shiuan Chien
- **Date:** 2026-10-18
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, evaluation, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Persistent memory turns prior interactions into durable agent state, but existing systems provide limited control over whether that state remains valid and whether it should influence a later query. We argue that reliable memory requires governance over both state formation and query-time influence. We introduce PLA...

### [Memory-Centric Continual Learning for AI Agents](https://arxiv.org/abs/2610.29357v1)

- **Authors:** Dongfang Li, Zhuoen Chen, Bonian Jia, Zixuan Liu, Zhengxuan Lu, Can Deng, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Discusses Engram-style or parametric memory mechanisms for language models.
- **Tags:** agent-memory, memory-systems, parametric-memory, llm-agents
- **Abstract summary:** Autonomous agents powered by foundation models can reason, plan, and use tools, but their fixed weights and context limits hinder sustained learning from experience over long-term deployment. While external memory systems attempt to bridge this gap, they mostly act as passive retrieval caches, evaluated primarily by...

### [MOSAIC: An Omni-Modal Benchmark for Long-Term Memory and Cross-Modal Reasoning in Conversational Agents](https://arxiv.org/abs/2610.29249v1)

- **Authors:** Hong Ting Tsang, Boyi Zhang, Haoyu Huang, Jiaxin Bai, Yufei Li, Yisen Gao, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, evaluation, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Omni-modal assistants must remember not only what users say, but also what they show and convey. Existing long-term memory benchmarks are mostly text-and-image or report a single end-to-end score, so they cannot locate whether evidence is lost when it is represented, retrieved, delivered, or read. We introduce MOSAI...

### [Persistent Memory and Iterative Improvement in an LLM Agent for Chinese-Character Drawing](https://doi.org/10.48550/arxiv.2610.24090)

- **Authors:** Peilin Wu, Yi-Zhuang You
- **Date:** 2026-10-16
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, long-term-memory, agent-memory, memory-systems
- **Abstract summary:** Does persistent memory accumulated from previous attempts help an LLM agent solve new problems, and does memory design affect that benefit? We study programmatic Chinese-character drawing across five agent conditions attempting the same 668 items. Accumulated memory produces modest aggregate gains despite substantia...

### [ProactEgoMem: Benchmarking Proactive Memory in Streaming Egocentric Video](https://arxiv.org/abs/2610.30089v1)

- **Authors:** Ruotong Liao, Meikel Kokowski, Xiaoxiao Sun, Yongqin Xian, Laura Bravo Sánchez, Shiye Su, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory storage, retrieval, update, or consolidation for LLM agents.
- **Tags:** memory-policy, evaluation, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Today's multimodal assistants are typically prompted to interpret the visual evidence presented to them. To offload the cognitive burden of remembering across long horizons, wearable assistants should instead proactively acquire and maintain useful memory as the user's surroundings evolve. Doing so on the user's beh...

### [Procedural Memory for Language Agents: A Neurosymbolic Perspective on Explicit Goal Structure](https://doi.org/10.48550/arxiv.2610.25996)

- **Authors:** Jonathan Leung, Zhiqi Shen, Deheng Ye
- **Date:** 2026-10-19
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Large language models remain unreliable on long-horizon tasks requiring procedural reasoning. We argue that a key cause is the absence of explicit procedural memory: accessible, modifiable knowledge of how tasks are accomplished, distinct from semantic and episodic memory. Goal-Oriented Graphs offer such a represent...

### [Remembering Through Change: Provenance-Preserving Hypergraph Memory for Multimodal Agents](https://arxiv.org/abs/2610.29995v1)

- **Authors:** Jielong Tang, Ling-An Zeng, Xujie Yuan, Xiao Dong, Zhiqian Xia, Qingfeng Li, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Long-term memory for multimodal agents remains challenging, as it must preserve fine-grained visual evidence while tracking entity evolution across sessions. Existing abstraction-based memories compress images into text, often discarding visually discriminative details, whereas pixel-preserving memories retain raw o...

### [Temporal Evidence-Parameter Co-Alignment for LLM Reasoning over Temporal Knowledge Graphs](https://www.semanticscholar.org/paper/40365fb2fb2161e6bac5931c448e4bad3ae5971a)

- **Authors:** Jia-Pu Wang
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Discusses Engram-style or parametric memory mechanisms for language models.
- **Tags:** parametric-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Large Language Models (LLMs) often struggle with temporally grounded reasoning because their static parametric memory is misaligned with the dynamic evolution of real-world knowledge. Although RAG and Parameter-Efficient Fine-Tuning (PEFT) provide practical ways to enhance LLMs, they remain insufficient for temporal...

### [HABIT-Bench: Evaluating Habit Induction from Longitudinal Weak Evidence in Agent Memory](https://doi.org/10.48550/arxiv.2610.24520)

- **Authors:** Junming Zhang, Rubin Wei, Xu Cheng, Hao Sun, Ruoxi Cheng, Xiquan Wang, et al.
- **Date:** 2026-10-17
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies governed shared memory or persistent memory protocols for LLM agents.
- **Tags:** agent-memory, llm-agents, memory-systems, evaluation
- **Abstract summary:** In long-term interactions with large language model (LLM) agents, users reveal habits through their choices and actions. These habits capture implicit user information that agents must infer across conversations. However, individual observations may provide only partial evidence about a habit or when it applies. Ret...

### [MemBubble: Benchmarking How Agent Memory Shapes LLM Response Diversity](https://doi.org/10.48550/arxiv.2610.25127)

- **Authors:** Jiajun Tan, Fei Sun, Xinyu Ma, Zhang Yuxuan, Du Su, Qi Cao, et al.
- **Date:** 2026-10-18
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, evaluation, llm-agents
- **Abstract summary:** Memory serves as the core component of LLM-based agents, enabling personalized responses via extracting and using user preferences from past interactions. However, its use may reduce response diversity, thereby narrowing the range of information available to users. Existing evaluations rely largely on synthetic inte...

### [PACE-Mem: Prefix-Aware Complementary Evidence for Multimodal Agents](https://doi.org/10.48550/arxiv.2610.24378)

- **Authors:** Shidu Ren, Rong-cheng Tu, Hang Zhou, Xiao Luo
- **Date:** 2026-10-17
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, llm-agents
- **Abstract summary:** As multimodal agents accumulate experience, their long-term memories contain many similar observations of recurring scenes, actions, and entities. Answer quality depends on the evidence retrieved from these memories into the model's context. However, query-relevant memories may contain overlapping information, and a...

## Maybe Relevant

### [The Geometry of Agent Memory: Forecasting Retrieval-Bound Memory Failures, and Characterizing Its Limits](https://doi.org/10.48550/arxiv.2610.26433)

- **Authors:** Iliya Zhechev, Radoslav Ralev, Chris Coleman, Srijith Rajamohan, Jen Agarwal, Tyler Hutcherson, et al.
- **Date:** 2026-10-19
- **Source:** openalex
- **Relevance:** maybe (69/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, benchmark, evaluation
- **Abstract summary:** We study whether geometric relationships between conversation turns, memory texts, and queries can predict answer correctness before generation. We evaluate four memory implementations with dense or hybrid retrieval and one observation-summary comparator. We embed these texts in a shared space. A logistic classifier...

### [Uni-Mem: Learning a Long-Horizon Agentic Memory Manager with Unified Online Policy Optimization](https://arxiv.org/abs/2610.29671v1)

- **Authors:** Zhiqian Xia, Jielong Tang, Ling-An Zeng, Shixiong Kai, Rong Yao, Hao Kong, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (69/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, benchmark
- **Abstract summary:** Long-term agent memory is shifting from predefined workflows toward learnable policies for memory construction and retrieval. Existing learning-based methods either optimize construction alone or combine retrieval-side online reinforcement learning (RL) with offline construction supervision, limiting co-adaptation b...

### [PerMIT: Securing Persistent Memory for LLM Agents via Machine-Checked Integrity Theorems and Scalable Community Trust](https://arxiv.org/abs/2610.28987v1)

- **Authors:** Tanqiu Jiang, Min Bai, Sadat Shahriar, Wanyu Du, Sandesh Swamy
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Persistent memory is a largely undefended surface for injection and poisoning, and the same risk limits memory sharing among agents. We present PerMIT, a memory architecture with provable integrity guarantees under an explicit trust assumption: only user-typed inputs and values confirmed at a gate are trusted. PerMI...

### [5uGUE: Agentic Hardware-in-the-Loop Fuzzing for 5G Devices and beyond](https://arxiv.org/abs/2610.29155v1)

- **Authors:** Guoqiang Hua, Sakshi Udeshi, Matheus Eduardo Garbelini, Daisuke Mashima, Sudipta Chattopadhyay
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** In this paper, we present 5uGUE, a large language model (LLM)-driven hardware-in-the-loop agent, which enables the wireless fuzzing of 5G-enabled devices (such as mobile phones). 5uGUE combines multi-step reasoning with tool-assisted interaction and integrates into the fuzzing pipeline by leveraging specialized tool...

### [AgentMonopoly: Behavioral Patterns and Persona Control in LLM Agents](https://arxiv.org/abs/2610.29330v1)

- **Authors:** Changshun Wu, Mengyu Li, Mathis Marsault, Xiaowei Huang, Chih-Hong Cheng
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** How do LLM agents' strategies differ, and how much can instructions to adopt a persona change their behavior over a game? We study these questions with AgentMonopoly, an environment where agents communicate, buy and trade properties, and make decisions that affect later turns. We compare models from four families, e...

### [Asymmetric On-Policy Distillation Learns In-Context Exploration](https://arxiv.org/abs/2610.30105v1)

- **Authors:** Sriyash Poddar, Yanda Bao, Jacob Krantz, Matthew Chang, Xavier Puig, Roozbeh Mottaghi, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Sequential decision-making under partial observability is difficult because agents must explore to infer hidden, task-relevant information before acting effectively. Learning such information-gathering behaviors tabula rasa via online reinforcement learning is sample-inefficient, whereas offline imitation averages e...

### [Benchmarking and Error Analysis of Deep Search and Deep Research LLM Agents](https://arxiv.org/abs/2610.29346v1)

- **Authors:** Zixuan Yu, Zhenheng Tang, Xiaowen Chu, Bo Han
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** As Large Language Models (LLMs) evolve into autonomous Deep Search and Deep Research Agents capable of executing long-horizon, multi-step tasks, evaluating their reliability becomes increasingly critical. However, existing evaluation paradigms predominantly focus on final task outcomes, leaving a significant gap in...

### [Beyond Binary Labels: Diagnostic Evaluation of LLM Safety with Prompt-Level Rubrics](https://arxiv.org/abs/2610.29225v1)

- **Authors:** Hongyu Li, Xinlong Huang, Zhan Yu, Jing Zhao, Zhe Zhao, Juntao Zhong, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Current LLM safety benchmarks predominantly rely on binary safe or unsafe labels, lacking explanatory depth and suffering from low consistency across automated judges. To address this, we introduce DiagSafe, a diagnostic evaluation framework that moves beyond binary classification by employing prompt-level rubrics....

### [Beyond Small Talk: Modeling Disclosure Trajectories in Human-AI Conversation](https://arxiv.org/abs/2610.29413v1)

- **Authors:** Keith Kwok, Wanting Ning, Tej Deep Pala, Desmond C. Ong, S. Supraja, Renwen Zhang, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Recently, we see a rise in conversational agents as a form of social and emotional support, where disclosure will unfold over time. Yet, current evaluations of these agents typically examine isolated conversational states. In analyses of naturally occurring conversations, disclosure history and current disclosure ar...

### [BIRD-RL: Scaling Agentic Reinforcement Learning over Stateful Data-Centric Environments](https://arxiv.org/abs/2610.29426v1)

- **Authors:** Ge Qu, Jinyang Li, Xiaohan Xu, Xiaolong Li, Bowen Qin, Nan Huo, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** While agentic reinforcement learning (RL) has emerged as a promising paradigm for training small language models (SLMs), existing frameworks are predominantly tool-centric and struggle with data-centric environments. Specifically, applying tool-centric frameworks to stateful tasks like SQL debugging introduces sever...

### [Cache Engineering for Agents](https://arxiv.org/abs/2610.28577v1)

- **Authors:** Tianyu Fu, Ruoxi Wang, Zihan Min, Zhongqi Ren, Zhihao Li, Tengxuan Liu, et al.
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Large Language Model (LLM) agents can handle increasingly complex tasks, navigating long trajectories of observations and actions. As these trajectories grow, key-value (KV) cache I/O and storage become the dominant cost. Trajectories can also exceed the LLM's maximum context length, requiring control over active ca...

### [Do Conversational Agents Need Explicit Memory? A Controlled Comparison with Raw-History Retrieval](https://doi.org/10.48550/arxiv.2610.24671)

- **Authors:** Yongjie Zhou, Shuai Wang, Bevan Koopman, Guido Zuccon
- **Date:** 2026-10-17
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Explicit memory systems transform conversation history into persistent representations intended to improve future access, often at substantial construction cost. Yet it remains unclear whether this added complexity yields better answer accuracy than retrieving directly from raw history. This study compares six state...

### [FaultGene: LLM-Assisted Fault-Augmented Test Generation for Hardware-in-the-Loop Validation of Autonomous Driving Systems](https://arxiv.org/abs/2610.29969v1)

- **Authors:** Chaoran Yuan, Fadi Kurdahi
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Reliable validation of autonomous driving cyber-physical systems requires testing not only nominal driving behavior but also failures arising from faults in sensing and embedded computation. Physical road testing provides realistic system behavior but is costly and difficult to reproduce, while simulation enables sc...

### [LLM-Based Exogenous World Modeling for Dynamic Scheduling](https://arxiv.org/abs/2610.29308v1)

- **Authors:** Ni Zhang, Haofeng Yuan, Jianan Zhou, Shiji Song, Zhiguang Cao
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Dynamic scheduling requires dispatching online arrivals while anticipating future jobs, as poor decisions can compound downstream costs under nonlinear tardiness objectives. We show that a pretrained large language model (LLM) can serve as the exogenous component of a structured world model, forecasting uncertain fu...

### [Multi-Agent AI Design of a Nanowatt Biomedical Low-Pass Filter from Topology to Layout](https://arxiv.org/abs/2610.28677v1)

- **Authors:** Danial Noori Zadeh, Devanshu Prasad, Mohamed B. Elamien
- **Date:** 2026-10-19
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We demonstrate a multi-agent framework that takes an analog circuit from topology synthesis to layout. A researcher agent directs schematic and layout agents, a four-tier memory stores the specification and lessons, and separate agents review the designs. Deterministic tools provide pass/fail simulation reports, sym...

### [Multi-agent LLMs on the Cloud-Edge-IoT Continuum: A Systematic Mapping Study on Architectures, Deployment, and Evaluation](https://arxiv.org/abs/2610.28702v1)

- **Authors:** Mahyar Tourchi Moghaddam, Tiziano Santilli, Leo Wilhelm Lierse, Sebastian Werner, Francesco Daghero
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** LLM applications are increasingly built as systems of cooperating components rather than as single prompt-response pipelines. IoT applications add constraints of their own, because sensing, reasoning, control, and actuation are spread across devices, edge nodes, and cloud services to meet latency, privacy, and bandw...

### [OmniSimulator: Aligning Small Language Models for Authentic Heterogeneous Behavior Modeling](https://arxiv.org/abs/2610.29472v1)

- **Authors:** Jiawei Chen, Ruoxi Xu, Boxi Cao, Zhuoqun Li, Ruotong Pan, Yunfei Zhang, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language models (LLMs) have shown great potential as general-purpose user simulators for interactive systems. Prior studies have demonstrated that training on high-quality data can substantially improve model reasoning and downstream task performance. However, the upper bound of user simulation is still constr...

### [Parallel AI Agent Collaboration as Graph-Structured Distributed Block Optimization](https://arxiv.org/abs/2610.30074v1)

- **Authors:** Hanmin Li, Yury Demidovich, Peter Richtárik
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Parallel AI agents can produce useful local edits yet degrade a shared solution when their edits are combined. We model this coordination problem as discrete block optimization with an exactly evaluable objective and a known dependency graph. Independent sets certify compatible edits whose verified gains, measured a...

### [RegoMender: A Multi-agent Framework for Automated Rego Policy Repair](https://arxiv.org/abs/2610.29456v1)

- **Authors:** Ruijie Zhang, Huaxiao Yin, Li Hu, Fanqi Kong, Haozhe Liang, Shaoyin Cheng, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Policy-as-Code (PaC) has emerged as a foundational paradigm in cloud-native systems. However, repairing Rego policies remains challenging due to their strict syntax, declarative semantics, and specific verification requirements. Existing automated program repair (APR) methods are mainly designed for mainstream langu...

### [StochIKM: Automated High-Fidelity Reconstruction of Individual Patient Data from Published Kaplan-Meier Curves](https://arxiv.org/abs/2610.29122v1)

- **Authors:** Liangze Ke, Daniel Zelterman, Wei Wei, Guannan Gong
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Individual patient data are the gold standard for secondary analysis of time-to-event evidence, but they are rarely released, and reconstruction from a published Kaplan-Meier figure could help. Existing methods all claim high fidelity, each judged by whichever agreements it happens to achieve, and each returns a sin...

### [SWE-DIVE: Multi-Turn Coding Agent Evaluation with Dynamic User Simulation](https://arxiv.org/abs/2610.30047v1)

- **Authors:** Lorenz Brehme, Benjamin Steenhoek, Ruth Breu
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Coding agents are typically evaluated using one-shot, well-formulated prompts. Benchmarks such as SWE-bench use existing GitHub issues as input for a coding agent and evaluate whether the agent successfully solves the task. However, in real-world use cases, prompts are often not as well-formulated or structured as e...

### [The Butterfly Effect in LLM Social Simulations: From Architecture Sensitivity to Robustness Audits](https://arxiv.org/abs/2610.28981v1)

- **Authors:** Jinyi Ye, Lei Cao, Ding Chen, Emilio Ferrara
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** A butterfly effect occurs when a local perturbation propagates through a system and produces divergence in its collective outcome. In LLM social simulations, this creates a particular challenge for scientific inference: sensitivity to implementation choices can enter agent interactions and alter the collective outco...

### [The End of Consensus Research?](https://arxiv.org/abs/2610.30114v1)

- **Authors:** Clément Burgelin, Rachid Guerraoui, Zicong Hong, Yinan Hu, Anne-Marie Kermarrec, Rafael Pires, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Consensus is a fundamental problem in distributed computing and at the core of state machine replication (SMR). Despite decades of active human research, discovering practical low-latency solutions to the problem is still open, as it requires combining protocol knowledge, correctness reasoning, implementation, and e...

### [TrainBridge: Agentic NPU Training Optimization Guided by GPU Compilation Evidence](https://arxiv.org/abs/2610.29171v1)

- **Authors:** Yupeng Chen, Kunxiang Zhao, Xingjian Wang, Yue Zhao, Yijing Wu, Ye Liu, et al.
- **Date:** 2026-10-21
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We study how to improve training efficiency on Ascend NPUs. In the NPU training programs we study, framework-level compilation optimizations such as operator fusion are only partially applied, leaving fragmented computation and avoidable execution overheads. Profiling-guided tuning can address these inefficiencies,...

### [MemDerive: A Diagnostic Benchmark for Agent Memory over Evolving Data](https://doi.org/10.48550/arxiv.2610.25373)

- **Authors:** Sen Gao, Yongan Li, Han Chen, Bingsheng He, Ming Wu, Jason Zeng, et al.
- **Date:** 2026-10-18
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, evaluation
- **Abstract summary:** Long-running agents rely on memory of their past interactions for task state, such as what has been completed and which conditions still hold. Such state is usually a derived state. No record states it, and it must be computed by rules from multiple records of an evolving history. Existing memory benchmarks score on...

### [Memory as Belief: Bayesian Evolution of Memory for Self-Evolving LLM Agents](https://doi.org/10.48550/arxiv.2610.25119)

- **Authors:** Yiming Xu, Qian Yang, Zihan Chen, Yuefei Wu, Wenhan Zeng, Bin Shi, et al.
- **Date:** 2026-10-18
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, llm-agents, evaluation
- **Abstract summary:** Large language model (LLM) agents increasingly rely on external memory to accumulate past experiences for continual adaptation. However, effectively reusing memory requires accurately assessing its value, as retrieved experiences may become unreliable when transferred across task contexts. Despite its importance, me...

### [MoobFS: experimental Linux filesystem layer for LLM-agent memory — source snapshot 02381fba](https://doi.org/10.5281/zenodo.23514719)

- **Authors:** Studio Moob
- **Date:** 2026-10-20
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** ENGLISH MoobFS is an experimental native Linux kernel module for file-based LLM-agent memory, developed with AI coding assistance and human direction, review and testing. It stacks over ext4, btrfs or XFS and provides typed extended attributes, an in-memory metadata index and directory-scoped query ioctls. Ranking,...
