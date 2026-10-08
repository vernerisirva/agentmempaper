# Paper Scout Live Smoke Report - 2026-10-08

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 250
- **Candidates fetched:** 162
- **Unique papers:** 152
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 60
- Sample title: Label-free cell counting and viability prediction with brightfield imaging and deep learning
- Sample source ID: 2610.10473
- Sample URL: https://arxiv.org/abs/2610.10473v1
- Sample published date: 2026-10-07
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: DeepRewind: Predicting and Repairing Premature Commitments in Deep Research Agents
- Sample source ID: W7214903403
- Sample URL: https://arxiv.org/abs/2609.36344
- Sample published date: 2026-09-28
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 2
- Sample title: EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution
- Sample source ID: c25f73c2268bc40010c3e6fbc1a678ec99d7cf88
- Sample URL: https://www.semanticscholar.org/paper/c25f73c2268bc40010c3e6fbc1a678ec99d7cf88
- Sample published date: 2026-10-03
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 40
- maybe: 13
- irrelevant: 99

## Top Relevant Or Maybe Papers

- **YouRA: A Persistent-State Architecture for Evidence-Traceable Autonomous Research Agents** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.01097v1
- **YouRA: A Persistent-State Architecture for Evidence-Traceable Autonomous Research Agents** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.01097
- **LawCompass: Navigating from Legal QA to Multi-Agent Deep Research with Grounded Evidence** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2610.01027v1
- **LawCompass: Navigating from Legal QA to Multi-Agent Deep Research with Grounded Evidence** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2610.01027
- **EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.48550/arxiv.2610.04517
- **EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2610.04517v1
- **Are We Measuring Scientific Intelligence? Rethinking the Evaluation of AI Scientists** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2610.04915
- **Are We Measuring Scientific Intelligence? Rethinking the Evaluation of AI Scientists** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2610.04915v1
- **The more you automate, the less you see: Hidden pitfalls of autonomous AI scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1073/pnas.2610214123
- **ScientistTwo Autonomous Research System Summary and Critical Assessment** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.70777/si.v3i3.18761

## Source Failures

- semantic_scholar (HTTP/API error) for `AI scientist`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.10468: arxiv:2610.10468, arxiv:2610.10468
- arxiv:2610.04911: arxiv:2610.04911, arxiv:2610.04911
- arxiv:2610.04517: arxiv:2610.04517, arxiv:2610.04517, semantic_scholar:c25f73c2268bc40010c3e6fbc1a678ec99d7cf88
- arxiv:2610.03174: arxiv:2610.03174, arxiv:2610.03174
- arxiv:2610.08927: arxiv:2610.08927, arxiv:2610.08927
- arxiv:2610.01097: arxiv:2610.01097, arxiv:2610.01097, semantic_scholar:a2f117bdfc10626be7e48df5eacd241f408c96e7
- doi:10.5281/zenodo.23051403: openalex:W7214949777, openalex:W7214949777
- doi:10.48550/arxiv.2610.04517: openalex:W7220652748, openalex:W7220652748
