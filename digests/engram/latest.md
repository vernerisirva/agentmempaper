# Latest Paper Scout Digest

Latest daily digest: [2026-09-06](2026-09-06.md).

# Paper Scout Digest - 2026-09-06

## Run Summary

- **Run ID:** 3
- **Candidates fetched:** 82
- **New unique papers:** 76
- **Relevant:** 5
- **Maybe relevant:** 0
- **Irrelevant:** 77
- **Source summary:** arxiv: 6, openalex: 75, semantic_scholar: 1

## Source Warnings

- openalex: incomplete discovery window for 'hashed memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'cross-model memory transfer'; single-page record limit reached.
- openalex: incomplete discovery window for 'learned lookup memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'engram'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'conditional memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'frozen memory reader adaptation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'tokenizer-agnostic engram'; single-page record limit reached.

## Highly Relevant

### [Memory Is Not Always Needed: Characterizing Conditional Memory in Scientific Reasoning](https://www.semanticscholar.org/paper/d447f4f7bd455c4d384e8fc1fb932ba295581f3a)

- **Authors:** Zhen Bi, Xueshu Chen, Yan Wang, Zhizhi Peng, Haosen Hong, Zhen Wang, et al.
- **Date:** 2026-08-25
- **Source:** arxiv
- **Relevance:** relevant (92/100)
- **Reason:** Studies model-integrated conditional memory; matched title/abstract rules: conditional-memory.
- **Tags:** conditional-memory
- **Abstract summary:** Scientific reasoning requires language models to retrieve specialized knowledge and incorporate it reliably into multi-step computation. Conditional memory provides an explicit lookup pathway that complements dense neural representations, but its usefulness is inherently input- and computation-dependent: retrieved i...
- **Automated evidence-based assessment:** 78/100 · Uncertain · Low confidence · title and abstract · Limited abstract-only assessment
- **Positive signals:** The contribution is stated explicitly.; A baseline or comparison system is described.

### [Cross-Model Memory Transfer via Target-Side Reader Adaptation](https://arxiv.org/abs/2608.17050)

- **Authors:** Mingyuan Li, Guangsheng Yu, Xu Wang, Shaoxiong Ji
- **Date:** 2026-08-17
- **Source:** openalex
- **Relevance:** relevant (92/100)
- **Reason:** Studies model-integrated conditional memory; matched title/abstract rules: hashed-ngram-memory, memory-transfer.
- **Tags:** engram, hashed-ngram-memory, memory-transfer
- **Abstract summary:** Methods for improving knowledge use in large language models typically fall into two regimes. Non-parametric retrieval offers flexible access to external knowledge, but adds retrieval latency, context overhead, and only shallow integration with the backbone. Parametric adaptation is efficient at inference time, but...
- **Automated evidence-based assessment:** 42/100 · Uncertain · Low confidence · title and abstract · Limited abstract-only assessment
- **Main concerns:** Comparative claims were detected without a suitable baseline in the available text.

### [Tokenizer-Agnostic Engram Module](https://arxiv.org/abs/2607.29065)

- **Authors:** Ji Hyun Lim, Hai Leong Chieu
- **Date:** 2026-07-31
- **Source:** openalex
- **Relevance:** relevant (92/100)
- **Reason:** Studies model-integrated conditional memory; matched title/abstract rules: conditional-memory, hashed-ngram-memory.
- **Tags:** engram, conditional-memory, hashed-ngram-memory
- **Abstract summary:** Deepseek's Engram, a conditional memory module, was introduced to trade-off storage versus reasoning in large language models. However, the module relies on token-level $N$-gram hashing for Engram embedding lookup, introducing a tight coupling to the tokenizer used: a model with a different tokenizer would have to t...
- **Automated evidence-based assessment:** 78/100 · Uncertain · Low confidence · title and abstract · Limited abstract-only assessment
- **Main concerns:** Comparative claims were detected without a suitable baseline in the available text.
- **Positive signals:** The contribution is stated explicitly.
