# Paper Scout Live Smoke Report - 2026-11-02

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 520
- **Unique papers:** 476
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 419
- Sample title: RoboArchitect: Automating the Design of Robotic Agents with Persistent Memory
- Sample source ID: 2610.42141
- Sample URL: https://arxiv.org/abs/2610.42141v1
- Sample published date: 2026-10-30
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: MemoryTax: The Bitter Lesson of Agent Memory
- Sample source ID: W7223250543
- Sample URL: https://arxiv.org/abs/2610.29823
- Sample published date: 2026-10-21
- Abstract: yes

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

- relevant: 25
- maybe: 50
- irrelevant: 401

## Top Relevant Or Maybe Papers

- **Recovery Budgets for Persistent AI-Agent Memory: Reproducibility Artifact** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.23623901
- **Learning to Remember: Advances in Memory Mechanisms for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2610.35089v1
- **Learning to Remember: Advances in Memory Mechanisms for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2610.35089
- **KITE: Retrieval as a Decision Procedure for Long-Term Conversational Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.41521v1
- **Agent Memory as Recommendation: Recommender-System Design for Long-Term Memory of LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.34673
- **TrawMem: Reframing Agent Memory as Task-Oriented Role-Adaptive Workspaces** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.36918
- **MemoryTax: The Bitter Lesson of Agent Memory** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2610.29823
- **gamma: grounded multi-agent memory with mechanical audit for memory-intensive manipulation** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.66977/xsci.2610.002q
- **The Right Fact, the Wrong Decision: SciValidityBench for Scientific Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.34767
- **Temporal Evidence-Parameter Co-Alignment for LLM Reasoning over Temporal Knowledge Graphs** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2610.28176v2

## Source Failures

- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.42141: arxiv:2610.42141, arxiv:2610.42141
- arxiv:2610.42068: arxiv:2610.42068, arxiv:2610.42068
- arxiv:2610.42004: arxiv:2610.42004, arxiv:2610.42004
- arxiv:2610.41688: arxiv:2610.41688, arxiv:2610.41688
- arxiv:2610.41563: arxiv:2610.41563, arxiv:2610.41563, arxiv:2610.41563
- arxiv:2610.41521: arxiv:2610.41521, arxiv:2610.41521
- arxiv:2610.41482: arxiv:2610.41482, arxiv:2610.41482
- arxiv:2610.41245: arxiv:2610.41245, arxiv:2610.41245
- arxiv:2610.41216: arxiv:2610.41216, arxiv:2610.41216, arxiv:2610.41216
- arxiv:2610.41172: arxiv:2610.41172, arxiv:2610.41172
- arxiv:2610.41169: arxiv:2610.41169, arxiv:2610.41169
- arxiv:2610.41143: arxiv:2610.41143, arxiv:2610.41143, arxiv:2610.41143
- arxiv:2610.41124: arxiv:2610.41124, arxiv:2610.41124
- arxiv:2610.41056: arxiv:2610.41056, arxiv:2610.41056
- arxiv:2610.40350: arxiv:2610.40350, arxiv:2610.40350
- arxiv:2610.40191: arxiv:2610.40191, arxiv:2610.40191
- arxiv:2610.41402: arxiv:2610.41402, arxiv:2610.41402
- arxiv:2610.37935: arxiv:2610.37935, arxiv:2610.37935
- arxiv:2610.35089: arxiv:2610.35089, arxiv:2610.35089, semantic_scholar:70c1c4f061c15e7ae74fcd369d07e073eedd4225
- arxiv:2610.34724: arxiv:2610.34724, arxiv:2610.34724, arxiv:2610.34724
- arxiv:2610.32464: arxiv:2610.32464, arxiv:2610.32464
- arxiv:2610.31401: arxiv:2610.31401, arxiv:2610.31401
- doi:10.1007/978-3-032-37667-1_15: arxiv:2610.41822, arxiv:2610.41822
- arxiv:2610.41104: arxiv:2610.41104, arxiv:2610.41104, arxiv:2610.41104
- arxiv:2610.42149: arxiv:2610.42149, arxiv:2610.42149
- arxiv:2610.42054: arxiv:2610.42054, arxiv:2610.42054
- arxiv:2610.41745: arxiv:2610.41745, arxiv:2610.41745
- arxiv:2610.41437: arxiv:2610.41437, arxiv:2610.41437
- arxiv:2610.41296: arxiv:2610.41296, arxiv:2610.41296
- arxiv:2610.41162: arxiv:2610.41162, arxiv:2610.41162
- arxiv:2610.40992: arxiv:2610.40992, arxiv:2610.40992
- doi:10.48550/arxiv.2610.34073: openalex:W7224013415, openalex:W7224013415, openalex:W7224013415
- doi:10.48550/arxiv.2610.34673: openalex:W7223960487, openalex:W7223960487
- doi:10.48550/arxiv.2610.35089: openalex:W7223835807, openalex:W7223835807, openalex:W7223835807
- doi:10.48550/arxiv.2610.40476: openalex:W7224880368, openalex:W7224880368
- doi:10.48550/arxiv.2610.39671: openalex:W7224750867, openalex:W7224750867
