# Paper Scout Live Smoke Report - 2026-11-05

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 52
- **Unique papers:** 47
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 51
- Sample title: When Is Fresh AI Stock Analysis Worth It? Allocating a Limited Research Budget Across Price Updates, Deep Forecast Refreshes, and Editorial Reviews of Top Stock Picks
- Sample source ID: 2611.04348
- Sample URL: https://arxiv.org/abs/2611.04348v2
- Sample published date: 2026-11-03
- Abstract: yes

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-10-22&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

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

- relevant: 11
- maybe: 7
- irrelevant: 29

## Top Relevant Or Maybe Papers

- **Letting AI Formulate the Research Question: Autonomous Research Agents** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.39620v1
- **VerifiedLab: Harnessing Knowns for Unknowns** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.37923v1
- **Reimagining computational quantum research with AI scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.02833v1
- **PAPERBENCHX: Can AI Reproduce Science Across Disciplines?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.39744v1
- **IdeaTaste: Do LLMs Share the Research Taste of Human Researchers?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.03424v1
- **El Agente Fármaco: A Scalable AI Scientist for Drug Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.03832v1
- **Do AI Scientists Know What's New?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.36511v1
- **Agentic Systems for Calibrating Cosmological Simulations** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.40685v1
- **RubricAtlas: Mining Type-Level Rubrics from Expert Reports to Evaluate Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2610.36878v1
- **Novel or Not? PatEx-Gym: Agentic Prior-Art Search for Novelty Assessment in Patent Examination** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2610.33503v1

## Source Failures

- openalex (HTTP/API error) for `deep research agent`: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-10-22&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- arxiv:2611.03723: arxiv:2611.03723, arxiv:2611.03723
- arxiv:2610.41228: arxiv:2610.41228, arxiv:2610.41228
- arxiv:2611.02833: arxiv:2611.02833, arxiv:2611.02833
- arxiv:2610.39620: arxiv:2610.39620, arxiv:2610.39620, semantic_scholar:62a4038c8b0563c7b0b2359577a2bb39225561d6
