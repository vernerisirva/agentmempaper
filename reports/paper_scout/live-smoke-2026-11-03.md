# Paper Scout Live Smoke Report - 2026-11-03

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 600
- **Candidates fetched:** 519
- **Unique papers:** 480
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 418
- Sample title: Spacetime Emergence in the Memory of a Learning Agent
- Sample source ID: 2611.03596
- Sample URL: https://arxiv.org/abs/2611.03596v1
- Sample published date: 2026-11-02
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
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 1
- Sample title: Learning to Remember: Advances in Memory Mechanisms for Large Language Models
- Sample source ID: 70c1c4f061c15e7ae74fcd369d07e073eedd4225
- Sample URL: https://www.semanticscholar.org/paper/70c1c4f061c15e7ae74fcd369d07e073eedd4225
- Sample published date: 2026-10-26
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 26
- maybe: 66
- irrelevant: 388

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

- semantic_scholar (HTTP/API error) for `parametric memory LLM`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.03596: arxiv:2611.03596, arxiv:2611.03596
- arxiv:2611.03576: arxiv:2611.03576, arxiv:2611.03576
- doi:10.1145/3799682.3839256: arxiv:2611.03434, arxiv:2611.03434, arxiv:2611.03434
- arxiv:2611.03330: arxiv:2611.03330, arxiv:2611.03330
- arxiv:2611.03289: arxiv:2611.03289, arxiv:2611.03289
- arxiv:2611.03178: arxiv:2611.03178, arxiv:2611.03178
- arxiv:2611.03157: arxiv:2611.03157, arxiv:2611.03157
- arxiv:2611.03005: arxiv:2611.03005, arxiv:2611.03005
- arxiv:2611.02912: arxiv:2611.02912, arxiv:2611.02912
- arxiv:2611.02905: arxiv:2611.02905, arxiv:2611.02905
- arxiv:2611.02644: arxiv:2611.02644, arxiv:2611.02644
- arxiv:2611.02605: arxiv:2611.02605, arxiv:2611.02605
- arxiv:2611.02601: arxiv:2611.02601, arxiv:2611.02601
- arxiv:2611.02455: arxiv:2611.02455, arxiv:2611.02455
- arxiv:2610.37935: arxiv:2610.37935, arxiv:2610.37935
- arxiv:2610.35089: arxiv:2610.35089, arxiv:2610.35089, semantic_scholar:70c1c4f061c15e7ae74fcd369d07e073eedd4225
- arxiv:2610.34724: arxiv:2610.34724, arxiv:2610.34724, arxiv:2610.34724
- arxiv:2610.32464: arxiv:2610.32464, arxiv:2610.32464
- arxiv:2611.02587: arxiv:2611.02587, arxiv:2611.02587
- arxiv:2611.00450: arxiv:2611.00450, arxiv:2611.00450, arxiv:2611.00450
- arxiv:2611.03496: arxiv:2611.03496, arxiv:2611.03496
- arxiv:2611.01778: arxiv:2611.01778, arxiv:2611.01778
- arxiv:2611.03094: arxiv:2611.03094, arxiv:2611.03094
- arxiv:2611.02950: arxiv:2611.02950, arxiv:2611.02950
- arxiv:2611.02833: arxiv:2611.02833, arxiv:2611.02833
- arxiv:2611.02797: arxiv:2611.02797, arxiv:2611.02797
- arxiv:2611.02681: arxiv:2611.02681, arxiv:2611.02681
- doi:10.48550/arxiv.2610.34073: openalex:W7224013415, openalex:W7224013415, openalex:W7224013415
- doi:10.48550/arxiv.2610.34673: openalex:W7223960487, openalex:W7223960487
- doi:10.66977/xsci.2610.002q: openalex:W7221537227, openalex:W7221537227
- doi:10.48550/arxiv.2610.35089: openalex:W7223835807, openalex:W7223835807, openalex:W7223835807
- doi:10.48550/arxiv.2610.40476: openalex:W7224880368, openalex:W7224880368
- doi:10.48550/arxiv.2610.39671: openalex:W7224750867, openalex:W7224750867
