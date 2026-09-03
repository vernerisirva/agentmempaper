# Paper Scout Live Smoke Report - 2026-09-03

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 600
- **Candidates fetched:** 527
- **Unique papers:** 481
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 425
- Sample title: Measurement-Driven Sub-Network Selection for On-Premise Retrieval-Augmented Factory Agents
- Sample source ID: 2609.02760
- Sample URL: https://arxiv.org/abs/2609.02760v1
- Sample published date: 2026-09-02
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
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 2
- Sample title: Gaming with AI: A Hybrid Reinforcement Learning, Large Language Model, and Procedural Content Generation Framework for Enhancing Player Engagement and User Experience
- Sample source ID: bef526c86452cbe462b7c6957f86ecb893f8c6d5
- Sample URL: https://www.semanticscholar.org/paper/bef526c86452cbe462b7c6957f86ecb893f8c6d5
- Sample published date: 2026-08-21
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 19
- maybe: 56
- irrelevant: 406

## Top Relevant Or Maybe Papers

- **The Judgment Layer: Turning Agent Memory into Wisdom** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://dhare.com.au
- **The Judgment Layer: Turning Agent Memory into Wisdom** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://dhare.com.au
- **InsightSeg: Reusing Correction Insights for Guideline-Consistent Segmentation** (relevant, 100/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.02002v1
- **CAPTURE: Disentangling Preference Drift from Memory Poisoning in Personalized LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.02265v1
- **Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.29606v1
- **Advantage-Driven Explicit Memory for Social Navigation** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.25610v1
- **Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.30177
- **The Memory Trust Gap: Capability-Dependent Failures in Persistent-Memory Agents** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2609.01852v1
- **Scoping Note: Shared features of agentic memory systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22234513
- **Scoping Note: Shared features of agentic memory systems** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://doi.org/10.5281/zenodo.22234512

## Source Failures

- semantic_scholar (HTTP/API error) for `parametric memory LLM`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- doi:10.5281/zenodo.22255631: arxiv:2609.02760, arxiv:2609.02760, arxiv:2609.02760
- arxiv:2609.02750: arxiv:2609.02750, arxiv:2609.02750
- arxiv:2609.02749: arxiv:2609.02749, arxiv:2609.02749, arxiv:2609.02749
- arxiv:2609.02730: arxiv:2609.02730, arxiv:2609.02730
- arxiv:2609.02309: arxiv:2609.02309, arxiv:2609.02309
- arxiv:2609.02265: arxiv:2609.02265, arxiv:2609.02265
- arxiv:2609.02253: arxiv:2609.02253, arxiv:2609.02253, arxiv:2609.02253, arxiv:2609.02253, arxiv:2609.02253
- arxiv:2609.02231: arxiv:2609.02231, arxiv:2609.02231
- arxiv:2609.02217: arxiv:2609.02217, arxiv:2609.02217, arxiv:2609.02217
- arxiv:2609.02129: arxiv:2609.02129, arxiv:2609.02129
- arxiv:2609.02094: arxiv:2609.02094, arxiv:2609.02094, arxiv:2609.02094
- arxiv:2609.02074: arxiv:2609.02074, arxiv:2609.02074
- arxiv:2609.02002: arxiv:2609.02002, arxiv:2609.02002, arxiv:2609.02002
- arxiv:2609.01971: arxiv:2609.01971, arxiv:2609.01971
- arxiv:2609.01861: arxiv:2609.01861, arxiv:2609.01861
- arxiv:2609.01852: arxiv:2609.01852, arxiv:2609.01852
- arxiv:2609.01836: arxiv:2609.01836, arxiv:2609.01836
- arxiv:2609.01818: arxiv:2609.01818, arxiv:2609.01818
- arxiv:2609.01272: arxiv:2609.01272, arxiv:2609.01272
- arxiv:2609.02339: arxiv:2609.02339, arxiv:2609.02339
- arxiv:2609.02110: arxiv:2609.02110, arxiv:2609.02110
- arxiv:2609.00718: arxiv:2609.00718, arxiv:2609.00718
- arxiv:2609.00291: arxiv:2609.00291, arxiv:2609.00291
- arxiv:2608.26530: arxiv:2608.26530, arxiv:2608.26530
- arxiv:2608.23268: arxiv:2608.23268, arxiv:2608.23268
- arxiv:2608.30563: arxiv:2608.30563, semantic_scholar:50b458d018f8452a620325eb4a6f80652a52e215
- arxiv:2609.02273: arxiv:2609.02273, arxiv:2609.02273
- arxiv:2609.01976: arxiv:2609.01976, arxiv:2609.01976
- doi:10.48550/arxiv.2608.23268: openalex:W7204175137, openalex:W7204175137
- doi:10.48550/arxiv.2608.22215: openalex:W7204197564, openalex:W7204197564
- doi:10.48550/arxiv.2608.27924: openalex:W7204753136, openalex:W7204753136
- doi:10.48175/ijarsct-38105: openalex:W7203824408, semantic_scholar:bef526c86452cbe462b7c6957f86ecb893f8c6d5
- doi:10.48550/arxiv.2608.19857: openalex:W7203923029, openalex:W7203923029
- doi:10.21203/rs.3.rs-10643317/v1: openalex:W7204958905, openalex:W7204958905
- doi:10.48550/arxiv.2608.20549: openalex:W7204093153, openalex:W7204093153
- doi:10.1177/09567976261461522: openalex:W4414430346, openalex:W4414430346
- doi:10.1145/3844940: openalex:W4385002547, openalex:W4385002547
- doi:10.64898/2026.08.24.746712: openalex:W7204441115, openalex:W7204441115
