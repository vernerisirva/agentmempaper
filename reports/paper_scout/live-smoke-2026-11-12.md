# Paper Scout Live Smoke Report - 2026-11-12

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 512
- **Unique papers:** 466
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 412
- Sample title: Continual-ARC: Measuring Skill Acquisition over a Working Lifetime
- Sample source ID: 2611.14505
- Sample URL: https://arxiv.org/abs/2611.14505v1
- Sample published date: 2026-11-10
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: MemoryDojo: Benchmarking Poisoning Through LLM Agent Memory
- Sample source ID: W7225613920
- Sample URL: https://arxiv.org/abs/2611.09721
- Sample published date: 2026-11-06
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 28
- maybe: 57
- irrelevant: 381

## Top Relevant Or Maybe Papers

- **Route to Remember: Adaptive Memory Selection for LLM Agents** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.05636v1
- **MIRIX-2.0: Multi-Agent Memory System** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.48550/arxiv.2611.12068
- **MIRIX-2.0: Multi-Agent Memory System** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.12068v1
- **Learning to remember: advances in memory mechanisms for large language models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.1007/s44336-026-00044-1
- **Writing rules for agent memory with two extractor models: a paired extension** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.5281/zenodo.24057927
- **MemoryDojo: Benchmarking Poisoning Through LLM Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.09721
- **FlyHash for LLM Agent Memory: An Empirical Validation and a New Application** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.23903302
- **Correct Answers from Insufficient Histories: A Controlled Study of Agent Memory Evaluation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.48550/arxiv.2611.11840
- **CogniLife: Continuous Cognitive Distillation for Deployed Multi-Expert Agent Marketplaces** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.04483v2
- **When Should Agents Remember? Falsification-Gated Self-Evolution for LLM Agents** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.14326v1

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.14505: arxiv:2611.14505, arxiv:2611.14505, arxiv:2611.14505
- arxiv:2611.14326: arxiv:2611.14326, arxiv:2611.14326
- arxiv:2611.14320: arxiv:2611.14320, arxiv:2611.14320, arxiv:2611.14320
- arxiv:2611.14017: arxiv:2611.14017, arxiv:2611.14017
- arxiv:2611.14009: arxiv:2611.14009, arxiv:2611.14009, arxiv:2611.14009
- arxiv:2611.13966: arxiv:2611.13966, arxiv:2611.13966
- arxiv:2611.13946: arxiv:2611.13946, arxiv:2611.13946
- arxiv:2611.13776: arxiv:2611.13776, arxiv:2611.13776
- arxiv:2611.13696: arxiv:2611.13696, arxiv:2611.13696
- arxiv:2611.13426: arxiv:2611.13426, arxiv:2611.13426
- arxiv:2611.13413: arxiv:2611.13413, arxiv:2611.13413
- arxiv:2611.13329: arxiv:2611.13329, arxiv:2611.13329
- arxiv:2611.12552: arxiv:2611.12552, arxiv:2611.12552
- arxiv:2611.12269: arxiv:2611.12269, arxiv:2611.12269
- arxiv:2611.12068: arxiv:2611.12068, arxiv:2611.12068, arxiv:2611.12068
- arxiv:2611.11509: arxiv:2611.11509, arxiv:2611.11509
- arxiv:2611.10477: arxiv:2611.10477, arxiv:2611.10477
- arxiv:2611.04483: arxiv:2611.04483, arxiv:2611.04483
- arxiv:2611.04003: arxiv:2611.04003, arxiv:2611.04003
- arxiv:2611.14033: arxiv:2611.14033, arxiv:2611.14033
- arxiv:2611.10542: arxiv:2611.10542, arxiv:2611.10542
- arxiv:2611.14382: arxiv:2611.14382, arxiv:2611.14382
- arxiv:2611.14323: arxiv:2611.14323, arxiv:2611.14323
- arxiv:2611.14171: arxiv:2611.14171, arxiv:2611.14171
- arxiv:2611.13894: arxiv:2611.13894, arxiv:2611.13894
- arxiv:2611.13713: arxiv:2611.13713, arxiv:2611.13713
- arxiv:2611.13680: arxiv:2611.13680, arxiv:2611.13680
- arxiv:2611.13543: arxiv:2611.13543, arxiv:2611.13543
- arxiv:2611.13524: arxiv:2611.13524, arxiv:2611.13524
- doi:10.1007/s44336-026-00044-1: openalex:W7223835807, openalex:W7223835807, openalex:W7223835807
- doi:10.48550/arxiv.2610.40985: openalex:W7225074700, openalex:W7225074700
- doi:10.48550/arxiv.2610.40476: openalex:W7224880368, openalex:W7224880368
- doi:10.48550/arxiv.2611.01460: openalex:W7225146488, openalex:W7225146488
- doi:10.1016/j.media.2026.104386: openalex:W7225173051, openalex:W7225173051
- doi:10.48550/arxiv.2610.39671: openalex:W7224750867, openalex:W7224750867
- doi:10.48550/arxiv.2611.05953: openalex:W7225304599, openalex:W7225304599
- doi:10.1145/3799682.3839997: openalex:W7225073136, openalex:W7225073136
- doi:10.7554/elife.112891.1.sa3: openalex:W7225227528, openalex:W7225227528
- doi:10.7554/elife.112891.1.sa1: openalex:W7225226572, openalex:W7225226572
- doi:10.7554/elife.112891.1.sa0: openalex:W7225265123, openalex:W7225265123
- doi:10.7554/elife.112891.1.sa2: openalex:W7225253425, openalex:W7225253425
