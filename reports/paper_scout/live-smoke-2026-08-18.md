# Paper Scout Live Smoke Report - 2026-08-18

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 518
- **Unique papers:** 481
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 417
- Sample title: Don't Drop the BATON: Long-Horizon Robot Manipulation via Agentic Subtask Exploration and Transition-aware Memory
- Sample source ID: 2608.16889
- Sample URL: https://arxiv.org/abs/2608.16889v1
- Sample published date: 2026-08-17
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Contemplative Agent
- Sample source ID: W7140295929
- Sample URL: https://doi.org/10.5281/zenodo.19212118
- Sample published date: 2026-08-09
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 1
- Sample title: Activation-Guided Neuron Intervention to Induce Alzheimer's-Related Computational Language Phenotypes in a Large Language Model
- Sample source ID: b5233936e6221a748c0bb73139ed33cb35a84580
- Sample URL: https://www.semanticscholar.org/paper/b5233936e6221a748c0bb73139ed33cb35a84580
- Sample published date: 2026-08-04
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 19
- maybe: 50
- irrelevant: 412

## Top Relevant Or Maybe Papers

- **What to Remember, What to Reveal: Privacy-Aware Memory for Conversational Agents** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2608.16551v1
- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775v1
- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775
- **From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.10502
- **FTA-Mem: Fact-Time-Affect Anchored Memory for Low-Density Long-Term Dialogue** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.16303v1
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://doi.org/10.48550/arxiv.2608.07169
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2608.07169
- **Valhalla: A Layered Knowledge-State and Service-Governance Framework for Long-Term Scientific Knowledge Work** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.15193v1
- **The Working Set of a Coding Agent: Coherence Debt in Repository-Scale Tasks** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.16630v1
- **Security of Foundation-Model-Powered Embodied Agents: Attack Surfaces, Attacks, Defenses, and Evaluation** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.16843v1

## Source Failures

- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.16889: arxiv:2608.16889, arxiv:2608.16889
- arxiv:2608.16630: arxiv:2608.16630, arxiv:2608.16630, arxiv:2608.16630
- arxiv:2608.16417: arxiv:2608.16417, arxiv:2608.16417
- arxiv:2608.16402: arxiv:2608.16402, arxiv:2608.16402
- arxiv:2608.16357: arxiv:2608.16357, arxiv:2608.16357, arxiv:2608.16357
- arxiv:2608.16303: arxiv:2608.16303, arxiv:2608.16303
- arxiv:2608.16185: arxiv:2608.16185, arxiv:2608.16185
- arxiv:2608.16168: arxiv:2608.16168, arxiv:2608.16168
- arxiv:2608.16114: arxiv:2608.16114, arxiv:2608.16114, arxiv:2608.16114
- arxiv:2608.15881: arxiv:2608.15881, arxiv:2608.15881
- arxiv:2608.12743: arxiv:2608.12743, arxiv:2608.12743
- arxiv:2608.10775: arxiv:2608.10775, arxiv:2608.10775
- arxiv:2608.10494: arxiv:2608.10494, arxiv:2608.10494, arxiv:2608.10494
- arxiv:2608.16515: arxiv:2608.16515, arxiv:2608.16515
- arxiv:2608.09227: arxiv:2608.09227, arxiv:2608.09227
- arxiv:2608.15975: arxiv:2608.15975, arxiv:2608.15975
- arxiv:2608.15071: arxiv:2608.15071, arxiv:2608.15071
- arxiv:2608.16697: arxiv:2608.16697, arxiv:2608.16697
- arxiv:2608.16627: arxiv:2608.16627, arxiv:2608.16627
- arxiv:2608.16513: arxiv:2608.16513, arxiv:2608.16513
- arxiv:2608.15910: arxiv:2608.15910, arxiv:2608.15910
- openalex:W7202230549: openalex:W7202230549, openalex:W7202230549, openalex:W7202230549
- doi:10.48550/arxiv.2608.07169: openalex:W7202132500, openalex:W7202132500
- openalex:W7201914503: openalex:W7201914503, openalex:W7201914503
- openalex:W7202417083: openalex:W7202417083, openalex:W7202417083
- doi:10.1007/s00146-026-03283-4: openalex:W4417529023, openalex:W4417529023
- openalex:W7202231382: openalex:W7202231382, openalex:W7202231382
- doi:10.1038/s41598-026-65740-w: openalex:W7202173114, openalex:W7202173114
- openalex:W7197053160: openalex:W7197053160, openalex:W7197053160
- doi:10.48550/arxiv.2608.11671: openalex:W7202415437, openalex:W7202415437
- doi:10.66308/air.e2026066: openalex:W7202050629, openalex:W7202050629
- doi:10.48550/arxiv.2608.09227: openalex:W7202157015, openalex:W7202157015
