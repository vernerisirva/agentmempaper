# Paper Scout Live Smoke Report - 2026-11-04

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 468
- **Unique papers:** 429
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 416
- Sample title: From Autonomous Agents to Cognitive Symbionts: Toward AI-Augmented Human Intelligence
- Sample source ID: 2611.05376
- Sample URL: https://arxiv.org/abs/2611.05376v1
- Sample published date: 2026-11-03
- Abstract: yes

### openalex

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 50
- Sample title: MemoryTax: The Bitter Lesson of Agent Memory
- Sample source ID: W7223250543
- Sample URL: https://arxiv.org/abs/2610.29823
- Sample published date: 2026-10-21
- Abstract: yes
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=memory+distillation+language+model&filter=from_publication_date%3A2026-10-21&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 2
- Sample title: Learning to Remember: Advances in Memory Mechanisms for Large Language Models
- Sample source ID: 70c1c4f061c15e7ae74fcd369d07e073eedd4225
- Sample URL: https://www.semanticscholar.org/paper/70c1c4f061c15e7ae74fcd369d07e073eedd4225
- Sample published date: 2026-10-26
- Abstract: yes


## Decisions

- relevant: 20
- maybe: 58
- irrelevant: 351

## Top Relevant Or Maybe Papers

- **Recovery Budgets for Persistent AI-Agent Memory: Reproducibility Artifact** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.23623901
- **Learning to Remember: Advances in Memory Mechanisms for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2610.35089v1
- **Learning to Remember: Advances in Memory Mechanisms for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2610.35089
- **KITE: Retrieval as a Decision Procedure for Long-Term Conversational Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.41521v1
- **Agent Memory as Recommendation: Recommender-System Design for Long-Term Memory of LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.34673
- **TrawMem: Reframing Agent Memory as Task-Oriented Role-Adaptive Workspaces** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.36918
- **MemoryTax: The Bitter Lesson of Agent Memory** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.29823
- **CogniLife: Continuous Cognitive Distillation for Deployed Multi-Expert Agent Marketplaces** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.04483v1
- **gamma: grounded multi-agent memory with mechanical audit for memory-intensive manipulation** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.66977/xsci.2610.002q
- **WASP-Mem: Let Agent Organize Procedural Memory. Human Spend Effort on Diagnosis** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2611.04003v1

## Source Failures

- openalex (HTTP/API error) for `memory distillation language model`: http error for https://api.openalex.org/works?search=memory+distillation+language+model&filter=from_publication_date%3A2026-10-21&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- arxiv:2611.05376: arxiv:2611.05376, arxiv:2611.05376
- arxiv:2611.05319: arxiv:2611.05319, arxiv:2611.05319
- arxiv:2611.05313: arxiv:2611.05313, arxiv:2611.05313, arxiv:2611.05313, arxiv:2611.05313
- arxiv:2611.05139: arxiv:2611.05139, arxiv:2611.05139
- arxiv:2611.05108: arxiv:2611.05108, arxiv:2611.05108
- arxiv:2611.05029: arxiv:2611.05029, arxiv:2611.05029
- arxiv:2611.04867: arxiv:2611.04867, arxiv:2611.04867
- arxiv:2611.04807: arxiv:2611.04807, arxiv:2611.04807
- arxiv:2611.04797: arxiv:2611.04797, arxiv:2611.04797
- arxiv:2611.04483: arxiv:2611.04483, arxiv:2611.04483, arxiv:2611.04483, arxiv:2611.04483
- arxiv:2611.04321: arxiv:2611.04321, arxiv:2611.04321
- arxiv:2611.04315: arxiv:2611.04315, arxiv:2611.04315
- arxiv:2611.04196: arxiv:2611.04196, arxiv:2611.04196
- arxiv:2611.04012: arxiv:2611.04012, arxiv:2611.04012
- arxiv:2611.04003: arxiv:2611.04003, arxiv:2611.04003, arxiv:2611.04003, arxiv:2611.04003
- arxiv:2611.04434: arxiv:2611.04434, arxiv:2611.04434
- arxiv:2611.04392: arxiv:2611.04392, arxiv:2611.04392
- arxiv:2610.37935: arxiv:2610.37935, arxiv:2610.37935
- arxiv:2610.35089: arxiv:2610.35089, arxiv:2610.35089, semantic_scholar:70c1c4f061c15e7ae74fcd369d07e073eedd4225
- arxiv:2610.34724: arxiv:2610.34724, arxiv:2610.34724
- arxiv:2611.00450: arxiv:2611.00450, arxiv:2611.00450, semantic_scholar:d5cf9c3375cf1ad3c4937263a17d121a802679f3
- arxiv:2611.04296: arxiv:2611.04296, arxiv:2611.04296
- arxiv:2611.01778: arxiv:2611.01778, arxiv:2611.01778
- arxiv:2611.05158: arxiv:2611.05158, arxiv:2611.05158
- arxiv:2611.04958: arxiv:2611.04958, arxiv:2611.04958
- arxiv:2611.04814: arxiv:2611.04814, arxiv:2611.04814
- arxiv:2611.04787: arxiv:2611.04787, arxiv:2611.04787
- arxiv:2611.04632: arxiv:2611.04632, arxiv:2611.04632
- arxiv:2611.04180: arxiv:2611.04180, arxiv:2611.04180
- doi:10.48550/arxiv.2610.34073: openalex:W7224013415, openalex:W7224013415
- doi:10.66977/xsci.2610.002q: openalex:W7221537227, openalex:W7221537227
