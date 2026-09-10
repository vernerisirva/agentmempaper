# Paper Scout Live Smoke Report - 2026-09-10

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 158
- **Unique papers:** 149
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 58
- Sample title: HLSFactory-Agent: Large-Scale Agentic HLS Dataset Construction from Academic and Open-Source Projects
- Sample source ID: 2609.09519
- Sample URL: https://arxiv.org/abs/2609.09519v1
- Sample published date: 2026-09-08
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

- relevant: 22
- maybe: 9
- irrelevant: 118

## Top Relevant Or Maybe Papers

- **Method of Working with AI in Creating Scientific Articles: Algorithm, Criteria, and Practice** (relevant, 98/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.5281/zenodo.22148513
- **Method of Working with AI in Creating Scientific Articles: Algorithm, Criteria, and Practice** (relevant, 98/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.5281/zenodo.22148512
- **Do AI Scientists' Results Replicate? Pre-registration of a multi-seed re-execution study of agent-generated empirical claims with matched human baselines and auditor calibration (AutoReplicate)** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.17605/osf.io/qm2c3
- **Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.64898/2026.09.03.749176
- **RATIO: A Benchmark for Retrieval Across Typed Ideation Operations in Scientific Literature** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.27394v3
- **PaperGym: Rubric-Centered Evolution for Research-Plan Generation** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2608.31119v1
- **OpenDiscoveryTrace: Process Traces for Evaluating AI Scientist Workflows** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.09203v1
- **Online Surrogate Repair: Decoupling High-Fidelity Feedback from Search Length in Closed-Loop Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.07655v1
- **Dr. Claw: An AI Scientist Workspace for Vibe Research** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.00365v1
- **Dr. Claw: An AI Scientist Workspace for Vibe Research** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.00365

## Source Failures

- semantic_scholar (HTTP/API error) for `deep research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2609.09410: arxiv:2609.09410, arxiv:2609.09410
- arxiv:2609.09203: arxiv:2609.09203, arxiv:2609.09203
- arxiv:2609.05079: arxiv:2609.05079, arxiv:2609.05079
- arxiv:2609.00365: arxiv:2609.00365, arxiv:2609.00365
- doi:10.5281/zenodo.22168098: openalex:W7204711696, openalex:W7204711696
- doi:10.5281/zenodo.22168097: openalex:W7204699780, openalex:W7204699780
- doi:10.1057/s41599-026-08832-2: openalex:W4414898195, openalex:W4414898195
- doi:10.1038/s41586-026-10950-5: openalex:W7205708811, openalex:W7205708811
- doi:10.1145/3845596: openalex:W4407310674, openalex:W4407310674
