# Paper Scout Live Smoke Report - 2026-08-19

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 525
- **Candidates fetched:** 515
- **Unique papers:** 466
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 415
- Sample title: On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification
- Sample source ID: 2608.18066
- Sample URL: https://arxiv.org/abs/2608.18066v1
- Sample published date: 2026-08-18
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
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 21
- maybe: 55
- irrelevant: 390

## Top Relevant Or Maybe Papers

- **What to Remember, What to Reveal: Privacy-Aware Memory for Conversational Agents** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2608.16551v1
- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775v1
- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775
- **From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.10502
- **D$^2$ACCI: A Dual-Loop Diagnostic Protocol for Evidence-Preserving Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.17756v1
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://doi.org/10.48550/arxiv.2608.07169
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2608.07169
- **KernelArc: A Multi-Agent Framework for GPU Kernel Optimization** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2608.17071v1
- **The Working Set of a Coding Agent: Coherence Debt in Repository-Scale Tasks** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.16630v1
- **Security of Foundation-Model-Powered Embodied Agents: Attack Surfaces, Attacks, Defenses, and Evaluation** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.16843v1

## Source Failures

- semantic_scholar (HTTP/API error) for `agent memory`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.18066: arxiv:2608.18066, arxiv:2608.18066
- arxiv:2608.17911: arxiv:2608.17911, arxiv:2608.17911
- arxiv:2608.17756: arxiv:2608.17756, arxiv:2608.17756
- arxiv:2608.17684: arxiv:2608.17684, arxiv:2608.17684
- arxiv:2608.17665: arxiv:2608.17665, arxiv:2608.17665, arxiv:2608.17665
- arxiv:2608.17605: arxiv:2608.17605, arxiv:2608.17605
- arxiv:2608.17592: arxiv:2608.17592, arxiv:2608.17592
- arxiv:2608.17347: arxiv:2608.17347, arxiv:2608.17347
- arxiv:2608.17310: arxiv:2608.17310, arxiv:2608.17310
- arxiv:2608.17247: arxiv:2608.17247, arxiv:2608.17247
- arxiv:2608.17209: arxiv:2608.17209, arxiv:2608.17209
- arxiv:2608.17148: arxiv:2608.17148, arxiv:2608.17148
- arxiv:2608.17071: arxiv:2608.17071, arxiv:2608.17071
- arxiv:2608.17053: arxiv:2608.17053, arxiv:2608.17053
- arxiv:2608.17007: arxiv:2608.17007, arxiv:2608.17007, arxiv:2608.17007
- arxiv:2608.16889: arxiv:2608.16889, arxiv:2608.16889
- arxiv:2608.16630: arxiv:2608.16630, arxiv:2608.16630
- arxiv:2608.16357: arxiv:2608.16357, arxiv:2608.16357
- arxiv:2608.12743: arxiv:2608.12743, arxiv:2608.12743
- arxiv:2608.10775: arxiv:2608.10775, arxiv:2608.10775
- arxiv:2608.10494: arxiv:2608.10494, arxiv:2608.10494, arxiv:2608.10494
- arxiv:2608.17443: arxiv:2608.17443, arxiv:2608.17443
- arxiv:2608.17050: arxiv:2608.17050, arxiv:2608.17050
- arxiv:2608.09227: arxiv:2608.09227, arxiv:2608.09227
- arxiv:2608.17515: arxiv:2608.17515, arxiv:2608.17515
- arxiv:2608.15071: arxiv:2608.15071, arxiv:2608.15071
- arxiv:2608.18027: arxiv:2608.18027, arxiv:2608.18027
- arxiv:2608.17781: arxiv:2608.17781, arxiv:2608.17781
- arxiv:2608.17567: arxiv:2608.17567, arxiv:2608.17567
- arxiv:2608.17336: arxiv:2608.17336, arxiv:2608.17336
- arxiv:2608.17253: arxiv:2608.17253, arxiv:2608.17253
- arxiv:2608.17084: arxiv:2608.17084, arxiv:2608.17084
- openalex:W7202230549: openalex:W7202230549, openalex:W7202230549, openalex:W7202230549
- doi:10.48550/arxiv.2608.07169: openalex:W7202132500, openalex:W7202132500
- openalex:W7201914503: openalex:W7201914503, openalex:W7201914503
- doi:10.48550/arxiv.2608.10538: openalex:W7202417083, openalex:W7202417083
- doi:10.1007/s00146-026-03283-4: openalex:W4417529023, openalex:W4417529023
- openalex:W7202231382: openalex:W7202231382, openalex:W7202231382
- doi:10.1038/s41598-026-65740-w: openalex:W7202173114, openalex:W7202173114
- doi:10.48550/arxiv.2608.11671: openalex:W7202415437, openalex:W7202415437
- doi:10.66308/air.e2026066: openalex:W7202050629, openalex:W7202050629
- openalex:W7202005914: openalex:W7202005914, openalex:W7202005914
- doi:10.48550/arxiv.2608.09227: openalex:W7202157015, openalex:W7202157015
- doi:10.5281/zenodo.21966214: openalex:W7203585882, openalex:W7203585882
- doi:10.5281/zenodo.21966215: openalex:W7203574771, openalex:W7203574771
