# Latest Paper Scout Digest

Latest daily digest: [2026-11-11](2026-11-11.md).

# Paper Scout Digest - 2026-11-11

## Run Summary

- **Run ID:** 177
- **Candidates fetched:** 958
- **New unique papers:** 850
- **Relevant:** 86
- **Maybe relevant:** 159
- **Irrelevant:** 713
- **Source summary:** arxiv: 545, openalex: 400, semantic_scholar: 13

## Source Warnings

- arxiv: incomplete discovery window for 'agent memory'; single-page record limit reached.
- arxiv: incomplete discovery window for 'cs.AI,cs.CL,cs.LG'; single-page record limit reached.
- openalex: incomplete discovery window for 'agent memory'; single-page record limit reached.
- openalex: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'memory distillation language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'parametric memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'agent memory'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- semantic_scholar failed for 'memory distillation': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar: incomplete discovery window for 'parametric memory LLM'; single-page record limit reached.

## Highly Relevant

### [On Agentic Manipulation Policies](https://doi.org/10.48550/arxiv.2611.09892)

- **Authors:** Chen Chen, Omid Bagherieh, Naveen Nikamanth Appiah Balaji, Jesse T. Gonzalez, Negin Heravi, Fahad Islam, et al.
- **Date:** 2026-11-06
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, memory-policy, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Recent work on robot manipulation has focused on specialist policies trained on demonstrations. We show that generalist AI models can control manipulators more reliably than specialist policies such as vision-language-action models (VLAs) and world-action models (WAMs). We systematically analyze agentic manipulation...

### [CogniLife: Continuous Cognitive Distillation for Deployed Multi-Expert Agent Marketplaces](https://arxiv.org/abs/2611.04483)

- **Authors:** Xuwei Tan, Jingchun Huang, Ming Cai, Shuang Lyu, Tiange Wang, Yinzhi Wang, et al.
- **Date:** 2026-11-03
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** benchmark, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Multi-expert agent marketplaces -- where creators publish domain-specific AI experts for end users to consult -- are an emerging deployment pattern for language technology. A published expert can receive many requests yet little evidence about its creator, who remains active elsewhere: the cold-expert problem. We fr...

### [MemoryDojo: Benchmarking Poisoning Through LLM Agent Memory](https://doi.org/10.48550/arxiv.2611.09721)

- **Authors:** David Yang, Blake Bullwinkel, Amanda Minnich, Mojtaba Amiri, Giorgio Severi
- **Date:** 2026-11-06
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** agent-memory, llm-agents, memory-systems, benchmark, evaluation
- **Abstract summary:** LLM agents benefit from using memory systems to improve performance on long-horizon, multi-session tasks. However, memory introduces a critical attack surface. Malicious instructions encountered in one session may be stored and propagated through memory before being retrieved and acted upon in later sessions. Becaus...

### [Building Production-Ready AI Agents with Scalable Long-Term Memory](https://doi.org/10.13140/rg.2.2.36579.72485)

- **Authors:** Ijaz Durrani
- **Date:** 2026-11-09
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** No abstract available.

### [Coding Agent Memory Post-Training II: Unlocking the Memory Potential of Pre-trained File Operations for Long-Horizon Tasks via On-Policy Distillation](https://arxiv.org/abs/2611.14009v1)

- **Authors:** Lirui Luo, Kelong Mao, Xinwei Yang, Rongqing Li, Luyu Chen, Kieran Wong, et al.
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies governed shared memory or persistent memory protocols for LLM agents.
- **Tags:** agent-memory, deep-research, memory-systems, llm-agents
- **Abstract summary:** Language-model agents increasingly tackle long-horizon tasks whose interaction histories exceed the model's active context. They must therefore decide what to write down and what to read back, and when to do either. Recent work has begun to use on-policy distillation (OPD) to make memory control part of the policy,...

### [Placing LLM Lookup Tables by Per-Layer Prefetch Deadlines](https://arxiv.org/abs/2611.13413v1)

- **Authors:** Wen Huang, Jack Liu
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Discusses Engram-style or parametric memory mechanisms for language models.
- **Tags:** parametric-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** DeepSeek-V4.1's 203 GB of Engram n-gram tables sit in host DRAM today, taking 190 of the 223 GiB a 4-GPU serving process uses. Row indices depend only on input tokens, so reads can start with each step and overlap earlier layers. V4.1's two Engram layers have windows that differ by 30x (0.3 vs. 9.3 ms). We show that...

### [Trojan Hippo Bench: A Dynamic Benchmark for Persistent Memory Attacks and Defenses in LLM Agents](https://doi.org/10.1145/3847352.3848090)

- **Authors:** Debeshee Das, Julien Piet, Darya Kaviani, Luca Beurer-Kellner, Florian Tramèr, David Wagner
- **Date:** 2026-11-09
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, llm-agents, memory-systems, long-term-memory, evaluation
- **Abstract summary:** Memory systems enable otherwise-stateless LLM agents to persist user information across sessions, but also introduce a new attack surface. The Trojan Hippo attack is a class of persistent memory attacks that operates under a more realistic threat model than prior memory poisoning work. The attacker plants a dormant...

### [When Should Agents Remember? Falsification-Gated Self-Evolution for LLM Agents](https://arxiv.org/abs/2611.14326v1)

- **Authors:** Runxuan Tang, Haoyu Gao, Yuyan Ding, Junyi Yao, Zihao Zheng, Zecheng Sheng, et al.
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, long-term-memory, agent-memory, memory-systems
- **Abstract summary:** LLM agents increasingly operate in long-horizon, verifier-rich environments, but current self-improvement mechanisms often write episode-derived lessons directly into memory, making local success an unreliable signal for reusable and safe knowledge. This paper addresses the core question of when an experience-derive...

### [Decision Context: Persistent Behavioral Learning for AI Agents](https://doi.org/10.48550/arxiv.2611.08644)

- **Authors:** Nima Vahdat, Pashootan Vaezipoor
- **Date:** 2026-11-05
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies governed shared memory or persistent memory protocols for LLM agents.
- **Tags:** agent-memory, llm-agents, memory-systems
- **Abstract summary:** LLM agents do not learn from corrections across sessions. A user fixes the same mistake at the start of every conversation. Existing agent memory systems primarily handle facts, such as preferences, entities, and conversational history, rather than procedural knowledge. We present Forge Decision Context (forge_dc),...

### [What an LLM-built knowledge graph keeps, and what a repair pass against its sources changes](https://doi.org/10.5281/zenodo.24046281)

- **Authors:** Luiz Antonio Busnello
- **Date:** 2026-11-07
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** agent-memory, memory-systems, llm-agents
- **Abstract summary:** A data note on one deployment of an agent memory system whose knowledge graph was extracted from its corpus by a language model, each relation citing the chunk of text it came from. Two studies, each under its own public pre-registration, ran on the same frozen uniform sample of 300 relations. The first asks how oft...

### [BioMem: Agentic Memory for Biomedical LLM Agents](https://arxiv.org/abs/2611.13426v1)

- **Authors:** Mingchen Li, Yongkang Xiao, Rumeng Li, Rui Zhang, Hong Yu
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** relevant (79/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** agent-memory, llm-agents, memory-policy, evaluation, memory-augmented
- **Abstract summary:** Large language models (LLMs) have demonstrated considerable potential in biomedical applications, while agentic memory systems have emerged as a promising approach to preserving and utilizing information across tasks and interactions. However, a fundamental question remains: how effectively and reliably do these sys...

## Maybe Relevant

### [Agent-Guided Discovery of Exchange-Correlation Functionals with Physics-based Validation](https://arxiv.org/abs/2611.13329v1)

- **Authors:** Achuth Chandrasekhar, Amir Barati Farimani
- **Date:** 2026-11-09
- **Source:** arxiv
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents, evaluation
- **Abstract summary:** Accurate, compact exchange--correlation functionals are central to predictive density functional theory. Symbolic search and language-model agents can propose new functional forms, but it remains unclear whether their gains survive self-consistency and external evaluation, whether the new terms carry physical conten...

### [On Private Knowledge Retrieval and Private Inference for secure multi-agent systems](https://arxiv.org/abs/2611.13696v1)

- **Authors:** Vicenç Torra, Maria Bras-Amorós
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Multi-agent systems provide a convenient framework for the massive deployment of agents based on Large Language Models (LLMs). It provides a sound framework where agents can interact with existing software to perform actions in an autonomous way. Agentic AI is the new term to denote these AI-based autonomous systems...

### [A computational framework for understanding embodied plans](https://arxiv.org/abs/2611.13669v1)

- **Authors:** Aalap D. Shah, Basil Saeed, Joshua B. Tenenbaum, Tobias Gerstenberg, Hyowon Gweon, Ilker Yildirim
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Reasoning about people's plans and goals based on their actions is fundamental to human social interaction and essential for cooperative, embodied artificial intelligence. Formalizing this capacity in naturalistic, embodied settings has been a longstanding challenge. Here, we present GenEA, a novel agent representat...

### [Agentic AI Meets Formal Verification in the Era of Agentic Hardware Development](https://arxiv.org/abs/2611.13705v1)

- **Authors:** Wenji Fang, Yuchao Wu, Jing Wang, Zhiyao Xie
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** As AI agents become increasingly capable of generating and optimizing hardware circuits, ensuring the correctness of AI-generated designs becomes more important. Meanwhile, advances in AI lower the barriers to developing and applying formal methods, creating new opportunities to automate and improve hardware verific...

### [AI Safety for AI Agents in Europe Part IV : Two Independent Checks and Endpoint-Side Reconstruction to Prevent Tool Misuse, Memory Poisoning, Unauthorized Delegation and Unlawful Data Use — Supporting EU AI Act Record-Keeping, Human Oversight and Cybersecurity, GDPR Purpose Limitation and DORA](https://doi.org/10.5281/zenodo.24078177)

- **Authors:** Sangam Das
- **Date:** 2026-11-09
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Abstract In most AI-agent and automation stacks, one component decides and a downstream component simply trusts that decision. A policy engine, gateway, classifier, trusted execution environment or approval step says yes. The tool, MCP server, database, cloud API or payment rail then carries out whatever request arr...

### [AutoCompress: Automated Hardware-Guided Model Compression](https://arxiv.org/abs/2611.08290)

- **Authors:** Sheldon Liang, Ali Taghibakhshi, Saurav Muralidharan, Sharath Turuvekere Sreenivas, Ashwath Aithal, Pavlo A. Molchanov, et al.
- **Date:** 2026-11-05
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** LLM pruning must preserve quality while meeting hardware- and workload-specific constraints on latency, throughput, and memory. Existing pruning workflows often target parameter counts, requiring practitioners to manually select model sizes that meet latency, throughput, and GPU memory limits. However, parameter cou...

### [AutoManifold: Agentic Design of Data Visualisation Algorithms via Manifold Embedding](https://arxiv.org/abs/2611.13710v1)

- **Authors:** Burak Susam, Ruiyuan Kang, Tingting Mu
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Manifold embedding for data visualisation is dominated by a small set of hand-designed state-of-the-art (SOTA) algorithms. Their design targets are fixed at development time, resulting in inflexible algorithmic behaviour that cannot be readily steered towards user-specified structural priorities. Hand-designing new...

### [Bursts That Outlast Themselves: Persistent Degradation in Prefix-Cached Agent Serving](https://arxiv.org/abs/2611.13412v1)

- **Authors:** Wen Huang, Jack Liu
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** LLM agents drive inference engines with closed-loop sessions whose context grows every turn, and serving them economically depends on prefix caching: a hit costs an incremental prefill of about a thousand tokens, a miss recomputes a 10--40K-token context. We show that this makes prefix-cached agent serving metastabl...

### [Chain of Physics: Supporting Fault Diagnosis with Engineering-Inspired Large Language Model Reasoning](https://arxiv.org/abs/2611.14263v1)

- **Authors:** Wenqi Zhou, Leonardo Baldo, Kai Goebel, Manuel Arias Chao
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Fault diagnosis in complex systems requires linking observed changes in physical quantities to the failure mechanisms that produce them. Experienced engineers perform this task by combining sensor information with knowledge of system behavior and fault propagation. Large Language Models (LLMs) can support this proce...

### [Continual-ARC: Measuring Skill Acquisition over a Working Lifetime](https://arxiv.org/abs/2611.14505v1)

- **Authors:** Daniel Lenton
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agent harnesses have emerged as a promising mechanism for continual learning, alongside test-time parametric learning. However, the current benchmarks have several limitations: they generally focus on a single applied domain, serve each instance only once, and assume a single family of learner, so memory-based and w...

### [Data Quality Challenges in Multimodal Tourism Recommender Systems](https://arxiv.org/abs/2611.13972v1)

- **Authors:** Zehui Wang, Wolfram Höpken, Dietmar Jannach
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Modern recommender systems increasingly consider diverse data modalities to enhance model performance. However, the quality of the underlying multimodal data (e.g. data from social media platforms) has received limited attention so far. Focusing on tourism recommendation, we examine real-world challenges encountered...

### [DisasterAgent: An Evidence-Driven Agent for Verifiable Disaster Report Generation From Remote Sensing Imagery](https://arxiv.org/abs/2611.13776v1)

- **Authors:** Zhijian Li, Jiawei Song, Chao Ren, Yidan Zhang, Peijin Wang, Xian Sun, et al.
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Remote sensing disaster assessment is moving from simple damage classification toward comprehensive report-level analysis. In this setting, responders need not only damage descriptions but also verifiable evidence to guide response and recovery. Recent vision-language models (VLMs) and tool-augmented agents offer st...

### [Discrete Model-Based Diffusion for Combinatorial Optimization in Multi-Robot Task Allocation](https://arxiv.org/abs/2611.13382v1)

- **Authors:** Haejoon Lee, Thomas Marshall Vielmetti, Xinyi Wang, Dimitra Panagou
- **Date:** 2026-11-09
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Decision making in multi-agent and multi-robot systems often involves discrete decision variables, leading to NP-hard combinatorial optimization problems that must be solved within seconds for near real-time implementation. Denoising diffusion has emerged as a powerful tool for such problems, but existing approaches...

### [Efficient control of multi-agent robust MDPs through tensor trees](https://arxiv.org/abs/2611.13672v1)

- **Authors:** Ruohan Wang, Giannis Delimpaltadakis, Luca Laurenti, Sofie Haesaert
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** This paper introduces a tensor-based framework for controller synthesis of stochastic multi-agent systems under temporal logic specifications that couple the agents, such as one agent reaching its goal only after another agent has reached its own. The agents are modeled as robust Markov decision processes (RMDPs), w...

### [EJAI: Judgment-Preserving Civic AI for Data Center Environmental Justice](https://arxiv.org/abs/2611.13525v1)

- **Authors:** Evan Pačes-Wiles, Bryen Alvarez, Sara Gulabani, Akshara Kolipaka, Snehalkumar 'Neil' S. Gaikwad
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Communities in the United States and around the world are contesting data centers, the physical infrastructure of AI. These disputes pose environmental justice issues: residents must weigh unevenly distributed burdens using evidence scattered across metrics, corporate claims, policy documents, and public testimony....

### [ForeSpark: Joint Draft and Verification Budget Scheduling for Parallel Speculative Decoding](https://arxiv.org/abs/2611.13442v1)

- **Authors:** Jaeyong Song, Daniel Wang, Pratyush Patel, Jonny Kong, Preyas Shah, Shobhit Kanaujia
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Parallel drafters accelerate LLM decoding by proposing a whole block of draft tokens in a single forward pass, making them attractive for LLM serving. Recent systems optimize goodput (i.e., accepted tokens per second) because rejected drafts steal compute from other requests. However, these systems control only how...

### [Framing-Induced Vulnerability in Large Language Models: Evidence from Chinese News Headlines](https://arxiv.org/abs/2611.13531v1)

- **Authors:** Mo Zhou, Yiwei Zhang
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language models increasingly evaluate, route, and moderate news, so a model's judgment of a headline has become a gatekeeping decision. We ask whether that judgment follows the fact being reported or the way the fact is framed. We combine an ecological audit of 63,926 Chinese news headlines with a controlled e...

### [From Counterfactual Edits to Human Narratives: LLM-Driven Interpretations for Recommender System Explanations](https://arxiv.org/abs/2611.13914v1)

- **Authors:** Vojtech Cahlik, Amir Reza Mohammadi, Rodrigo Alves, Pavel Kordik, Eva Zangerle
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Recommender systems increasingly influence what users discover and consume online, yet the decision logic behind their outputs often remains opaque. Counterfactual explanation (CFX) methods provide an effective way to show which changes to a user's interaction history would alter a recommendation. In recommendation...

### [Large language model agents in watershed environmental response: a hypothesis-and-theory framework for the cognitive orchestration layer](https://doi.org/10.3389/fenvs.2026.1974405)

- **Authors:** Yibo Chen, Xiao Ma, Haopeng Zhai
- **Date:** 2026-11-09
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Introduction Watershed environmental governance increasingly combines dense sensing infrastructure with institutions whose attention, authority, and coordination capacity remain limited. We develop the cognitive orchestration layer as a theory-building concept for examining how large language model (LLM)-based agent...

### [Lilo: A Multi-Agent Conversational Sandbox for Children's Digital Communication](https://arxiv.org/abs/2611.14260v1)

- **Authors:** Ofri Elbaum, Amit Malik, Tomer Malkevich, Zohar Elyoseph, Adir Solomon, Rotem Dror, et al.
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Children's peer conflicts increasingly play out in group chats, where tone and timing are stripped away, and a hurtful message is easier to send than to say aloud. We present Lilo, a multi-agent conversational system that lets children practice such conversations, so they are better prepared when they encounter them...

### [LM-SimBench: A Unified Framework, Dataset, and Benchmark for Large Language Model Training Simulation](https://arxiv.org/abs/2611.14285v1)

- **Authors:** Yu Dong, Hong Li, Qiang Sun, Xu Zhou, Jinbiao Huo, Qixiu Cheng, et al.
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Evaluating candidate parallelization strategies through distributed training runs makes strategy selection prohibitively expensive at scale. Performance simulation offers a lower cost alternative, yet controlled comparisons among existing simulators remain difficult because they differ in the training stages they mo...

### [MOAI: Module-Optimizing Architecture for non-interactive secure transformer Inference](https://arxiv.org/abs/2611.13641v1)

- **Authors:** Linru Zhang, Xiangning Wang, Jun Jie Sim, Zhicong Huang, Jiahao Zhong, Huaxiong Wang, et al.
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Privacy concerns have been raised in Large Language Models (LLM) inference when models are deployed in Cloud Service Providers (CSP). Homomorphic encryption (HE) offers a promising solution by enabling secure inference directly over encrypted inputs. However, the high computational overhead of HE remains a major bot...

### [Mobile AI Factory: Building Specialized Language Models for Your Mobile Device](https://arxiv.org/abs/2611.13509v1)

- **Authors:** Evan Li, Krishna Deshpande, Wen Cheng, Shyamnath Gollakota
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Small language models (SLMs) running on mobile devices can keep user data private and work without connectivity. But they perform well only when fine-tuned for the target task and sized for the target device, a process that today requires repeated expert tuning. We present {\it Mobile AI Factory}, an agentic system...

### [One Byte, One Token: Byteifying a 27B Hybrid-Attention LLM with Self-Generated Data](https://arxiv.org/abs/2611.13607v1)

- **Authors:** Liwei Zhang, ZhiMing Tong
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Byte-level BPE fragments Chinese text (for Qwen3.8 on Chinese Wikipedia, 3.84 bytes per token on average; 64% of tokens are single characters) and hides spelling from the model. We ask whether an already-trained 27B subword model can be converted directly into a pure byte-level model (one byte, one token), without a...

### [One Policy for 100 Household Tasks: Our Solution for the 2026 BEHAVIOR Challenge](https://arxiv.org/abs/2611.14432v1)

- **Authors:** Ilia Larchenko, Gleb Zarin, Atindra Nair, Keerti Manney, Vitaly Kleban, Mirko Kiefer, et al.
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We describe our solution for the 2026 BEHAVIOR Challenge: 100 long-horizon household tasks in the OmniGibson simulator. We placed 9th on the final leaderboard, the only independent team in the top 10. The core of the solution is a single vision-language-action (VLA) model, one checkpoint for all 100 tasks, built on...

### [OpticalRAG: Pixel-Space Compression for Token-Efficient Retrieval-Augmented Generation](https://arxiv.org/abs/2611.13675v1)

- **Authors:** Senhao Liu, Yuheng Zhang, Chunyu Wei, Yueguo Chen, Xinran Zhang
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Retrieval-augmented generation (RAG) is bottlenecked by the token budget of large language models: feeding long documents into the context window is expensive, while aggressive textual compression discards fine-grained information that is irreversibly lost in a one-dimensional token sequence. We argue that this bott...

### [REAL Loss: Optimizing Real Expected Acceptance Length for Speculative Decoding](https://arxiv.org/abs/2611.14399v1)

- **Authors:** Yu Tian
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Speculative decoding accelerates LLM inference by having a draft model propose multiple tokens for the target model to verify in one pass. The speedup is governed by the expected acceptance length (EAL), yet standard training objectives such as cross-entropy, KL divergence, and total variation focus only on distribu...

### [SHADOWPREFILL: Keeping Your Next Model Warm for Per-Step Model Routing in Agentic LLM Serving](https://arxiv.org/abs/2611.13176v1)

- **Authors:** Haoran Qiu, Rohan Mahapatra, Rodrigo Fonseca, Mark Russinovich
- **Date:** 2026-11-09
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Per-step model routers send each LLM call of an agent to the cost-optimal model dynamically within each session. However, every model switch discards prefix-cache reuse: KV caches are per model, so the new model must prefill the relevant context before it emits a token. Across representative agentic workloads, inclu...

### [SinkState: On-the-Fly SVD of Recurrent States for Efficient Hybrid LLM Serving](https://arxiv.org/abs/2611.14246v1)

- **Authors:** Haolin Jiang, Weihang Li, Zhongzhu Zhou, Jinwen Pan, Santosh Pandey, Hang Liu
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Hybrid models combine softmax attention with linear attention, which compresses history into fixed-size recurrent states to balance model quality and inference efficiency. However, linear attention has not pushed this compression to its limit: we find that the queries, keys, and values of linear layers concentrate i...

### [SteerDistill: Quantizing LLM Agents via Closed-Loop Teacher Steering](https://arxiv.org/abs/2611.13410v1)

- **Authors:** Genming Cui, Xiangyu Li, Zixu Hao, Xin Ding, Yunxin Liu, Ting Cao
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Low-bit quantization reduces the inference cost of LLM agents but can compromise task success. Examining failed rollouts, we find that quantized agents overlook task requirements or environmental conditions, producing environment transitions that diverge from successful full-precision references. Correcting these be...

### [TAPCO-G: LLM-Guided Design-Adaptive Timing and Power Co-Optimization with Graph-Based Physical Priors](https://arxiv.org/abs/2611.13931v1)

- **Authors:** Wuqian Tang, Zixiao Wang, Che-Chien Lin, Fong-Hua Fu, Laura Angélica Shion-Korsak, Xinyun Zhang, et al.
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Post-placement timing and power co-optimization is critical to meeting setup timing targets and reducing power within placement constraints. A cell replacement can improve timing along one path while increasing power or reducing slack on others. Conventional optimizers follow fixed rules for scheduling and accepting...

### [Tree-Ising: Repairing Language Models with Bit-Level Ising Edits](https://arxiv.org/abs/2611.14210v1)

- **Authors:** Hadi Salloum, Ammar Ali
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Weight-space programming, introduced in recent MIT work by Takehi et al., enables a frontier LLM agent to read a network's weights and write a repair. Their GPT-6 Astra agent corrected the reasoning loops of Qwen3.5-0.8B without gradients, using 158 agent turns, 89.7 million tokens, and 50 forward-pass requests. Our...

### [Verifiable Agentic Traffic Class: A Policed Quality-of-Service Mechanism for Agentic AI Traffic, Evaluated from Simulation to Real-Kernel Adversarial Testing](https://arxiv.org/abs/2611.14211v1)

- **Authors:** Naveen Babu Narayanan Nair, Sajay Kurup
- **Date:** 2026-11-10
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Software agents built on large language models generate traffic unlike human web traffic, yet routers have no class for it and cannot verify a sender's claim to be an agent. This paper proposes the Verifiable Agentic Traffic Class (VATC), which combines a reserved Differentiated Services Code Point (DSCP) value decl...

### [WAM-Sim0.1: World Anchored Memory Meets Online RL for Consistent and Realistic Driving Simulation](https://arxiv.org/abs/2611.07939)

- **Authors:** Jiahao Cui, Jiaye Li, Wenhao Zhang, Yaoyi Li, Shan Luan, Tang Quanhui, et al.
- **Date:** 2026-11-05
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Autoregressive driving world models systematically suffer from structural drift, identity drift, and quality decay over long rollout horizons due to transient conditioning signals that lack persistent state. We present WAM-Sim, a driving world model anchored by a persistent hierarchical memory and optimized via onli...

### [carryovergate: a derivation-authority re-fire gate for LLM agents](https://doi.org/10.5281/zenodo.24094737)

- **Authors:** Venkata Manikanta Sangaraju
- **Date:** 2026-11-10
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, llm-agents
- **Abstract summary:** Derivation-authority re-fire gate for agent memory: block scheduled and recalled actions whose derivation cannot trace to the user.

### [Dynamic Sleep Schedules for AI Agents](https://doi.org/10.5281/zenodo.24091863)

- **Authors:** Arsenii Emelin
- **Date:** 2026-11-09
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, evaluation
- **Abstract summary:** This concept paper proposes the term dynamic sleep schedule for AI agents. Building on recent work on agent memory and sleep-based continual learning, it argues that an agent's inactive periods should be used not only to consolidate memories, but to revisit past decisions across time and learn how much computation a...

### [LIV: Validity Estimates for Facts in Enterprise Agent Memory](https://doi.org/10.5281/zenodo.24077471)

- **Authors:** Bogdan Raduta
- **Date:** 2026-11-09
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, evaluation
- **Abstract summary:** Agents that act on stored enterprise facts act on values that may have changed since they were last verified. We study a per-fact validity estimate with calibration as a target, learned from an organisation's own change and re-verification events, that gives the probability that a stored value has not changed since...

### [Replication package: Unprompted coordination through shared memory in LLM agents, a locked two-implementation replication and extension](https://doi.org/10.5281/zenodo.23965305)

- **Authors:** Pekka Abrahamsson, Muhammad Waseem, Esa Karjalainen, Petrus Jussila, Henri Laukkanen, Jussi Rasku, et al.
- **Date:** 2026-11-09
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, llm-agents
- **Abstract summary:** Replication package for the paper "Unprompted coordination through shared memory in LLM agents: a locked two-implementation replication and extension" (GPT-Lab, Tampere University). The study was run in two independently built implementations under hashed locks. The package holds both halves. replicator/: runner sou...

### [revsim: Revocation reliability simulator for cloud AI-agent delegation chains (code and data)](https://doi.org/10.5281/zenodo.24091915)

- **Authors:** Yulliwas Ameur
- **Date:** 2026-11-09
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Monte Carlo simulator, sanity tests, parameters and raw results supporting the article "Revocation Is a Reliability Problem for Cloud AI Agents" (Y. Ameur, 2026). The model represents a delegation chain of cloud AI agents (orchestrator, sub-agents, tool sessions, secrets in agent memory). At t = 0 the principal revo...
