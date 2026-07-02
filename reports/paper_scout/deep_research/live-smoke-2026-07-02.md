# Paper Scout Live Smoke Report - 2026-07-02

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 0
- **Sources failed:** 3
- **Raw records:** 302
- **Candidates fetched:** 25
- **Unique papers:** 16
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 18
- Raw records: 177
- Converted candidates: 24
- Sample title: Breaking the Evaluation Paradox: Evaluating High-Entropy Search with Computationally Irreducible Constraints
- Sample source ID: 2606.22783
- Sample URL: https://arxiv.org/abs/2606.22783v1
- Sample published date: 2026-06-22
- Abstract: yes
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22AutoResearch%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-06-18&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable

### semantic_scholar

- Status: Failed
- Queries attempted: 6
- Raw records: 125
- Converted candidates: 1
- Sample title: Clarus: Coordinating Autonomous Research Agents toward Web-Scale Scientific Collaboration
- Sample source ID: e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample URL: https://www.semanticscholar.org/paper/e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample published date: 2026-06-29
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 15
- maybe: 1
- irrelevant: 0

## Top Relevant Or Maybe Papers

- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.29981v1
- **One Reflection Is Not Enough: Self-Correcting Autonomous Research via Multi-Hypothesis Failure Attribution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2606.31478v1
- **Socratic agents for autonomous scientific discovery in high-dimensional physical systems** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.26722v1
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.31273v1
- **Position: Correct Answer, Wrong Mechanism -- When AI Scientists Defend General Claims Their Own Data Contradicts** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.23175v1
- **Measuring Biological Capabilities and Risks of AI Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.19899v1
- **Joint discovery of governing partial differential equations from multi-source datasets by competitive optimization** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.30699v1
- **Agentic-Ideation: Sample Efficient Agentic Trajectories Synthesis for Scientific Ideation Agents** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.31229v1
- **Agentic evolution of physically constrained foundation models** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.25532v1
- **AICID: Unique Identifiers for AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.28756v2

## Source Failures

- openalex (HTTP/API error) for `deep research agent`: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-06-18&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable
- semantic_scholar (HTTP/API error) for `AI research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- arxiv (HTTP/API error) for `AutoResearch`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22AutoResearch%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- arxiv:2606.22783: arxiv:2606.22783, arxiv:2606.22783
- arxiv:2606.20122: arxiv:2606.20122, arxiv:2606.20122
- arxiv:2606.19893: arxiv:2606.19893, arxiv:2606.19893
- arxiv:2606.31478: arxiv:2606.31478, arxiv:2606.31478, arxiv:2606.31478
- arxiv:2606.30246: arxiv:2606.30246, arxiv:2606.30246, semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- arxiv:2606.29981: arxiv:2606.29981, arxiv:2606.29981
- arxiv:2606.22859: arxiv:2606.22859, arxiv:2606.22859
