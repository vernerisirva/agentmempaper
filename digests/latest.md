# Latest Paper Scout Digest

Latest daily digest: [2026-10-21](2026-10-21.md).

# Paper Scout Digest - 2026-10-21

## Run Summary

- **Run ID:** 159
- **Candidates fetched:** 517
- **New unique papers:** 459
- **Relevant:** 74
- **Maybe relevant:** 95
- **Irrelevant:** 348
- **Source summary:** arxiv: 100, openalex: 400, semantic_scholar: 17

## Source Warnings

- arxiv: incomplete discovery window for 'agent memory'; single-page record limit reached.
- arxiv failed for 'procedural memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+AND+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- arxiv failed for 'parametric memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aparametric+AND+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- arxiv failed for 'memory distillation': http error for https://export.arxiv.org/api/query?search_query=all%3Amemory+AND+all%3Adistillation&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- arxiv failed for 'self-improving language models': timeout error for https://export.arxiv.org/api/query?search_query=all%3Aself+AND+all%3Aimproving+AND+all%3Alanguage+AND+all%3Amodels&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out
- arxiv failed for 'cs.AI,cs.CL,cs.LG': http error for https://export.arxiv.org/api/query?search_query=cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG&start=0&max_results=300&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- openalex: incomplete discovery window for 'agent memory'; single-page record limit reached.
- openalex: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'memory distillation language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'parametric memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'agent memory'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'memory distillation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'parametric memory LLM'; single-page record limit reached.

## Highly Relevant

### [From Relevant Memories to Sufficient Evidence: Rethinking Memory Utilization in LLM Agents](https://doi.org/10.48550/arxiv.2610.22668)

- **Authors:** Shixuan Li, Wei Yang, Peiyu Zhang, Anzhe Cheng, Heng Ping, Xiaole Zhang, et al.
- **Date:** 2026-10-15
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, long-term-memory, benchmark, agent-memory, memory-systems
- **Abstract summary:** Long-term memory enables LLM agents to reuse past experiences, yet retrieving relevant memories does not necessarily provide sufficient evidence for answering a query. Essential information may remain fragmented across memory records, obscured by abstraction, or disconnected from the relations required for reasoning...

### [M-Plan: Comprehensive Planning For LLM Agents with Memory Arrangement](https://arxiv.org/abs/2610.27032v1)

- **Authors:** Ziyang Liu, Jiakang Yuan, Jiayuan Fan, Tao Chen
- **Date:** 2026-10-19
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, long-term-memory, memory-policy, agent-memory, memory-systems
- **Abstract summary:** Large language model (LLM)-based agents have recently demonstrated outstanding performance in single-turn tasks, yet they continue to struggle with long-horizon tasks, particularly in environments without prior training. A key limitation of single LLMs is their difficulty in processing long contexts, which stems fro...

### [Memory as Code: Declarative Retrieval over Codified Long-Term Memory](https://arxiv.org/abs/2610.27700v1)

- **Authors:** Aoting Zeng, Yuxin Du, Jianwei Wang, Yizhang He, Shan Jiang, Xuemin Lin, et al.
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, memory-systems, long-term-memory, benchmark, agent-memory
- **Abstract summary:** In long-term memory systems, memories are constructed from interaction histories and retrieved in response to queries, enhancing the reasoning ability of LLM agents. In complex scenarios, facts are scattered across sessions and their relationships evolve over time, making it difficult for existing memory systems to...

### [Multimodal Filesystem Memory For Long-Horizon Embodied Agents](https://doi.org/10.48550/arxiv.2610.22686)

- **Authors:** Chloe Su, Jiahan Li, Zhenting Qi, Chen Cheng, Haoyu Chen, Sejoon Jun, et al.
- **Date:** 2026-10-15
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Studies governed shared memory or persistent memory protocols for LLM agents.
- **Tags:** agent-memory, long-term-memory, memory-types, memory-systems, llm-agents
- **Abstract summary:** Agents operating over long horizons need an effective memory that allows them to reuse their experience throughout long interactions. If the entire history of an interaction is retained, it becomes difficult to find the relevant experience, while compressing it into summaries may result in the loss of visual and spa...

### [RL-Guided Temporal Localization for Dual-Channel Retrieval in Long-Horizon Agent Memory](https://doi.org/10.48550/arxiv.2610.23598)

- **Authors:** Dabin Sheng, Zhe Wu, Jinming Zhao, Junliang Xing, Yuanchun Shi
- **Date:** 2026-10-16
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, llm-agents, long-term-memory, memory-types, benchmark, memory-systems
- **Abstract summary:** Time-aware retrieval is crucial for long-horizon LLM agents to effectively leverage ever-growing long-term memory. Existing methods focus on lexical or semantic similarity, leading to target memories being crowded out by temporally mismatched yet semantically similar candidates. Even time-aware approaches inject tem...

### [SAFE-Mem: Secure Agentic Memory with Fine-Grained Authority and Governance-Aware Retrieval](https://doi.org/10.48550/arxiv.2610.22959)

- **Authors:** LI Haoming, Dingyi Kang, Xu Hu, Jinxin Yang, Zhu Xu, Chenru Wang, et al.
- **Date:** 2026-10-16
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** agent-memory, llm-agents, long-term-memory, memory-policy, benchmark, memory-systems
- **Abstract summary:** Large language model (LLM) agents increasingly rely on persistent memory to support long-term reasoning and personalized interactions. However, information collected from external sources can introduce security risks when untrusted claims (i.e., atomic statements) are later treated as authorized preferences, policie...

### [Fast and scalable multi-GPU sliced FFT solvers for asymptotically compatible discretizations of 3D nonlocal diffusion problems](https://arxiv.org/abs/2610.28372v1)

- **Authors:** Yulong Li, Jiale Meng, Zhenlin Guo, Jiwei Zhang
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** benchmark, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Large-scale 3D peridynamic transient diffusion simulations are constrained by the computational cost and memory requirements of nonlocal interactions. We propose a fast and scalable multi-GPU sliced FFT algorithm based on the recently developed asymptotically compatible finite difference (ACFD) scheme. By exploiting...

### [AutoRedClaw: Automated Red-Teaming for Claw-Style Agents](https://arxiv.org/abs/2610.27244v1)

- **Authors:** Hao Li, Tongyan Hu, Weidi Luo, Shanghao Shi, Xiaogeng Liu, Aiden Suh, et al.
- **Date:** 2026-10-19
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Agent systems are shifting from task-scoped tool-use agents to persistent, personalized assistants such as OpenClaw. These claw-style agents maintain configuration files (e.g., AGENTS.md), long-term memory, and reusable skills. Once poisoned, this persistent state is repeatedly reloaded into the agent's context, cre...

### [ClawMMU: Protection-Coherent Virtual Memory for Stateful LLM Agents](https://arxiv.org/abs/2610.28093v1)

- **Authors:** Jinhao Hu, Bardia Mohammadi, Mofasshara Binte Rafique, Lars Henning Klein, Akhil Arora, Ashvin Goel, et al.
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, long-term-memory, agent-memory, memory-systems
- **Abstract summary:** AI agents keep long-term memory, much of which comes from web pages and tool results. Agent harnesses, the software that runs the model, do not record who may act on this memory, so an instruction hidden in a fetched page can be treated as the user's own instruction. We propose ClawMMU, a protection layer that label...

### [Disclosure Begets Disclosure: A Self-Reinforcing Privacy Loop in LLM Agents with Persistent Memory](https://arxiv.org/abs/2610.28315v1)

- **Authors:** Masahiro Kaneko, Hiromi Arai, Timothy Baldwin
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** llm-agents, long-term-memory, agent-memory, memory-systems
- **Abstract summary:** Large language model (LLM) agents increasingly use persistent memory to personalize responses, and personal attributes in this memory pose a privacy risk if exposed. We ask how consulting memory during dialogue changes what users go on to say, and thus what the memory comes to reveal. In multi-session simulations, a...

### [DuplexLedger: Benchmarking Transactional Memory in Full-Duplex Speech Agents](https://arxiv.org/abs/2610.27581v1)

- **Authors:** Yuxuan Li, Xiangchen Guan, Kunrong Li, Jin Wang, Kaiwen Luo, Yang Xiao, et al.
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Focuses on persistent or long-term memory for agent behavior.
- **Tags:** long-term-memory, evaluation, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Full-duplex speech agents must update persistent memory while listening and speaking, yet it remains unclear which events should be stored, revised, or excluded. Existing benchmarks isolate interaction timing from memory outcomes, obscuring the state transitions behind a correct answer. We introduce DuplexLedger, a...

### [Industrial ReMEmbR: Scaling Spatiotemporal Memory to Robot Fleets](https://arxiv.org/abs/2610.28624v1)

- **Authors:** Jad Yammine, Malek Wahidi, Abrar Anwar, Yan Chang, Mihir Acharya, Anthony Rizk
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** memory-types, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Warehouse robot fleets continuously observe operational conditions, but preserving these observations as reusable semantic memory incurs substantial computation, communication, and storage costs. For example, explaining recurring aisle blockages can require reviewing video from multiple robots across several shifts....

### [SPEM: Structure-Aware Procedural Memory for Efficient Skill Use in LLM Agents](https://arxiv.org/abs/2610.26995v1)

- **Authors:** Ran Zhou, Zehui Kong, Fanyu Lin, Jiaheng Liu, Zhen Zhang, Yuxiang Ren
- **Date:** 2026-10-19
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** llm-agents, memory-types, agent-memory, memory-systems
- **Abstract summary:** LLM-based agents increasingly rely on reusable skills. However, scaling skill libraries makes efficient and accurate skill use difficult. Full skill loading incurs high token and runtime overhead. In contrast, flat semantic retrieval treats skills as independent text entries, ignoring dependencies, execution order,...

### [Knowledge Graph Based Memory for Large Language Model Systems: A Systematic Review Protocol](https://osf.io/9kdt2)

- **Authors:** Kathleen M. Jagodnik, Nirmal Gelal, Aryan Singh Dalal, Hande Küçük McGinty, Yinglun Zhang
- **Date:** 2026-10-17
- **Source:** openalex
- **Relevance:** relevant (90/100)
- **Reason:** Studies governed shared memory or persistent memory protocols for LLM agents.
- **Tags:** agent-memory, evaluation, memory-systems, llm-agents
- **Abstract summary:** This project conducts a systematic literature review of knowledge graph-based memory systems for large language model (LLM) based systems. LLMs face several persistent limitations in long-horizon and personalized tasks: knowledge cutoffs prevent access to recent information, finite context windows constrain in-conte...

## Maybe Relevant

### [From Memory Hits to Answerable Evidence: Query-Conditioned Memory Compilation for Long-Term Agent Memory](https://doi.org/10.48550/arxiv.2610.23313)

- **Authors:** Shangze Li, Yanyu Yao, Derong Xu, Zhi Zheng, Tong Xu
- **Date:** 2026-10-16
- **Source:** openalex
- **Relevance:** maybe (69/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, benchmark
- **Abstract summary:** Long-term agent memory requires recovering answer-relevant evidence dispersed across turns and sessions. Existing systems increasingly use structured memories and adaptive retrieval, yet often pass retrieved or expanded units directly to the reader, coupling memory addressing with evidence presentation and leaving t...

### [Beyond Experience: Knowledge-Guided Evolution for NPU Kernel Generation](https://arxiv.org/abs/2610.27588v1)

- **Authors:** Xi Chen, Ming Shen, Haotian Yan, Ruoyu Sun, Tianjun Yao
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** LLM agents have become capable kernel engineers on mainstream GPU stacks, but they struggle on emerging accelerators such as Ascend NPUs, whose programming model is barely represented in pretraining data. Recent NPU agents address this gap largely through experience: they accumulate memory from their own generation...

### [GBClaw: An agentic AI framework for atomistic grain boundary research and mechanistic discovery](https://arxiv.org/abs/2610.28629v1)

- **Authors:** Yazhuo Liu, Kunqing Ding, Xiaoguo Gong, Zifeng Wang, Yichen Yang, Yifeng Che, et al.
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agentic artificial intelligence (AI) systems hold immense potential for automating complex workflows in materials discovery and design, but extending them to domain-intensive mechanistic investigations remains challenging. Here, we present GBClaw, an agentic AI framework for investigating the structure and deformati...

### [HexaShell: A Thin Harness for Exploring the Limits of VLM Agents as Robot Coding Agents](https://arxiv.org/abs/2610.23479v2)

- **Authors:** Hongcheng Gao, Alex Zhou, Jay Zhu, Zelin Zheng, Shijia Ge, Xiping Li, et al.
- **Date:** 2026-10-16
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agents built on vision language models (VLMs) now compete with learned policies on robot manipulation leaderboards. We ask how far a coding agent can go when it controls a robot instead of a computer, and where it stops. Our system, HexaShell, gives the agent a thin harness: one command line that turns its commands...

### [How Intervention History Changes AI Agent Sabotage on Subsequent Tasks](https://arxiv.org/abs/2610.26935v1)

- **Authors:** Daniel Saeedi, Amirali Aghazadeh
- **Date:** 2026-10-17
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** AI control evaluations often reset agents' memory between tasks, although deployed agents may retain records of prior interventions. We ask whether learning that an earlier attack was caught changes an agent's ability to evade defer-to-trusted (DtT), a protocol that replaces suspicious work with a trusted model's so...

### [Interruption-Aware Recurrent Reinforcement Learning for UAS Navigation Under Temporary Overrides](https://arxiv.org/abs/2610.28121v1)

- **Authors:** Christopher Conrad, Deepak Panda, Weisi Guo, Antonios Tsourdos
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Safe autonomous navigation of UASs requires tactical deconfliction to address conflicts that strategic coordination cannot prevent. This task is challenging under partial observability, when sensor or traffic data are missing, delayed, or degraded. Geometry-based methods can offer separation assurances but face limi...

### [SAGE-HAP: Sustainability-Certified Agentic Communication and Computing at a Solar-Powered High-Altitude Platform](https://arxiv.org/abs/2610.27513v1)

- **Authors:** Haoxiang Luo, Bang Huang, Mohamed-Slim Alouini
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The solar-powered High-Altitude Platforms (HAP) can provide persistent communication and computing services beyond terrestrial coverage. However, changing mission priorities, coupled resource demands, and uncertain solar supply complicate sustainable scheduling, while large language model proposals require independe...

### [Toward Agentic AI for the 6G Physical Layer: From Algorithm Discovery to Verified Baseband Silicon](https://arxiv.org/abs/2610.27797v1)

- **Authors:** Eric Mittag, Lukas Brechtel, Maximilian Stark, Hans D. Schotten
- **Date:** 2026-10-20
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** 6G will be designed faster than it can be built: AI-driven search already proposes physical-layer algorithms at machine speed, while carrying a single one onto embedded baseband silicon remains specialist work. That silicon imposes hard memory and numeric limits, but also exposes cost structures a GPU lacks, and a d...

### [Understanding KV Residency in Production-Scale Agentic LLM Workloads](https://doi.org/10.48550/arxiv.2610.22863)

- **Authors:** Mayank Arya, Agrim Bari, Anjaly Parayil, Yogesh L. Simmhan, Renée St. Amant, Victor Rühle, et al.
- **Date:** 2026-10-16
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agentic large language model (LLM) applications turn one user request into a sequence of model and tool calls over a growing context. Retaining this context's key-value (KV) state in GPU memory lets later calls reuse it instead of recomputing it, but at fleet scale this needs substantial memory. We characterize four...

### [Beyond Marginal Influence: Interaction-Aware Memory Selection for LLM Agents](https://doi.org/10.48550/arxiv.2610.23266)

- **Authors:** BHVSP Subrahmanyam, Neeraj Choudhary
- **Date:** 2026-10-16
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, llm-agents
- **Abstract summary:** LLM-agent memory selection often uses retrieval rankings based on record relevance or individual influence. Such rankings cannot identify sufficient subsets under redundant or jointly necessary evidence. We study per-decision memory sufficiency: selecting a small subset that preserves full-memory behavior. To separa...

### [GLOBE: Evolving Structured Agentic Memory for E-commerce Product Optimization in Generative Search](https://doi.org/10.48550/arxiv.2610.23709)

- **Authors:** Hyunseo Kim, Suil Choe, Sukkyoung So, Daeyeon Yi
- **Date:** 2026-10-16
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** Optimizing product listings for generative search requires language agents not only to rewrite effectively but also to continually self-improve by retaining successful strategies across diverse categories. However, existing approaches often treat structured listings as free-form text, leaving effective strategies im...

### [Readers that can open the memory folder: Codex's read path and memory tools over replayed agent memory folders. Protocol and materials frozen before the run (Paper 7, Study 4)](https://doi.org/10.5281/zenodo.23481694)

- **Authors:** Kazuki Nakayashiki
- **Date:** 2026-10-19
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, llm-agents
- **Abstract summary:** Frozen protocol, code and materials of the fourth study of a paper on what LLM agents' memory pipelines pass on from a run of tool outcomes, deposited before any smoke or confirmatory model call (the manifest's OpenTimestamps proof is included; its Bitcoin attestation is checked by the gated launcher). The second st...

### [REM: What to Store, When to Recall, What to Forget in Experience Memory for Coding Agents](https://arxiv.org/abs/2610.27377v1)

- **Authors:** Xinyi Lisa Chen, Pedro Herrero-Vidal, Xiaohan Chen, Xiaojing Yu, Cris Liu, Bingqing Song, et al.
- **Date:** 2026-10-19
- **Source:** arxiv
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, llm-agents
- **Abstract summary:** Large language model (LLM) agents now autonomously complete long-horizon tasks, such as repository-level coding, through hundreds of think-act steps, yet the experience each run produces is rarely reused on the next. Prior memory systems concentrate on retrieval, finding the most relevant past trajectory. Retrieval...
