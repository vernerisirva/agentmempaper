# Latest Paper Scout Digest

Latest daily digest: [2026-09-15](2026-09-15.md).

# Paper Scout Digest - 2026-09-15

## Run Summary

- **Run ID:** 86
- **Candidates fetched:** 100
- **New unique papers:** 94
- **Relevant:** 8
- **Maybe relevant:** 2
- **Irrelevant:** 90
- **Source summary:** openalex: 100, semantic_scholar: 0

## Source Warnings

- arxiv failed for 'all:deep and all:research and all:agent': http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+and+all%3Aresearch+and+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- arxiv failed for 'all:autonomous and all:research and all:agent': timeout error for https://export.arxiv.org/api/query?search_query=all%3Aautonomous+and+all%3Aresearch+and+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out
- arxiv failed for 'all:"ai scientist"': http error for https://export.arxiv.org/api/query?search_query=all%3A%22ai+scientist%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- arxiv failed for 'all:automated and all:literature and all:review': http error for https://export.arxiv.org/api/query?search_query=all%3Aautomated+and+all%3Aliterature+and+all%3Areview&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- openalex: incomplete discovery window for 'deep research agent'; single-page record limit reached.
- openalex: incomplete discovery window for 'autonomous research agent'; single-page record limit reached.
- openalex: incomplete discovery window for 'AI scientist'; single-page record limit reached.
- openalex: incomplete discovery window for 'automated literature review'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'deep research agent'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'autonomous research agent'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'AI scientist'; single-page record limit reached.
- semantic_scholar failed for 'automated literature review': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Highly Relevant

### [Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents](https://arxiv.org/abs/2609.11243)

- **Authors:** Jiaqiang Li, Yajie Yang, Zhiheng Xi, Jiadong Chen, Enyu Zhou, Senjie Jin, et al.
- **Date:** 2026-09-10
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies source-grounded research workflows, citation verification, or evidence-backed research reports.
- **Tags:** deep-research-agents, citation-grounding
- **Abstract summary:** Autonomous research agents are increasingly expected to search the literature, analyze experimental evidence, and generate scientific hypotheses. These capabilities require multi-step evidence grounded reasoning that progressively acquires, integrates, and verifies evidence before reaching a conclusion. Existing mul...
- **Automated evidence-based assessment:** 53/100 · Uncertain · Low confidence · partial full text
- **Main concerns:** Comparative claims were detected without a suitable baseline in the available text.
- **Positive signals:** The contribution is stated explicitly.; The available text identifies data or a benchmark used by the work.

### [Closing the Empirical Loop: Autonomous AI Agents Conduct End‐to‐end Research With Human Participants](https://doi.org/10.1002/advs.76675)

- **Authors:** Gabrielle Wehr, Reuben Rideaux, Amaya Fox, David R. Lightfoot, Jason M. Tangen, Jason B. Mattingley, et al.
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** relevant (93/100)
- **Reason:** Studies AI-scientist or scientific-discovery agents.
- **Tags:** ai-scientist, deep-research-agents
- **Abstract summary:** Artificial intelligence systems are transforming scientific discovery by accelerating specific research tasks, from protein structure prediction to materials design, yet remain confined to narrow domains requiring substantial human oversight. Exponential growth of scientific literature and increasing domain speciali...
- **Automated evidence-based assessment:** 42/100 · Uncertain · Low confidence · title and abstract · Limited abstract-only assessment
- **Positive signals:** User, expert, operational, or deployment evidence is described.; Limitations or threats to validity are acknowledged.
