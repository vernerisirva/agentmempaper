# Paper Scout Live Smoke Report - 2026-08-22

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 150
- **Unique papers:** 139
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 50
- Sample title: A Comprehensive Review of Large Language Models for Nanophotonics: From Surrogate Modeling to Autonomous Design
- Sample source ID: 2608.18279
- Sample URL: https://arxiv.org/abs/2608.18279v1
- Sample published date: 2026-08-18
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Not Worth Another Token: Marginal Value Estimation for Efficient Deep Research Agents
- Sample source ID: W7202203446
- Sample URL: https://arxiv.org/abs/2608.08389
- Sample published date: 2026-08-09
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 27
- maybe: 16
- irrelevant: 96

## Top Relevant Or Maybe Papers

- **SGHA: Evidence-Grounded Research Problem Discovery with Local Language Models** (relevant, 98/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2608.17501v1
- **The AI scientist arrives: a new epoch in autonomous discovery** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.66178/aie-0026-0017
- **OmniScientist: An Omni-Modal Omni-Discipline AI Scientist** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.13558v1
- **OmniScientist: An Omni-Modal Omni-Discipline AI Scientist** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.13558
- **What Constitutes an Omni-Modal Omni- Discipline AI Scientist -And What Good Is He?** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.13140/rg.2.2.25199.80804
- **Training AI Scientists to Replicate Research** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.13331v1
- **Training AI Scientists to Replicate Research** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.13331
- **The Past and Future of AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.14407v1
- **The Past and Future of AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.14407
- **The Landscape of LLM-based Search Agents: A Survey** (relevant, 93/100): Studies autonomous or deep research agents. https://doi.org/10.20944/preprints202608.0572.v1

## Source Failures

- semantic_scholar (HTTP/API error) for `deep research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.18279: arxiv:2608.18279, arxiv:2608.18279
- arxiv:2608.18034: arxiv:2608.18034, arxiv:2608.18034
- arxiv:2608.14747: arxiv:2608.14747, arxiv:2608.14747
- arxiv:2608.10714: arxiv:2608.10714, arxiv:2608.10714
- arxiv:2608.13558: arxiv:2608.13558, arxiv:2608.13558
- doi:10.1016/j.neucom.2026.134793: openalex:W4415346766, openalex:W4415346766
- doi:10.1371/journal.pcsy.0000120: openalex:W7118930316, openalex:W7118930316
- doi:10.48550/arxiv.2608.11195: openalex:W7202259539, openalex:W7202259539
- doi:10.5445/ir/32582000: openalex:W1564124598, openalex:W1564124598
- openalex:W7167446164: openalex:W7167446164, openalex:W7167446164
- doi:10.66178/aie-0026-0017: openalex:W7203458829, openalex:W7203458829
