# Paper Scout Live Smoke Report - 2026-09-12

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 514
- **Unique papers:** 488
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 414
- Sample title: Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding
- Sample source ID: 2609.11899
- Sample URL: https://arxiv.org/abs/2609.11899v1
- Sample published date: 2026-09-10
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
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 18
- maybe: 54
- irrelevant: 416

## Top Relevant Or Maybe Papers

- **Personalizing LLM Agent Memory Using Biometrics** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2609.08558
- **InsightSeg: Reusing Correction Insights for Guideline-Consistent Segmentation** (relevant, 100/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.02002v1
- **Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.11060v1
- **What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.08279
- **MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging** (relevant, 99/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.08273
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260019
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260018
- **Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.30177
- **Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.08258
- **Procedural Memory Under Change: Reuse and Interference in Controlled Web Tasks** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.09774v1

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2609.11636: arxiv:2609.11636, arxiv:2609.11636
- arxiv:2609.11308: arxiv:2609.11308, arxiv:2609.11308
- arxiv:2609.11294: arxiv:2609.11294, arxiv:2609.11294
- arxiv:2609.11133: arxiv:2609.11133, arxiv:2609.11133
- arxiv:2609.11060: arxiv:2609.11060, arxiv:2609.11060
- arxiv:2609.10922: arxiv:2609.10922, arxiv:2609.10922, arxiv:2609.10922, arxiv:2609.10922
- arxiv:2609.10155: arxiv:2609.10155, arxiv:2609.10155
- arxiv:2609.09774: arxiv:2609.09774, arxiv:2609.09774
- arxiv:2609.09153: arxiv:2609.09153, arxiv:2609.09153
- arxiv:2609.08944: arxiv:2609.08944, arxiv:2609.08944
- arxiv:2609.02253: arxiv:2609.02253, arxiv:2609.02253
- arxiv:2609.00718: arxiv:2609.00718, arxiv:2609.00718
- arxiv:2609.00291: arxiv:2609.00291, arxiv:2609.00291
- arxiv:2609.10767: arxiv:2609.10767, arxiv:2609.10767
- arxiv:2609.11864: arxiv:2609.11864, arxiv:2609.11864
- arxiv:2609.11699: arxiv:2609.11699, arxiv:2609.11699
- arxiv:2609.11677: arxiv:2609.11677, arxiv:2609.11677
- doi:10.1109/cbmi66578.2025.11339313: arxiv:2609.11322, arxiv:2609.11322
- arxiv:2609.10996: arxiv:2609.10996, arxiv:2609.10996
- doi:10.48550/arxiv.2609.02253: openalex:W7207710217, openalex:W7207710217
- doi:10.21203/rs.3.rs-10643317/v1: openalex:W7204958905, openalex:W7204958905
- doi:10.56201/ijcsmt.vol.12.no4.2026.pg239.255: openalex:W7207779244, openalex:W7207779244
- doi:10.1145/3844940: openalex:W4385002547, openalex:W4385002547
- doi:10.1145/3844947: openalex:W4417515043, openalex:W4417515043
