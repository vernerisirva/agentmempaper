# Paper Scout Live Smoke Report - 2026-08-07

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 250
- **Candidates fetched:** 156
- **Unique papers:** 147
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 55
- Sample title: Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding
- Sample source ID: 2608.05876
- Sample URL: https://arxiv.org/abs/2608.05876v1
- Sample published date: 2026-08-06
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Training Documents Reranker with Search Rubrics for Deep Research Agent
- Sample source ID: W7172495184
- Sample URL: https://doi.org/10.48550/arxiv.2608.03527
- Sample published date: 2026-08-04
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 1
- Sample title: EviGraph: Evidence-Guided Autonomous Research Agents
- Sample source ID: 84171611669441638d18bf3266065b796ed5cd5d
- Sample URL: https://www.semanticscholar.org/paper/84171611669441638d18bf3266065b796ed5cd5d
- Sample published date: 2026-08-05
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 29
- maybe: 7
- irrelevant: 111

## Top Relevant Or Maybe Papers

- **AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping** (relevant, 95/100): Studies automated literature-review systems or literature-review agents. https://doi.org/10.5281/zenodo.21523009
- **AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping** (relevant, 95/100): Studies automated literature-review systems or literature-review agents. https://doi.org/10.5281/zenodo.21523008
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **Same Atomic Content, Different Falsification Histories: A causal protocol for testing whether AI scientists inherit falsification** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21758298
- **Same Atomic Content, Different Falsification Histories: A causal protocol for testing whether AI scientists inherit falsification** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21758297
- **Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2608.05876v1
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2607.25865
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.25865v1
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.25865

## Source Failures

- semantic_scholar (HTTP/API error) for `AI scientist`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.04317: arxiv:2608.04317, arxiv:2608.04317
- arxiv:2607.27853: arxiv:2607.27853, arxiv:2607.27853
- arxiv:2607.27562: arxiv:2607.27562, arxiv:2607.27562
- arxiv:2608.04738: arxiv:2608.04738, semantic_scholar:84171611669441638d18bf3266065b796ed5cd5d
- doi:10.1002/widm.70111: openalex:W4390730779, openalex:W4390730779
- doi:10.1038/s43587-026-01186-z: openalex:W4407423733, openalex:W4407423733
- openalex:W7172172436: openalex:W7172172436, openalex:W7172172436
- doi:10.48550/arxiv.2607.27853: openalex:W7172007986, openalex:W7172007986
- openalex:W7171750087: openalex:W7171750087, openalex:W7171750087
