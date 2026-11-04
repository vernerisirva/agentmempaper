# Paper Scout Live Smoke Report - 2026-11-04

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 225
- **Candidates fetched:** 82
- **Unique papers:** 77
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 56
- Sample title: When Is Fresh AI Stock Analysis Worth It? Allocating a Limited Research Budget Across Price Updates, Deep Forecast Refreshes, and Editorial Reviews of Top Stock Picks
- Sample source ID: 2611.04348
- Sample URL: https://arxiv.org/abs/2611.04348v1
- Sample published date: 2026-11-03
- Abstract: yes

### openalex

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 25
- Sample title: Mind2Report: Expert-Level Commercial Report Synthesis via Cognitive Deep Research Agent
- Sample source ID: W7119689058
- Sample URL: https://doi.org/10.1145/3799682.3840672
- Sample published date: 2026-11-03
- Abstract: yes
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=autonomous+research+agent&filter=from_publication_date%3A2026-10-21&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 1
- Sample title: Letting AI Formulate the Research Question: Autonomous Research Agents
- Sample source ID: 62a4038c8b0563c7b0b2359577a2bb39225561d6
- Sample URL: https://www.semanticscholar.org/paper/62a4038c8b0563c7b0b2359577a2bb39225561d6
- Sample published date: 2026-10-29
- Abstract: yes


## Decisions

- relevant: 20
- maybe: 9
- irrelevant: 48

## Top Relevant Or Maybe Papers

- **Letting AI Formulate the Research Question: Autonomous Research Agents** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.39620v1
- **Letting AI Formulate the Research Question: Autonomous Research Agents** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.39620
- **VerifiedLab: Harnessing Knowns for Unknowns** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.37923v1
- **Reimagining computational quantum research with AI scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.02833v1
- **PAPERBENCHX: Can AI Reproduce Science Across Disciplines?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.39744v1
- **IdeaTaste: Do LLMs Share the Research Taste of Human Researchers?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.03424v1
- **ExpEvolve: Structuring and Reusing Experience for Open-Ended Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.29303v1
- **El Agente Fármaco: A Scalable AI Scientist for Drug Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.03832v1
- **Do AI Scientists Know What's New?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.36511v1
- **Agentic Systems for Calibrating Cosmological Simulations** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.40685v1

## Source Failures

- openalex (HTTP/API error) for `autonomous research agent`: http error for https://api.openalex.org/works?search=autonomous+research+agent&filter=from_publication_date%3A2026-10-21&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- arxiv:2611.03723: arxiv:2611.03723, arxiv:2611.03723
- arxiv:2610.41228: arxiv:2610.41228, arxiv:2610.41228
- arxiv:2611.02833: arxiv:2611.02833, arxiv:2611.02833
- arxiv:2610.39620: arxiv:2610.39620, arxiv:2610.39620, semantic_scholar:62a4038c8b0563c7b0b2359577a2bb39225561d6
