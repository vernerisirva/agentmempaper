# Paper Scout Live Smoke Report - 2026-09-10

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 525
- **Candidates fetched:** 517
- **Unique papers:** 481
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 417
- Sample title: TRACE: Trajectory-robust Admission with Evidence Ordering for Efficient GUI Agents
- Sample source ID: 2609.10297
- Sample URL: https://arxiv.org/abs/2609.10297v1
- Sample published date: 2026-09-09
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

- relevant: 22
- maybe: 44
- irrelevant: 415

## Top Relevant Or Maybe Papers

- **Personalizing LLM Agent Memory Using Biometrics** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.48550/arxiv.2609.08558
- **Personalizing LLM Agent Memory Using Biometrics** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2609.08558v1
- **InsightSeg: Reusing Correction Insights for Guideline-Consistent Segmentation** (relevant, 100/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.02002v1
- **What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.48550/arxiv.2609.08279
- **MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.48550/arxiv.2609.08273
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260019
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260018
- **Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.30177
- **Scoping Note: Shared features of agentic memory systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22234513
- **Scoping Note: Shared features of agentic memory systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22234512

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2609.10266: arxiv:2609.10266, arxiv:2609.10266
- arxiv:2609.10263: arxiv:2609.10263, arxiv:2609.10263
- arxiv:2609.10155: arxiv:2609.10155, arxiv:2609.10155, arxiv:2609.10155
- arxiv:2609.10144: arxiv:2609.10144, arxiv:2609.10144
- arxiv:2609.09985: arxiv:2609.09985, arxiv:2609.09985
- arxiv:2609.09875: arxiv:2609.09875, arxiv:2609.09875
- arxiv:2609.09778: arxiv:2609.09778, arxiv:2609.09778
- arxiv:2609.09774: arxiv:2609.09774, arxiv:2609.09774, arxiv:2609.09774
- arxiv:2609.09565: arxiv:2609.09565, arxiv:2609.09565
- arxiv:2609.09476: arxiv:2609.09476, arxiv:2609.09476
- arxiv:2609.09404: arxiv:2609.09404, arxiv:2609.09404
- arxiv:2609.09153: arxiv:2609.09153, arxiv:2609.09153, arxiv:2609.09153, arxiv:2609.09153
- arxiv:2609.08944: arxiv:2609.08944, arxiv:2609.08944, arxiv:2609.08944
- arxiv:2609.02253: arxiv:2609.02253, arxiv:2609.02253
- arxiv:2609.00718: arxiv:2609.00718, arxiv:2609.00718
- arxiv:2609.00291: arxiv:2609.00291, arxiv:2609.00291
- arxiv:2609.10441: arxiv:2609.10441, arxiv:2609.10441
- arxiv:2609.09363: arxiv:2609.09363, arxiv:2609.09363
- arxiv:2609.10177: arxiv:2609.10177, arxiv:2609.10177
- arxiv:2609.10135: arxiv:2609.10135, arxiv:2609.10135
- arxiv:2609.10122: arxiv:2609.10122, arxiv:2609.10122
- arxiv:2609.10113: arxiv:2609.10113, arxiv:2609.10113
- arxiv:2609.09776: arxiv:2609.09776, arxiv:2609.09776
- arxiv:2609.09625: arxiv:2609.09625, arxiv:2609.09625
- arxiv:2609.09468: arxiv:2609.09468, arxiv:2609.09468
- doi:10.48550/arxiv.2608.27924: openalex:W7204753136, openalex:W7204753136
- doi:10.48550/arxiv.2609.02253: openalex:W7207710217, openalex:W7207710217
- doi:10.48550/arxiv.2608.26895: openalex:W7204528475, openalex:W7204528475
- doi:10.1145/3844940: openalex:W4385002547, openalex:W4385002547
- doi:10.1145/3844947: openalex:W4417515043, openalex:W4417515043
- doi:10.64898/2026.08.24.746712: openalex:W7204441115, openalex:W7204441115
