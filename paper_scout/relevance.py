from __future__ import annotations

import re

from paper_scout.models import ClassificationResult, PaperCandidate

INCLUDE_PATTERNS = {
    "agent-memory": [
        r"\bagent(ic)? memory\b",
        r"\bmemory (for|in) (llm|language model|large language model)(?:\s+\([^)]+\))? agents?\b",
    ],
    "llm-agents": [r"\bllm agents?\b", r"\blarge language model(?:\s+\([^)]+\))? agents?\b", r"\blanguage model agents?\b"],
    "memory-systems": [
        r"\bagent[- ]native memory\b",
        r"\bagent memory systems?\b",
        r"\bmemory systems?\b.*\b(llm|large language model|language model|autonomous) agents?\b",
        r"\b(llm|large language model|language model|autonomous) agents?\b.*\bmemory systems?\b",
        r"\bmemory modules?\b.*\b(llm|large language model|language model|autonomous) agents?\b",
    ],
    "long-term-memory": [r"\blong[- ]term memory\b", r"\bpersistent memory\b"],
    "memory-types": [r"\bepisodic memory\b", r"\bsemantic memory\b", r"\bprocedural memory\b"],
    "memory-policy": [
        r"\bmemory (write|read|retrieval|update|maintenance|governance|policy|policies|representation|storage|consolidation|security|isolation|access control)\b",
        r"\b(write|read|retrieval) polic(y|ies)\b",
        r"\bshared memory\b.*\b(governance|access control|write polic(y|ies)|retrieval)\b",
        r"\bmemory\b.*\bstorage\b.*\bretrieval\b.*\bmaintenance\b",
    ],
    "benchmark": [r"\b(agent )?memory benchmark\b", r"\bmemory\b.{0,60}\bbenchmark\b", r"\bagent memory evaluation\b", r"\blongmemeval\b", r"\blocomo\b", r"\bagentshield bench\b"],
    "evaluation": [
        r"\bagent memory evaluation\b",
        r"\bmemory\b.{0,80}\bevaluat(e|es|ed|ion|ing)\b",
        r"\bevaluat(e|es|ed|ion|ing)\b.{0,80}\bmemory\b",
        r"\bare we ready\b.{0,120}\b(agent[- ]native )?memory systems?\b",
    ],
    "deep-research": [r"\bdeep research\b", r"\bautoresearch\b", r"\bliterature[- ]review agents?\b", r"\bresearch agents?\b"],
    "parametric-memory": [r"\bparametric memory\b", r"\bengram\b", r"\bmodel[- ]internal memory\b", r"\bmemory mechanism\b"],
    "memory-augmented": [r"\bmemory[- ]augmented (llm|language model|agent)\b", r"\bmemory[- ]augmented language agents?\b"],
}

EXCLUDE_PATTERNS = [
    r"\bgpu memory\b",
    r"\bcuda memory\b",
    r"\bmemory[- ]efficient attention\b",
    r"\bmemory optimization\b",
    r"\bkv cache\b",
    r"\bdatabase memory\b",
    r"\bin-memory database\b",
    r"\boperating system memory\b",
    r"\bmemory paging\b",
    r"\bmemory bandwidth\b",
    r"\bcache optimization\b",
    r"\bvector database\b",
    r"\bvector search\b",
    r"\bgeneric rag\b",
    r"\bwithout agent memory\b",
    r"\bwithout persistent memory\b",
    r"\bhuman memory\b",
    r"\bhuman cognitive memory\b",
    r"\bworking memory in humans\b",
    r"\bprotein[- ]synthesis[- ]dependent\b",
    r"\bfear memory\b",
    r"\bneural inactivation\b",
    r"\bhippocampus\b",
    r"\bamygdala\b",
    r"\banimal memory\b",
    r"\bpsychology experiments?\b",
    r"\bneuroscience\b",
]

BIOLOGICAL_MEMORY_PATTERNS = [
    r"\bprotein[- ]synthesis[- ]dependent\b",
    r"\bfear memory\b",
    r"\bneural inactivation\b",
    r"\bhippocampus\b",
    r"\bamygdala\b",
    r"\banimal memory\b",
    r"\bhuman cognitive memory\b",
    r"\bpsychology experiments?\b",
    r"\bneuroscience\b",
]

AGENT_CONTEXT = [
    r"\bagents?\b",
    r"\bllm\b",
    r"\blarge language model\b",
    r"\blanguage model\b",
    r"\bautonomous research\b",
    r"\bdeep research\b",
]

AI_MEMORY_CONTEXT = [
    r"\bllm\b",
    r"\blarge language model\b",
    r"\blanguage model agents?\b",
    r"\bai agents?\b",
    r"\bagent memory\b",
    r"\bagent[- ]native memory\b",
]

HIGH_CONFIDENCE_AGENT_MEMORY_PATTERNS = {
    "agent-native memory": r"\bagent[- ]native memory\b",
    "agent memory system": r"\bagent memory systems?\b",
    "memory system for LLM agents": r"\bmemory systems?\b.*\b(llm|large language model|language model)(?:\s+\([^)]+\))? agents?\b|\bmemory (for|in) (llm|large language model|language model)(?:\s+\([^)]+\))? agents?\b.*\b(systems?|storage|retrieval|update|consolidation|maintenance|governance)\b",
    "memory systems and LLM agents": r"\b(llm|large language model|language model) agents?\b.*\bmemory systems?\b|\bmemory systems?\b.*\b(llm|large language model|language model) agents?\b",
    "memory module LLM agent": r"\bmemory modules?\b.*\b(llm|large language model|language model)?\s*agents?\b",
    "persistent memory agent": r"\bpersistent memory\b.*\bagents?\b|\bagents?\b.*\bpersistent memory\b",
    "long-term memory agent": r"\blong[- ]term memory\b.*\bagents?\b|\bagents?\b.*\blong[- ]term memory\b",
    "memory type agent": r"\b(episodic|semantic|procedural) memory\b.*\bagents?\b|\bagents?\b.*\b(episodic|semantic|procedural) memory\b",
    "memory policy LLM agent": r"\bmemory (write|read|retrieval|update|maintenance|governance|policy|policies)\b.*\b(llm|large language model|language model)?\s*agents?\b",
    "memory representation retrieval agent": r"\bmemory representation\b.*\bretrieval\b.*\bagents?\b|\bagents?\b.*\bmemory representation\b.*\bretrieval\b",
    "storage retrieval maintenance memory": r"\b(llm|agent|agents)\b.*\bmemory\b.*\bstorage\b.*\bretrieval\b.*\bmaintenance\b|\bmemory\b.*\bstorage\b.*\bretrieval\b.*\bmaintenance\b.*\b(llm|agent|agents)\b",
    "memory consolidation agent": r"\bmemory consolidation\b.*\bagents?\b|\bagents?\b.*\bmemory consolidation\b",
    "agent memory evaluation": r"\bagent memory evaluation\b",
    "memory benchmark agent": r"\bmemory\b.{0,60}\bbenchmark\b.*\bagents?\b|\bagents?\b.*\bmemory\b.{0,60}\bbenchmark\b",
    "memory security autonomous LLM agents": r"\bmemory security\b.*\bautonomous llm agents?\b|\bautonomous llm agents?\b.*\bmemory security\b",
    "shared memory multi-agent LLM": r"\bshared memory\b.*\bmulti[- ]agent llm systems?\b|\bmulti[- ]agent llm systems?\b.*\bshared memory\b",
    "personal AI agent memory protocol": r"\bmemory protocol\b.*\bpersonal ai agents?\b|\bpersonal ai agents?\b.*\bmemory protocol\b",
    "autoresearch shared memory": r"\bautoresearch\b.*\bshared memory\b|\bshared memory\b.*\bautoresearch\b",
    "agent memory cross-session": r"\bagent memory\b.*\b(cross[- ]session|cross[- ]temporal|persistent)\b|\b(cross[- ]session|cross[- ]temporal|persistent)\b.*\bagent memory\b",
    "parametric memory LLM": r"\b(parametric memory|engram)\b.*\b(llm|large language model|language model|agents?)\b",
    "procedural memory distillation": r"\b(procedural memory distillation|memory distillation|cross[- ]episode signals?)\b.*\b(language models?|llms?|model weights?|policy)\b|\b(language models?|llms?)\b.*\b(procedural memory distillation|memory distillation|cross[- ]episode signals?)\b|\breusable procedural memory\b.*\b(distill(?:ed|ing|ation)?|model weights?|online reflection|cross[- ]episode)\b",
}

BROAD_PERIPHERAL_PATTERNS = {
    "recommender-system evaluation": r"\brecommender\b|\ba/b testing\b",
    "broad agentic AI/AGI": r"\bagentic ai\b|\bagentic artificial intelligence\b|\bartificial general intelligence\b|\bagi\b",
    "personality/empathy": r"\bpersonality\b|\bempathy\b|\bhuman shaping\b",
    "cybersecurity/phishing": r"\bphishing\b|\bcybersecurity\b|\bvulnerabilit(y|ies)\b",
    "evacuation/traffic/simulation": r"\bevacuation\b|\btraffic\b|\bsimulation\b|\bphysics-based building\b",
    "GPU/infrastructure": r"\bgpu\b|\bscheduling\b|\bserving\b|\binfrastructure\b|\blow-latency\b",
    "generic RAG": r"\brag\b|\bretrieval augmented generation\b",
}

WEAK_CONTEXT_TAGS = {"llm-agents", "evaluation"}
SYSTEM_LEVEL_HIGH_CONFIDENCE = {
    "agent-native memory",
    "agent memory system",
    "memory system for LLM agents",
    "memory systems and LLM agents",
    "memory module LLM agent",
    "agent memory evaluation",
    "memory benchmark agent",
    "memory security autonomous LLM agents",
    "shared memory multi-agent LLM",
    "personal AI agent memory protocol",
    "autoresearch shared memory",
    "agent memory cross-session",
    "parametric memory LLM",
    "procedural memory distillation",
}
NEGATED_AGENT_MEMORY_PATTERNS = [
    r"\bwithout (studying )?(persistent |long[- ]term |agent[- ]native )?agent memory\b",
    r"\bwithout (studying )?(persistent |long[- ]term )?memory\b",
    r"\bnot (a |about |studying )?(persistent |long[- ]term )?agent memory\b",
    r"\bdoes not (include|use|study|address|evaluate) (persistent |long[- ]term |agent[- ]native )?memory\b",
    r"\bdoes not (study|address|evaluate) (persistent |long[- ]term |agent[- ]native )?agent memory systems?\b",
    r"\bnot (persistent )?(llm[- ]agent|llm agent|agent) memory systems?\b",
    r"\bnot (a |about |studying )?(persistent |long[- ]term )?memory systems?\b",
]

DEEP_RESEARCH_INCLUDE_PATTERNS = {
    "deep-research-agents": [
        r"\bdeep research agents?\b",
        r"\bautonomous research agents?\b",
        r"\bautomated research agents?\b",
        r"\bai research agents?\b",
        r"\bresearch assistant agents?\b",
        r"\bllm research assistants?\b",
    ],
    "ai-scientist": [
        r"\bai scientists?\b",
        r"\bai scientific discovery\b",
        r"\bautomated scientific discovery\b",
        r"\bscientific discovery (llm|language model) agents?\b",
    ],
    "literature-review": [
        r"\bliterature[- ]review agents?\b",
        r"\bautomated literature review\b",
        r"\bllm literature review\b",
    ],
    "citation-grounding": [
        r"\bcitation verification\b",
        r"\bevidence[- ]ground(ed|ing)\b",
        r"\bsource[- ]grounded research\b",
        r"\bresearch reports?\b.{0,80}\bcitations?\b",
        r"\bcitations?\b.{0,80}\bresearch reports?\b",
    ],
    "research-planning": [
        r"\bresearch planning agents?\b",
        r"\bresearch task decomposition\b",
        r"\bmulti[- ]step research planning\b",
        r"\bresearch workflow agents?\b",
    ],
    "multi-agent-research": [
        r"\bmulti[- ]agent research systems?\b",
        r"\bmulti[- ]agent research workflows?\b",
    ],
    "hypothesis-experiment": [
        r"\bhypothesis generation agents?\b",
        r"\bexperiment design agents?\b",
        r"\bhypothesis generation\b.{0,80}\bexperiment design\b",
    ],
    "web-research": [
        r"\bweb[- ]browsing research agents?\b",
        r"\bopenresearch agents?\b",
        r"\bautoresearch\b",
    ],
    "research-memory": [
        r"\bresearch[- ]agent memory\b",
        r"\bresearch state\b",
        r"\biterative research state\b",
    ],
    "benchmark": [
        r"\bresearch agents?\b.{0,80}\bbenchmark\b",
        r"\bbenchmark\b.{0,80}\bresearch agents?\b",
    ],
}

HIGH_CONFIDENCE_DEEP_RESEARCH_PATTERNS = {
    "autonomous research agent": r"\b(autonomous|automated|deep) research agents?\b",
    "source-grounded research agent": r"\bsource[- ]grounded research agents?\b",
    "citation verification": r"\bcitation verification\b|\bevidence[- ]ground(ed|ing)\b.*\bresearch\b",
    "AI scientist": r"\bai scientists?\b|\bai scientific discovery\b|\bautomated scientific discovery\b|\bscientific discovery (llm|language model) agents?\b",
    "literature review agent": r"\bliterature[- ]review agents?\b|\bautomated literature review\b.*\b(llm|agent|agents)\b",
    "research planning": r"\bmulti[- ]step research planning\b|\bresearch planning agents?\b|\bresearch task decomposition\b",
    "multi-agent research workflow": r"\bmulti[- ]agent research (workflow|system)s?\b",
    "hypothesis experiment agent": r"\bhypothesis generation agents?\b|\bexperiment design agents?\b",
    "research reports with citations": r"\bresearch reports?\b.{0,80}\bcitations?\b|\bcitations?\b.{0,80}\bresearch reports?\b",
    "research-agent memory": r"\bresearch[- ]agent memory\b|\biterative research state\b",
}

DEEP_RESEARCH_EXCLUDE_PATTERNS = {
    "generic deep learning": r"\bgeneric deep learning\b|\bdeep learning\b.*\b(image classification|training method|optimization)\b",
    "generic automl": r"\bautoml\b(?!.*\b(research workflow|research agent|scientific discovery|hypothesis|experiment design)\b)",
    "market research": r"\bmarket research\b|\bbusiness research\b|\bcustomer surveys?\b",
    "human ai scientist bibliometrics": r"\byoung ai scientists?\b|\bcareer novelty\b|\bresearch trajectories\b|\bbibliometric\b.*\bhuman ai researchers?\b",
    "robotics/autonomous driving": r"\bautonomous driving\b|\brobotics\b|\bmobile robots?\b",
    "general chatbot": r"\bchatbots?\b(?!.*\b(research|citation|evidence|literature review)\b)",
    "generic rag": r"\brag\b(?!.*\b(research|citation|evidence|literature review|source[- ]grounded)\b)|\bretrieval augmented generation\b(?!.*\b(research|citation|evidence|literature review|source[- ]grounded)\b)",
    "generic benchmark": r"\bbenchmark\b(?!.*\b(research agent|deep research|literature review|citation|scientific discovery)\b)",
}

DEEP_RESEARCH_REVIEW_PATTERNS = {
    "general LLM agent research workflow": r"\bllm agents?\b.*\bresearch\b|\bresearch\b.*\bllm agents?\b",
    "research-adjacent rag": r"\b(rag|retrieval augmented generation)\b.*\b(citation|evidence|literature review|research)\b",
    "scientific automl": r"\bautoml\b.*\b(scientific discovery|experiment design|hypothesis|research workflow)\b",
    "web browsing agent": r"\bweb[- ]browsing agents?\b.*\bresearch\b|\bresearch\b.*\bweb[- ]browsing agents?\b",
}

NEGATED_DEEP_RESEARCH_PATTERNS = [
    r"\bwithout (an? )?(autonomous |agentic |source[- ]grounded )?research workflows?\b",
    r"\bdoes not (include|study|evaluate|address) (autonomous |agentic |source[- ]grounded )?research (planning|workflows?|agents?)\b",
    r"\bwithout (citation verification|evidence[- ]grounding|source[- ]grounded research)\b",
    r"\bdoes not (include|study|evaluate|address) (citation[- ]verification|evidence[- ]grounding|source[- ]grounded research)( agents?)?\b",
    r"\bnot about research agents?\b",
    r"\bunrelated to research workflows?\b",
    r"\bnot (a |about )?(deep research|autonomous research|research[- ]agent) systems?\b",
]

# --- Computer vision -------------------------------------------------------------
#
# The track's emphasis is object detection, because that is the work the reader does, but
# the screen has to keep the rest of the field in view and has to stay hostile to the two
# failure modes a detection-heavy profile invites: a single-family echo chamber, and the
# flood of domain applications that run an off-the-shelf detector on one private dataset.
#
# Three signals do that work and are kept separate on purpose:
#
# * COMPUTER_VISION_CONTEXT gates everything. A paper with no visual subject at all is
#   never a computer-vision paper however many generic systems words it shares with one,
#   which is what keeps RAG, agent frameworks, recommenders and memory-management work out
#   without needing a rule per topic.
# * COMPUTER_VISION_METHOD_PATTERNS is what lifts a domain paper back to core. Domain work
#   is explicitly not excluded: a medical or remote-sensing paper that contributes a
#   generally useful method belongs in the library. Only the ones with no method claim are
#   held back as review candidates.
# * COMPUTER_VISION_SUPPORTING_TAGS cannot carry a paper on their own. Latency, FLOPs,
#   benchmarks and synthetic data describe many fields; they are evidence about a vision
#   paper, not evidence that a paper is one.
#
# Nothing here scores scientific quality. These rules decide topic only, and the metric
# vocabulary below is recognized so that detection papers are found, never so that a
# reported number is rewarded.
COMPUTER_VISION_INCLUDE_PATTERNS = {
    "object-detection": [
        r"\bobject detect(?:ion|or|ors)\b",
        r"\b(?:one|single|two)[- ]stage detect(?:or|ors|ion)\b",
        r"\banchor[- ]free\b",
        r"\banchor[- ]based detect\w*\b",
        r"\bregion proposal networks?\b",
        r"\bdetection heads?\b",
        r"\blabel assignment\b",
        r"\bnon[- ]maximum suppression\b",
        r"\bbounding[- ]box (?:regression|prediction|refinement)\b",
        r"\bsmall[- ]object detection\b",
        r"\boriented object detection\b",
        r"\bopen[- ]vocabulary detect(?:ion|or|ors)\b",
    ],
    "yolo": [r"\byolo(?:v\d+|[- ]?x|[- ]?nas|[- ]?world|9000)?\b"],
    "detr": [
        r"\bdetr\b",
        r"\brt[- ]?detr\b",
        r"\bdeformable detr\b",
        r"\bend[- ]to[- ]end object detection\b",
        r"\bquery[- ]based detect(?:ion|or|ors)\b",
        r"\bset[- ]prediction detect\w*\b",
    ],
    "segmentation": [
        r"\b(?:semantic|instance|panoptic|promptable|referring|open[- ]vocabulary|image|video) segmentation\b",
        r"\bsegment anything\b",
        r"\bmask (?:prediction|head|decoder)\b",
        r"\bsegmentation (?:model|network|method|mask)s?\b",
    ],
    "tracking": [
        r"\bmulti[- ]object tracking\b",
        r"\btracking[- ]by[- ]detection\b",
        r"\bvisual object tracking\b",
        r"\bperson re[- ]identification\b",
        r"\btrack(?:let|ing) association\b",
    ],
    "pose": [
        r"\b(?:human|hand|body|animal|object|head|6d) pose estimation\b",
        r"\bpose estimation\b",
        r"\bkeypoint (?:detection|estimation|localization)\b",
    ],
    "vision-transformer": [
        r"\bvision transformers?\b",
        r"\bswin transformer\b",
        r"\bhierarchical vision transformer\b",
        r"\bvit\b",
    ],
    "backbone": [
        r"\b(?:convolutional|visual|image|vision) backbones?\b",
        r"\bfeature pyramid networks?\b",
        r"\bcnn architectures?\b",
        r"\bconvolutional neural network architectures?\b",
    ],
    "visual-representation": [
        r"\bvisual representation learning\b",
        r"\bself[- ]supervised (?:visual|vision|image)\w*\b",
        r"\bimage recognition\b",
        r"\bimage classification\b",
        r"\b(?:object|visual|scene) recognition\b",
        r"\bvisual encoders?\b",
        r"\bvisual features\b",
        r"\bvision foundation models?\b",
        # "foundation models in computer vision" is the same claim written the other way
        # round, and a visual-pretraining paper often names neither phrase exactly. Both
        # halves are required, so this cannot match a language-only pretraining paper.
        r"\bfoundation models?\b[^\n]{0,40}\bcomputer vision\b",
        r"\bcomputer vision\b[^\n]{0,40}\bfoundation models?\b",
        r"\b(?:image|visual) pre[- ]?training\b",
    ],
    "3d-vision": [
        r"\b3d (?:object detection|reconstruction|scene understanding|vision)\b",
        r"\bpoint clouds?\b",
        r"\bstereo matching\b",
        r"\bnovel view synthesis\b",
        r"\bneural rendering\b",
        r"\bstructure[- ]from[- ]motion\b",
        r"\bvisual geometry\b",
    ],
    "depth": [
        r"\bdepth estimation\b",
        r"\bdepth prediction\b",
        r"\bdisparity estimation\b",
    ],
    "vision-language": [
        r"\bvision[- ]language\b",
        r"\bvisual question answering\b",
        r"\bimage[- ]text\b",
        r"\bvisual instruction tuning\b",
        r"\bvisual grounding\b",
    ],
    "efficient-vision": [
        r"\breal[- ]time (?:object detection|detection|segmentation|inference|perception|tracking)\b",
        r"\befficient (?:object detect\w*|detectors?|vision (?:models?|transformers?|architectures?))\b",
        r"\binference latency\b",
        r"\bframes per second\b",
        r"\bfps\b",
        r"\bflops\b",
        r"\bquantiz(?:ation|ed|ing)\b",
        r"\b(?:structured |channel )?pruning\b",
        r"\bknowledge distillation\b",
        r"\bthroughput\b",
    ],
    "edge-deployment": [
        r"\bedge (?:device|devices|deployment|inference|computing)\b",
        r"\bembedded (?:device|devices|vision|deployment|platform)\b",
        r"\bon[- ]device inference\b",
        r"\btensorrt\b",
        r"\bjetson\b",
    ],
    "synthetic-data": [
        r"\bsynthetic (?:data|images?|datasets?|training data)\b",
        r"\bdomain randomi[sz]ation\b",
        r"\bsim[- ]to[- ]real\b",
    ],
    "benchmark": [
        r"\b(?:ms[- ])?coco\b",
        r"\bpascal voc\b",
        r"\bimagenet\b",
        r"\b(?:ade20k|cityscapes|lvis|objects365|kitti|nuscenes|mot17|mot20|crowdhuman|visdrone|dota)\b",
        r"\b(?:detection|segmentation|tracking|vision) benchmarks?\b",
    ],
    "metrics": [
        # Recognized so detection papers are discoverable and so the different averages
        # stay distinguishable in text. AP50, AP75 and mAP50-95 are separate quantities
        # and are never treated as the same number; none of them is scored here.
        r"\bmap\s?50[-– ]?95\b",
        r"\bap\s?50\b",
        r"\bap\s?75\b",
        r"\bmean average precision\b",
        r"\bmiou\b",
        r"\bintersection over union\b",
        r"\bpanoptic quality\b",
    ],
}

#: Tags that describe evidence about a paper rather than establishing it is a vision
#: paper. They never earn a core decision on their own.
COMPUTER_VISION_SUPPORTING_TAGS = frozenset({
    "efficient-vision", "edge-deployment", "synthetic-data", "benchmark", "metrics",
    "vision-language",
})

#: Any visual subject at all. Everything else is gated on this, so a paper that shares
#: systems vocabulary with vision work but never looks at an image cannot reach the track.
COMPUTER_VISION_CONTEXT = [
    r"\bcomputer vision\b",
    r"\bvisual\b",
    r"\bvision\b",
    r"\bimages?\b",
    r"\bimagery\b",
    r"\bvideos?\b",
    r"\bpixels?\b",
    r"\bcameras?\b",
    r"\bdetect(?:ion|or|ors)\b",
    r"\bsegmentation\b",
    r"\bbounding box(?:es)?\b",
    r"\bpoint clouds?\b",
    r"\bscene understanding\b",
    r"\bdepth (?:estimation|prediction|map|maps)\b",
    r"\bstereo\b",
    r"\boptical flow\b",
    r"\bpose estimation\b",
    r"\bkeypoints?\b",
]

HIGH_CONFIDENCE_COMPUTER_VISION_PATTERNS = {
    "object detection": r"\bobject detect(?:ion|or|ors)\b",
    "YOLO / real-time detection": r"\byolo(?:v\d+|[- ]?x|[- ]?nas|[- ]?world|9000)?\b",
    "DETR-family detection": r"\b(?:rt[- ]?)?detr\b|\bdeformable detr\b|\bend[- ]to[- ]end object detection\b",
    "detector architecture": r"\b(?:one|single|two)[- ]stage detect(?:or|ors|ion)\b|\banchor[- ]free detect\w*\b|\bregion proposal networks?\b|\bdetection heads?\b|\blabel assignment\b",
    "segmentation method": r"\b(?:semantic|instance|panoptic|promptable|referring|open[- ]vocabulary|image|video) segmentation\b|\bsegment anything\b",
    "visual tracking": r"\bmulti[- ]object tracking\b|\btracking[- ]by[- ]detection\b|\bvisual object tracking\b",
    "pose estimation": r"\b(?:human|hand|body|animal|object|head|6d) pose estimation\b|\bkeypoint (?:detection|estimation|localization)\b",
    "visual backbone": r"\bvision transformers?\b|\bswin transformer\b|\b(?:convolutional|visual|image|vision) backbones?\b|\bfeature pyramid networks?\b",
    "visual representation learning": r"\bvisual representation learning\b|\bself[- ]supervised (?:visual|vision|image)\w*\b|\bvision foundation models?\b|\bvisual encoders?\b|\bvisual features\b|\bfoundation models?\b[^\n]{0,40}\bcomputer vision\b|\bcomputer vision\b[^\n]{0,40}\bfoundation models?\b|\b(?:image|visual) pre[- ]?training\b",
    "3D and depth": r"\bdepth estimation\b|\b3d (?:object detection|reconstruction|scene understanding)\b|\bstereo matching\b|\bnovel view synthesis\b|\bpoint cloud (?:detection|segmentation|registration|completion)\b",
    "efficient visual inference": r"\breal[- ]time (?:object detection|detection|segmentation|perception|tracking)\b|\befficient (?:object detect\w*|detectors?|vision (?:models?|transformers?|architectures?))\b",
}

COMPUTER_VISION_EXCLUDE_PATTERNS = {
    "memory or database systems": r"\b(?:gpu|cuda|database|operating system) memory\b|\bin[- ]memory databases?\b|\bmemory (?:allocator|paging|bandwidth|fragmentation|management)\b",
    "retrieval-augmented generation": r"\bretrieval[- ]augmented generation\b|\brag (?:system|pipeline|framework)s?\b",
    "language-agent framework": r"\b(?:llm|language[- ]model|multi)[- ]agent (?:framework|system|architecture|orchestration|workflow)s?\b|\btool[- ]using agents?\b",
    "recommender system": r"\brecommend(?:er|ation) systems?\b|\bcollaborative filtering\b",
    "image generation only": r"\btext[- ]to[- ]image\b|\bimage synthesis\b|\bgenerative (?:image|diffusion) models?\b",
}

#: Signals that a paper is adjacent rather than core. An application signal alone holds a
#: paper at review; combined with a method-contribution signal it does not.
COMPUTER_VISION_REVIEW_PATTERNS = {
    # The recurring applied-detection domains. A long list, and deliberately so: the "X-YOLO
    # for <narrow subject>" paper is the single largest category the cs.CV and OpenAlex
    # detection queries return, and there is no structural signal that separates it from a
    # general detector paper -- only its subject. Matching here does not exclude anything;
    # it asks the paper for a general-method claim before it is treated as a core result.
    "domain application": r"\b(?:medical|clinical|radiolog\w*|histopatholog\w*|colonoscop\w*|endoscop\w*|x[- ]ray|ct scans?|mri|ultrasound|lesions?|tumou?rs?|cancer|diagnos\w*|remote sensing|satellite|aerial|uav|drone|synthetic aperture radar|\bsar\b|sonar|underwater|marine|benthic|maritime|agricultur\w*|crops?|weed|livestock|cattle|wildlife|fish|insects?|pests?|traffic|pedestrians?|vehicles?|road|driving scenes?|retail|warehouse|industrial|manufacturing|inspection|defect detection|weld\w*|pcb|construction site|mining|surveillance|security screening|assistive)\b",
    "off-the-shelf model use": r"\b(?:off[- ]the[- ]shelf|pre[- ]?trained|standard|existing|established)\b[^\n]{0,40}\b(?:detectors?|yolo\w*|models?|networks?)\b|\b(?:appl(?:y|ies|ied)|employ(?:s|ed)?|us(?:e|es|ed)|fine[- ]tun\w+)\b[^\n]{0,40}\b(?:yolo\w*|detectors?|faster r[- ]?cnn|mask r[- ]?cnn)\b",
    "vision-language model": r"\bvision[- ]language models?\b|\bmultimodal large language models?\b|\bvisual instruction tuning\b|\bvisual question answering\b",
    "robotics perception": r"\brobots?\b|\brobotic\w*\b|\bmanipulation polic\w+\b|\bautonomous driving\b|\bnavigation polic\w+\b|\bslam\b",
    "synthetic data": r"\bsynthetic (?:data|images?|datasets?|training data)\b|\bsim[- ]to[- ]real\b|\bdomain randomi[sz]ation\b",
}

#: Review labels that mean "this is an application of vision", as opposed to adjacency of
#: some other kind. Only these trigger the application downgrade.
COMPUTER_VISION_APPLICATION_LABELS = frozenset({
    "domain application", "off-the-shelf model use", "synthetic data", "robotics perception",
})

#: What a paper has to show for a general contribution. Deliberately about the *shape* of
#: the claim rather than about any reported number: no minimum AP improvement exists here,
#: and none should, because a small benchmark gain is not by itself a contribution.
#:
#: Only some of these are strong enough to cancel the domain-application downgrade -- see
#: COMPUTER_VISION_GENERAL_METHOD_LABELS below.
COMPUTER_VISION_METHOD_PATTERNS = {
    "proposed architecture": r"\b(?:we|this (?:paper|work|study))\b[^\n]{0,60}\b(?:propose|proposes|introduce|introduces|present|presents)\b[^\n]{0,60}\b(?:architecture|detector|network|backbone|head|module|framework|method|operator|layer)s?\b|\bnovel (?:architecture|detector|backbone|head|module|operator|representation)s?\b",
    "training or matching method": r"\blabel assignment\b|\bloss (?:function|design|formulation)\b|\b(?:localization|regression|classification|detection|focal|iou|contrastive) loss(?:es)?\b|\bbipartite matching\b|\bmatching (?:strategy|cost)\b|\btraining (?:strategy|recipe|scheme|objective)\b|\bassignment strategy\b",
    "generality claim": r"\bgeneral(?:i[sz]es?|i[sz]ation|i[sz]able)\b|\bacross (?:multiple |several |diverse )?(?:datasets|domains|benchmarks|backbones|detectors)\b|\bplug[- ]and[- ]play\b|\b(?:model|detector|architecture)[- ]agnostic\b",
    "controlled analysis": r"\bablation\w*\b",
}

#: The subset of method signals that answer "is this broadly useful?" rather than merely
#: "did they build something?". Every application paper says it proposes a framework, and
#: an ablation shows rigour rather than breadth, so neither cancels the downgrade. A stated
#: generality claim does, and so does a training, matching or loss contribution, which is a
#: detector-level technique rather than a dataset-level result -- detection losses and
#: matching are first-class topics for this track wherever the motivating images came from.
COMPUTER_VISION_GENERAL_METHOD_LABELS = frozenset({
    "generality claim", "training or matching method",
})

NEGATED_COMPUTER_VISION_PATTERNS = [
    r"\btext[- ]only\b",
    r"\blanguage[- ]only\b",
    r"\bwithout (?:any )?(?:visual|vision|image|perceptual) (?:input|inputs|component|components|perception|supervision)\b",
    r"\bdoes not (?:include|study|evaluate|address) (?:visual|vision|image|object detection|computer vision)\b",
    r"\bno (?:visual|vision|perception) (?:component|contribution)\b",
    r"\bnot (?:a |about )?(?:computer vision|object detection|vision) (?:paper|system|method|contribution)s?\b",
    r"\bunrelated to computer vision\b",
]


def classify_with_rules(candidate: PaperCandidate, profile: str = "agent_memory") -> ClassificationResult:
    from paper_scout.config import validate_track
    validate_track(profile)
    if profile == "engram":
        from paper_scout.engram import classify_engram
        return classify_engram(candidate)
    if profile == "deep_research":
        return _classify_deep_research_with_rules(candidate)
    if profile == "computer_vision":
        return _classify_computer_vision_with_rules(candidate)
    evidence = explain_rule_matches(candidate)
    text = evidence["text"]
    exclude_hits = evidence["exclude_hits"]
    biological_hits = evidence["biological_memory_hits"]
    include_tags = list(evidence["include_tags"])
    high_confidence_hits = evidence["high_confidence_hits"]
    if "procedural memory distillation" in high_confidence_hits:
        for tag in ["procedural-memory", "parametric-memory", "memory-distillation", "self-improvement", "language-model-memory", "cross-episode-learning"]:
            if tag not in include_tags:
                include_tags.append(tag)
    has_agent_context = bool(evidence["agent_context_hits"])
    broad_hits = evidence["broad_peripheral_hits"]
    negated_memory_focus = bool(evidence["negated_memory_focus_hits"])
    effective_high_confidence_hits = [] if negated_memory_focus else list(high_confidence_hits)
    if broad_hits and not any(hit in SYSTEM_LEVEL_HIGH_CONFIDENCE for hit in effective_high_confidence_hits):
        effective_high_confidence_hits = []

    if biological_hits and not _matches(AI_MEMORY_CONTEXT, text):
        return ClassificationResult(
            score=5,
            decision="irrelevant",
            reason="Excluded: memory topic is biological/cognitive, not LLM-agent memory.",
            tags=["excluded-memory-sense"],
            abstract_summary=_summary(candidate.abstract),
        )

    if negated_memory_focus:
        return ClassificationResult(
            score=20 if has_agent_context else 10,
            decision="irrelevant",
            reason="Peripheral candidate: mentions memory, but not clearly LLM-agent memory.",
            tags=[tag for tag in include_tags if tag in WEAK_CONTEXT_TAGS],
            abstract_summary=_summary(candidate.abstract),
        )

    if exclude_hits and (not include_tags or _matches([r"\bwithout agent memory\b", r"\bwithout persistent memory\b"], text)):
        return ClassificationResult(
            score=5,
            decision="irrelevant",
            reason="Excluded: memory topic is biological/cognitive, hardware, database, or otherwise not LLM-agent memory.",
            tags=["excluded-memory-sense"],
            abstract_summary=_summary(candidate.abstract),
        )

    core_tags = [tag for tag in include_tags if tag not in WEAK_CONTEXT_TAGS]
    if not core_tags and not effective_high_confidence_hits:
        if broad_hits and has_agent_context:
            return ClassificationResult(
                score=45,
                decision="maybe",
                reason="Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.",
                tags=[tag for tag in include_tags if tag in WEAK_CONTEXT_TAGS],
                abstract_summary=_summary(candidate.abstract),
            )
        return ClassificationResult(
            score=20 if has_agent_context else 10,
            decision="irrelevant",
            reason="Peripheral candidate: discusses agents, but not persistent agent memory." if has_agent_context else "Peripheral candidate: mentions memory, but not clearly LLM-agent memory.",
            tags=include_tags,
            abstract_summary=_summary(candidate.abstract),
        )

    score = min(85, len(core_tags) * 18 + (10 if has_agent_context else 0))
    if "agent-memory" in include_tags:
        score += 15
    if "memory-systems" in include_tags and has_agent_context:
        score += 12
    if "benchmark" in include_tags:
        score += 8
    if effective_high_confidence_hits:
        score = max(score, 90)
    if broad_hits and not effective_high_confidence_hits:
        include_tags = [tag for tag in include_tags if tag in WEAK_CONTEXT_TAGS]
        score = max(45, min(score, 62))
    score = min(100, score)

    if effective_high_confidence_hits:
        decision = "relevant"
        reason = _high_confidence_reason(effective_high_confidence_hits)
    elif score >= 70:
        decision = "relevant"
        reason = _focused_reason(include_tags)
    elif score >= 40:
        decision = "maybe"
        reason = (
            "Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory."
            if broad_hits
            else "Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory."
        )
    else:
        decision = "irrelevant"
        reason = "Does not clearly address persistent memory for LLM agents."

    return ClassificationResult(
        score=score,
        decision=decision,
        reason=reason,
        tags=include_tags,
        abstract_summary=_summary(candidate.abstract),
    )


def _classify_deep_research_with_rules(candidate: PaperCandidate) -> ClassificationResult:
    evidence = explain_rule_matches(candidate, profile="deep_research")
    include_tags = list(evidence["include_tags"])
    high_confidence_hits = list(evidence["high_confidence_hits"])
    exclude_hits = list(evidence["exclude_hits"])
    review_hits = list(evidence["review_hits"])
    negated_research_focus = bool(evidence["negated_research_focus_hits"])
    text = evidence["text"]
    summary = _summary(candidate.abstract)

    if negated_research_focus:
        return ClassificationResult(
            score=10,
            decision="irrelevant",
            reason="Excluded: explicitly lacks autonomous research-agent or citation-grounded workflow focus.",
            tags=[],
            abstract_summary=summary,
        )

    if exclude_hits and (not high_confidence_hits or "human ai scientist bibliometrics" in exclude_hits):
        if review_hits or include_tags:
            return ClassificationResult(
                score=45,
                decision="maybe",
                reason="Review candidate: research-adjacent system, but the agentic research workflow evidence is limited.",
                tags=include_tags or ["research-adjacent"],
                abstract_summary=summary,
            )
        return ClassificationResult(
            score=10,
            decision="irrelevant",
            reason="Excluded: not clearly about autonomous research agents or source-grounded research workflows.",
            tags=["excluded-research-sense"],
            abstract_summary=summary,
        )

    if high_confidence_hits:
        score = min(100, 86 + len(high_confidence_hits) * 3 + len(include_tags) * 2)
        return ClassificationResult(
            score=score,
            decision="relevant",
            reason=_deep_research_reason(high_confidence_hits, include_tags),
            tags=include_tags,
            abstract_summary=summary,
        )

    if include_tags:
        score = min(78, 42 + len(include_tags) * 9 + len(review_hits) * 4)
        decision = "relevant" if score >= 70 and len(include_tags) >= 3 else "maybe"
        reason = (
            "Studies autonomous or source-grounded research-agent workflows."
            if decision == "relevant"
            else "Review candidate: may support deep research workflows but needs human judgment."
        )
        return ClassificationResult(score=score, decision=decision, reason=reason, tags=include_tags, abstract_summary=summary)

    if review_hits:
        return ClassificationResult(
            score=45,
            decision="maybe",
            reason="Review candidate: adjacent to research-agent workflows, but not clearly a deep research system.",
            tags=["research-adjacent"],
            abstract_summary=summary,
        )

    if _matches([r"\bresearch\b", r"\bscientific\b", r"\bliterature review\b"], text):
        return ClassificationResult(
            score=25,
            decision="irrelevant",
            reason="Peripheral candidate: mentions research, but not autonomous research agents or citation-grounded workflows.",
            tags=[],
            abstract_summary=summary,
        )

    return ClassificationResult(
        score=10,
        decision="irrelevant",
        reason="Does not clearly address autonomous research agents or AI-assisted scientific discovery workflows.",
        tags=[],
        abstract_summary=summary,
    )


def _classify_computer_vision_with_rules(candidate: PaperCandidate) -> ClassificationResult:
    """Screen one candidate for the computer-vision track.

    The order of the checks is the policy. A denial of visual focus settles the paper; a
    missing visual subject settles it next, which is what excludes the whole class of
    generic systems and language work without a rule per topic. Only then do the positive
    signals run, and the application downgrade sits *after* the high-confidence check on
    purpose: a domain paper is held at review because it makes no general method claim,
    never because of the domain it works in.
    """
    evidence = explain_rule_matches(candidate, profile="computer_vision")
    include_tags = list(evidence["include_tags"])
    high_confidence_hits = list(evidence["high_confidence_hits"])
    exclude_hits = list(evidence["exclude_hits"])
    review_hits = list(evidence["review_hits"])
    method_hits = list(evidence["method_contribution_hits"])
    negated_vision_focus = bool(evidence["negated_vision_focus_hits"])
    summary = _summary(candidate.abstract)
    core_tags = [tag for tag in include_tags if tag not in COMPUTER_VISION_SUPPORTING_TAGS]
    application_hits = [hit for hit in review_hits if hit in COMPUTER_VISION_APPLICATION_LABELS]
    general_method_hits = [hit for hit in method_hits if hit in COMPUTER_VISION_GENERAL_METHOD_LABELS]
    # A core tag establishes a visual subject by itself. Several genuine vision topics --
    # depth estimation, stereo matching, point clouds, pose -- can be written up without
    # the words "image", "visual" or "vision" appearing anywhere, so requiring the generic
    # vocabulary alone would drop them.
    vision_context = bool(evidence["vision_context_hits"]) or bool(core_tags)

    if negated_vision_focus:
        return ClassificationResult(
            score=10,
            decision="irrelevant",
            reason="Excluded: explicitly states it makes no visual or computer-vision contribution.",
            tags=[],
            abstract_summary=summary,
        )

    if not vision_context:
        return ClassificationResult(
            score=5,
            decision="irrelevant",
            reason="Excluded: no visual subject; this is not a computer-vision paper.",
            tags=["excluded-non-vision"],
            abstract_summary=summary,
        )

    if exclude_hits and not high_confidence_hits:
        if core_tags or review_hits:
            return ClassificationResult(
                score=45,
                decision="maybe",
                reason="Review candidate: touches vision, but the excluded framing leaves the visual contribution unclear.",
                tags=include_tags or ["vision-adjacent"],
                abstract_summary=summary,
            )
        return ClassificationResult(
            score=10,
            decision="irrelevant",
            reason="Excluded: not a computer-vision methodological contribution.",
            tags=["excluded-vision-scope"],
            abstract_summary=summary,
        )

    if high_confidence_hits:
        if application_hits and not general_method_hits:
            # Domain work is welcome; domain work with no *general* method is a review
            # candidate. The distinction is the breadth of the claim, not the application
            # area. "We propose a framework for X-ray bone tumours" is an application;
            # "this loss generalizes across detectors" is a contribution to the field.
            return ClassificationResult(
                score=55,
                decision="maybe",
                reason=_computer_vision_application_reason(application_hits),
                tags=include_tags,
                abstract_summary=summary,
            )
        score = min(100, 86 + len(high_confidence_hits) * 3 + len(core_tags) * 2)
        return ClassificationResult(
            score=score,
            decision="relevant",
            reason=_computer_vision_reason(high_confidence_hits, include_tags),
            tags=include_tags,
            abstract_summary=summary,
        )

    if core_tags:
        score = min(78, 42 + len(core_tags) * 9 + len(method_hits) * 4)
        if application_hits and not general_method_hits:
            score = min(score, 55)
        decision = "relevant" if score >= 70 and len(core_tags) >= 3 else "maybe"
        reason = (
            _computer_vision_reason([], include_tags)
            if decision == "relevant"
            else "Review candidate: vision-related, but the methodological contribution to computer vision is not clear."
        )
        return ClassificationResult(score=score, decision=decision, reason=reason, tags=include_tags, abstract_summary=summary)

    if review_hits:
        return ClassificationResult(
            score=45,
            decision="maybe",
            reason="Review candidate: adjacent to computer vision, but no vision method is clearly studied.",
            tags=include_tags or ["vision-adjacent"],
            abstract_summary=summary,
        )

    return ClassificationResult(
        score=20,
        decision="irrelevant",
        reason="Peripheral candidate: mentions visual data, but studies no computer-vision method.",
        tags=include_tags,
        abstract_summary=summary,
    )


def explain_rule_matches(candidate: PaperCandidate, profile: str = "agent_memory") -> dict[str, object]:
    from paper_scout.config import validate_track
    validate_track(profile)
    if profile == "engram":
        from paper_scout.engram import engram_evidence
        return engram_evidence(candidate)
    text = _paper_text(candidate)
    if profile == "deep_research":
        include_tags = [
            tag
            for tag, patterns in DEEP_RESEARCH_INCLUDE_PATTERNS.items()
            if _matches(patterns, text)
        ]
        high_confidence_hits = _matches_labeled(HIGH_CONFIDENCE_DEEP_RESEARCH_PATTERNS, text)
        if high_confidence_hits:
            for tag in ["deep-research-agents"]:
                if tag not in include_tags:
                    include_tags.append(tag)
        return {
            "text": text,
            "include_tags": include_tags,
            "exclude_hits": _matches_labeled(DEEP_RESEARCH_EXCLUDE_PATTERNS, text),
            "biological_memory_hits": [],
            "agent_context_hits": [],
            "high_confidence_hits": high_confidence_hits,
            "broad_peripheral_hits": [],
            "negated_memory_focus_hits": [],
            "negated_research_focus_hits": _matches(NEGATED_DEEP_RESEARCH_PATTERNS, text),
            "negated_vision_focus_hits": [],
            "review_hits": _matches_labeled(DEEP_RESEARCH_REVIEW_PATTERNS, text),
            "vision_context_hits": [],
            "method_contribution_hits": [],
        }
    if profile == "computer_vision":
        include_tags = [
            tag
            for tag, patterns in COMPUTER_VISION_INCLUDE_PATTERNS.items()
            if _matches(patterns, text)
        ]
        high_confidence_hits = _matches_labeled(HIGH_CONFIDENCE_COMPUTER_VISION_PATTERNS, text)
        if "YOLO / real-time detection" in high_confidence_hits and "yolo" not in include_tags:
            # The tag is what the dashboard filters on, so a YOLO paper is always tagged
            # even when the phrasing only reached the high-confidence pattern.
            include_tags.append("yolo")
        return {
            "text": text,
            "include_tags": include_tags,
            "exclude_hits": _matches_labeled(COMPUTER_VISION_EXCLUDE_PATTERNS, text),
            "biological_memory_hits": [],
            "agent_context_hits": [],
            "high_confidence_hits": high_confidence_hits,
            "broad_peripheral_hits": [],
            "negated_memory_focus_hits": [],
            "negated_research_focus_hits": [],
            "negated_vision_focus_hits": _matches(NEGATED_COMPUTER_VISION_PATTERNS, text),
            "review_hits": _matches_labeled(COMPUTER_VISION_REVIEW_PATTERNS, text),
            "vision_context_hits": _matches(COMPUTER_VISION_CONTEXT, text),
            "method_contribution_hits": _matches_labeled(COMPUTER_VISION_METHOD_PATTERNS, text),
        }
    include_tags = [
        tag
        for tag, patterns in INCLUDE_PATTERNS.items()
        if _matches(patterns, text)
    ]
    high_confidence_hits = _matches_labeled(HIGH_CONFIDENCE_AGENT_MEMORY_PATTERNS, text)
    negated_memory_focus_hits = _matches(NEGATED_AGENT_MEMORY_PATTERNS, text)
    if high_confidence_hits and not negated_memory_focus_hits:
        for tag in ["agent-memory", "memory-systems", "llm-agents"]:
            if tag not in include_tags:
                include_tags.append(tag)
        if _matches(INCLUDE_PATTERNS["memory-policy"], text) and "memory-policy" not in include_tags:
            include_tags.append("memory-policy")
        if _matches(INCLUDE_PATTERNS["evaluation"], text) and "evaluation" not in include_tags:
            include_tags.append("evaluation")
    return {
        "text": text,
        "include_tags": include_tags,
        "exclude_hits": _matches(EXCLUDE_PATTERNS, text),
        "biological_memory_hits": _matches(BIOLOGICAL_MEMORY_PATTERNS, text),
        "agent_context_hits": _matches(AGENT_CONTEXT, text),
        "high_confidence_hits": high_confidence_hits,
        "broad_peripheral_hits": _matches_labeled(BROAD_PERIPHERAL_PATTERNS, text),
        "negated_memory_focus_hits": negated_memory_focus_hits,
        "negated_research_focus_hits": [],
        "negated_vision_focus_hits": [],
        "review_hits": [],
        "vision_context_hits": [],
        "method_contribution_hits": [],
    }


def should_consider_for_llm(result: ClassificationResult) -> bool:
    return result.decision in {"relevant", "maybe"} and result.score >= 40


def _paper_text(candidate: PaperCandidate) -> str:
    return f"{candidate.title}\n{candidate.abstract}".lower()


def _matches(patterns: list[str], text: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, flags=re.I)]


def _matches_labeled(patterns: dict[str, str], text: str) -> list[str]:
    return [label for label, pattern in patterns.items() if re.search(pattern, text, flags=re.I)]


def _high_confidence_reason(matches: list[str]) -> str:
    if "procedural memory distillation" in matches:
        return "Studies how cross-episode experience can be converted into reusable procedural memory and distilled into a language model's weights."
    if any("benchmark" in match or "evaluation" in match for match in matches):
        return "Evaluates memory mechanisms or benchmarks for LLM agents."
    if any("security" in match for match in matches):
        return "Evaluates memory security or cross-session memory risks in autonomous LLM agents."
    if any("shared memory" in match or "protocol" in match or "cross-session" in match for match in matches):
        return "Studies governed shared memory or persistent memory protocols for LLM agents."
    if any("parametric" in match or "Engram" in match for match in matches):
        return "Discusses Engram-style or parametric memory mechanisms for language models."
    if any("consolidation" in match or "policy" in match or "storage" in match or "retrieval" in match for match in matches):
        return "Studies memory storage, retrieval, update, or consolidation for LLM agents."
    if any("persistent" in match or "long-term" in match for match in matches):
        return "Focuses on persistent or long-term memory for agent behavior."
    return "Studies memory systems or memory modules for LLM agents."


def _focused_reason(tags: list[str]) -> str:
    if "benchmark" in tags or "evaluation" in tags:
        return "Evaluates memory mechanisms or benchmarks for LLM agents."
    if "parametric-memory" in tags:
        return "Discusses Engram-style or parametric memory mechanisms for language models."
    if "memory-policy" in tags:
        return "Studies memory storage, retrieval, update, or consolidation for LLM agents."
    if "long-term-memory" in tags:
        return "Focuses on persistent or long-term memory for agent behavior."
    if "memory-types" in tags:
        return "Studies episodic, semantic, or procedural memory for agents."
    if "memory-systems" in tags:
        return "Studies memory systems or memory modules for LLM agents."
    return "Studies agent memory with explicit LLM or agent context."


def _deep_research_reason(matches: list[str], tags: list[str]) -> str:
    if any("citation" in match or "source-grounded" in match or "reports" in match for match in matches):
        return "Studies source-grounded research workflows, citation verification, or evidence-backed research reports."
    if any("AI scientist" in match or "scientific discovery" in match for match in matches):
        return "Studies AI-scientist or scientific-discovery agents."
    if any("literature" in match for match in matches) or "literature-review" in tags:
        return "Studies automated literature-review systems or literature-review agents."
    if any("planning" in match or "multi-agent" in match or "hypothesis" in match for match in matches):
        return "Studies multi-step planning, multi-agent workflows, or hypothesis and experiment-design agents for research."
    if "research-memory" in tags:
        return "Studies research-agent memory or iterative research state."
    return "Studies autonomous or deep research agents."


def _computer_vision_reason(matches: list[str], tags: list[str]) -> str:
    if "YOLO / real-time detection" in matches or "yolo" in tags:
        return "Studies YOLO-family or real-time object detection."
    if "DETR-family detection" in matches or "detr" in tags:
        return "Studies DETR-family or query-based object detection."
    if "object detection" in matches or "detector architecture" in matches or "object-detection" in tags:
        return "Studies object-detection architecture, training, or evaluation."
    if "segmentation method" in matches or "segmentation" in tags:
        return "Studies semantic, instance, panoptic, or promptable segmentation."
    if "visual tracking" in matches or "tracking" in tags:
        return "Studies multi-object or visual object tracking."
    if "pose estimation" in matches or "pose" in tags:
        return "Studies pose estimation or keypoint localization."
    if "visual backbone" in matches or {"vision-transformer", "backbone"} & set(tags):
        return "Studies visual backbones or vision-transformer architecture."
    if "visual representation learning" in matches or "visual-representation" in tags:
        return "Studies visual representation learning or large visual encoders."
    if "3D and depth" in matches or {"3d-vision", "depth"} & set(tags):
        return "Studies 3D vision, depth estimation, or geometric visual understanding."
    if "efficient visual inference" in matches or "efficient-vision" in tags:
        return "Studies efficient or real-time visual inference."
    return "Studies a computer-vision method."


def _computer_vision_application_reason(application_hits: list[str]) -> str:
    if "domain application" in application_hits:
        return "Review candidate: applies vision models in a specific domain without a clearly general method contribution."
    if "off-the-shelf model use" in application_hits:
        return "Review candidate: uses an existing detector or model without a clearly general method contribution."
    if "robotics perception" in application_hits:
        return "Review candidate: robotics or driving system where the vision contribution is not clearly the subject."
    return "Review candidate: synthetic-data or applied use of vision models without a clearly general method contribution."


def _summary(abstract: str, max_chars: int = 320) -> str:
    compact = " ".join((abstract or "").split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."
