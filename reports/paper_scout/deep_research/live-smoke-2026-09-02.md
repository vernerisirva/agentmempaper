# Paper Scout Live Smoke Report - 2026-09-02

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 154
- **Unique papers:** 144
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 54
- Sample title: Explore Before Committing: Hypothesis-Guided Search for Deep Research Agents
- Sample source ID: 2609.01294
- Sample URL: https://arxiv.org/abs/2609.01294v1
- Sample published date: 2026-09-01
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: From Inertia to Objectivity: Improving Deep Research Agents with Noise Isolation
- Sample source ID: W7204199332
- Sample URL: https://arxiv.org/abs/2608.23045
- Sample published date: 2026-08-24
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 33
- maybe: 5
- irrelevant: 106

## Top Relevant Or Maybe Papers

- **Method of Working with AI in Creating Scientific Articles: Algorithm, Criteria, and Practice** (relevant, 98/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.5281/zenodo.22148513
- **Method of Working with AI in Creating Scientific Articles: Algorithm, Criteria, and Practice** (relevant, 98/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.5281/zenodo.22148512
- **audit-closed-ai-scientist** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://github.com/kadubon/audit-closed-ai-scientist/tree/v0.2.0
- **Who Co-Authors the Future? Globalisation, Translation Politics, and Narrative Power in Waste Tide and AI 2041** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1080/02560046.2026.2675416
- **Symposium: Trust via Auditable Records for Communities of AI Scientist Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.19511v1
- **Symposium: Trust via Auditable Records for Communities of AI Scientist Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.19511
- **Structurally-bounded Agentic Graph Exploration for Evidence-Grounded Scholarly DeepSearch** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2608.24809v1
- **Structurally-bounded Agentic Graph Exploration for Evidence-Grounded Scholarly DeepSearch** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2608.24809
- **Science Done on a Machine by a Machine: AI Agents in Computational Chemistry** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.18508v1
- **Science Done on a Machine by a Machine: AI Agents in Computational Chemistry** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.18508

## Source Failures

- semantic_scholar (HTTP/API error) for `deep research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.27912: arxiv:2608.27912, arxiv:2608.27912
- arxiv:2608.26701: arxiv:2608.26701, arxiv:2608.26701
- arxiv:2609.00365: arxiv:2609.00365, arxiv:2609.00365
- arxiv:2608.28490: arxiv:2608.28490, arxiv:2608.28490
- arxiv:2608.23336: arxiv:2608.23336, arxiv:2608.23336
- doi:10.5281/zenodo.22168098: openalex:W7204711696, openalex:W7204711696
- doi:10.5281/zenodo.22168097: openalex:W7204699780, openalex:W7204699780
- doi:10.1038/s42256-026-01296-8: openalex:W4386721710, openalex:W4386721710
- doi:10.1504/ijhm.2026.154223: openalex:W7165131551, openalex:W7165131551
- doi:10.1145/3841472: openalex:W4392677943, openalex:W4392677943
