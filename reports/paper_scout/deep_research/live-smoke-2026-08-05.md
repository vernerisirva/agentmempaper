# Paper Scout Live Smoke Report - 2026-08-05

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 250
- **Candidates fetched:** 153
- **Unique papers:** 144
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 53
- Sample title: Training Documents Reranker with Search Rubrics for Deep Research Agent
- Sample source ID: 2608.03527
- Sample URL: https://arxiv.org/abs/2608.03527v1
- Sample published date: 2026-08-04
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Exploring Large Language Model‐Based Intelligent Agents: Definitions, Methods, and Prospects
- Sample source ID: W4390730779
- Sample URL: https://doi.org/10.1002/widm.70111
- Sample published date: 2026-07-24
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 30
- maybe: 8
- irrelevant: 106

## Top Relevant Or Maybe Papers

- **AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping** (relevant, 95/100): Studies automated literature-review systems or literature-review agents. https://doi.org/10.5281/zenodo.21523009
- **AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping** (relevant, 95/100): Studies automated literature-review systems or literature-review agents. https://doi.org/10.5281/zenodo.21523008
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **Same Atomic Content, Different Falsification Histories: A causal protocol for testing whether AI scientists inherit falsification** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21758298
- **Same Atomic Content, Different Falsification Histories: A causal protocol for testing whether AI scientists inherit falsification** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21758297
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2607.25865
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.25865v1
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.25865
- **LegalCiteTrust: Benchmarking Citation Trustworthiness in Chinese Long-Form Legal Research Reports** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2607.20872v1

## Source Failures

- semantic_scholar (HTTP/API error) for `AI scientist`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2607.27853: arxiv:2607.27853, arxiv:2607.27853
- arxiv:2607.27562: arxiv:2607.27562, arxiv:2607.27562
- arxiv:2607.27435: arxiv:2607.27435, arxiv:2607.27435
- doi:10.1002/widm.70111: openalex:W4390730779, openalex:W4390730779
- doi:10.1016/j.chbr.2026.101220: openalex:W4417084818, openalex:W4417084818, openalex:W4417084818
- doi:10.1038/s43587-026-01186-z: openalex:W4407423733, openalex:W4407423733
- openalex:W7172172436: openalex:W7172172436, openalex:W7172172436
- doi:10.48550/arxiv.2607.27853: openalex:W7172007986, openalex:W7172007986
