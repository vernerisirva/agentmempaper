# Paper Scout Live Smoke Report - 2026-09-08

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 153
- **Unique papers:** 142
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 53
- Sample title: APEx: Distillation of Agent Procedural Experience for Adaptive Deep Research Question Answering
- Sample source ID: 2609.02253
- Sample URL: https://arxiv.org/abs/2609.02253v1
- Sample published date: 2026-09-02
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: DualStake: Dual-Path Confidence Calibration in Deep Research Agents
- Sample source ID: W7206178088
- Sample URL: https://arxiv.org/abs/2609.00935
- Sample published date: 2026-09-01
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
- irrelevant: 111

## Top Relevant Or Maybe Papers

- **audit-closed-ai-scientist** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.18870260
- **Structurally-bounded Agentic Graph Exploration for Evidence-Grounded Scholarly DeepSearch** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2608.24809v1
- **Structurally-bounded Agentic Graph Exploration for Evidence-Grounded Scholarly DeepSearch** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2608.24809
- **RATIO: A Benchmark for Retrieval Across Typed Ideation Operations in Scientific Literature** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.27394v3
- **PaperGym: Rubric-Centered Evolution for Research-Plan Generation** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.31119v1
- **HypoForge: A Self-Improving Multi-Agent Framework for Automated Hypothesis Generation and Testing via Scientific Skill Learning** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.25770v1
- **Dr. Claw: An AI Scientist Workspace for Vibe Research** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.00365v1
- **Dr. Claw: An AI Scientist Workspace for Vibe Research** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.00365
- **Closing the Loop in AI-Driven Biomedical Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.20944/preprints202608.2107.v1
- **Beyond Execution: Auditing Experimental Fidelity in LLM-Driven Scientific Research** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.26753v1

## Source Failures

- semantic_scholar (HTTP/API error) for `deep research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.27912: arxiv:2608.27912, arxiv:2608.27912
- arxiv:2608.26701: arxiv:2608.26701, arxiv:2608.26701
- arxiv:2609.05079: arxiv:2609.05079, arxiv:2609.05079
- arxiv:2609.00365: arxiv:2609.00365, arxiv:2609.00365
- arxiv:2608.28490: arxiv:2608.28490, arxiv:2608.28490
- doi:10.5281/zenodo.22168098: openalex:W7204711696, openalex:W7204711696
- doi:10.5281/zenodo.22168097: openalex:W7204699780, openalex:W7204699780
- doi:10.1057/s41599-026-08832-2: openalex:W4414898195, openalex:W4414898195
- doi:10.1038/s42256-026-01296-8: openalex:W4386721710, openalex:W4386721710
- doi:10.1038/s41586-026-10950-5: openalex:W7205708811, openalex:W7205708811
- doi:10.1145/3845596: openalex:W4407310674, openalex:W4407310674
