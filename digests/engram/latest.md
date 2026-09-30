# Latest Paper Scout Digest

Latest daily digest: [2026-09-30](2026-09-30.md).

# Paper Scout Digest - 2026-09-30

## Run Summary

- **Run ID:** 29
- **Candidates fetched:** 58
- **New unique papers:** 57
- **Relevant:** 3
- **Maybe relevant:** 0
- **Irrelevant:** 55
- **Source summary:** arxiv: 6, openalex: 51, semantic_scholar: 1

## Source Warnings

- openalex failed for 'hashed memory language model': http error for https://api.openalex.org/works?search=hashed+memory+language+model&filter=from_publication_date%3A2026-09-20&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- openalex: incomplete discovery window for 'cross-model memory transfer'; single-page record limit reached.
- openalex: incomplete discovery window for 'learned lookup memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'Engram'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'conditional memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'frozen memory reader adaptation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'tokenizer-agnostic Engram'; single-page record limit reached.

## Highly Relevant

### [FactorEngram: Factorized N-gram Memory with Basis-Level Gating for Language Models](https://doi.org/10.48550/arxiv.2609.35578)

- **Authors:** Bowen Yang, Jingbo Zhou, Qinghong Miao, Hua Wu
- **Date:** 2026-09-28
- **Source:** openalex
- **Relevance:** relevant (92/100)
- **Reason:** Studies model-integrated conditional memory; matched title/abstract rules: hashed-ngram-memory.
- **Tags:** engram, hashed-ngram-memory
- **Abstract summary:** Lookup-based memory has been a promising way to scale the parameters of large language models (LLMs). It retrieves learned representations of local token patterns, such as n-grams, instead of reconstructing them through successive layers of computation. However, existing designs such as Engram treat each retrieved e...
