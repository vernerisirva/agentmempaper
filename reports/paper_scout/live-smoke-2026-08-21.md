# Paper Scout Live Smoke Report - 2026-08-21

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 575
- **Candidates fetched:** 516
- **Unique papers:** 471
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 416
- Sample title: Break It Down, Pass It On: Cross-Task Skill Transfer in LLM Agents
- Sample source ID: 2608.20274
- Sample URL: https://arxiv.org/abs/2608.20274v1
- Sample published date: 2026-08-20
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
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 24
- maybe: 53
- irrelevant: 394

## Top Relevant Or Maybe Papers

- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775v1
- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775
- **From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.10502
- **D$^2$ACCI: A Dual-Loop Diagnostic Protocol for Evidence-Preserving Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.17756v2
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://doi.org/10.48550/arxiv.2608.07169
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2608.07169
- **The Working Set of a Coding Agent: Coherence Debt in Repository-Scale Tasks** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.16630v1
- **Report on The 1st Workshop on Human-Centered Proactive and Personalized Agents for Interactive Information Access at CHIIR 2026** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.18638v1
- **Remember, Verify, or Ask? Cross-Family Evaluation of Memory Commitment in LLM Agents** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.19564v1
- **RAF-LLM: A retrieval-augmented large language model framework for remaining useful life prediction of rotating machinery** (relevant, 91/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.1088/1361-6501/ae989d

## Source Failures

- semantic_scholar (HTTP/API error) for `memory distillation`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.20274: arxiv:2608.20274, arxiv:2608.20274
- arxiv:2608.20201: arxiv:2608.20201, arxiv:2608.20201
- arxiv:2608.19857: arxiv:2608.19857, arxiv:2608.19857
- arxiv:2608.19842: arxiv:2608.19842, arxiv:2608.19842
- arxiv:2608.19779: arxiv:2608.19779, arxiv:2608.19779
- arxiv:2608.19701: arxiv:2608.19701, arxiv:2608.19701
- arxiv:2608.19662: arxiv:2608.19662, arxiv:2608.19662
- arxiv:2608.19652: arxiv:2608.19652, arxiv:2608.19652
- arxiv:2608.19621: arxiv:2608.19621, arxiv:2608.19621, arxiv:2608.19621
- arxiv:2608.19564: arxiv:2608.19564, arxiv:2608.19564
- arxiv:2608.19197: arxiv:2608.19197, arxiv:2608.19197, arxiv:2608.19197
- arxiv:2608.19047: arxiv:2608.19047, arxiv:2608.19047
- arxiv:2608.19029: arxiv:2608.19029, arxiv:2608.19029
- arxiv:2608.19013: arxiv:2608.19013, arxiv:2608.19013
- arxiv:2608.18952: arxiv:2608.18952, arxiv:2608.18952, arxiv:2608.18952
- arxiv:2608.18637: arxiv:2608.18637, arxiv:2608.18637
- arxiv:2608.19151: arxiv:2608.19151, arxiv:2608.19151
- arxiv:2608.12743: arxiv:2608.12743, arxiv:2608.12743
- arxiv:2608.10775: arxiv:2608.10775, arxiv:2608.10775
- arxiv:2608.10494: arxiv:2608.10494, arxiv:2608.10494, arxiv:2608.10494
- arxiv:2608.15071: arxiv:2608.15071, arxiv:2608.15071
- arxiv:2608.20318: arxiv:2608.20318, arxiv:2608.20318
- arxiv:2608.20290: arxiv:2608.20290, arxiv:2608.20290
- arxiv:2608.19807: arxiv:2608.19807, arxiv:2608.19807
- arxiv:2608.19490: arxiv:2608.19490, arxiv:2608.19490
- arxiv:2608.18933: arxiv:2608.18933, arxiv:2608.18933
- openalex:W7202230549: openalex:W7202230549, openalex:W7202230549, openalex:W7202230549
- doi:10.48550/arxiv.2608.07169: openalex:W7202132500, openalex:W7202132500
- doi:10.48550/arxiv.2608.11654: openalex:W7202382037, openalex:W7202382037
- doi:10.1007/s00146-026-03283-4: openalex:W4417529023, openalex:W4417529023
- doi:10.48550/arxiv.2608.10538: openalex:W7202417083, openalex:W7202417083
- openalex:W7202231382: openalex:W7202231382, openalex:W7202231382
- doi:10.1038/s41598-026-65740-w: openalex:W7202173114, openalex:W7202173114
- doi:10.48550/arxiv.2608.11671: openalex:W7202415437, openalex:W7202415437
- doi:10.66308/air.e2026066: openalex:W7202050629, openalex:W7202050629
- doi:10.48550/arxiv.2608.10775: openalex:W7202244235, openalex:W7202244235
- doi:10.48550/arxiv.2608.08512: openalex:W7202187479, openalex:W7202187479
- doi:10.48550/arxiv.2608.09227: openalex:W7202157015, openalex:W7202157015
- doi:10.5281/zenodo.21966214: openalex:W7203585882, openalex:W7203585882
- doi:10.5281/zenodo.21966215: openalex:W7203574771, openalex:W7203574771
