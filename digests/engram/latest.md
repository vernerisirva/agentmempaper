# Latest Paper Scout Digest

Latest daily digest: [2026-09-29](2026-09-29.md).

# Paper Scout Digest - 2026-09-29

## Run Summary

- **Run ID:** 28
- **Candidates fetched:** 33
- **New unique papers:** 32
- **Relevant:** 2
- **Maybe relevant:** 0
- **Irrelevant:** 31
- **Source summary:** arxiv: 6, openalex: 26, semantic_scholar: 1

## Source Warnings

- openalex failed for 'hashed memory language model': http error for https://api.openalex.org/works?search=hashed+memory+language+model&filter=from_publication_date%3A2026-09-19&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- openalex failed for 'cross-model memory transfer': http error for https://api.openalex.org/works?search=cross-model+memory+transfer&filter=from_publication_date%3A2026-09-19&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests
- openalex: incomplete discovery window for 'learned lookup memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'Engram'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'conditional memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'frozen memory reader adaptation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'tokenizer-agnostic Engram'; single-page record limit reached.

## Highly Relevant

### [FactorEngram: Factorized N-gram Memory with Basis-Level Gating for Language Models](https://arxiv.org/abs/2609.35578v1)

- **Authors:** Bowen Yang, Jingbo Zhou, Qinghong Miao, Hua Wu
- **Date:** 2026-09-28
- **Source:** arxiv
- **Relevance:** relevant (92/100)
- **Reason:** Studies model-integrated conditional memory; matched title/abstract rules: hashed-ngram-memory.
- **Tags:** engram, hashed-ngram-memory
- **Abstract summary:** Lookup-based memory has been a promising way to scale the parameters of large language models (LLMs). It retrieves learned representations of local token patterns, such as n-grams, instead of reconstructing them through successive layers of computation. However, existing designs such as Engram treat each retrieved e...
