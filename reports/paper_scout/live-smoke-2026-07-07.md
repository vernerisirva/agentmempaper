# Paper Scout Live Smoke Report - 2026-07-07

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 0
- **Sources failed:** 3
- **Raw records:** 161
- **Candidates fetched:** 89
- **Unique papers:** 50
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 22
- Raw records: 136
- Converted candidates: 64
- Sample title: Your Agent's Memories Are Not Its Own: Forged Reasoning Attacks on LLM Agent Memory and Defenses
- Sample source ID: 2607.05029
- Sample URL: https://arxiv.org/abs/2607.05029v1
- Sample published date: 2026-07-06
- Abstract: yes
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22memory+consolidation+LLM+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 25
- Sample title: Beyond Retrieval: Layered Epistemic Agent Protocol for Memory Coherence
- Sample source ID: W7166574053
- Sample URL: https://doi.org/10.5281/zenodo.21029662
- Sample published date: 2026-06-29
- Abstract: yes
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=agentic+memory&filter=from_publication_date%3A2026-06-23&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 27
- maybe: 13
- irrelevant: 10

## Top Relevant Or Maybe Papers

- **Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.24322v1
- **MemoryBioRAG: A Reproducible Methodology for Vector-Free Biomimetic Agent Memory Using Conceptual Spaces and Synaptic Graphs on SQLite** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.21204978
- **MemoryBioRAG: A Reproducible Methodology for Vector-Free Biomimetic Agent Memory Using Conceptual Spaces and Synaptic Graphs on SQLite** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.21204977
- **Are We Ready For An Agent-Native Memory System?** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.24775v1
- **Are We Ready For An Agent-Native Memory System?** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.24775
- **A-TMA: Decoupling State-Aware Memory Failures in Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2607.01935
- **A-TMA: Decoupling State-Aware Memory Failures in Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.01935v1
- **A-TMA: Decoupling State-Aware Memory Failures in Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.01935
- **MemDelta: Controlled Baselines and Hidden Confounds in Agent Memory Evaluation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.48550/arxiv.2606.29914
- **MemDelta: Controlled Baselines and Hidden Confounds in Agent Memory Evaluation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2606.29914v1

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- openalex (HTTP/API error) for `agentic memory`: http error for https://api.openalex.org/works?search=agentic+memory&filter=from_publication_date%3A2026-06-23&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- arxiv (HTTP/API error) for `memory consolidation LLM agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22memory+consolidation+LLM+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- arxiv:2607.05029: arxiv:2607.05029, arxiv:2607.05029, arxiv:2607.05029
- arxiv:2607.04391: arxiv:2607.04391, arxiv:2607.04391
- arxiv:2607.04089: arxiv:2607.04089, arxiv:2607.04089
- arxiv:2607.03726: arxiv:2607.03726, arxiv:2607.03726
- arxiv:2607.01935: arxiv:2607.01935, arxiv:2607.01935
- arxiv:2607.01916: arxiv:2607.01916, arxiv:2607.01916
- arxiv:2607.01709: arxiv:2607.01709, arxiv:2607.01709
- arxiv:2607.01071: arxiv:2607.01071, arxiv:2607.01071
- arxiv:2607.02579: arxiv:2607.02579, arxiv:2607.02579
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
