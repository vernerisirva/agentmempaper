from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from paper_scout.llm import classify_with_optional_llm
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.relevance import classify_with_rules, should_consider_for_llm


@dataclass(frozen=True)
class RelevanceExample:
    name: str
    expected_relevant: bool
    candidate: PaperCandidate
    expected_decision: str | None = None


def relevance_fixture_examples(profile: str = "agent_memory") -> list[RelevanceExample]:
    from paper_scout.config import validate_track
    validate_track(profile)
    if profile == "engram":
        from paper_scout.engram_evaluation import seed_fixtures, regression_cases
        examples = [RelevanceExample(p.arxiv_id, True, p, "relevant") for p in seed_fixtures()]
        for title, abstract, decision in regression_cases():
            examples.append(RelevanceExample(title, decision in {"relevant", "maybe"}, PaperCandidate(title, ["Synthetic fixture"], abstract, "fixture", title), decision))
        return examples
    if profile == "deep_research":
        return deep_research_fixture_examples()
    if profile == "computer_vision":
        return computer_vision_fixture_examples()
    relevant = [
        ("long-term memory for LLM agents", "Long-Term Memory for LLM Agents", "Persistent long-term memory for language model agents with retrieval and update policies."),
        ("episodic memory in autonomous agents", "Episodic Memory in Autonomous Agents", "Autonomous LLM agents store episodic memory across multi-step tasks."),
        ("semantic memory for deep research agents", "Semantic Memory for Deep Research Agents", "Deep research agents maintain semantic memory while producing literature reviews."),
        ("procedural memory for tool-using agents", "Procedural Memory for Tool-Using Agents", "Tool-using language agents learn procedural memory for recurring workflows."),
        ("persistent memory in literature-review agents", "Persistent Memory in Literature-Review Agents", "Research agents use persistent memory to avoid stale literature-review context."),
        ("memory write/read policies for LLM agents", "Memory Write and Read Policies for LLM Agents", "We evaluate memory write policy and retrieval policy choices in LLM agents."),
        ("agent memory benchmark", "Agent Memory Benchmark", "A benchmark for persistent memory in language model agents."),
        ("agent-native memory system", "Are We Ready For An Agent-Native Memory System?", "Memory for large language model agents supports persistent information storage, retrieval, update, consolidation, and lifecycle governance throughout agent execution."),
        ("parametric memory for language agents", "Parametric Memory for Language Agents", "Parametric memory mechanisms are evaluated in agent behavior."),
        (
            "procedural memory distillation",
            "Procedural Memory Distillation: Online Reflection for Self-Improving Language Models",
            "Cross-episode signals and online reflection convert experience into reusable procedural memory distilled into a language model's weights for self-improvement.",
        ),
        ("Engram-style mechanisms in LLMs", "Engram-Style Mechanisms in LLMs", "Engram memory mechanisms alter language model behavior for long-running agents."),
        ("multilingual Engram-style memory", "Multilingual Engram-Style Memory", "A multilingual Engram memory mechanism for language model agents."),
    ]
    irrelevant = [
        ("GPU memory allocation", "GPU Memory Allocation for Training", "CUDA kernels allocate GPU memory efficiently."),
        ("CUDA memory fragmentation", "CUDA Memory Fragmentation", "A runtime method reduces CUDA memory fragmentation."),
        ("memory-efficient attention only", "Memory-Efficient Attention", "Attention kernels reduce KV cache and memory use."),
        ("database in-memory indexing", "In-Memory Database Indexing", "Database memory indexing improves transaction throughput."),
        ("operating system memory paging", "Operating System Memory Paging", "A memory paging algorithm for operating systems."),
        ("human memory psychology without AI agents", "Human Cognitive Memory", "Psychology experiments study human memory recall."),
        ("generic RAG without persistent memory", "Generic RAG for Question Answering", "A generic RAG system retrieves documents without persistent memory."),
        ("vector database retrieval without agent memory", "Vector Database Retrieval", "Vector search improves document retrieval without agent memory."),
        ("memory bandwidth optimization", "Memory Bandwidth Optimization", "Hardware memory bandwidth optimization for GPUs."),
        ("cache optimization", "Cache Optimization", "Compiler cache optimization for numerical kernels."),
    ]
    examples: list[RelevanceExample] = []
    for name, title, abstract in relevant:
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=True,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/relevant", published_date="2026-01-01"),
            )
        )
    for name, title, abstract in irrelevant:
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=False,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/irrelevant", published_date="2026-01-01"),
            )
        )
    return examples


def deep_research_fixture_examples() -> list[RelevanceExample]:
    relevant = [
        ("deep research agent", "Deep Research Agents for Source-Grounded Reports", "A deep research agent decomposes research tasks, browses sources, verifies citations, and writes source-grounded research reports."),
        ("autonomous research agent", "Autonomous Research Agents", "Autonomous research agents plan multi-step scientific literature reviews and synthesize evidence."),
        ("AI scientist", "AI Scientist for Automated Scientific Discovery", "An AI scientist agent proposes hypotheses, designs experiments, and evaluates scientific evidence."),
        ("automated literature review", "Automated Literature Review Agents", "LLM literature review agents search papers, extract evidence, and maintain citation-grounded review state."),
        ("citation verification agent", "Citation Verification Agents for Research Reports", "A citation verification agent checks source support and evidence grounding in generated research reports."),
        ("multi-agent research workflow", "Multi-Agent Research Workflow System", "A multi-agent research workflow coordinates planning, source analysis, and report writing."),
        ("hypothesis and experiment agent", "Hypothesis Generation and Experiment Design Agents", "Agents generate hypotheses and design experiments for AI-assisted scientific discovery."),
        ("research-agent memory", "Iterative Research State for Deep Research Agents", "Research-agent memory preserves iterative research state across literature search sessions."),
    ]
    irrelevant = [
        ("generic deep learning", "Deep Learning Optimization for Image Classification", "A generic deep learning optimization method for image classification."),
        ("generic AutoML", "AutoML for Hyperparameter Search", "AutoML selects model hyperparameters without autonomous research workflows."),
        ("market research", "Market Research Automation with Chatbots", "A chatbot automates customer survey analysis for business market research."),
        ("autonomous driving", "Autonomous Driving Planning Benchmark", "Robotics and autonomous driving planning benchmark unrelated to research workflows."),
        ("generic chatbot", "General Chatbot Alignment", "A general chatbot paper without research, citation, evidence, or literature-review workflow."),
        ("generic RAG", "Generic RAG for Question Answering", "A generic RAG system retrieves documents without research workflow or citation verification."),
        ("generic benchmark", "General LLM Benchmark Suite", "A generic benchmark paper not about research agents."),
    ]
    examples: list[RelevanceExample] = []
    for name, title, abstract in relevant:
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=True,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/deep-relevant", published_date="2026-01-01"),
            )
        )
    for name, title, abstract in irrelevant:
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=False,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/deep-irrelevant", published_date="2026-01-01"),
            )
        )
    return examples


def computer_vision_fixture_examples() -> list[RelevanceExample]:
    """Pinned distinctions for the computer-vision screen.

    Three groups, and the middle one carries the policy. Core papers are methodological
    vision contributions. Hard negatives share vocabulary with vision work but have no
    visual subject at all. The borderline group is where a detection-heavy profile would
    otherwise overfit: a domain application of an existing detector, a vision-language
    model, a robotics system and a synthetic-data pipeline are review candidates rather
    than core papers, because none of them states a general vision method. A domain paper
    that does state one is a core paper, which the last core example pins directly.
    """
    relevant = [
        ("yolo detector architecture", "An Anchor-Free One-Stage Detector with Improved Label Assignment",
         "We present a real-time one-stage object detector with an anchor-free head and a new label assignment strategy. On COCO the detector improves mAP50-95 at matched latency, and we report an ablation over the neck design and frames per second on an embedded platform."),
        ("real-time detr improvement", "Real-Time Detection Transformers with an Efficient Hybrid Encoder",
         "We propose a query-based end-to-end object detection architecture whose hybrid encoder decouples intra-scale interaction from cross-scale fusion. Experiments on COCO compare against YOLO baselines at matched latency, with ablations on the matching strategy."),
        ("semantic segmentation method", "Hierarchical Decoders for Semantic Segmentation",
         "We introduce a decoder for semantic segmentation that aggregates multi-scale features. Results on ADE20K and Cityscapes report mIoU against strong baselines, with an ablation of each component."),
        ("visual backbone", "A Convolutional Backbone for Dense Visual Prediction",
         "We propose a convolutional backbone for image recognition and dense prediction. The architecture generalizes across detection and segmentation heads and is evaluated on ImageNet and COCO."),
        ("multi-object tracking method", "Association Beyond Confidence for Multi-Object Tracking",
         "We study tracking-by-detection and propose a tracklet association method that generalizes across detectors. Results on MOT17 and MOT20 include ablations over the association cost."),
        ("self-supervised visual representation", "Self-Supervised Visual Representation Learning at Scale",
         "We present a self-supervised visual pre-training method that produces a general visual encoder. Frozen features are evaluated on image classification, detection and segmentation across multiple datasets."),
        ("pose estimation method", "Real-Time Human Pose Estimation with a Lightweight Keypoint Head",
         "We propose a keypoint detection head for real-time human pose estimation. The method generalizes across backbones, and we report an ablation and latency on edge devices."),
        ("monocular depth estimation", "Scale-Consistent Monocular Depth Estimation",
         "We introduce a training objective for monocular depth estimation that generalizes across datasets. Ablations isolate the contribution of each term and we compare against stereo matching baselines."),
        ("efficient detector deployment", "Quantization-Aware Training for Efficient Object Detectors",
         "We propose a quantization scheme for efficient object detection that is detector-agnostic. We report mAP50-95, inference latency and throughput on embedded hardware, with an ablation per layer group."),
        ("domain paper with a general method", "A Scale-Aware Detection Head for Small Lesion Detection",
         "We propose a novel detection head for small-object detection. Although motivated by medical imaging, the module is plug-and-play and generalizes across detectors and datasets; ablations isolate its contribution."),
    ]
    irrelevant = [
        ("generic rag", "Generic RAG for Question Answering",
         "A retrieval-augmented generation system retrieves documents from a corpus and answers user questions."),
        ("generic agent framework", "A Multi-Agent LLM Framework for Tool Use",
         "A multi-agent language model framework orchestrates tool calls and planning across text-based tasks."),
        ("gpu database memory", "In-Memory Database Indexing",
         "Database memory indexing and GPU memory management improve transaction throughput on modern servers."),
        ("text-only llm", "Instruction Tuning for Text-Only Language Models",
         "We study text-only instruction tuning for large language models and evaluate on reasoning benchmarks."),
        ("recommendation system", "Collaborative Filtering for Recommendation",
         "A recommender system ranks items using collaborative filtering and learned user embeddings."),
        ("image generation only", "Text-to-Image Diffusion with Improved Sampling",
         "We improve sampling for text-to-image generative diffusion models and evaluate image synthesis quality."),
    ]
    borderline = [
        ("medical application of standard yolo", "Automated Polyp Detection in Colonoscopy Video Using YOLOv8",
         "We apply a standard pre-trained YOLOv8 detector to a private colonoscopy dataset and report clinical screening accuracy for our hospital."),
        ("remote sensing detection application", "Ship Detection in Satellite Imagery with a Fine-Tuned Detector",
         "We fine-tune an existing detector on remote sensing imagery and report detection accuracy for maritime monitoring."),
        ("multimodal vlm", "A Vision-Language Model for Document Question Answering",
         "A multimodal large language model answers questions about document images using visual instruction tuning."),
        ("robotics with cameras", "Reinforcement Learning for Robot Manipulation from Camera Observations",
         "A manipulation policy for robots learns from camera observations in simulation and is transferred to hardware."),
        ("synthetic image generation for detection", "Synthetic Training Images for Warehouse Object Detection",
         "We generate synthetic data with domain randomization and fine-tune an existing detector for warehouse inventory."),
    ]
    examples: list[RelevanceExample] = []
    for name, title, abstract in relevant:
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=True,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/cv-relevant", published_date="2026-01-01"),
                expected_decision="relevant",
            )
        )
    for name, title, abstract in irrelevant:
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=False,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/cv-irrelevant", published_date="2026-01-01"),
                expected_decision="irrelevant",
            )
        )
    for name, title, abstract in borderline:
        # Expected relevant in the precision/recall sense (a review candidate is surfaced,
        # not discarded) while the exact decision is pinned to "maybe".
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=True,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/cv-borderline", published_date="2026-01-01"),
                expected_decision="maybe",
            )
        )
    return examples


def evaluate_relevance_examples(examples: list[RelevanceExample], use_llm: bool = False, profile: str = "agent_memory") -> dict[str, object]:
    rows: list[dict[str, object]] = []
    decision_mismatches: list[str] = []
    false_positives: list[str] = []
    false_negatives: list[str] = []
    true_positive = false_positive = true_negative = false_negative = 0

    for example in examples:
        rule_result = classify_with_rules(example.candidate, profile=profile)
        result = (
            classify_with_optional_llm(example.candidate, rule_result)
            if use_llm and should_consider_for_llm(rule_result)
            else rule_result
        )
        if example.expected_decision and result.decision != example.expected_decision:
            decision_mismatches.append(example.name)
        predicted_relevant = result.decision in {"relevant", "maybe"}
        if predicted_relevant and example.expected_relevant:
            true_positive += 1
        elif predicted_relevant and not example.expected_relevant:
            false_positive += 1
            false_positives.append(example.name)
        elif not predicted_relevant and example.expected_relevant:
            false_negative += 1
            false_negatives.append(example.name)
        else:
            true_negative += 1

        rows.append(
            {
                "name": example.name,
                "expected": example.expected_decision or ("relevant" if example.expected_relevant else "irrelevant"),
                "decision": result.decision,
                "score": result.score,
                "reason": result.reason,
                "tags": result.tags,
            }
        )

    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 1.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 1.0
    return {
        "decision_mismatches": decision_mismatches,
        "precision": precision,
        "recall": recall,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "true_negative": true_negative,
        "false_negative": false_negative,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "rows": rows,
        "used_llm": use_llm,
        "profile": profile,
    }


def write_relevance_report(report: dict[str, object], report_dir: Path, report_date: str | None = None) -> Path:
    active_date = report_date or date.today().isoformat()
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"relevance-eval-{active_date}.md"
    path.write_text(render_relevance_report(report, active_date), encoding="utf-8")
    return path


def render_relevance_report(report: dict[str, object], report_date: str) -> str:
    lines = [
        f"# Paper Scout Relevance Evaluation - {report_date}",
        "",
        "> Fixed regression-set results; these scores do not measure production literature coverage.",
        "",
        f"- **Precision-like score:** {report['precision']:.3f}",
        f"- **Recall-like score:** {report['recall']:.3f}",
        f"- **False positives:** {len(report['false_positives'])}",
        f"- **False negatives:** {len(report['false_negatives'])}",
        f"- **LLM classifier used:** {report['used_llm']}",
        f"- **Exact decision mismatches:** {len(report.get('decision_mismatches', []))}",
        f"- **Profile:** {report.get('profile', 'agent_memory')}",
        "",
        "## False Positives",
        "",
    ]
    lines.extend([f"- {name}" for name in report["false_positives"]] or ["- None"])
    lines.extend(["", "## False Negatives", ""])
    lines.extend([f"- {name}" for name in report["false_negatives"]] or ["- None"])
    lines.extend(["", "## Per-Example Decisions", ""])
    for row in report["rows"]:
        lines.extend(
            [
                f"### {row['name']}",
                "",
                f"- **Expected:** {row['expected']}",
                f"- **Decision:** {row['decision']}",
                f"- **Score:** {row['score']}",
                f"- **Reason:** {row['reason']}",
                f"- **Tags:** {', '.join(row['tags']) if row['tags'] else 'none'}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
