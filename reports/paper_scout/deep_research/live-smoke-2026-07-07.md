# Paper Scout Live Smoke Report - 2026-07-07

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 0
- **Sources failed:** 3
- **Raw records:** 25
- **Candidates fetched:** 25
- **Unique papers:** 25
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 25
- Sample title: Agent-Fence: Mapping Security Vulnerabilities Across Deep Research Agents
- Sample source ID: W7165677059
- Sample URL: https://doi.org/10.1609/aaaiss.v9i1.42945
- Sample published date: 2026-06-23
- Abstract: yes
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=deep+research+agents&filter=from_publication_date%3A2026-06-23&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 5
- maybe: 0
- irrelevant: 20

## Top Relevant Or Maybe Papers

- **Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. I. Uncertainty Quantification, ML on Therapeutic Data Commons, and Agent-Based Modeling** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.64898/2026.06.24.734302
- **DEEPMED Search: An Open-Source Agentic Platform for Medical Deep Research with Introspective Verification** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.48550/arxiv.2606.29746
- **DEEPMED Search: An Open-Source Agentic Platform for Medical Deep Research with Introspective Verification** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2606.29746
- **Checklist Rubric-Driven Iterative Control for Mitigating Context Drift in Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://doi.org/10.14801/jkiit.2026.24.6.1
- **Agent-Fence: Mapping Security Vulnerabilities Across Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://doi.org/10.1609/aaaiss.v9i1.42945

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- semantic_scholar (HTTP/API error) for `deep research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- openalex (HTTP/API error) for `deep research agents`: http error for https://api.openalex.org/works?search=deep+research+agents&filter=from_publication_date%3A2026-06-23&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- No duplicates found.
