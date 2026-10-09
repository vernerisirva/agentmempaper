# Paper Scout Live Smoke Report - 2026-10-09

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 200
- **Candidates fetched:** 103
- **Unique papers:** 99
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

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

- Status: Success
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 3
- Sample title: Revisit to Segment: Working Memory Distillation for Reasoning Segmentation
- Sample source ID: b14255a74a257c02d84c51a6fe10276ee2843f4e
- Sample URL: https://www.semanticscholar.org/paper/b14255a74a257c02d84c51a6fe10276ee2843f4e
- Sample published date: 2026-09-28
- Abstract: yes


## Decisions

- relevant: 13
- maybe: 19
- irrelevant: 67

## Top Relevant Or Maybe Papers

- **Revisit to Segment: Working Memory Distillation for Reasoning Segmentation** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://www.semanticscholar.org/paper/b14255a74a257c02d84c51a6fe10276ee2843f4e
- **Revisit to Segment: Working Memory Distillation for Reasoning Segmentation** (relevant, 100/100): Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights. https://arxiv.org/abs/2609.34863
- **MemFit: Efficient Long-Term Agentic Memory** (relevant, 100/100): Focuses on persistent or long-term memory for agent behavior. https://arxiv.org/abs/2610.00872
- **What the Score Measured: Failure Attribution in an Agent Memory Evaluation** (relevant, 99/100): Evaluates memory mechanisms or benchmarks for LLM agents. https://doi.org/10.5281/zenodo.22980059
- **RecallDB: A Local-First, Bitemporal Hybrid Engine for Long-Horizon Agent Memory and Decoupled Evaluation** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.23107755
- **ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://www.semanticscholar.org/paper/57563394951aebb6d7f5611808eac0ba14a5bb87
- **OmniSmartHome: A Multimodal Reasoning Benchmark for Smart-Home Agents** (relevant, 91/100): Studies memory systems or memory modules for LLM agents. https://arxiv.org/abs/2609.32569
- **Coding Agent Memory Post-training: Unlocking the Memory Potential of Pre-trained File Operations for Long-Horizon Tasks via Reinforcement Learning** (relevant, 91/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://arxiv.org/abs/2609.34422
- **Understanding and Mitigating Inference-Time Overreliance Using Agentic Memory** (relevant, 90/100): Studies memory systems or memory modules for LLM agents. https://doi.org/10.48550/arxiv.2610.07311
- **The Homeostatic Substrate Hypothesis Persistent Agent Memory as Ecological Tissue** (relevant, 90/100): Studies governed shared memory or persistent memory protocols for LLM agents. https://doi.org/10.5281/zenodo.23239488

## Source Failures

- arxiv (HTTP/API error) for `agent memory`: http error for https://export.arxiv.org/api/query?search_query=all%3Aagent+AND+all%3Amemory&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- doi:10.48550/arxiv.2609.37725: openalex:W7214993655, openalex:W7214993655
- doi:10.1016/j.wpi.2026.102506: openalex:W7214490834, openalex:W7214490834
- doi:10.48550/arxiv.2609.30936: openalex:W7214630903, openalex:W7214630903
- doi:10.48550/arxiv.2609.33268: openalex:W7214747287, openalex:W7214747287
