# Paper Scout Live Smoke Report - 2026-09-08

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 525
- **Candidates fetched:** 518
- **Unique papers:** 486
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 418
- Sample title: Does Your Agent's Memory Survive a Model Upgrade? A Controlled Study of Memory Portability
- Sample source ID: 2609.05339
- Sample URL: https://arxiv.org/abs/2609.05339v1
- Sample published date: 2026-09-04
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents
- Sample source ID: W7206151206
- Sample URL: https://doi.org/10.5281/zenodo.22260018
- Sample published date: 2026-09-02
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 18
- maybe: 66
- irrelevant: 402

## Top Relevant Or Maybe Papers

- **When Users Don't Ask: Benchmarking Context-Driven Memory Retrieval in Conversational Agents** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.03467v1
- **Linguistic Trajectory Encoding for Efficient Long-Horizon Spatial Memory in Embodied Agents** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.04802v1
- **InsightSeg: Reusing Correction Insights for Guideline-Consistent Segmentation** (relevant, 100/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.02002v1
- **ICM-Bench: Person-Level Identity Reasoning in Multimodal Agents with Long-Term Memory** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.04438v1
- **Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.29606v1
- **Advantage-Driven Explicit Memory for Social Navigation** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.25610v1
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260019
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260018
- **Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.30177
- **Scoping Note: Shared features of agentic memory systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22234513

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2609.05339: arxiv:2609.05339, arxiv:2609.05339
- arxiv:2609.05324: arxiv:2609.05324, arxiv:2609.05324, arxiv:2609.05324
- arxiv:2609.05232: arxiv:2609.05232, arxiv:2609.05232
- arxiv:2609.05104: arxiv:2609.05104, arxiv:2609.05104
- arxiv:2609.04915: arxiv:2609.04915, arxiv:2609.04915
- arxiv:2609.04875: arxiv:2609.04875, arxiv:2609.04875
- arxiv:2609.04869: arxiv:2609.04869, arxiv:2609.04869, arxiv:2609.04869
- arxiv:2609.04852: arxiv:2609.04852, arxiv:2609.04852
- arxiv:2609.04820: arxiv:2609.04820, arxiv:2609.04820
- arxiv:2609.04802: arxiv:2609.04802, arxiv:2609.04802
- arxiv:2609.04778: arxiv:2609.04778, arxiv:2609.04778
- arxiv:2609.04444: arxiv:2609.04444, arxiv:2609.04444
- arxiv:2609.03753: arxiv:2609.03753, arxiv:2609.03753, arxiv:2609.03753
- arxiv:2609.02253: arxiv:2609.02253, arxiv:2609.02253, arxiv:2609.02253
- arxiv:2609.00718: arxiv:2609.00718, arxiv:2609.00718
- arxiv:2609.00291: arxiv:2609.00291, arxiv:2609.00291
- arxiv:2609.05295: arxiv:2609.05295, arxiv:2609.05295
- arxiv:2609.05262: arxiv:2609.05262, arxiv:2609.05262
- arxiv:2609.05221: arxiv:2609.05221, arxiv:2609.05221
- arxiv:2609.04894: arxiv:2609.04894, arxiv:2609.04894
- arxiv:2609.04665: arxiv:2609.04665, arxiv:2609.04665
- doi:10.48550/arxiv.2608.27924: openalex:W7204753136, openalex:W7204753136
- doi:10.48550/arxiv.2609.02253: openalex:W7207710217, openalex:W7207710217
- doi:10.21203/rs.3.rs-10643317/v1: openalex:W7204958905, openalex:W7204958905
- doi:10.48550/arxiv.2608.26895: openalex:W7204528475, openalex:W7204528475
- doi:10.1177/09567976261461522: openalex:W4414430346, openalex:W4414430346
- doi:10.1145/3844940: openalex:W4385002547, openalex:W4385002547
- doi:10.64898/2026.08.24.746712: openalex:W7204441115, openalex:W7204441115
