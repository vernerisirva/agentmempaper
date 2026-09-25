# Paper Scout Live Smoke Report - 2026-09-25

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 100
- **Unique papers:** 97
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Agent READMEs: An Empirical Study of Context Files for Agentic Coding
- Sample source ID: W4416360710
- Sample URL: https://doi.org/10.1145/3840295
- Sample published date: 2026-09-15
- Abstract: yes

### semantic_scholar

- Status: Success - zero results
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 0


## Decisions

- relevant: 11
- maybe: 6
- irrelevant: 80

## Top Relevant Or Maybe Papers

- **PrimeScientist: Strategic Allocation of Research Effort in Autonomous Research** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.17846
- **Closing the Empirical Loop: Autonomous AI Agents Conduct End‐to‐end Research With Human Participants** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1002/advs.76675
- **AppliedScientist: Automated Scientific Revision Through Iterative AI Reviewing** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.14738
- **AI for Science with GPT-6 Astra: Thermal Design and Electrothermal Analysis of 2D CFET** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.17123
- **AI Scientists for Building Virtual-Cell Models** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.21203/rs.3.rs-10954762/v1
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide · v2 (typography)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854691
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide · v2 (typography)** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854690
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854324
- **AGI-CHOI JUNE의 편지 · 세계 AI 회사와 AI 과학·기술자 여러분께 · A Letter from AGI-CHOI JUNE · To AI Companies and Scientists Worldwide** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.22854323
- **A Closed-Loop Robot Scientist for Autonomous Biological Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.64898/2026.09.11.751076

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable

## Deduplication Examples

- doi:10.1145/3840295: openalex:W4416360710, openalex:W4416360710
- doi:10.1145/3845797: openalex:W4390529182, openalex:W4390529182
- doi:10.21203/rs.3.rs-10996966/v1: openalex:W7212260582, openalex:W7212260582
