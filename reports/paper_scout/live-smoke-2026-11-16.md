# Paper Scout Live Smoke Report - 2026-11-16

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 600
- **Candidates fetched:** 511
- **Unique papers:** 483
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 411
- Sample title: Alignment by Socialization: Learning Tradeoffs Under Selection
- Sample source ID: 2611.18531
- Sample URL: https://arxiv.org/abs/2611.18531v1
- Sample published date: 2026-11-13
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: The Agent Memory Wall
- Sample source ID: W7225828643
- Sample URL: https://doi.org/10.5281/zenodo.24146465
- Sample published date: 2026-11-11
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 28
- maybe: 53
- irrelevant: 402

## Top Relevant Or Maybe Papers

- **Route to Remember: Adaptive Memory Selection for LLM Agents** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.05636v1
- **MIRIX-2.0: Multi-Agent Memory System** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.12068v1
- **MIRIX-2.0: Multi-Agent Memory System** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.12068
- **Learning to remember: advances in memory mechanisms for large language models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.1007/s44336-026-00044-1
- **Forget the Lineage: Forward-Secure, Lineage-Complete Cryptographic Erasure for LLM-Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.18133v1
- **DISCERN: Preserve at Write, Resolve at Read for Persistent LLM-Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.15729v1
- **DISCERN: Preserve at Write, Resolve at Read for Persistent LLM-Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.15729
- **Agent Memory Integrity Benchmark (AMIB)** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.24227858
- **Writing rules for agent memory with two extractor models: a paired extension** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.5281/zenodo.24057927
- **MemoryDojo: Benchmarking Poisoning Through LLM Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.09721

## Source Failures

- semantic_scholar (HTTP/API error) for `parametric memory LLM`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.18531: arxiv:2611.18531, arxiv:2611.18531
- arxiv:2611.18516: arxiv:2611.18516, arxiv:2611.18516
- arxiv:2611.18397: arxiv:2611.18397, arxiv:2611.18397
- arxiv:2611.18235: arxiv:2611.18235, arxiv:2611.18235
- arxiv:2611.18150: arxiv:2611.18150, arxiv:2611.18150
- arxiv:2611.18139: arxiv:2611.18139, arxiv:2611.18139
- arxiv:2611.18067: arxiv:2611.18067, arxiv:2611.18067
- arxiv:2611.17788: arxiv:2611.17788, arxiv:2611.17788
- arxiv:2611.16487: arxiv:2611.16487, arxiv:2611.16487
- arxiv:2611.16433: arxiv:2611.16433, arxiv:2611.16433
- arxiv:2611.16378: arxiv:2611.16378, arxiv:2611.16378
- arxiv:2611.16143: arxiv:2611.16143, arxiv:2611.16143
- arxiv:2611.15766: arxiv:2611.15766, arxiv:2611.15766
- arxiv:2611.12068: arxiv:2611.12068, arxiv:2611.12068, arxiv:2611.12068
- arxiv:2611.10477: arxiv:2611.10477, arxiv:2611.10477
- arxiv:2611.17524: arxiv:2611.17524, arxiv:2611.17524
- arxiv:2611.17686: arxiv:2611.17686, arxiv:2611.17686
- arxiv:2611.17563: arxiv:2611.17563, arxiv:2611.17563
- doi:10.48550/arxiv.2611.12068: openalex:W7225721830, openalex:W7225721830
- doi:10.48550/arxiv.2611.14009: openalex:W7225818297, openalex:W7225818297
- doi:10.1007/s44336-026-00044-1: openalex:W7223835807, openalex:W7223835807, openalex:W7223835807
- doi:10.48550/arxiv.2611.13127: openalex:W7225816720, openalex:W7225816720
- doi:10.48550/arxiv.2611.13855: openalex:W7225801991, openalex:W7225801991
- doi:10.1145/3799682.3839997: openalex:W7225073136, openalex:W7225073136
- doi:10.7554/elife.112891.1.sa3: openalex:W7225227528, openalex:W7225227528
- doi:10.7554/elife.112891.1.sa2: openalex:W7225253425, openalex:W7225253425
