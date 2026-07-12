# Paper Scout Live Smoke Report - 2026-07-12

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 1087
- **Candidates fetched:** 74
- **Unique papers:** 33
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 18
- Raw records: 137
- Converted candidates: 46
- Sample title: What to Keep, What to Forget: A Rate--Distortion View of Memory Compaction in LLMs and Agents
- Sample source ID: 2607.08032
- Sample URL: https://arxiv.org/abs/2607.08032v1
- Sample published date: 2026-07-09
- Abstract: yes
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22memory+module+LLM+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-06-28&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success
- Queries attempted: 38
- Raw records: 950
- Converted candidates: 28
- Sample title: Your Agent's Memories Are Not Its Own: Forged Reasoning Attacks on LLM Agent Memory and Defenses
- Sample source ID: 25de4e59b61dc7b659a16ba7a5ca60fc7cee940a
- Sample URL: https://www.semanticscholar.org/paper/25de4e59b61dc7b659a16ba7a5ca60fc7cee940a
- Sample published date: 2026-07-06
- Abstract: yes


## Decisions

- relevant: 8
- maybe: 13
- irrelevant: 12

## Top Relevant Or Maybe Papers

- **A-TMA: Decoupling State-Aware Memory Failures in Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.01935v2
- **MemDelta: Controlled Baselines and Hidden Confounds in Agent Memory Evaluation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.29914v1
- **Mandol: An Agglomerative Agent Memory System for Long-Term Conversations** (relevant, 99/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2606.29778v1
- **Your Agent's Memories Are Not Its Own: Forged Reasoning Attacks on LLM Agent Memory and Defenses** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.05029v1
- **When Claws Remember but Do Not Tell: Stealthy Memory Injection in Persistent Personal Agents** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://www.semanticscholar.org/paper/6588cc046337c7f7d219b43965f38e6553daacfc
- **Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2606.29824v1
- **Forensic Trajectory Signatures for Agent Memory Poisoning Detection** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2606.30566v1
- **PLACEMEM: Toward a Compute-Aware Memory Plane for Lifelong Agents** (relevant, 90/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2607.04089v1
- **When Agents Remember Too Much: Memory Poisoning Attacks on Large Language Model Agents** (maybe, 62/100): Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory. https://arxiv.org/abs/2607.06595v1
- **What to Keep, What to Forget: A Rate--Distortion View of Memory Compaction in LLMs and Agents** (maybe, 62/100): Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory. https://arxiv.org/abs/2607.08032v1

## Source Failures

- openalex (HTTP/API error) for `agent memory`: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-06-28&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- arxiv (HTTP/API error) for `memory module LLM agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22memory+module+LLM+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- arxiv:2607.08032: arxiv:2607.08032, arxiv:2607.08032
- arxiv:2607.06595: arxiv:2607.06595, arxiv:2607.06595, arxiv:2607.06595
- arxiv:2607.05577: arxiv:2607.05577, arxiv:2607.05577, arxiv:2607.05577, arxiv:2607.05577
- arxiv:2607.05029: arxiv:2607.05029, arxiv:2607.05029, arxiv:2607.05029, semantic_scholar:25de4e59b61dc7b659a16ba7a5ca60fc7cee940a, semantic_scholar:25de4e59b61dc7b659a16ba7a5ca60fc7cee940a
- arxiv:2607.04391: arxiv:2607.04391, arxiv:2607.04391
- arxiv:2607.04089: arxiv:2607.04089, arxiv:2607.04089
- arxiv:2607.03726: arxiv:2607.03726, arxiv:2607.03726
- arxiv:2607.01935: arxiv:2607.01935, arxiv:2607.01935
- arxiv:2607.01916: arxiv:2607.01916, arxiv:2607.01916
- arxiv:2607.01709: arxiv:2607.01709, arxiv:2607.01709
- arxiv:2607.01071: arxiv:2607.01071, arxiv:2607.01071
- arxiv:2607.02579: arxiv:2607.02579, arxiv:2607.02579, semantic_scholar:4fb25898ca80ee688df1096f87ab779fa5adaf92
- arxiv:2606.31612: arxiv:2606.31612, arxiv:2606.31612
- arxiv:2606.30566: arxiv:2606.30566, arxiv:2606.30566
- arxiv:2606.29914: arxiv:2606.29914, arxiv:2606.29914, arxiv:2606.29914, arxiv:2606.29914, semantic_scholar:e188192b0740b7f057f24700093d30e47c7c97f0
- arxiv:2606.29824: arxiv:2606.29824, arxiv:2606.29824, semantic_scholar:05c11d86a4b91c94b0178c1b5f80340720a5bfec
- arxiv:2606.29788: arxiv:2606.29788, arxiv:2606.29788
- arxiv:2606.29778: arxiv:2606.29778, arxiv:2606.29778, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8, arxiv:2606.29778, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8, arxiv:2606.29778, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8, semantic_scholar:7c31c2a517bcab53fd7c6d2767c3f53356e5bdb8
- arxiv:2606.29774: arxiv:2606.29774, arxiv:2606.29774
- arxiv:2606.30639: semantic_scholar:4a397b42a1352f4a67938b84d3332382b0c7bdea, semantic_scholar:4a397b42a1352f4a67938b84d3332382b0c7bdea
- semantic_scholar:16086f872f1c52a6a5ea2c7ce7ac79b026c2b3c7: semantic_scholar:16086f872f1c52a6a5ea2c7ce7ac79b026c2b3c7, semantic_scholar:16086f872f1c52a6a5ea2c7ce7ac79b026c2b3c7
- doi:10.48550/arxiv.2603.14864: semantic_scholar:b3e7ab1bc79d25997b391e500f72bc0a3cfbed06, semantic_scholar:b3e7ab1bc79d25997b391e500f72bc0a3cfbed06
- arxiv:2607.07666: semantic_scholar:bef4f8d6f6d71354ded8c081cfbfb2ddb2641b4b, semantic_scholar:bef4f8d6f6d71354ded8c081cfbfb2ddb2641b4b
