# Paper Scout Live Smoke Report - 2026-08-12

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 101
- **Unique papers:** 96
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
- Sample title: African Journal of Microbiology Research
- Sample source ID: W4248107455
- Sample URL: https://doi.org/10.5897/ajmr
- Sample published date: 2026-08-03
- Abstract: yes

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 1
- Sample title: EviGraph: Evidence-Guided Autonomous Research Agents
- Sample source ID: 84171611669441638d18bf3266065b796ed5cd5d
- Sample URL: https://www.semanticscholar.org/paper/84171611669441638d18bf3266065b796ed5cd5d
- Sample published date: 2026-08-05
- Abstract: yes


## Decisions

- relevant: 28
- maybe: 8
- irrelevant: 60

## Top Relevant Or Maybe Papers

- **An AI Scientist that Doesn't Drift: Taste, Structure, and Falsifiable Findings in a Quadruped Navigation Research Loop** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2608.07542
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **The Autonomous AI Scientist of 2030 Needs Inferential Arbitrage** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1145/3770855.3818657
- **Same Atomic Content, Different Falsification Histories: A causal protocol for testing whether AI scientists inherit falsification** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21758298
- **Same Atomic Content, Different Falsification Histories: A causal protocol for testing whether AI scientists inherit falsification** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21758297
- **Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding** (relevant, 93/100): Studies autonomous or deep research agents. https://doi.org/10.48550/arxiv.2608.05876
- **Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2608.05876
- **Google DeepMind and Edison Are Building the AI Scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1177/27681572261475914
- **An Independent Evaluation of AI Scientist v2 on Biomedical Research Tasks** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21754162

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- doi:10.1007/s11831-026-10738-w: openalex:W4414091311, openalex:W4414091311, openalex:W4414091311
- doi:10.1038/s43587-026-01186-z: openalex:W4407423733, openalex:W4407423733
- doi:10.26192/9xxqv: openalex:W107356373, openalex:W107356373
- openalex:W7172172436: openalex:W7172172436, openalex:W7172172436
