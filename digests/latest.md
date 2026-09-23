# Latest Paper Scout Digest

Latest daily digest: [2026-09-23](2026-09-23.md).

# Paper Scout Digest - 2026-09-23

## Run Summary

- **Run ID:** 132
- **Candidates fetched:** 118
- **New unique papers:** 118
- **Relevant:** 7
- **Maybe relevant:** 20
- **Irrelevant:** 91
- **Source summary:** openalex: 100, semantic_scholar: 18

## Source Warnings

- arxiv failed for 'all:procedural and all:memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+and+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:parametric and all:memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aparametric+and+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'agent memory': http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'memory distillation': http error for https://export.arxiv.org/api/query?search_query=all%3Amemory+AND+all%3Adistillation&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'self-improving language models': http error for https://export.arxiv.org/api/query?search_query=all%3Aself+AND+all%3Aimproving+AND+all%3Alanguage+AND+all%3Amodels&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'cs.AI,cs.CL,cs.LG': http error for https://export.arxiv.org/api/query?search_query=cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG&start=0&max_results=300&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex failed for 'agent memory': http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-09-13&per-page=100: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- openalex: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- openalex failed for 'memory distillation language model': http error for https://api.openalex.org/works?search=memory+distillation+language+model&filter=from_publication_date%3A2026-09-13&per-page=100: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- openalex failed for 'parametric memory language model': http error for https://api.openalex.org/works?search=parametric+memory+language+model&filter=from_publication_date%3A2026-09-13&per-page=100: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- semantic_scholar: incomplete discovery window for 'agent memory'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'procedural memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'memory distillation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'parametric memory LLM'; single-page record limit reached.

## Highly Relevant

### [RPMem: Learning Long-Term Recurrent Parametric Memory Across Sessions for LLM Agents](https://www.semanticscholar.org/paper/d84232d26104a0f9ad8acce504a732c50f1cfe41)

- **Authors:** Fan-Yu Zhao, Rui-Ke Cao, Liang Dong, Fu-Gen Yao, Jian Xu, Guan-Jun Jiang, et al.
- **Date:** 2026-09-20
- **Source:** semantic_scholar
- **Relevance:** relevant (100/100)
- **Reason:** Discusses Engram-style or parametric memory mechanisms for language models.
- **Tags:** llm-agents, long-term-memory, evaluation, parametric-memory, agent-memory, memory-systems
- **Abstract summary:** Long-running LLM agents require memory that persists and evolves across sessions. Text-based memory retrieves and reconstructs past interactions at every query, making long-horizon performance increasingly dependent on retrieval quality and contextual reasoning as histories grow. Parametric memory encodes experience...

## Maybe Relevant

### [Control-Plane Placement and Memory Substrates in Modern Agentic AI: A Comparative Method for Prompt-Native Systems, Agent Shells, and Durable Runtimes](https://doi.org/10.2478/lpts-2026-0036)

- **Authors:** A. Bondarenko, N. Zamorskaia, D. Djakons, A. Djakona, R. Djakons
- **Date:** 2026-09-21
- **Source:** openalex
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Abstract AI agents that autonomously write, test, and modify code are now deployed across architectures that share similar surface features but differ substantially in where and how operating control is exercised. Contemporary systems span general-purpose SDKs, prompt-native work-flow packs, interactive coding shell...

### [Designer-RSI: Evolving Procedural Memory from User Traffic for Agentic Graphic Design](https://arxiv.org/abs/2609.22086)

- **Authors:** Hongyang Du, Lan Yan, Christian Flores, Asim Kadav
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (62/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** llm-agents
- **Abstract summary:** Professional graphic design is a long-horizon agentic task in which structured, editable artifacts emerge from many interdependent actions, yet outcomes admit no reliable programmatic oracle. We introduce a continual adaptation framework in which a frozen frontier model operates professional design software through...

### [AdaRepair-Mem: Adaptive Experience Orchestration for Repository-Level Program Repair](https://arxiv.org/abs/2609.20130)

- **Authors:** Z. C. Luo, J.C. Guo, W. J. He, S. Y. Wang, J. S. Yu, F. M. Zhao, et al.
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (46/100)
- **Reason:** Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory.
- **Tags:** memory-types, memory-policy
- **Abstract summary:** Recent memory-augmented repository-level program repair methods reuse historical repair experiences to improve LLM-based issue resolution. However, our analysis reveals three limitations in existing repository-level memory retrieval. First, episodic memory is highly imbalanced across repositories, leaving low-resour...

### [Artificial Intelligence-Related Risks in Interventional Pulmonology: An Exploratory Enumeration and Ranking Study Across Five General-Purpose Large Language Models](https://doi.org/10.3390/jcm15197340)

- **Authors:** Gianluca Marchi, Lorenzo Corbetta
- **Date:** 2026-09-22
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Background/Objectives: Artificial intelligence (AI) is entering interventional pulmonology (IP) faster than its potential risks have been systematically catalogued. We explored whether general-purpose large language models (LLMs), now widely consulted informally by patients and clinicians, could provide a rapid and...

### [LSREP: A Longitudinal State-Replay Protocol for Evaluating Conversational Memory, with ICE v2 as an Audited Local-First Architecture](https://arxiv.org/abs/2609.16730)

- **Authors:** Deepesh Sonar
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** evaluation
- **Abstract summary:** Conversational memory changes during use, so endpoint question answering alone cannot establish how a persistent state accumulates, ages, or incorporates revisions. We introduce LSREP, a Longitudinal State-Replay Evaluation Protocol combining ordered replay, explicit lifecycle schedules, repeated probes, evolving re...

### [Market Signal Injection: Adversarial Context Manipulation of LLM Pricing Agents](https://arxiv.org/abs/2609.18357)

- **Authors:** Dohun Lee, Hyunwoo Park
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.
- **Tags:** untagged
- **Abstract summary:** Large language model (LLM) pricing agents may respond to how market data is presented, even when its numerical values remain unchanged. We introduce market signal injection (MSI), an attack that manipulates numerical formatting, competitor ordering, or qualitative market commentary without issuing explicit instructi...
