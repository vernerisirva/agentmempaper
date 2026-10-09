# Paper Scout Live Smoke Report - 2026-10-09

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 103
- **Unique papers:** 99
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
- Sample URL: https://arxiv.org/abs/2609.36344
- Sample published date: 2026-09-28
- Abstract: yes

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 3
- Sample title: EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution
- Sample source ID: c25f73c2268bc40010c3e6fbc1a678ec99d7cf88
- Sample URL: https://www.semanticscholar.org/paper/c25f73c2268bc40010c3e6fbc1a678ec99d7cf88
- Sample published date: 2026-10-03
- Abstract: yes


## Decisions

- relevant: 23
- maybe: 5
- irrelevant: 71

## Top Relevant Or Maybe Papers

- **YouRA: A Persistent-State Architecture for Evidence-Traceable Autonomous Research Agents** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://www.semanticscholar.org/paper/a2f117bdfc10626be7e48df5eacd241f408c96e7
- **YouRA: A Persistent-State Architecture for Evidence-Traceable Autonomous Research Agents** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.01097
- **LawCompass: Navigating from Legal QA to Multi-Agent Deep Research with Grounded Evidence** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2610.01027
- **EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://www.semanticscholar.org/paper/c25f73c2268bc40010c3e6fbc1a678ec99d7cf88
- **EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2610.04517
- **Are We Measuring Scientific Intelligence? Rethinking the Evaluation of AI Scientists** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.04915
- **The more you automate, the less you see: Hidden pitfalls of autonomous AI scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1073/pnas.2610214123
- **ScientistTwo Autonomous Research System Summary and Critical Assessment** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.70777/si.v3i3.18761
- **Just-In-Time Agent Memory with Runtime Agentic Research** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2609.34385
- **From Scientific Observations to Mechanisms: Benchmarking Hypothesis Generation by AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.05197

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- doi:10.5281/zenodo.23051403: openalex:W7214949777, openalex:W7214949777
- doi:10.48550/arxiv.2610.04517: openalex:W7220652748, openalex:W7220652748
- doi:10.48550/arxiv.2610.01097: openalex:W7215909366, openalex:W7215909366
- doi:10.3389/fgene.2026.1954843: openalex:W7220861580, openalex:W7220861580
