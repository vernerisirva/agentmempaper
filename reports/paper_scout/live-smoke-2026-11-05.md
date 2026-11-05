# Paper Scout Live Smoke Report - 2026-11-05

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 475
- **Candidates fetched:** 417
- **Unique papers:** 391
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 416
- Sample title: PyRUA-REAL: Robot Exploration and Adaptive Learning through RSI in the Real World
- Sample source ID: 2611.06768
- Sample URL: https://arxiv.org/abs/2611.06768v1
- Sample published date: 2026-11-04
- Abstract: yes

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-10-22&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 1
- Sample title: Learning to Remember: Advances in Memory Mechanisms for Large Language Models
- Sample source ID: 70c1c4f061c15e7ae74fcd369d07e073eedd4225
- Sample URL: https://www.semanticscholar.org/paper/70c1c4f061c15e7ae74fcd369d07e073eedd4225
- Sample published date: 2026-10-26
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 13
- maybe: 37
- irrelevant: 341

## Top Relevant Or Maybe Papers

- **Route to Remember: Adaptive Memory Selection for LLM Agents** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.05636v1
- **Learning to Remember: Advances in Memory Mechanisms for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2610.35089v1
- **KITE: Retrieval as a Decision Procedure for Long-Term Conversational Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.41521v1
- **CogniLife: Continuous Cognitive Distillation for Deployed Multi-Expert Agent Marketplaces** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.04483v1
- **WASP-Mem: Let Agent Organize Procedural Memory. Human Spend Effort on Diagnosis** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2611.04003v1
- **TalentRL: Strategy-Guided Reinforcement Learning for Hierarchical Skill Routing** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.41143v1
- **PyRUA-REAL: Robot Exploration and Adaptive Learning through RSI in the Real World** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.06768v1
- **Learning by Doing: Autonomously Compiling and Curating Agent Skills from Verified Traces** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2611.01386v1
- **From Lookups to Lessons: Turning Retrieved Knowledge into Parametric Memory** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.00450v1
- **FlyHash for LLM Agent Memory: An Empirical Validation and a New Application** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2611.05791v1

## Source Failures

- openalex (HTTP/API error) for `agent memory`: http error for https://api.openalex.org/works?search=agent+memory&filter=from_publication_date%3A2026-10-22&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.06704: arxiv:2611.06704, arxiv:2611.06704
- arxiv:2611.06687: arxiv:2611.06687, arxiv:2611.06687
- arxiv:2611.06554: arxiv:2611.06554, arxiv:2611.06554
- arxiv:2611.06445: arxiv:2611.06445, arxiv:2611.06445
- arxiv:2611.06382: arxiv:2611.06382, arxiv:2611.06382
- arxiv:2611.06116: arxiv:2611.06116, arxiv:2611.06116
- arxiv:2611.06084: arxiv:2611.06084, arxiv:2611.06084
- arxiv:2611.06049: arxiv:2611.06049, arxiv:2611.06049
- arxiv:2611.05953: arxiv:2611.05953, arxiv:2611.05953
- arxiv:2611.05791: arxiv:2611.05791, arxiv:2611.05791
- arxiv:2611.05753: arxiv:2611.05753, arxiv:2611.05753
- arxiv:2611.05731: arxiv:2611.05731, arxiv:2611.05731
- arxiv:2611.05636: arxiv:2611.05636, arxiv:2611.05636
- arxiv:2611.05313: arxiv:2611.05313, arxiv:2611.05313, arxiv:2611.05313
- arxiv:2611.06827: arxiv:2611.06827, arxiv:2611.06827
- arxiv:2611.04483: arxiv:2611.04483, arxiv:2611.04483
- arxiv:2611.04003: arxiv:2611.04003, arxiv:2611.04003, arxiv:2611.04003
- arxiv:2611.06715: arxiv:2611.06715, arxiv:2611.06715
- arxiv:2611.00450: arxiv:2611.00450, arxiv:2611.00450
- arxiv:2610.35089: arxiv:2610.35089, semantic_scholar:70c1c4f061c15e7ae74fcd369d07e073eedd4225
- arxiv:2611.06606: arxiv:2611.06606, arxiv:2611.06606
- arxiv:2611.06381: arxiv:2611.06381, arxiv:2611.06381
- doi:10.18653/2026.lmplayschool-1.3: arxiv:2611.06065, arxiv:2611.06065
- arxiv:2611.05895: arxiv:2611.05895, arxiv:2611.05895
