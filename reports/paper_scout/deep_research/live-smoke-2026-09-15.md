# Paper Scout Live Smoke Report - 2026-09-15

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 100
- **Unique papers:** 96
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: Timeout/network error: timeout error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out

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

- relevant: 12
- maybe: 3
- irrelevant: 81

## Top Relevant Or Maybe Papers

- **Do AI Scientists' Results Replicate? Pre-registration of a multi-seed re-execution study of agent-generated empirical claims with matched human baselines and auditor calibration (AutoReplicate)** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.17605/osf.io/qm2c3
- **OpenDiscoveryTrace: Process Traces for Evaluating AI Scientist Workflows** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.09203
- **Mr.LHDR: A Benchmark for Multimodal Real-World Long-Horizon Deep Research Agents** (relevant, 93/100): Studies autonomous or deep research agents. https://doi.org/10.48550/arxiv.2609.11318
- **Mr.LHDR: A Benchmark for Multimodal Real-World Long-Horizon Deep Research Agents** (relevant, 93/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.11318
- **Closing the Empirical Loop: Autonomous AI Agents Conduct End‐to‐end Research With Human Participants** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1002/advs.76675
- **AI Scientists Need a Theory of Scientific Value** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/mgmw1-gw451
- **AI Scientists Need a Theory of Scientific Value** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/eebvr-g1f33
- **Explore Before Committing: Hypothesis-Guided Search for Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.01294
- **DualStake: Dual-Path Confidence Calibration in Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.00935
- **Auto-RecSys: Harnessing Autonomous Research Agents for Industry-Scale Recommender System** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.10922

## Source Failures

- arxiv (Timeout/network error) for `deep research agent`: timeout error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out

## Deduplication Examples

- doi:10.1057/s41599-026-08832-2: openalex:W4414898195, openalex:W4414898195
- doi:10.1038/s41586-026-10950-5: openalex:W7205708811, openalex:W7205708811
- doi:10.21203/rs.3.rs-10996966/v1: openalex:W7212260582, openalex:W7212260582
- doi:10.1145/3845596: openalex:W4407310674, openalex:W4407310674
