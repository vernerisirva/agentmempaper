# Latest Paper Scout Digest

Latest daily digest: [2026-06-26](2026-06-26.md).

# Paper Scout Digest - 2026-06-26

## Run Summary

- **Run ID:** 4
- **Candidates fetched:** 593
- **New unique papers:** 291
- **Relevant:** 76
- **Maybe relevant:** 168
- **Irrelevant:** 349
- **Source summary:** arxiv: 29, openalex: 557, semantic_scholar: 7

## Source Warnings

- semantic_scholar failed for 'LLM agent memory': http error for https://api.semanticscholar.org/graph/v1/paper/search?query=LLM+agent+memory&limit=25&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds: request failed after 3 attempts: HTTP Error 500: Internal Server Error
- arxiv failed for 'memory mechanism language model': http error for https://export.arxiv.org/api/query?search_query=all%3A%22memory+mechanism+language+model%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Highly Relevant

### [Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees](https://arxiv.org/abs/2606.24322)

- **Authors:** Yedidel Louck
- **Date:** 2026-06-23
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Matches the agent-memory rubric with explicit LLM or agent context.
- **Tags:** agent-memory, long-term-memory, memory-policy
- **Abstract summary:** LLM agents increasingly rely on persistent long-term memory, which creates a critical vulnerability that we study here: memory poisoning. An adversary can store untrusted content in one session that later steers a consequential action, such as a payment, a setting change, or data exfiltration, in a future session. E...

### [MEMPROBE: Probing Long-Term Agent Memory via Hidden User-State Recovery](https://arxiv.org/abs/2606.24595)

- **Authors:** Enze Ma, Yufan Zhou, W E I-Xing Huang, Jie Yang, Huanhuan Ma, Zixuan Wang, et al.
- **Date:** 2026-06-23
- **Source:** openalex
- **Relevance:** relevant (77/100)
- **Reason:** Matches the agent-memory rubric with explicit LLM or agent context.
- **Tags:** agent-memory, long-term-memory
- **Abstract summary:** Long-term memory promises LLM agents that grow more capable across sessions, maintaining an accurate, evolving understanding of the user that interaction forms. In practice, however, this memory is evaluated mostly through downstream behavior, such as later answers, personalization quality, or task success, which te...

## Maybe Relevant

### [Governed Shared Memory for Multi-Agent LLM Systems](https://arxiv.org/abs/2606.24535)

- **Authors:** Yanki Margalit, Nurit Cohen-Inger, Erni Avram, Ran Taig, Oded Margalit
- **Date:** 2026-06-23
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** agent-memory
- **Abstract summary:** Multi-agent LLM environments require robust mechanisms for shared knowledge management. This paper formalizes the fleet-memory problem and identifies four foundational failure modes: unauthorized leakage, stale propagation, contradiction persistence, and provenance collapse. To address these, we define explicit syst...

### [Are We Ready For An Agent-Native Memory System?](https://arxiv.org/abs/2606.24775)

- **Authors:** Wei Zhou, X J Zhou, Shaokun Han, Hongming Xu, Guoliang Li, Zhiyu Li, et al.
- **Date:** 2026-06-23
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** agent-memory
- **Abstract summary:** Memory for large language model (LLM) agents has rapidly evolved from simple retrieval-augmented mechanisms into a data management system that supports persistent information storage, retrieval, update, consolidation, and dynamic lifecycle governance throughout agent execution. Despite this evolution, existing evalu...

### [Lamarckian Scars: Inheritable Runtime Constraints for Persistent LLM Agents](https://doi.org/10.5281/zenodo.20842692)

- **Authors:** TENGJIAO LIU
- **Date:** 2026-06-25
- **Source:** openalex
- **Relevance:** maybe (40/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** long-term-memory
- **Abstract summary:** Long-lived LLM agents increasingly act through tools, APIs, and external environments. While long-term memory helps agents accumulate experience, textual memories are retrieved probabilistically and may fail to prevent previously observed tool-use violations when context is diluted, retrieval is incomplete, or memor...

### [Lamarckian Scars: Inheritable Runtime Constraints for Persistent LLM Agents](https://doi.org/10.5281/zenodo.20842693)

- **Authors:** TENGJIAO LIU
- **Date:** 2026-06-25
- **Source:** openalex
- **Relevance:** maybe (40/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** long-term-memory
- **Abstract summary:** Long-lived LLM agents increasingly act through tools, APIs, and external environments. While long-term memory helps agents accumulate experience, textual memories are retrieved probabilistically and may fail to prevent previously observed tool-use violations when context is diluted, retrieval is incomplete, or memor...

### [Memory Makes the Difference: Evaluating How Different Memory Roles Shape Conversational Agents](https://doi.org/10.48550/arxiv.2606.25361)

- **Authors:** Yuxin Wang, Paul Thomas, Zhiwei Yu, Yuan Gao, Saeed Hassanpour, Soroush Vosoughi, et al.
- **Date:** 2026-06-24
- **Source:** openalex
- **Relevance:** maybe (40/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** parametric-memory
- **Abstract summary:** Prior research on memory mechanism in RAG-based conversational system has emphasized how memory is stored and retrieved. However, far less is known about how memories with different functional roles influence response quality. Specifically, how they shape an agent's responses under varying conversational contexts an...

### [Staying In Character: Perspective-Bounded Memory For Book-Based Role-Playing Agents](https://doi.org/10.48550/arxiv.2606.25632)

- **Authors:** Xushuo Tang, Junhe Zhang, Zihan Yang, Yifu Tang, Sichao Li, Longbin Lai, et al.
- **Date:** 2026-06-24
- **Source:** openalex
- **Relevance:** maybe (40/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** parametric-memory
- **Abstract summary:** Recent LLM role-playing systems build character agents from novels by extracting characters, scenes, and relations. Yet long-narrative role-playing suffers from two failures: Factual Overreach, where shared retrieval or parametric memory lets a character use facts outside its perspective, and Stylistic Monotony, whe...

### [TRUSTMEM: Learning Trustworthy Memory Consolidation for LLM Agents with Long-Term Memory](https://doi.org/10.48550/arxiv.2606.25161)

- **Authors:** Tianyu Yang, Sudipta Paul, Vijay Srinivasan, Vivek Kulkarni, Srinivas Chappidi
- **Date:** 2026-06-23
- **Source:** openalex
- **Relevance:** maybe (40/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** long-term-memory
- **Abstract summary:** Large language model (LLM) agents rely on long-term memory to support extended interactions and personalized assistance beyond finite context windows. Existing memory agents actively update external memory through generated write, revise, and delete operations, but these updates may omit important information, corru...

### [Memory Retrieval in Visuomotor Policies for Long-Horizon Robot Control](https://doi.org/10.48550/arxiv.2606.25136)

- **Authors:** Rutav Shah, Yisu Li, Femi Bello, Yuke Zhu, Roberto Martín-Martín
- **Date:** 2026-06-23
- **Source:** openalex
- **Relevance:** maybe (40/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** memory-policy
- **Abstract summary:** General-purpose robots operating in partially observable environments, such as homes, require memory to support autonomy. They must recall diverse information from the past, such as where objects were placed, which tasks a human partner has completed, and when an appliance was turned on. Achieving this versatility r...

### [OpenClaw and Ollama in Agentic AI: Toward Fully Autonomous and Scalable AI Agent Systems](https://www.semanticscholar.org/paper/7eaf69b789b1a23d054d86b4893519463abeb308)

- **Authors:** Konstantinos I. Roumeliotis, Ranjan Sapkota
- **Date:** 2026
- **Source:** semantic_scholar
- **Relevance:** maybe (40/100)
- **Reason:** Touches memory concepts that may be relevant if connected to agent behavior.
- **Tags:** long-term-memory
- **Abstract summary:** The rapid transition from reactive large language model (LLM) interfaces to persistent, action-capable systems has revealed fundamental gaps in the architectural understanding of Agentic AI, particularly in disentangling inference, orchestration, and execution layers. Despite significant progress, there remains a la...
