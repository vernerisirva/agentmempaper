# Paper Scout Live Smoke Report - 2026-07-28

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 225
- **Candidates fetched:** 146
- **Unique papers:** 136
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 46
- Sample title: Constrained Reinforcement Learning Using Successor Representations
- Sample source ID: 2607.24057
- Sample URL: https://arxiv.org/abs/2607.24057v1
- Sample published date: 2026-07-27
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Total Recall QA: A Verifiable Evaluation Suite for Deep Research Agents
- Sample source ID: W7168405860
- Sample URL: https://doi.org/10.1145/3805712.3808629
- Sample published date: 2026-07-15
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 31
- maybe: 9
- irrelevant: 96

## Top Relevant Or Maybe Papers

- **PEARL: Auditable Repair for Scientific Reasoning Graph Extraction** (relevant, 98/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2607.17917v1
- **AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping** (relevant, 95/100): Studies automated literature-review systems or literature-review agents. https://doi.org/10.5281/zenodo.21523009
- **AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping** (relevant, 95/100): Studies automated literature-review systems or literature-review agents. https://doi.org/10.5281/zenodo.21523008
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **SciHazard: A Benchmark for Measuring Scientific Safety Risks with Decomposed Harm Scoring** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2607.18665v1
- **Recent Advances in AI for Automated ICD Coding: A Systematic Literature Review** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.1007/s10916-026-02429-7
- **LegalCiteTrust: Benchmarking Citation Trustworthiness in Chinese Long-Form Legal Research Reports** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2607.20872v1
- **Is Deep Research Reliable? Misleading Knowledge Induces False Conclusions** (relevant, 93/100): Studies autonomous or deep research agents. https://doi.org/10.48550/arxiv.2607.20891
- **Is Deep Research Reliable? Misleading Knowledge Induces False Conclusions** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2607.20891v1

## Source Failures

- semantic_scholar (HTTP/API error) for `autonomous research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2607.23336: arxiv:2607.23336, arxiv:2607.23336
- arxiv:2607.21461: arxiv:2607.21461, arxiv:2607.21461
- arxiv:2607.18665: arxiv:2607.18665, arxiv:2607.18665
- arxiv:2607.14582: arxiv:2607.14582, arxiv:2607.14582
- arxiv:2607.14178: arxiv:2607.14178, arxiv:2607.14178
- doi:10.1002/widm.70111: openalex:W4390730779, openalex:W4390730779
- doi:10.1016/j.chbr.2026.101220: openalex:W4417084818, openalex:W4417084818, openalex:W4417084818
- doi:10.1162/qss.a.502: openalex:W4410348581, openalex:W4410348581
- doi:10.1017/psrm.2026.10110: openalex:W4411728625, openalex:W4411728625
