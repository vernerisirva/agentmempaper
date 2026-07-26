# Latest Paper Scout Digest

Latest daily digest: [2026-07-26](2026-07-26.md).

# Paper Scout Digest - 2026-07-26

## Run Summary

- **Run ID:** 64
- **Candidates fetched:** 824
- **New unique papers:** 762
- **Relevant:** 43
- **Maybe relevant:** 145
- **Irrelevant:** 636
- **Source summary:** arxiv: 420, openalex: 400, semantic_scholar: 4

## Source Warnings

- semantic_scholar failed for 'agent memory': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar failed for 'parametric memory LLM': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Highly Relevant

### [Retain or Consolidate? Budget-Dependent Operator Selection for Language Agent Memory](https://arxiv.org/abs/2607.17545)

- **Authors:** Qingcan Kang, Mingyang Liu, Shixiong Kai, Kaichao Liang, Tang Z, Yuqi Cui, et al.
- **Date:** 2026-07-20
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Studies memory storage, retrieval, update, or consolidation for LLM agents.
- **Tags:** agent-memory, memory-policy, benchmark, memory-systems, llm-agents
- **Abstract summary:** Language agents depend on memory across interactions. However, the limited context windows of large language models (LLMs) and their inference costs constrain how much memory can be used at once. Existing systems mainly follow two strategies: memory retention and memory consolidation. Retention keeps raw records and...

### [Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents](https://arxiv.org/abs/2606.27472)

- **Authors:** Vedant Patel
- **Date:** 2026-06-25
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Studies memory storage, retrieval, update, or consolidation for LLM agents.
- **Tags:** llm-agents, memory-policy, benchmark, agent-memory, memory-systems
- **Abstract summary:** Large language model (LLM) agents operate over long, multi-session interactions in which facts change: a user moves, a price updates, a plan is revised. Acting correctly requires using the current value of a fact and discarding values that have been superseded. We isolate this ability on real conversational data and...

### [Dimension Reduction for Quantum Adaptive Agents](https://arxiv.org/abs/2607.19156)

- **Authors:** Rishi Sundar, Thomas J. Elliott
- **Date:** 2026-07-21
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Evaluates memory mechanisms or benchmarks for LLM agents.
- **Tags:** benchmark, agent-memory, memory-systems, llm-agents
- **Abstract summary:** Adaptive agents realise complex reactive behaviours by using a memory of past input stimuli and output actions to guide structured future responses. Quantum adaptive agents can operate while storing less information in memory than optimal classical counterparts; yet, this does not necessarily translate into a reduce...

### [Navigating Epistemic Parity in LLM Agents: A Benchmark for Cross-Source Conflict Resolution Between Memory and Procedural Skills](https://doi.org/10.5281/zenodo.21533560)

- **Authors:** Prakhar Pandey
- **Date:** 2026-07-24
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** llm-agents, memory-types, evaluation, agent-memory, memory-systems
- **Abstract summary:** Production LLM agents increasingly rely on two context-provisioning systems in tandem: episodic memory pipelines, which inject persistent user preferences and historical state, and procedural skill modules (e.g., SKILL.md files), which inject standardized, developer-defined operating procedures. Because these two so...

### [Navigating Epistemic Parity in LLM Agents: A Benchmark for Cross-Source Conflict Resolution Between Memory and Procedural Skills](https://doi.org/10.5281/zenodo.21533559)

- **Authors:** Prakhar Pandey
- **Date:** 2026-07-24
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory systems or memory modules for LLM agents.
- **Tags:** llm-agents, memory-types, evaluation, agent-memory, memory-systems
- **Abstract summary:** Production LLM agents increasingly rely on two context-provisioning systems in tandem: episodic memory pipelines, which inject persistent user preferences and historical state, and procedural skill modules (e.g., SKILL.md files), which inject standardized, developer-defined operating procedures. Because these two so...

### [GateMem: Benchmarking Memory Governance in Multi-Principal Shared-Memory Agents](https://arxiv.org/abs/2606.18829)

- **Authors:** Z Ren, Yibo Yang, Yimeng Chen, Z. Zhao, Benshuo Fu, Zhihao Shu, et al.
- **Date:** 2026-06-17
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies memory storage, retrieval, update, or consolidation for LLM agents.
- **Tags:** llm-agents, memory-policy, evaluation, agent-memory, memory-systems
- **Abstract summary:** Memory benchmarks for LLM agents largely assume single-user settings, leaving shared assistants for hospitals, workplaces, campuses, and households understudied. In these deployments, multiple principals write to a common memory pool and query it under different roles, scopes, and relationships, so memory quality re...

## Maybe Relevant

### [Agentic Context Management: Solving Agent Memory and Cost by Treating Them as Lifecycle and Architecture Problems](https://doi.org/10.48550/arxiv.2607.21503)

- **Authors:** Gaurav Dadhich
- **Date:** 2026-07-23
- **Source:** openalex
- **Relevance:** maybe (69/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, benchmark
- **Abstract summary:** Production AI agents' failures are less often due to an inability to reason well and more often because they cannot manage what is in their reasoning context: conversation histories, large prompts, large tool definitions, and ballooning tool outputs. Agents drown in their own accumulating history while paying a toke...

### [Supra Cognitive Modes: A Routed Architecture for Agent Memory](https://arxiv.org/abs/2607.19096)

- **Authors:** Joshua Tobkin, D Yang
- **Date:** 2026-07-21
- **Source:** openalex
- **Relevance:** maybe (69/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, benchmark
- **Abstract summary:** Agent-memory workloads mix direct factual lookup, relation-chain and current-state reasoning, and broad synthesis over long histories. We describe Supra Cognitive Modes (SCM), an architecture that maps explicit or automatically selected per-query modes to retrieval and synthesis payloads over one shared ingest subst...

### [Identity Dissolution: The Absence of a Persistent Identity Substrate as a Structural Mechanism for Context-Dependent Identity Instability in Memory-Augmented Large Language Model Agents](https://doi.org/10.5281/zenodo.20684023)

- **Authors:** Creighton Baxter
- **Date:** 2026-06-18
- **Source:** openalex
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** This working paper introduces Identity Dissolution as a candidate structural mechanism for context-dependent identity instability in memory-augmented large language model (LLM) agents. Prior papers in this series document invariant failures at the semantic, goal, evaluative, motivational, and system-level layers. Id...

### [Agentic AI Systems as a Persistent Attack Surface: How Memory Poisoning, Skill Injection, Trace Leakage, Delegation Opacity, Instruction Hierarchy Collapse, and Prompt Injection Jointly Define a Candidate Framework for Runtime Integrity Failure](https://doi.org/10.5281/zenodo.20731134)

- **Authors:** Saluca Agentic AI Research Team
- **Date:** 2026-06-17
- **Source:** openalex
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Version 2 — revised in response to an external structural review and an automated critique pass. See "Response to Review" appendix in the PDF for the change log. Agentic AI systems — LLM-powered agents that plan, invoke tools, maintain persistent memory, and delegate to sub-agents — are being deployed in production...

### [Exploratory and Assimilating Reflection: Reflective Recall Cycle for Long-term Memory](https://arxiv.org/abs/2607.17879)

- **Authors:** Ganesh Senrayan, Moyuru Yamada, Ishan Jindal, Kiran Purohit
- **Date:** 2026-07-20
- **Source:** openalex
- **Relevance:** maybe (46/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** long-term-memory, memory-policy
- **Abstract summary:** LLM-based autonomous agents require external memory to overcome their statelessness and limited context window for long-term interaction and dynamic knowledge reasoning. However, existing memory retrieval methods often lack adaptability and sample efficiency, and struggle to retrieve the right mixture of memories fr...

### [Hayula Core: A Self-Improving Agent Platform with Skill-Based Architecture and Multi-Layer Memory](https://doi.org/10.5281/zenodo.21537059)

- **Authors:** Yahya Saqban
- **Date:** 2026-07-24
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We present Hayula Core, a self-improving AI agent runtime built from 100% original Python code that replaces Hermes/OpenClaw as the central execution engine of the Hayula Agent OS ecosystem. Unlike existing agent frameworks that wrap monolithic LLM calls in fixed pipelines, Hayula Core introduces a skill-based archi...

### [Hayula Core: A Self-Improving Agent Platform with Skill-Based Architecture and Multi-Layer Memory](https://doi.org/10.5281/zenodo.21537060)

- **Authors:** Yahya Saqban
- **Date:** 2026-07-24
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** We present Hayula Core, a self-improving AI agent runtime built from 100% original Python code that replaces Hermes/OpenClaw as the central execution engine of the Hayula Agent OS ecosystem. Unlike existing agent frameworks that wrap monolithic LLM calls in fixed pipelines, Hayula Core introduces a skill-based archi...

### [MemTools: A Unified Research Framework for Interoperable Agent Memory](https://doi.org/10.48550/arxiv.2607.21404)

- **Authors:** Chengfeng Zhao, Jinhui Chen, S Liang, Shizhu He, Yequan Wang, Jun Zhao, et al.
- **Date:** 2026-07-23
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** While memory systems are essential for agent architectures, pervasive architectural fragmentation restricts systematic research. Existing implementations typically couple different stages of the memory lifecycle, entangle evaluation logic with specific datasets, and provide limited support for the management of hete...

### [Current Trends in Artificial Intelligence Architectures: From Model Scaling to System Intelligence, Post-Transformer Hybrids and World Models](https://doi.org/10.3390/electronics15153254)

- **Authors:** Salvatore Rampone
- **Date:** 2026-07-23
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Artificial intelligence architecture is no longer adequately described by model size alone. Dense Transformers remain the reference architecture for language and multimodal reasoning, but production systems increasingly combine conditional computation, retrieval, memory, tools, verifiers, edge-cloud routing, observa...

### [Engineering Intelligent Decision-Support Systems for Medical Image Analysis: A Review of Computer Vision Models and Clinical Chatbots](https://doi.org/10.59543/jidmis.v3.807)

- **Authors:** Humberto J. Navarro
- **Date:** 2026-07-23
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Deploying artificial intelligence systems for medical image analysis in clinical settings involves considerations that go beyond model accuracy: infrastructure constraints, integration with existing workflows, and generalization across patient populations all determine whether a system works outside a research lab....

### [Per-Token Confidence Trajectory in LoRA Fine-Tuning: Substrate-Output Evidence for Cumulative Calibration Collapse](https://doi.org/10.5281/zenodo.21520555)

- **Authors:** Tomas Pødenphant Lund
- **Date:** 2026-07-23
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Why do fine-tuned language models hallucinate more confidently than their in-context-learning counterparts on the same knowledge? Mechanism. Each backward pass under cross-entropy loss amplifies the winning route asymmetrically and presses alternatives below the noise floor at the substrate-output layer; the depth o...

### [Per-Token Confidence Trajectory in LoRA Fine-Tuning: Substrate-Output Evidence for Cumulative Calibration Collapse](https://doi.org/10.5281/zenodo.20145218)

- **Authors:** Tomas Pødenphant Lund
- **Date:** 2026-07-23
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Why do fine-tuned language models hallucinate more confidently than their in-context-learning counterparts on the same knowledge? Mechanism. Each backward pass under cross-entropy loss amplifies the winning route asymmetrically and presses alternatives below the noise floor at the substrate-output layer; the depth o...

### [Coordinating from Memory: Graph-Structured Experience Reuse for Multi-Agent Adaptation in Dynamic Manufacturing](https://doi.org/10.48550/arxiv.2607.19985)

- **Authors:** Chengxiao Dai, Zhanhui Lin, Zhaokun Yan, Youyang Ni, Chenjun Lei, Luyan Zhang
- **Date:** 2026-07-22
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Dynamic manufacturing environments require multi-agent systems to coordinate effectively under frequent operational disturbances such as machine failures, urgent job arrivals, and processing time variations. Existing multi-agent reinforcement learning approaches treat each disturbance episode independently, discardi...

### [Coordinating from Memory: Graph-Structured Experience Reuse for Multi-Agent Adaptation in Dynamic Manufacturing](https://arxiv.org/abs/2607.19985)

- **Authors:** Chengxiao Dai, Zhanhui Lin, Zhaokun Yan, Youyang Ni, Chenjun Lei, Luyan Zhang
- **Date:** 2026-07-22
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Dynamic manufacturing environments require multi-agent systems to coordinate effectively under frequent operational disturbances such as machine failures, urgent job arrivals, and processing time variations. Existing multi-agent reinforcement learning approaches treat each disturbance episode independently, discardi...

### [Cultural evolution of music and language](https://doi.org/10.1093/oxfordhb/9780192894700.013.0028)

- **Authors:** Yuto Ozaki, Marianne de Heer Kloots, Andrea Ravignani, Patrick E. Savage
- **Date:** 2026-07-22
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Abstract Music and language are both forms of communication universally observed across human societies, prompting researchers to investigate why and how they evolved. Such research initially focused on the biological evolution of the capacities to create and perceive language and music; later work has been increasi...

### [Mi-Memory: A Lifecycle Memory Framework for Personal AI](https://arxiv.org/abs/2607.18975)

- **Authors:** Xule Liu, Hanlin Teng, Chao Li, Yanan Ni, S Lu, Audrey Wang, et al.
- **Date:** 2026-07-21
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Personal AI is moving beyond chat-only interaction toward continuous services that span phones, cars, homes, wearables, cameras, and tools. In this setting, memory cannot remain a cache of prior conversations. It should serve as a continuity and governance substrate: preserving durable user state, grounding answers...

### [HindsightBench: A Black-Box Behavioral Audit Protocol for Parametric Hindsight in Time-Indexed LLM Decision Tasks](https://arxiv.org/abs/2607.18867)

- **Authors:** Haozhe Jia
- **Date:** 2026-07-21
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language models leak parametric knowledge of realized outcomes into historical financial decision tasks. Existence is settled; what users lack is a cheap way to audit a given model for it. We present HindsightBench, a black-box behavioral audit protocol that profiles parametric hindsight in any time-indexed LL...

### [The Chronos Vulnerability: A Taxonomy of Temporal Persistence and Memory-Based Deception in Agentic AI](https://arxiv.org/abs/2607.19433)

- **Authors:** Om Narayan, Ramkinker Singh, Praveen Baskar
- **Date:** 2026-07-20
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The transition from stateless generative models in artificial intelligence to stateful, autonomous agents represents an architectural evolution that, while providing the capabilities of long-term planning and the automation of enterprise workflows, also represents the introduction of a new form of security threat, t...

### [The Chronos Vulnerability: A Taxonomy of Temporal Persistence and Memory-Based Deception in Agentic AI](https://doi.org/10.48550/arxiv.2607.19433)

- **Authors:** Om Narayan, Ramkinker Singh, Praveen Baskar
- **Date:** 2026-07-20
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** The transition from stateless generative models in artificial intelligence to stateful, autonomous agents represents an architectural evolution that, while providing the capabilities of long-term planning and the automation of enterprise workflows, also represents the introduction of a new form of security threat, t...

### [Towards Agentic Agent-based Models: Feasibility, Performance, and Statistical Model Checking](https://arxiv.org/abs/2607.17948)

- **Authors:** Stefano Blando, Emanuele Guerrazzi, Riccardo Porcedda, Giuseppe Squillace, Max Tschaikowski, Andrea Vandin
- **Date:** 2026-07-20
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Agent-based models (ABMs) rely on simple, explicit and reproducible rules for individual decision making, while complex collective behavior emerges from interactions among agents. Recent advances in large language models (LLMs) make it tempting to replace, enrich, or perturb these rules with LLM-based agentic capabi...

### [Evidence-in-the-Loop: Trace-Driven Optimization for Customer-Service LLM Agents](https://arxiv.org/abs/2607.18039)

- **Authors:** C E Wu, Dafei Qiu, Congde Yuan, Charles Quan, Jun Wu, Suipeng Li, et al.
- **Date:** 2026-07-20
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Production customer-service bots must improve answer quality across iterative releases, yet large language models must not bypass evidence boundaries, policy rules, or human-handoff safeguards. We present an \textbf{Evidence-Grounded Customer-Service Agent Workflow} deployed in a real-world customer-service setting....

### [LLMs and Agentic AI Systems for Smart Grids: A Tutorial on Architectures and Applications](https://arxiv.org/abs/2607.18147)

- **Authors:** Daniela Rojas, Abdulwahab Albassam, Aidan G. Leung, Jett Ngo, Ryan Luo, Peter R. Quawas, et al.
- **Date:** 2026-07-20
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language models (LLMs) and agentic AI systems have evolved from natural language tasks to using external tools to plan, retrieve, and act in technical domains. In smart grids, recent work applies agentic schemes to forecasting, optimization, and control, wrapping trusted solvers behind language interfaces and...

### [AGENTS4GEOS: agentic platform for open-source multi-physics simulation](https://arxiv.org/abs/2607.18557)

- **Authors:** Adriano Cortês, Roberto M. Velho, Fernando A. Rochinha, Álvaro L. G. A. Coutinho, Mauricio Araya-Polo, Hervé Gross
- **Date:** 2026-07-20
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Multi-physics simulations are essential for understanding and monitoring intricate subsurface processes such as CO2 storage. Their computational demands call for surrogate models and, for unstructured meshes, Graph Neural Networks (GNNs) are natural candidates. The main bottleneck in developing them is generating an...

### [PhyAgentOS: A Self-Evolving Operating System for Embodied Agents with Decoupled Cognitive Planning and Physical Execution](https://arxiv.org/abs/2607.16636)

- **Authors:** Yang Liu, Weixing Chen, Xinshuai Song, Tao Pu, Siwen Mo, Yongjie Bai, et al.
- **Date:** 2026-07-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Vision-language-action models, world models, and agentic planners each advance physical intelligence, yet their composition lacks a common execution abstraction, shared state, semantic verification, and persistent experience across heterogeneous embodiments. We present PhyAgentOS, a runtime foundation delivering sch...

### [Environment-free Synthetic Data Generation for API-Calling Agents](https://arxiv.org/abs/2607.16900)

- **Authors:** Seanie Lee, Sanjoy Chowdhury, C Y Jiang, Cheng-Yu Hsieh, Ting-Yao Hu, Alexander Toshev, et al.
- **Date:** 2026-07-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Training API-calling large language model (LLM) agents demands massive amounts of high-quality trajectories. However, collecting such data at scale typically requires fully implemented environments with executable APIs and realistic, pre-populated backend databases, creating a major bottleneck for scalability. To ov...

### [Distribution-First Population Simulation: Collapse, Calibration, and Recall in Non-WEIRD LLM Persona Modeling](https://arxiv.org/abs/2607.18310)

- **Authors:** Gurkan Ozkan
- **Date:** 2026-07-17
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Synthetic-population tools increasingly run every individual as an independent large language model (LLM) agent. Using real survey microdata, we show that this paradigm has a basic failure mode, and we set a distribution-first corrective against it, all measured with a deterministic, construct-validated verifier on...

### [AttriMem: Attribution-Guided Process Feedback for Agent Memory Learning](https://doi.org/10.48550/arxiv.2607.21106)

- **Authors:** Qinfeng Li, Yinghui Bao, Xinyan Yu, Hongze Chen, Wenqi Zhang, Xuhong Zhang
- **Date:** 2026-07-23
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory, llm-agents
- **Abstract summary:** Effective memory is crucial for LLM agents, yet constructing it effectively remains challenging. A memory-construction policy decides what information to extract, store, update, compress, or discard as interactions accumulate. Heuristic memory methods rely on subjective, task-specific rules, which can misalign with...

### [Does Memory Credit Travel? Paired Factorial Audits of LLM-Agent Memory](https://doi.org/10.13140/rg.2.2.11232.44801)

- **Authors:** Alessio Rocchi
- **Date:** 2026-07-23
- **Source:** openalex
- **Relevance:** maybe (43/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** agent-memory
- **Abstract summary:** No abstract available.
