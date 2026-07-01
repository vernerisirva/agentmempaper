# Paper Scout Live Smoke Report - 2026-07-01

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 0
- **Sources failed:** 3
- **Raw records:** 135
- **Candidates fetched:** 66
- **Unique papers:** 26
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 21
- Raw records: 135
- Converted candidates: 66
- Sample title: What Memory Do GUI Agents Really Need? From Passive Records to Active Task-Driving States
- Sample source ID: 2606.31612
- Sample URL: https://arxiv.org/abs/2606.31612v1
- Sample published date: 2026-06-30
- Abstract: yes
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22memory+retrieval+LLM+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-06-17&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.semanticscholar.org/graph/v1/paper/search?query=agent+memory&limit=25&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds: request failed after 3 attempts: HTTP Error 500: Internal Server Error


## Decisions

- relevant: 14
- maybe: 9
- irrelevant: 3

## Top Relevant Or Maybe Papers

- **Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.24322v1
- **AtomMem: Building Simple and Effective Memory System for LLM Agents via Atomic Facts** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2606.19847v1
- **Are We Ready For An Agent-Native Memory System?** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.24775v1
- **Nous: A Predictive World Model for Long-Term Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.22030v1
- **MemDelta: Controlled Baselines and Hidden Confounds in Agent Memory Evaluation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.29914v1
- **Mandol: An Agglomerative Agent Memory System for Long-Term Conversations** (relevant, 99/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2606.29778v1
- **RaMem: Contextual Reinstatement for Long-term Agentic Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2606.22844v1
- **Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2606.29824v1
- **MEMPROBE: Probing Long-Term Agent Memory via Hidden User-State Recovery** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2606.24595v1
- **Forensic Trajectory Signatures for Agent Memory Poisoning Detection** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2606.30566v1

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: http error for https://api.semanticscholar.org/graph/v1/paper/search?query=agent+memory&limit=25&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds: request failed after 3 attempts: HTTP Error 500: Internal Server Error
- openalex (HTTP/API error) for `agent memory`: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-06-17&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable
- arxiv (HTTP/API error) for `memory retrieval LLM agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22memory+retrieval+LLM+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- arxiv:2606.31612: arxiv:2606.31612, arxiv:2606.31612
- arxiv:2606.30566: arxiv:2606.30566, arxiv:2606.30566
- arxiv:2606.29914: arxiv:2606.29914, arxiv:2606.29914, arxiv:2606.29914, arxiv:2606.29914
- arxiv:2606.29824: arxiv:2606.29824, arxiv:2606.29824
- arxiv:2606.29788: arxiv:2606.29788, arxiv:2606.29788
- arxiv:2606.29778: arxiv:2606.29778, arxiv:2606.29778, arxiv:2606.29778, arxiv:2606.29778
- arxiv:2606.29774: arxiv:2606.29774, arxiv:2606.29774
- arxiv:2606.28781: arxiv:2606.28781, arxiv:2606.28781, arxiv:2606.28781, arxiv:2606.28781
- arxiv:2606.27499: arxiv:2606.27499, arxiv:2606.27499, arxiv:2606.27499, arxiv:2606.27499
- arxiv:2606.26627: arxiv:2606.26627, arxiv:2606.26627
- arxiv:2606.25206: arxiv:2606.25206, arxiv:2606.25206, arxiv:2606.25206, arxiv:2606.25206
- arxiv:2606.25115: arxiv:2606.25115, arxiv:2606.25115
- arxiv:2606.24775: arxiv:2606.24775, arxiv:2606.24775, arxiv:2606.24775, arxiv:2606.24775
- arxiv:2606.24595: arxiv:2606.24595, arxiv:2606.24595
- arxiv:2606.24535: arxiv:2606.24535, arxiv:2606.24535
- arxiv:2606.24322: arxiv:2606.24322, arxiv:2606.24322, arxiv:2606.24322
- arxiv:2606.23195: arxiv:2606.23195, arxiv:2606.23195
- arxiv:2606.22844: arxiv:2606.22844, arxiv:2606.22844
- arxiv:2606.22263: arxiv:2606.22263, arxiv:2606.22263
- arxiv:2606.22030: arxiv:2606.22030, arxiv:2606.22030
- arxiv:2606.21649: arxiv:2606.21649, arxiv:2606.21649, arxiv:2606.21649, arxiv:2606.21649
- arxiv:2606.21562: arxiv:2606.21562, arxiv:2606.21562
- arxiv:2606.20954: arxiv:2606.20954, arxiv:2606.20954
- arxiv:2606.20515: arxiv:2606.20515, arxiv:2606.20515
- arxiv:2606.19857: arxiv:2606.19857, arxiv:2606.19857
