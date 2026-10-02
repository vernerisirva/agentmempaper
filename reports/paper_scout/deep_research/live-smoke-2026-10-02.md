# Paper Scout Live Smoke Report - 2026-10-02

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 150
- **Candidates fetched:** 101
- **Unique papers:** 93
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: DeepRewind: Predicting and Repairing Premature Commitments in Deep Research Agents
- Sample source ID: W7214903403
- Sample URL: https://doi.org/10.48550/arxiv.2609.36344
- Sample published date: 2026-09-28
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 1
- Sample title: YouRA: A Persistent-State Architecture for Evidence-Traceable Autonomous Research Agents
- Sample source ID: a2f117bdfc10626be7e48df5eacd241f408c96e7
- Sample URL: https://www.semanticscholar.org/paper/a2f117bdfc10626be7e48df5eacd241f408c96e7
- Sample published date: 2026-10-01
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 15
- maybe: 9
- irrelevant: 69

## Top Relevant Or Maybe Papers

- **YouRA: A Persistent-State Architecture for Evidence-Traceable Autonomous Research Agents** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://www.semanticscholar.org/paper/a2f117bdfc10626be7e48df5eacd241f408c96e7
- **ScientistTwo Autonomous Research System Summary and Critical Assessment** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.70777/si.v3i3.18761
- **ScholarStack: Layered Research Asset Orchestration and Cross-Task Reuse for Scientific Agents** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2609.23735
- **Can AI Scientists Change Their Minds? Prior-Evidence Conflict in Synthetic Universes** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2609.36726
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide · v2 (typography)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854691
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide · v2 (typography)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854690
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854324
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854323
- **A Closed-Loop Robot Scientist for Autonomous Biological Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.64898/2026.09.11.751076
- **Too Far to Turn Back: Prior-Art Blindness Increases With Project Investment in Autonomous Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://doi.org/10.5281/zenodo.23023674

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- semantic_scholar (HTTP/API error) for `AI scientist`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- doi:10.48550/arxiv.2609.23986: openalex:W7213995952, openalex:W7213995952
- doi:10.5281/zenodo.23051403: openalex:W7214961531, openalex:W7214961531
- doi:10.5281/zenodo.23051404: openalex:W7214949777, openalex:W7214949777
- doi:10.1136/jme-2026-112004: openalex:W7130572291, openalex:W7130572291
- doi:10.1038/s41598-026-72525-8: openalex:W7213672938, openalex:W7213672938
- doi:10.1145/3829807.3829820: openalex:W4407091665, openalex:W4407091665
- doi:10.1117/1.ap.8.5.054003: openalex:W7214214533, openalex:W7214214533
- doi:10.1016/j.respol.2026.105598: openalex:W7106159402, openalex:W7106159402
