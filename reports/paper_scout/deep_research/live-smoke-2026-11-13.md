# Paper Scout Live Smoke Report - 2026-11-13

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 150
- **Unique papers:** 149
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 50
- Sample title: From Delegation to Coordination: Learning Efficient Multi-Agent Deep Research
- Sample source ID: 2611.17041
- Sample URL: https://arxiv.org/abs/2611.17041v1
- Sample published date: 2026-11-12
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Mind2Report: Expert-Level Commercial Report Synthesis via Cognitive Deep Research Agent
- Sample source ID: W7119689058
- Sample URL: https://doi.org/10.1145/3799682.3840672
- Sample published date: 2026-11-03
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 23
- maybe: 8
- irrelevant: 118

## Top Relevant Or Maybe Papers

- **Does an Open Targets dossier skill help an AI scientist agent? An OpenScientist experiment** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.24026258
- **The Harness Is the Lab: Measured Self-Improvement for Ontology-Grounded AI Scientists** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.24144799
- **Sage-Taiyi: A Metacognitive Architecture for Scientific Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.12762v1
- **Reimagining computational quantum research with AI scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.02833v1
- **Reimagining computational quantum research with AI scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.02833
- **IdeaTaste: Do LLMs Share the Research Taste of Human Researchers?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.03424v1
- **IdeaTaste: Do LLMs Share the Research Taste of Human Researchers?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.03424
- **ExpEvolve: Structuring and Reusing Experience for Open-Ended Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.66977/xsci.2611.0004
- **EvoNova Scientist: A Neuro-Symbolic Multi-Agent Framework for Physical Constraint-Preserving Autonomous Scientific Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.23942796
- **El Agente Fármaco: A Scalable AI Scientist for Drug Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.03832v1

## Source Failures

- semantic_scholar (HTTP/API error) for `deep research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.02833: arxiv:2611.02833, arxiv:2611.02833
