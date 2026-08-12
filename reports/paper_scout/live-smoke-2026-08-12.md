# Paper Scout Live Smoke Report - 2026-08-12

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 125
- **Candidates fetched:** 29
- **Unique papers:** 29
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 25
- Sample title: R4DSG: Relative 4D Scene Graph Memory for Object-Centric Question Answering in Long Egocentric Video
- Sample source ID: 2608.11017
- Sample URL: https://arxiv.org/abs/2608.11017v1
- Sample published date: 2026-08-11
- Abstract: yes
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-07-29&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 4
- Sample title: Activation-Guided Neuron Intervention to Induce Alzheimer's-Related Computational Language Phenotypes in a Large Language Model
- Sample source ID: b5233936e6221a748c0bb73139ed33cb35a84580
- Sample URL: https://www.semanticscholar.org/paper/b5233936e6221a748c0bb73139ed33cb35a84580
- Sample published date: 2026-08-04
- Abstract: yes


## Decisions

- relevant: 5
- maybe: 5
- irrelevant: 19

## Top Relevant Or Maybe Papers

- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775v1
- **From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.10502v1
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://www.semanticscholar.org/paper/ef80169359a279f206b2dcc012b3100bc4fe8de1
- **Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2608.10357v1
- **ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://www.semanticscholar.org/paper/57563394951aebb6d7f5611808eac0ba14a5bb87
- **On Understanding, Identifying, and Mitigating Vulnerabilities in Agentic Large Language Models** (maybe, 62/100): Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory. https://arxiv.org/abs/2608.10530v1
- **MESA:Task-Adaptive Multi-Structure Evidence Selection for Long-Horizon Agent Memory** (maybe, 45/100): Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory. https://arxiv.org/abs/2608.10108v1
- **Learning Preference Adaptation for Large Language Model Personalization via Verbal Reinforcement Learning** (maybe, 45/100): Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory. https://arxiv.org/abs/2608.09507v1
- **ComBodied Agents: a New Paradigm of Human-Centric Agentic AI** (maybe, 45/100): Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory. https://arxiv.org/abs/2608.10915v1
- **MemCollab: Cross-Agent Memory Collaboration via Contrastive Trajectory Distillation** (maybe, 43/100): Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory. https://www.semanticscholar.org/paper/8f7789628df0f85cb0f54e60861b6fa3c3b3d1ec

## Source Failures

- arxiv (HTTP/API error) for `procedural memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aprocedural+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- openalex (HTTP/API error) for `agent memory`: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-07-29&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- No duplicates found.
