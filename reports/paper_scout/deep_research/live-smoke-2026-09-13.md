# Paper Scout Live Smoke Report - 2026-09-13

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 100
- **Unique papers:** 95
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

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

- Status: Success - zero results
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 0


## Decisions

- relevant: 11
- maybe: 3
- irrelevant: 81

## Top Relevant Or Maybe Papers

- **Do AI Scientists' Results Replicate? Pre-registration of a multi-seed re-execution study of agent-generated empirical claims with matched human baselines and auditor calibration (AutoReplicate)** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.17605/osf.io/qm2c3
- **Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.64898/2026.09.03.749176
- **OpenDiscoveryTrace: Process Traces for Evaluating AI Scientist Workflows** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2609.09203
- **Mr.LHDR: A Benchmark for Multimodal Real-World Long-Horizon Deep Research Agents** (relevant, 93/100): Studies autonomous or deep research agents. https://doi.org/10.13140/rg.2.2.29034.48321
- **Dr. Claw: An AI Scientist Workspace for Vibe Research** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.00365
- **Explore Before Committing: Hypothesis-Guided Search for Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.01294
- **DualStake: Dual-Path Confidence Calibration in Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.00935
- **Differential Knowledge-State Tracking for Token-Efficient Autonomous Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://doi.org/10.5281/zenodo.22168098
- **Differential Knowledge-State Tracking for Token-Efficient Autonomous Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://doi.org/10.5281/zenodo.22168097
- **Agent and Tool Search: Foundations, Techniques, and Open Challenges** (relevant, 91/100): Studies autonomous or deep research agents. https://doi.org/10.20944/preprints202609.0402.v1

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- doi:10.5281/zenodo.22168098: openalex:W7204711696, openalex:W7204711696
- doi:10.5281/zenodo.22168097: openalex:W7204699780, openalex:W7204699780
- doi:10.1057/s41599-026-08832-2: openalex:W4414898195, openalex:W4414898195
- doi:10.1038/s41586-026-10950-5: openalex:W7205708811, openalex:W7205708811
- doi:10.1145/3845596: openalex:W4407310674, openalex:W4407310674
