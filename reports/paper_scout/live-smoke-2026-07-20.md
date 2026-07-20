# Paper Scout Live Smoke Report - 2026-07-20

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 600
- **Candidates fetched:** 501
- **Unique papers:** 477
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 401
- Sample title: SkillNav: Score-Level Skill Intervention for Zero-Shot Object Goal Navigation
- Sample source ID: 2607.15758
- Sample URL: https://arxiv.org/abs/2607.15758v1
- Sample published date: 2026-07-17
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Provenance Is Not Independence: The False-Corroboration Exclusion Rule for Multi-Agent Memory
- Sample source ID: W7169678469
- Sample URL: https://doi.org/10.5281/zenodo.21431717
- Sample published date: 2026-07-18
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 23
- maybe: 52
- irrelevant: 402

## Top Relevant Or Maybe Papers

- **TF-Engram: A Train-Free Engram with SSD-Backed Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.07388
- **ReflectWorld-MM: An Entity-Oriented Multimodal Memory System for Open-Ended Video Streams** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.09759v2
- **Memory Is Not Live State — Cross-Agent Memory Governance by Transplanting the Reflective Context Governor onto Agent Memory (memgov v0.1.0)** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://github.com/mobius-style/rcgov
- **Memory Is Not Live State — Cross-Agent Memory Governance by Transplanting the Reflective Context Governor onto Agent Memory (memgov v0.1.0)** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.21231158
- **arielagor/lem-research: Learning to Withdraw v1.0 — Reflexive Environments Benchmark for Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://github.com/arielagor/lem-research/tree/v1.0
- **arielagor/lem-research: Learning to Withdraw v1.0 — Reflexive Environments Benchmark for Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.21301553
- **From Organizational Knowledge to AI Agent Memory: Empirical Validation of the SECI Model on the LongMemEval Benchmark** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.21203/rs.3.rs-9801639/v1
- **Your Agent's Memories Are Not Its Own: Forged Reasoning Attacks on LLM Agent Memory and Defenses** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2607.05029
- **Your Agent's Memories Are Not Its Own: Forged Reasoning Attacks on LLM Agent Memory and Defenses** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.05029
- **Write-Protected Discrete Bottlenecks for Language-Grounded World Models: A Structural Limitation and Sufficient Fix** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2607.08312

## Source Failures

- semantic_scholar (HTTP/API error) for `parametric memory LLM`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2607.15715: arxiv:2607.15715, arxiv:2607.15715
- arxiv:2607.15657: arxiv:2607.15657, arxiv:2607.15657
- arxiv:2607.15591: arxiv:2607.15591, arxiv:2607.15591
- arxiv:2607.15257: arxiv:2607.15257, arxiv:2607.15257
- arxiv:2607.14952: arxiv:2607.14952, arxiv:2607.14952
- arxiv:2607.14865: arxiv:2607.14865, arxiv:2607.14865
- arxiv:2607.13940: arxiv:2607.13940, arxiv:2607.13940
- arxiv:2607.13854: arxiv:2607.13854, arxiv:2607.13854
- arxiv:2607.13591: arxiv:2607.13591, arxiv:2607.13591
- arxiv:2607.08960: arxiv:2607.08960, arxiv:2607.08960
- doi:10.1007/s10115-026-02818-x: arxiv:2607.06796, openalex:W7167618879
- arxiv:2607.15736: arxiv:2607.15736, arxiv:2607.15736
- arxiv:2607.15202: arxiv:2607.15202, arxiv:2607.15202
- arxiv:2607.14777: arxiv:2607.14777, arxiv:2607.14777
- openalex:W7169633739: openalex:W7169633739, openalex:W7169633739
- doi:10.1007/978-981-92-2369-5_20: openalex:W7167717851, openalex:W7167717851
- openalex:W7167855587: openalex:W7167855587, openalex:W7167855587
- openalex:W7169633262: openalex:W7169633262, openalex:W7169633262, openalex:W7169633262
- openalex:W7169473804: openalex:W7169473804, openalex:W7169473804
- doi:10.1145/3805712.3809958: openalex:W7161162685, openalex:W7161162685
- openalex:W7167980834: openalex:W7167980834, openalex:W7167980834
- openalex:W7167855542: openalex:W7167855542, openalex:W7167855542
- openalex:W7167981271: openalex:W7167981271, openalex:W7167981271
