# Paper Scout Live Smoke Report - 2026-07-12

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 0
- **Sources failed:** 3
- **Raw records:** 625
- **Candidates fetched:** 11
- **Unique papers:** 10
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
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-06-28&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Failed
- Queries attempted: 26
- Raw records: 625
- Converted candidates: 11
- Sample title: Clarus: Coordinating Autonomous Research Agents toward Web-Scale Scientific Collaboration
- Sample source ID: e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample URL: https://www.semanticscholar.org/paper/e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample published date: 2026-06-29
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 3
- maybe: 2
- irrelevant: 5

## Top Relevant Or Maybe Papers

- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://www.semanticscholar.org/paper/8b5edab1fd875d24c9aed5f088f6ea3656bdd78c
- **Minos: A Multi-Agent Collaborative Framework for Provenance-Based Backward Tracking** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://www.semanticscholar.org/paper/25ec27ac37209016869d85dfe961fff9c484a23d
- **Clarus: Coordinating Autonomous Research Agents toward Web-Scale Scientific Collaboration** (relevant, 91/100): Studies autonomous or deep research agents. https://www.semanticscholar.org/paper/e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- **SEGMENTAÇÃO LINEAR HOMOGÊNEA DE PAVIMENTOS: COMPARAÇÃO ENTRE MÉTODOS CLÁSSICOS, CLUSTERING WARD 1D E PELT COM AUTORESEARCH** (maybe, 51/100): Review candidate: may support deep research workflows but needs human judgment. https://www.semanticscholar.org/paper/bb4010c89b8edcdd1aa638740c696fb744dbe103
- **ACSS-PSL at #SMM4H-HeaRD 2026: An LLM-Driven Autoresearch Loop for Opioid-Impact NER** (maybe, 51/100): Review candidate: may support deep research workflows but needs human judgment. https://www.semanticscholar.org/paper/7522887867a6b88399228e535e5bdd45dd2609e6

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- openalex (HTTP/API error) for `deep research agent`: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-06-28&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- semantic_scholar (HTTP/API error) for `scientific discovery LLM agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2606.30246: semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1, semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1
