# Paper Scout Live Smoke Report - 2026-09-04

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 525
- **Candidates fetched:** 524
- **Unique papers:** 494
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 424
- Sample title: Extending concurrent separation logic to the hardware level to verify the xv6 OS kernel on RISC-V with AI agents
- Sample source ID: 2609.04043
- Sample URL: https://arxiv.org/abs/2609.04043v1
- Sample published date: 2026-09-03
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: InjecMEM: Memory Injection Attack on LLM Agent Memory Systems
- Sample source ID: W7204186950
- Sample URL: https://arxiv.org/abs/2608.23471
- Sample published date: 2026-08-24
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 20
- maybe: 64
- irrelevant: 410

## Top Relevant Or Maybe Papers

- **When Users Don't Ask: Benchmarking Context-Driven Memory Retrieval in Conversational Agents** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2609.03467v1
- **InsightSeg: Reusing Correction Insights for Guideline-Consistent Segmentation** (relevant, 100/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.02002v1
- **CAPTURE: Disentangling Preference Drift from Memory Poisoning in Personalized LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.02265v1
- **Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.29606v1
- **Advantage-Driven Explicit Memory for Social Navigation** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.25610v1
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260019
- **ZenBrain: Neuroscience-Inspired Agent Memory Library for LLM Agents** (relevant, 91/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.22260018
- **Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.30177
- **Scoping Note: Shared features of agentic memory systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22234513
- **Scoping Note: Shared features of agentic memory systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22234512

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2609.03915: arxiv:2609.03915, arxiv:2609.03915
- arxiv:2609.03871: arxiv:2609.03871, arxiv:2609.03871
- arxiv:2609.03753: arxiv:2609.03753, arxiv:2609.03753, arxiv:2609.03753, arxiv:2609.03753
- arxiv:2609.03727: arxiv:2609.03727, arxiv:2609.03727
- arxiv:2609.03619: arxiv:2609.03619, arxiv:2609.03619
- arxiv:2609.03467: arxiv:2609.03467, arxiv:2609.03467
- arxiv:2609.03450: arxiv:2609.03450, arxiv:2609.03450
- arxiv:2609.03425: arxiv:2609.03425, arxiv:2609.03425
- arxiv:2609.03340: arxiv:2609.03340, arxiv:2609.03340
- arxiv:2609.03201: arxiv:2609.03201, arxiv:2609.03201
- arxiv:2609.02760: arxiv:2609.02760, arxiv:2609.02760
- arxiv:2609.02749: arxiv:2609.02749, arxiv:2609.02749
- arxiv:2609.03432: arxiv:2609.03432, arxiv:2609.03432
- arxiv:2609.02253: arxiv:2609.02253, arxiv:2609.02253, arxiv:2609.02253
- arxiv:2609.00718: arxiv:2609.00718, arxiv:2609.00718
- arxiv:2609.00291: arxiv:2609.00291, arxiv:2609.00291
- arxiv:2608.26530: arxiv:2608.26530, arxiv:2608.26530
- arxiv:2609.03937: arxiv:2609.03937, arxiv:2609.03937
- arxiv:2609.03844: arxiv:2609.03844, arxiv:2609.03844
- arxiv:2609.03350: arxiv:2609.03350, arxiv:2609.03350
- doi:10.48550/arxiv.2608.23268: openalex:W7204175137, openalex:W7204175137
- doi:10.48550/arxiv.2608.22215: openalex:W7204197564, openalex:W7204197564
- doi:10.48550/arxiv.2608.27924: openalex:W7204753136, openalex:W7204753136
- doi:10.21203/rs.3.rs-10643317/v1: openalex:W7204958905, openalex:W7204958905
- doi:10.1177/09567976261461522: openalex:W4414430346, openalex:W4414430346
- doi:10.1145/3844940: openalex:W4385002547, openalex:W4385002547
- doi:10.64898/2026.08.24.746712: openalex:W7204441115, openalex:W7204441115
