# Paper Scout Live Smoke Report - 2026-09-01

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 525
- **Candidates fetched:** 524
- **Unique papers:** 479
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 424
- Sample title: S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?
- Sample source ID: 2608.31100
- Sample URL: https://arxiv.org/abs/2608.31100v1
- Sample published date: 2026-08-31
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-08-20
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.semanticscholar.org/graph/v1/paper/search?query=agent+memory&limit=25&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds%2CopenAccessPdf: request failed after 3 attempts: HTTP Error 500: Internal Server Error


## Decisions

- relevant: 20
- maybe: 51
- irrelevant: 408

## Top Relevant Or Maybe Papers

- **UTILMEM: Benchmarking Evidence Utilization in Long-Term Conversational Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2608.30508v1
- **The Judgment Layer: Turning Agent Memory into Wisdom** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://dhare.com.au
- **The Judgment Layer: Turning Agent Memory into Wisdom** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://dhare.com.au
- **Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.29606v1
- **Advantage-Driven Explicit Memory for Social Navigation** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.25610v1
- **Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.30177v1
- **Rank-Bounded Agent Memory: A Storage-Level, By-Design Defense Against Memory-Poisoning Attacks** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.21994004
- **Mitigating Identity Essentialism in LLM Agents with Longitudinal Life Trajectories** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.19621v2
- **Mitigating Identity Essentialism in LLM Agents with Longitudinal Life Trajectories** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.19621
- **MegaMem: A Retrieval Solution for Ultra-Large Context Windows** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.22137v1

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: http error for https://api.semanticscholar.org/graph/v1/paper/search?query=agent+memory&limit=25&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds%2CopenAccessPdf: request failed after 3 attempts: HTTP Error 500: Internal Server Error

## Deduplication Examples

- arxiv:2608.31100: arxiv:2608.31100, arxiv:2608.31100, arxiv:2608.31100
- arxiv:2608.31057: arxiv:2608.31057, arxiv:2608.31057
- arxiv:2608.31022: arxiv:2608.31022, arxiv:2608.31022
- arxiv:2608.30676: arxiv:2608.30676, arxiv:2608.30676, arxiv:2608.30676
- arxiv:2608.30508: arxiv:2608.30508, arxiv:2608.30508
- arxiv:2608.30478: arxiv:2608.30478, arxiv:2608.30478, arxiv:2608.30478
- arxiv:2608.30396: arxiv:2608.30396, arxiv:2608.30396
- arxiv:2608.30252: arxiv:2608.30252, arxiv:2608.30252
- arxiv:2608.30237: arxiv:2608.30237, arxiv:2608.30237
- arxiv:2608.29910: arxiv:2608.29910, arxiv:2608.29910
- arxiv:2608.29897: arxiv:2608.29897, arxiv:2608.29897
- arxiv:2608.29678: arxiv:2608.29678, arxiv:2608.29678
- arxiv:2608.26530: arxiv:2608.26530, arxiv:2608.26530
- arxiv:2608.23268: arxiv:2608.23268, arxiv:2608.23268
- arxiv:2608.22854: arxiv:2608.22854, arxiv:2608.22854
- arxiv:2608.22562: arxiv:2608.22562, arxiv:2608.22562
- arxiv:2608.22533: arxiv:2608.22533, arxiv:2608.22533
- arxiv:2608.22339: arxiv:2608.22339, arxiv:2608.22339
- arxiv:2608.21792: arxiv:2608.21792, arxiv:2608.21792
- arxiv:2608.29606: arxiv:2608.29606, arxiv:2608.29606
- arxiv:2608.31119: arxiv:2608.31119, arxiv:2608.31119
- arxiv:2608.31111: arxiv:2608.31111, arxiv:2608.31111
- arxiv:2608.31077: arxiv:2608.31077, arxiv:2608.31077
- arxiv:2608.31046: arxiv:2608.31046, arxiv:2608.31046
- arxiv:2608.31009: arxiv:2608.31009, arxiv:2608.31009
- arxiv:2608.30980: arxiv:2608.30980, arxiv:2608.30980
- arxiv:2608.30959: arxiv:2608.30959, arxiv:2608.30959
- arxiv:2608.30760: arxiv:2608.30760, arxiv:2608.30760
- arxiv:2608.30530: arxiv:2608.30530, arxiv:2608.30530
- arxiv:2608.30461: arxiv:2608.30461, arxiv:2608.30461
- arxiv:2608.30429: arxiv:2608.30429, arxiv:2608.30429
- arxiv:2608.30426: arxiv:2608.30426, arxiv:2608.30426
- arxiv:2608.30376: arxiv:2608.30376, arxiv:2608.30376
- doi:10.48550/arxiv.2608.23268: openalex:W7204175137, openalex:W7204175137
- doi:10.48550/arxiv.2608.22215: openalex:W7204197564, openalex:W7204197564
- doi:10.48550/arxiv.2608.19857: openalex:W7203923029, openalex:W7203923029
- doi:10.48550/arxiv.2608.20549: openalex:W7204093153, openalex:W7204093153
- doi:10.48550/arxiv.2608.26895: openalex:W7204528475, openalex:W7204528475
- doi:10.48550/arxiv.2608.25177: openalex:W7204435811, openalex:W7204435811
- doi:10.1177/09567976261461522: openalex:W4414430346, openalex:W4414430346
- doi:10.64898/2026.08.24.746712: openalex:W7204441115, openalex:W7204441115
- doi:10.48550/arxiv.2608.18952: openalex:W7203894965, openalex:W7203894965
