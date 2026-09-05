"""Fixed regression examples; never interpreted as production discovery recall."""
from __future__ import annotations

import json
from pathlib import Path
from paper_scout.models import PaperCandidate


def seed_fixtures() -> list[PaperCandidate]:
    path = Path(__file__).resolve().parents[1] / "config/fixtures/engram-seeds.json"
    return [PaperCandidate(**item, source="arxiv", source_id=item["arxiv_id"],
                           url=f'https://arxiv.org/abs/{item["arxiv_id"]}',
                           publication_date_precision="day", publication_date_source="arxiv")
            for item in json.loads(path.read_text(encoding="utf-8"))["papers"]]


def regression_cases() -> list[tuple[str, str, str]]:
    # Synthetic adversarial examples supplement the recorded seed metadata.
    return [
        ("Engram table offloading for LLMs", "We evaluate hashed n-gram memory tables attached to a transformer backbone, measuring GPU/CPU memory offloading and reader latency.", "relevant"),
        ("Engram replication with negative results", "We replicate conditional memory in language models with learned n-gram tables and gating. No reasoning improvement survives matched-compute controls.", "relevant"),
        ("Learned lookup tables for language models", "We introduce learned external memory tables with hashed n-gram addressing and gates that inject values into the transformer backbone.", "relevant"),
        ("Generated conditional memory for reasoning", "We study conditional memory generated offline as hidden representations and read through lookup into a language model backbone.", "relevant"),
        ("Editing conditional memory in multilingual LLMs", "We train and update a conditional memory table addressed through byte sequences and a learned reader.", "relevant"),
        ("Biological engrams in mice", "Neuroscience studies hippocampal engram cells and synaptic memory in rodents.", "irrelevant"),
        ("Engram: a vector database for LLM agents", "Engram stores chat history and retrieves text passages into prompts using generic RAG.", "irrelevant"),
        ("Engram: a software package manager", "A database-backed package manager for application deployment.", "irrelevant"),
        ("Cross-Model Memory Transfer for LLM Agents", "We train a reader to retrieve chat history from a vector database into prompts.", "irrelevant"),
        ("Generic retrieval augmented generation", "We retrieve documents into a language model prompt for question answering.", "irrelevant"),
        ("Fine-tuning parametric memory in LLMs", "We fine-tune and distill a language model's weights for continual learning.", "irrelevant"),
        ("Efficient transformer training", "We reduce GPU memory and CUDA allocation for attention kernels.", "irrelevant"),
        ("Document retrieval for LLMs", "Related work cites Engram, a conditional memory module with hashed n-gram tables. We evaluate retrieval augmented generation over documents.", "irrelevant"),
        ("Neural memory layers for language models", "We evaluate product-key memory layers and learned addressing, with an indirect relation to conditional-memory designs.", "maybe"),
        ("Test-time memory for language models", "We investigate test-time memory through an adaptive neural memory layer; its relation to Engram is unestablished.", "maybe"),
        ("Continual learning for language models", "We study continual learning without conditional memory or learned lookup tables.", "irrelevant"),
    ]
