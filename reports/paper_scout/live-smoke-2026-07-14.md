# Paper Scout Live Smoke Report - 2026-07-14

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 509
- **Unique papers:** 472
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 408
- Sample title: Forgetting Our Way to Shared Meaning: Effects of Forgetting on Conceptual Alignment in a Non-Partnership Coordination Game
- Sample source ID: 2607.11787
- Sample URL: https://arxiv.org/abs/2607.11787v1
- Sample published date: 2026-07-13
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-07-09
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 1
- Sample title: Procedural Memory Distillation: Online Reflection for Self-Improving Language Models
- Sample source ID: 7e542f0d9e83c39599a3589125f5c71d0e63bc47
- Sample URL: https://www.semanticscholar.org/paper/7e542f0d9e83c39599a3589125f5c71d0e63bc47
- Sample published date: 2026-07-01
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 27
- maybe: 41
- irrelevant: 404

## Top Relevant Or Maybe Papers

- **TF-Engram: A Train-Free Engram with SSD-Backed Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.07388
- **ReflectWorld-MM: An Entity-Oriented Multi-Media Memory System for Open-Ended Video Streams** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2607.09759v1
- **Procedural Memory Distillation: Online Reflection for Self-Improving Language Models** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://doi.org/10.48550/arxiv.2607.01480
- **Procedural Memory Distillation: Online Reflection for Self-Improving Language Models** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2607.01480v1
- **Procedural Memory Distillation: Online Reflection for Self-Improving Language Models** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2607.01480
- **MemoryBioRAG: A Reproducible Methodology for Vector-Free Biomimetic Agent Memory Using Conceptual Spaces and Synaptic Graphs on SQLite** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.21204978
- **MemoryBioRAG: A Reproducible Methodology for Vector-Free Biomimetic Agent Memory Using Conceptual Spaces and Synaptic Graphs on SQLite** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.21204977
- **Memory Is Not Live State — Cross-Agent Memory Governance by Transplanting the Reflective Context Governor onto Agent Memory (memgov v0.1.0)** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://github.com/mobius-style/rcgov
- **Memory Is Not Live State — Cross-Agent Memory Governance by Transplanting the Reflective Context Governor onto Agent Memory (memgov v0.1.0)** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://doi.org/10.5281/zenodo.21231158
- **Episodic-to-Semantic Consolidation Without Identity Drift** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2607.01988v1

## Source Failures

- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2607.11787: arxiv:2607.11787, arxiv:2607.11787
- arxiv:2607.11707: arxiv:2607.11707, arxiv:2607.11707
- arxiv:2607.11530: arxiv:2607.11530, arxiv:2607.11530
- arxiv:2607.11523: arxiv:2607.11523, arxiv:2607.11523
- arxiv:2607.11377: arxiv:2607.11377, arxiv:2607.11377
- arxiv:2607.11357: arxiv:2607.11357, arxiv:2607.11357
- arxiv:2607.11226: arxiv:2607.11226, arxiv:2607.11226
- arxiv:2607.11138: arxiv:2607.11138, arxiv:2607.11138
- arxiv:2607.11126: arxiv:2607.11126, arxiv:2607.11126
- arxiv:2607.10878: arxiv:2607.10878, arxiv:2607.10878
- arxiv:2607.10582: arxiv:2607.10582, arxiv:2607.10582
- arxiv:2607.10526: arxiv:2607.10526, arxiv:2607.10526
- arxiv:2607.08960: arxiv:2607.08960, arxiv:2607.08960, arxiv:2607.08960
- arxiv:2607.01480: arxiv:2607.01480, arxiv:2607.01480, semantic_scholar:7e542f0d9e83c39599a3589125f5c71d0e63bc47
- arxiv:2607.00605: arxiv:2607.00605, arxiv:2607.00605
- arxiv:2607.00712: arxiv:2607.00712, arxiv:2607.00712
- arxiv:2607.10784: arxiv:2607.10784, arxiv:2607.10784
- doi:10.1007/s10115-026-02818-x: arxiv:2607.06796, openalex:W7167618879
- arxiv:2607.11736: arxiv:2607.11736, arxiv:2607.11736
- arxiv:2607.11689: arxiv:2607.11689, arxiv:2607.11689
- arxiv:2607.11307: arxiv:2607.11307, arxiv:2607.11307
- arxiv:2607.11175: arxiv:2607.11175, arxiv:2607.11175
- arxiv:2607.11026: arxiv:2607.11026, arxiv:2607.11026
- arxiv:2607.10966: arxiv:2607.10966, arxiv:2607.10966
- arxiv:2607.10805: arxiv:2607.10805, arxiv:2607.10805
- doi:10.1109/isbi61048.2026.11515401: arxiv:2607.10992, arxiv:2607.10988
- doi:10.1007/978-981-92-2369-5_20: openalex:W7167717851, openalex:W7167717851
- openalex:W7167380153: openalex:W7167380153, openalex:W7167380153
- doi:10.21203/rs.3.rs-9701113/v1: openalex:W4391556095, openalex:W4391556095
- openalex:W7167380864: openalex:W7167380864, openalex:W7167380864
- doi:10.48550/arxiv.2607.01480: openalex:W7167266087, openalex:W7167266087
- openalex:W7167154514: openalex:W7167154514, openalex:W7167154514
- openalex:W7167980834: openalex:W7167980834, openalex:W7167980834
- openalex:W7167855542: openalex:W7167855542, openalex:W7167855542
- openalex:W7167981271: openalex:W7167981271, openalex:W7167981271
