# Paper Scout Live Smoke Report - 2026-10-08

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 550
- **Candidates fetched:** 520
- **Unique papers:** 492
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Success
- Queries attempted: 6
- Raw records: 425
- Converted candidates: 420
- Sample title: EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution
- Sample source ID: 2610.10498
- Sample URL: https://arxiv.org/abs/2610.10498v1
- Sample published date: 2026-10-07
- Abstract: yes

### openalex

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 100
- Sample title: Just-In-Time Agent Memory with Runtime Agentic Research
- Sample source ID: W7214766919
- Sample URL: https://arxiv.org/abs/2609.34385
- Sample published date: 2026-09-28
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 2
- Raw records: 25
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 26
- maybe: 41
- irrelevant: 425

## Top Relevant Or Maybe Papers

- **agmi: Agent Memory Integrity, a conformance test suite for tamper evidence in AI agent memory and checkpoint stores** (relevant, 100/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.22860886
- **Revisit to Segment: Working Memory Distillation for Reasoning Segmentation** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2609.34863
- **Relevance Is Not Sufficiency: What Actually Closes the Evidence Gap in Long-Term Memory QA** (relevant, 100/100): Studies memory storage, retrieval, update, or consolidation for LLM agents. https://arxiv.org/abs/2610.09348v1
- **MemFit: Efficient Long-Term Agentic Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.00872
- **MINDSET: Energy-based Schema Evolution for Long Conversational Agent Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.08586v1
- **What the Score Measured: Failure Attribution in an Agent Memory Evaluation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.22980059
- **Stale, Misattributed, or Late: Where Personal Memory Fails Before Generation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://arxiv.org/abs/2610.10265v1
- **Whose Memory Is It? Scope-Aware Commit Rules for Long-Term LLM Memory** (relevant, 91/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.09008v1
- **Scope Before You Persist: Preventing Cross-Family Interference in Agent Memory** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2609.29144
- **RecallDB: A Local-First, Bitemporal Hybrid Engine for Long-Horizon Agent Memory and Decoupled Evaluation** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.23107755

## Source Failures

- semantic_scholar (HTTP/API error) for `procedural memory language model`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- arxiv:2610.10498: arxiv:2610.10498, arxiv:2610.10498
- arxiv:2610.10265: arxiv:2610.10265, arxiv:2610.10265
- arxiv:2610.10242: arxiv:2610.10242, arxiv:2610.10242
- arxiv:2610.10183: arxiv:2610.10183, arxiv:2610.10183
- arxiv:2610.10091: arxiv:2610.10091, arxiv:2610.10091
- arxiv:2610.10071: arxiv:2610.10071, arxiv:2610.10071, arxiv:2610.10071
- arxiv:2610.09872: arxiv:2610.09872, arxiv:2610.09872
- arxiv:2610.09832: arxiv:2610.09832, arxiv:2610.09832
- arxiv:2610.09590: arxiv:2610.09590, arxiv:2610.09590
- arxiv:2610.08630: arxiv:2610.08630, arxiv:2610.08630, arxiv:2610.08630
- arxiv:2610.08048: arxiv:2610.08048, arxiv:2610.08048
- arxiv:2610.02542: arxiv:2610.02542, arxiv:2610.02542
- arxiv:2610.09639: arxiv:2610.09639, arxiv:2610.09639, arxiv:2610.09639
- arxiv:2610.04262: arxiv:2610.04262, arxiv:2610.04262
- arxiv:2610.10058: arxiv:2610.10058, arxiv:2610.10058
- arxiv:2610.10088: arxiv:2610.10088, arxiv:2610.10088
- arxiv:2610.09841: arxiv:2610.09841, arxiv:2610.09841
- arxiv:2610.09795: arxiv:2610.09795, arxiv:2610.09795
- arxiv:2610.09700: arxiv:2610.09700, arxiv:2610.09700
- arxiv:2610.09665: arxiv:2610.09665, arxiv:2610.09665
- doi:10.48550/arxiv.2609.37725: openalex:W7214993655, openalex:W7214993655
- doi:10.1016/j.wpi.2026.102506: openalex:W7214490834, openalex:W7214490834
- doi:10.48550/arxiv.2609.30936: openalex:W7214630903, openalex:W7214630903
- doi:10.48550/arxiv.2609.33268: openalex:W7214747287, openalex:W7214747287
- doi:10.1145/3843750: openalex:W7216260891, openalex:W7216260891
