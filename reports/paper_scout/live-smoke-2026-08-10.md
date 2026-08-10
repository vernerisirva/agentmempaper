# Paper Scout Live Smoke Report - 2026-08-10

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 103
- **Unique papers:** 98
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: Timeout/network error: timeout error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-08-02
- Abstract: yes

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 3
- Sample title: Activation-Guided Neuron Intervention to Induce Alzheimer's-Related Computational Language Phenotypes in a Large Language Model
- Sample source ID: b5233936e6221a748c0bb73139ed33cb35a84580
- Sample URL: https://www.semanticscholar.org/paper/b5233936e6221a748c0bb73139ed33cb35a84580
- Sample published date: 2026-08-04
- Abstract: yes


## Decisions

- relevant: 19
- maybe: 11
- irrelevant: 68

## Top Relevant Or Maybe Papers

- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2607.29032
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2607.27080
- **MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.27080
- **ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2607.27773
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://www.semanticscholar.org/paper/ef80169359a279f206b2dcc012b3100bc4fe8de1
- **MutMem: Cryptographically Authorized Mutation in Persistent Agent Memory** (relevant, 99/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.48550/arxiv.2608.02843
- **MutMem: Cryptographically Authorized Mutation in Persistent Agent Memory** (relevant, 99/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2608.02843
- **Metis: Memory Foundation Model** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2607.26760
- **MemTX: Transactional Belief Commit for Stateful Agent Memory** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.48550/arxiv.2607.23929

## Source Failures

- arxiv (Timeout/network error) for `agent memory`: timeout error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out

## Deduplication Examples

- doi:10.1145/3831684: openalex:W4405562150, openalex:W4405562150
- openalex:W7171902691: openalex:W7171902691, openalex:W7171902691
- openalex:W7197053160: openalex:W7197053160, openalex:W7197053160
- openalex:W7172474001: openalex:W7172474001, openalex:W7172474001
- doi:10.48550/arxiv.2607.29032: openalex:W7172337063, openalex:W7172337063
