# Paper Scout Live Smoke Report - 2026-09-02

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 525
- **Candidates fetched:** 525
- **Unique papers:** 484
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 425
- Sample title: EmbodiedSkills: A Unified Framework for Orchestrating, Training, and Deploying VLA Agents
- Sample source ID: 2609.01281
- Sample URL: https://arxiv.org/abs/2609.01281v1
- Sample published date: 2026-09-01
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-08-20
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 18
- maybe: 64
- irrelevant: 402

## Top Relevant Or Maybe Papers

- **UTILMEM: Benchmarking Evidence Utilization in Long-Term Conversational Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2608.30508v1
- **The Judgment Layer: Turning Agent Memory into Wisdom** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://dhare.com.au
- **The Judgment Layer: Turning Agent Memory into Wisdom** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://dhare.com.au
- **Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.29606v1
- **Advantage-Driven Explicit Memory for Social Navigation** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.25610v1
- **Transferable End-to-End Optimization for Indirect Long-Term Memory Poisoning in LLM Agents** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.00523v1
- **Mitigating Identity Essentialism in LLM Agents with Longitudinal Life Trajectories** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.19621v2
- **Mitigating Identity Essentialism in LLM Agents with Longitudinal Life Trajectories** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.19621
- **Learning What to Retain: Gated-Memory Routing for Efficient Collaboration in Multi-Agent LLM Systems** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2609.00237v1
- **HERO: Human-profile Enhanced Retrieval Optimization Framework for Long-term Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.22310

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2609.01281: arxiv:2609.01281, arxiv:2609.01281
- arxiv:2609.01272: arxiv:2609.01272, arxiv:2609.01272, arxiv:2609.01272
- arxiv:2609.01245: arxiv:2609.01245, arxiv:2609.01245
- arxiv:2609.01235: arxiv:2609.01235, arxiv:2609.01235
- arxiv:2609.01111: arxiv:2609.01111, arxiv:2609.01111
- arxiv:2609.01058: arxiv:2609.01058, arxiv:2609.01058, arxiv:2609.01058
- arxiv:2609.00865: arxiv:2609.00865, arxiv:2609.00865, arxiv:2609.00865
- arxiv:2609.00859: arxiv:2609.00859, arxiv:2609.00859
- arxiv:2608.31100: arxiv:2608.31100, arxiv:2608.31100
- arxiv:2608.30676: arxiv:2608.30676, arxiv:2608.30676
- arxiv:2609.01126: arxiv:2609.01126, arxiv:2609.01126
- arxiv:2609.00718: arxiv:2609.00718, arxiv:2609.00718, arxiv:2609.00718
- arxiv:2609.00291: arxiv:2609.00291, arxiv:2609.00291
- arxiv:2608.26530: arxiv:2608.26530, arxiv:2608.26530
- arxiv:2608.23268: arxiv:2608.23268, arxiv:2608.23268
- arxiv:2608.22854: arxiv:2608.22854, arxiv:2608.22854
- arxiv:2608.22562: arxiv:2608.22562, arxiv:2608.22562
- arxiv:2608.22533: arxiv:2608.22533, arxiv:2608.22533
- arxiv:2608.22339: arxiv:2608.22339, arxiv:2608.22339
- arxiv:2609.01182: arxiv:2609.01182, arxiv:2609.01182
- arxiv:2609.00753: arxiv:2609.00753, arxiv:2609.00753
- arxiv:2609.00834: arxiv:2609.00834, arxiv:2609.00834
- arxiv:2609.01532: arxiv:2609.01532, arxiv:2609.01532
- arxiv:2609.01437: arxiv:2609.01437, arxiv:2609.01437
- arxiv:2609.01422: arxiv:2609.01422, arxiv:2609.01422
- arxiv:2609.01274: arxiv:2609.01274, arxiv:2609.01274
- arxiv:2609.00898: arxiv:2609.00898, arxiv:2609.00898
- arxiv:2609.00652: arxiv:2609.00652, arxiv:2609.00652
- doi:10.48550/arxiv.2608.23268: openalex:W7204175137, openalex:W7204175137
- doi:10.48550/arxiv.2608.22215: openalex:W7204197564, openalex:W7204197564
- doi:10.48550/arxiv.2608.19857: openalex:W7203923029, openalex:W7203923029
- doi:10.48550/arxiv.2608.20549: openalex:W7204093153, openalex:W7204093153
- doi:10.48550/arxiv.2608.26895: openalex:W7204528475, openalex:W7204528475
- doi:10.48550/arxiv.2608.25177: openalex:W7204435811, openalex:W7204435811
- doi:10.1177/09567976261461522: openalex:W4414430346, openalex:W4414430346
- doi:10.64898/2026.08.24.746712: openalex:W7204441115, openalex:W7204441115
- doi:10.48550/arxiv.2608.18952: openalex:W7203894965, openalex:W7203894965
