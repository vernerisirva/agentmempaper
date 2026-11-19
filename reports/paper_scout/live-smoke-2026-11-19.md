# Paper Scout Live Smoke Report - 2026-11-19

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 525
- **Candidates fetched:** 513
- **Unique papers:** 470
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 413
- Sample title: Isabelle Pool Server: a pooled verification service for prover training and multi-agent proving
- Sample source ID: 2611.24788
- Sample URL: https://arxiv.org/abs/2611.24788v1
- Sample published date: 2026-11-18
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
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 28
- maybe: 60
- irrelevant: 382

## Top Relevant Or Maybe Papers

- **MIRIX-2.0: Multi-Agent Memory System** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.12068v1
- **MIRIX-2.0: Multi-Agent Memory System** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2611.12068
- **Learning to remember: advances in memory mechanisms for large language models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.1007/s44336-026-00044-1
- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2611.20759
- **Instant Weight-Space Consolidation for Long-Term Memory in LLMs** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2611.20759v1
- **DISCERN: Preserve at Write, Resolve at Read for Persistent LLM-Agent Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.15729
- **Agent Memory Integrity Benchmark (AMIB)** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.24227858
- **Writing rules for agent memory with two extractor models: a paired extension** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.5281/zenodo.24057927
- **SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.22017v1
- **MemoryDojo: Benchmarking Poisoning Through LLM Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2611.09721

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2611.24788: arxiv:2611.24788, arxiv:2611.24788
- arxiv:2611.24651: arxiv:2611.24651, arxiv:2611.24651, arxiv:2611.24651
- arxiv:2611.24636: arxiv:2611.24636, arxiv:2611.24636
- arxiv:2611.24619: arxiv:2611.24619, arxiv:2611.24619
- arxiv:2611.24422: arxiv:2611.24422, arxiv:2611.24422
- arxiv:2611.24302: arxiv:2611.24302, arxiv:2611.24302
- arxiv:2611.24294: arxiv:2611.24294, arxiv:2611.24294
- arxiv:2611.24115: arxiv:2611.24115, arxiv:2611.24115
- arxiv:2611.24052: arxiv:2611.24052, arxiv:2611.24052
- arxiv:2611.24039: arxiv:2611.24039, arxiv:2611.24039
- arxiv:2611.24028: arxiv:2611.24028, arxiv:2611.24028
- arxiv:2611.24004: arxiv:2611.24004, arxiv:2611.24004
- doi:10.1109/tro.2026.3754505: arxiv:2611.23930, arxiv:2611.23930
- doi:10.1145/3862322.3863775: arxiv:2611.23695, arxiv:2611.23695
- arxiv:2611.23678: arxiv:2611.23678, arxiv:2611.23678
- arxiv:2611.23651: arxiv:2611.23651, arxiv:2611.23651, arxiv:2611.23651, arxiv:2611.23651
- arxiv:2611.23476: arxiv:2611.23476, arxiv:2611.23476
- arxiv:2611.24166: arxiv:2611.24166, arxiv:2611.24166
- arxiv:2611.24058: arxiv:2611.24058, arxiv:2611.24058
- arxiv:2611.12068: arxiv:2611.12068, arxiv:2611.12068
- arxiv:2611.24043: arxiv:2611.24043, arxiv:2611.24043
- arxiv:2611.24830: arxiv:2611.24830, arxiv:2611.24830
- arxiv:2611.24650: arxiv:2611.24650, arxiv:2611.24650
- arxiv:2611.24588: arxiv:2611.24588, arxiv:2611.24588
- arxiv:2611.24578: arxiv:2611.24578, arxiv:2611.24578
- arxiv:2611.24301: arxiv:2611.24301, arxiv:2611.24301
- arxiv:2611.24077: arxiv:2611.24077, arxiv:2611.24077
- arxiv:2611.23962: arxiv:2611.23962, arxiv:2611.23962
- arxiv:2611.23750: arxiv:2611.23750, arxiv:2611.23750
- arxiv:2611.23716: arxiv:2611.23716, arxiv:2611.23716
- arxiv:2611.23702: arxiv:2611.23702, arxiv:2611.23702
- arxiv:2611.23673: arxiv:2611.23673, arxiv:2611.23673
- doi:10.48550/arxiv.2611.12068: openalex:W7225721830, openalex:W7225721830
- doi:10.1007/s44336-026-00044-1: openalex:W7223835807, openalex:W7223835807, openalex:W7223835807
- doi:10.48550/arxiv.2611.14838: openalex:W7226014162, openalex:W7226014162
- doi:10.48550/arxiv.2611.13127: openalex:W7225816720, openalex:W7225816720
- doi:10.1016/j.media.2026.104386: openalex:W7225173051, openalex:W7225173051
- doi:10.1145/3767308.3835716: openalex:W7106700227, openalex:W7106700227
- doi:10.48550/arxiv.2611.13855: openalex:W7225801991, openalex:W7225801991
