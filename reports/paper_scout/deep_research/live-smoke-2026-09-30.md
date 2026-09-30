# Paper Scout Live Smoke Report - 2026-09-30

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 40
- **Unique papers:** 37
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 40
- Sample title: DeepRewind: Predicting and Repairing Premature Commitments in Deep Research Agents
- Sample source ID: 2609.36344
- Sample URL: https://arxiv.org/abs/2609.36344v1
- Sample published date: 2026-09-28
- Abstract: yes

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-09-16&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success - zero results
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 0


## Decisions

- relevant: 9
- maybe: 5
- irrelevant: 23

## Top Relevant Or Maybe Papers

- **ReproBench: Benchmarking LLM Agents on Reproducing Vulnerability From Scratch** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2609.34450v1
- **LongCat-DeepResearch Technical Report** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2609.36071v1
- **Large-Scale Autonomous Discovery of Kissing Number Constructions** (relevant, 93/100): Studies multi-step planning, multi-agent workflows, or hypothesis and experiment-design agents for research. https://arxiv.org/abs/2609.35051v1
- **Can AI Scientists Change Their Minds? Prior-Evidence Conflict in Synthetic Universes** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2609.36726v1
- **Reward Hacking Challenges Oversight of Autonomous Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.28614v1
- **Orchestrating GenAI for Interdisciplinary Research** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.30588v1
- **Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.34296v1
- **DeepRewind: Predicting and Repairing Premature Commitments in Deep Research Agents** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.36344v1
- **CodeGraph: Open-Taxonomy Knowledge Graph for Source Code with Wikidata Grounding** (relevant, 91/100): Studies autonomous or deep research agents. https://arxiv.org/abs/2609.29474v1
- **From Search to Research: Exploring Search Scaling in Autonomous Quantitative Factor Mining** (maybe, 55/100): Review candidate: may support deep research workflows but needs human judgment. https://arxiv.org/abs/2609.35559v1

## Source Failures

- openalex (HTTP/API error) for `deep research agent`: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-09-16&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- arxiv:2609.33509: arxiv:2609.33509, arxiv:2609.33509
- arxiv:2609.32245: arxiv:2609.32245, arxiv:2609.32245
- arxiv:2609.30588: arxiv:2609.30588, arxiv:2609.30588
