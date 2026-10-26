# Latest Paper Scout Digest

Latest daily digest: [2026-10-26](2026-10-26.md).

# Paper Scout Digest - 2026-10-26

## Run Summary

- **Run ID:** 53
- **Candidates fetched:** 85
- **New unique papers:** 79
- **Relevant:** 4
- **Maybe relevant:** 0
- **Irrelevant:** 81
- **Source summary:** arxiv: 5, openalex: 79, semantic_scholar: 1

## Source Warnings

- openalex: incomplete discovery window for 'hashed memory language model'; single-page record limit reached.
- openalex: incomplete discovery window for 'cross-model memory transfer'; single-page record limit reached.
- openalex: incomplete discovery window for 'learned lookup memory language model'; single-page record limit reached.
- semantic_scholar failed for 'Engram': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar: incomplete discovery window for 'conditional memory language model'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'frozen memory reader adaptation'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'tokenizer-agnostic Engram'; single-page record limit reached.

## Highly Relevant

### [Fast to Write, Slow to Learn: Instant N-gram Notes that Upgrade to Learning Neurons for Two-Layer Dynamic Memory in a Production Inference Engine](https://doi.org/10.5281/zenodo.23604600)

- **Authors:** Ashley Hart, Petrus Pennanen
- **Date:** 2026-10-23
- **Source:** openalex
- **Relevance:** relevant (92/100)
- **Reason:** Studies model-integrated conditional memory; matched title/abstract rules: hashed-ngram-memory.
- **Tags:** engram, hashed-ngram-memory
- **Abstract summary:** A language model in use keeps hearing facts it should remember, such as a new address or a changed preference. Retraining is too slow for this, and putting every fact into the prompt costs tokens on every answer. DeepSeek's Engram showed that an n-gram lookup table inside a model is a cheap, high-capacity memory, bu...

### [Low-Bit N-Gram Embeddings for Language Models](https://arxiv.org/abs/2610.31646)

- **Authors:** Stephen Chung, Wenyu Du
- **Date:** 2026-10-22
- **Source:** openalex
- **Relevance:** relevant (92/100)
- **Reason:** Studies model-integrated conditional memory; matched title/abstract rules: hashed-ngram-memory.
- **Tags:** engram, hashed-ngram-memory
- **Abstract summary:** Many recent open-weight language models use n-gram embedding tables to improve performance. These tables store learned representations of short token sequences, such as pairs or triples of consecutive tokens, which the model retrieves during processing. However, they can require substantial memory: DeepSeek-V4.1-Fla...

### [Delta N-gram: Forward-Only Continual Writing into a Language Model's Native N-gram Memory](https://arxiv.org/abs/2610.31125)

- **Authors:** Hao Wu
- **Date:** 2026-10-22
- **Source:** openalex
- **Relevance:** relevant (92/100)
- **Reason:** Studies model-integrated conditional memory; matched title/abstract rules: hashed-ngram-memory.
- **Tags:** hashed-ngram-memory
- **Abstract summary:** Our previous analysis found that a model's native hashed N-gram table is where continual updates disturb the base least, but its writes needed backpropagation and changed the pretrained table. We present Delta N-gram, a forward-only write path into that table. The pretrained table T^0 is never modified. Evidence is...
