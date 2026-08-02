# Paper Scout Live Smoke Report - 2026-08-02

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 250
- **Candidates fetched:** 148
- **Unique papers:** 135
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 48
- Sample title: FinanceHarness: Autonomous Financial Deep Research Framework
- Sample source ID: 2607.27853
- Sample URL: https://arxiv.org/abs/2607.27853v1
- Sample published date: 2026-07-30
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: DRNOISE: Benchmarking Deep Research Agents in Misleading Evidence Environments
- Sample source ID: W7170112771
- Sample URL: https://arxiv.org/abs/2607.17291
- Sample published date: 2026-07-19
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 25
- maybe: 10
- irrelevant: 100

## Top Relevant Or Maybe Papers

- **PEARL: Auditable Repair for Scientific Reasoning Graph Extraction** (relevant, 98/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2607.17917v1
- **AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping** (relevant, 95/100): Studies automated literature-review systems or literature-review agents. https://doi.org/10.5281/zenodo.21523009
- **AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping** (relevant, 95/100): Studies automated literature-review systems or literature-review agents. https://doi.org/10.5281/zenodo.21523008
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **SciHazard: A Benchmark for Measuring Scientific Safety Risks with Decomposed Harm Scoring** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2607.18665v1
- **SciHazard: A Benchmark for Measuring Scientific Safety Risks with Decomposed Harm Scoring** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2607.18665
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2607.25865
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.25865v1
- **OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2607.25865

## Source Failures

- semantic_scholar (HTTP/API error) for `AI scientist`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2607.27853: arxiv:2607.27853, arxiv:2607.27853
- arxiv:2607.27562: arxiv:2607.27562, arxiv:2607.27562
- arxiv:2607.27435: arxiv:2607.27435, arxiv:2607.27435
- arxiv:2607.23336: arxiv:2607.23336, arxiv:2607.23336
- arxiv:2607.21461: arxiv:2607.21461, arxiv:2607.21461
- arxiv:2607.18665: arxiv:2607.18665, arxiv:2607.18665
- doi:10.1002/widm.70111: openalex:W4390730779, openalex:W4390730779
- doi:10.1016/j.chbr.2026.101220: openalex:W4417084818, openalex:W4417084818, openalex:W4417084818
- doi:10.1162/qss.a.502: openalex:W4410348581, openalex:W4410348581
- doi:10.1038/s43587-026-01186-z: openalex:W4407423733, openalex:W4407423733
- doi:10.48550/arxiv.2607.27853: openalex:W7172007986, openalex:W7172007986
- openalex:W7171750087: openalex:W7171750087, openalex:W7171750087
