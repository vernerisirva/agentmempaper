# Paper Scout Live Smoke Report - 2026-08-14

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 600
- **Candidates fetched:** 519
- **Unique papers:** 467
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 417
- Sample title: Intern-S2-Preview: Scientific Agentic Foundation Model
- Sample source ID: 2608.13505
- Sample URL: https://arxiv.org/abs/2608.13505v1
- Sample published date: 2026-08-13
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
- Queries attempted: 4
- Raw records: 75
- Converted candidates: 2
- Sample title: Activation-Guided Neuron Intervention to Induce Alzheimer's-Related Computational Language Phenotypes in a Large Language Model
- Sample source ID: b5233936e6221a748c0bb73139ed33cb35a84580
- Sample URL: https://www.semanticscholar.org/paper/b5233936e6221a748c0bb73139ed33cb35a84580
- Sample published date: 2026-08-04
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 28
- maybe: 38
- irrelevant: 401

## Top Relevant Or Maybe Papers

- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://doi.org/10.48550/arxiv.2607.29032
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032v1
- **TransMem: Transforming Hidden States into Memory for Large Language Models** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2607.29032
- **The Sleeping Agent: What Gist-Based Context Compression Loses and Why** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.11775v1
- **SkillLens: Visual Skill Cards for Retrieval-Augmented GUI Action Prediction and On-Policy Distillation** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2608.10775v1
- **RippleMem: From Isolated Retrieval to Associative Recollection for Long-Term Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.13334v1
- **RING: Retrieval-Internalized Generation for Continual Large-Scale Knowledge Injection** (relevant, 100/100): Discusses Engram-style or parametric memory mechanisms for language models. https://arxiv.org/abs/2608.01630v1
- **LycheeMemory V2: Efficient Long-Term Memory for LLM Agents via Semantic Segment-Level Consolidation** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2608.12990v1
- **ERSkill: Evolving for Skill-Guided Adaptive Memory Retrieval** (relevant, 100/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2608.12720v1
- **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://doi.org/10.48550/arxiv.2608.07169

## Source Failures

- semantic_scholar (HTTP/API error) for `parametric memory LLM`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2608.13505: arxiv:2608.13505, arxiv:2608.13505, arxiv:2608.13505
- arxiv:2608.13420: arxiv:2608.13420, arxiv:2608.13420
- arxiv:2608.13334: arxiv:2608.13334, arxiv:2608.13334
- arxiv:2608.13317: arxiv:2608.13317, arxiv:2608.13317
- arxiv:2608.12990: arxiv:2608.12990, arxiv:2608.12990
- arxiv:2608.12888: arxiv:2608.12888, arxiv:2608.12888
- arxiv:2608.12847: arxiv:2608.12847, arxiv:2608.12847, arxiv:2608.12847
- arxiv:2608.12841: arxiv:2608.12841, arxiv:2608.12841, arxiv:2608.12841
- arxiv:2608.12743: arxiv:2608.12743, arxiv:2608.12743, arxiv:2608.12743, arxiv:2608.12743
- arxiv:2608.12720: arxiv:2608.12720, arxiv:2608.12720, arxiv:2608.12720
- arxiv:2608.12629: arxiv:2608.12629, arxiv:2608.12629
- arxiv:2608.12627: arxiv:2608.12627, arxiv:2608.12627
- arxiv:2608.12626: arxiv:2608.12626, arxiv:2608.12626
- arxiv:2608.12476: arxiv:2608.12476, arxiv:2608.12476
- arxiv:2608.12308: arxiv:2608.12308, arxiv:2608.12308
- arxiv:2608.11967: arxiv:2608.11967, arxiv:2608.11967, arxiv:2608.11967
- arxiv:2608.12428: arxiv:2608.12428, arxiv:2608.12428
- arxiv:2608.12973: arxiv:2608.12973, arxiv:2608.12973
- arxiv:2608.12573: arxiv:2608.12573, arxiv:2608.12573
- arxiv:2608.12486: arxiv:2608.12486, arxiv:2608.12486, arxiv:2608.12486
- arxiv:2608.10775: arxiv:2608.10775, arxiv:2608.10775
- arxiv:2608.10494: arxiv:2608.10494, arxiv:2608.10494, arxiv:2608.10494
- arxiv:2608.04009: arxiv:2608.04009, arxiv:2608.04009
- doi:10.1145/3744916.3787762: arxiv:2608.03286, openalex:W7196981404
- arxiv:2608.03067: arxiv:2608.03067, semantic_scholar:b5233936e6221a748c0bb73139ed33cb35a84580
- arxiv:2608.09227: arxiv:2608.09227, arxiv:2608.09227
- arxiv:2608.07169: arxiv:2608.07169, semantic_scholar:ef80169359a279f206b2dcc012b3100bc4fe8de1
- arxiv:2608.13560: arxiv:2608.13560, arxiv:2608.13560
- arxiv:2608.13463: arxiv:2608.13463, arxiv:2608.13463
- arxiv:2608.12977: arxiv:2608.12977, arxiv:2608.12977
- arxiv:2608.12290: arxiv:2608.12290, arxiv:2608.12290
- openalex:W7202230549: openalex:W7202230549, openalex:W7202230549, openalex:W7202230549
- doi:10.48550/arxiv.2608.07169: openalex:W7202132500, openalex:W7202132500
- openalex:W7201914503: openalex:W7201914503, openalex:W7201914503
- doi:10.1145/3831684: openalex:W4405562150, openalex:W4405562150
- openalex:W7202231382: openalex:W7202231382, openalex:W7202231382
- doi:10.1038/s41598-026-65740-w: openalex:W7202173114, openalex:W7202173114
- openalex:W7197053160: openalex:W7197053160, openalex:W7197053160
- openalex:W7202005914: openalex:W7202005914, openalex:W7202005914
- openalex:W7172474001: openalex:W7172474001, openalex:W7172474001
- doi:10.48550/arxiv.2607.29032: openalex:W7172337063, openalex:W7172337063
- doi:10.48550/arxiv.2608.09227: openalex:W7202157015, openalex:W7202157015
