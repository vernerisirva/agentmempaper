# Paper Scout Live Smoke Report - 2026-09-28

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 100
- **Candidates fetched:** 4
- **Unique papers:** 4
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-09-14&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 4
- Sample title: ProMem-agent: Procedural memory-augmented large language model agents for clinical trajectory reasoning.
- Sample source ID: 1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
- Sample URL: https://www.semanticscholar.org/paper/1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
- Sample published date: 2026-09-17
- Abstract: no


## Decisions

- relevant: 3
- maybe: 1
- irrelevant: 0

## Top Relevant Or Maybe Papers

- **RPMem: Learning Long-Term Recurrent Parametric Memory Across Sessions for LLM Agents** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://www.semanticscholar.org/paper/d84232d26104a0f9ad8acce504a732c50f1cfe41
- **ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://www.semanticscholar.org/paper/57563394951aebb6d7f5611808eac0ba14a5bb87
- **ProMem-agent: Procedural memory-augmented large language model agents for clinical trajectory reasoning.** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://www.semanticscholar.org/paper/1f4a4a482f4b028ab8522ab614b69bb37c7b4fb0
- **Designer-RSI: Evolving Procedural Memory from User Traffic for Agentic Graphic Design** (maybe, 62/100): Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory. https://www.semanticscholar.org/paper/9c5233012d0a37e45f8e3a28beabe595c01d0bfd

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex (HTTP/API error) for `agent memory`: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-09-14&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable

## Deduplication Examples

- No duplicates found.
