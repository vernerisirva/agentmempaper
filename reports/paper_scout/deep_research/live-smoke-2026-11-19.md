# Paper Scout Live Smoke Report - 2026-11-19

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 225
- **Candidates fetched:** 147
- **Unique papers:** 143
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 47
- Sample title: Discovery of new antiviral agents through artificial intelligence: in vitro and in vivo results
- Sample source ID: 2611.22230
- Sample URL: https://arxiv.org/abs/2611.22230v1
- Sample published date: 2026-11-17
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Security of Deep Research Agents: Attack Surface, Defenses, Benchmarks, and Agenda Seeding against Research Planning
- Sample source ID: W7235735698
- Sample URL: https://doi.org/10.48550/arxiv.2611.20045
- Sample published date: 2026-11-15
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 24
- maybe: 4
- irrelevant: 115

## Top Relevant Or Maybe Papers

- **Does an Open Targets dossier skill help an AI scientist agent? An OpenScientist experiment** (relevant, 96/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.24026258
- **The Harness Is the Lab: Measured Self-Improvement for Ontology-Grounded AI Scientists** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.24144799
- **The AI scientist in the mirror: Shared flaws, joint remedies** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1073/pnas.2633303123
- **Sage-Taiyi: A Metacognitive Architecture for Scientific Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.12762v2
- **Inventa: Decentralized Self-Improving Agents for Autonomous Scientific Discovery** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.21847v1
- **Ground, Iterate, Trace: Decomposing AI Research Ideation** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.24887v1
- **Eliciting Research Taste in LLMs through Future Research Direction Choice** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.19794v1
- **DiscoveryAgent: A Framework for Scientist-centric Agentic AI** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.21950v1
- **ChemDFT: open-core snapshot (schemas, contracts and engine wrappers), release 0.0.60** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.24082321
- **Blind Variation, Selective Retention: Improving Creative Idea Generation in AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2611.12184v1

## Source Failures

- semantic_scholar (HTTP/API error) for `autonomous research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.20045: arxiv:2611.20045, arxiv:2611.20045
- arxiv:2611.19202: arxiv:2611.19202, arxiv:2611.19202
- arxiv:2611.21950: arxiv:2611.21950, arxiv:2611.21950
- doi:10.48550/arxiv.2611.13994: openalex:W7225800606, openalex:W7225800606
