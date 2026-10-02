# Latest Paper Scout Digest

Latest daily digest: [2026-10-02](2026-10-02.md).

# Paper Scout Digest - 2026-10-02

## Run Summary

- **Run ID:** 11
- **Candidates fetched:** 436
- **New unique papers:** 405
- **Relevant:** 63
- **Maybe relevant:** 217
- **Irrelevant:** 156
- **Source summary:** arxiv: 336, openalex: 100, semantic_scholar: 0

## Source Warnings

- arxiv failed for 'object detection': timeout error for https://export.arxiv.org/api/query?search_query=all%3Aobject+AND+all%3Adetection&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: The read operation timed out
- arxiv: incomplete discovery window for 'vision transformer'; single-page record limit reached.
- arxiv: incomplete discovery window for 'cs.CV'; single-page record limit reached.
- openalex: incomplete discovery window for 'real-time object detection'; single-page record limit reached.
- openalex: incomplete discovery window for 'YOLO object detector'; single-page record limit reached.
- openalex: incomplete discovery window for 'vision transformer image recognition'; single-page record limit reached.
- openalex: incomplete discovery window for 'image segmentation deep learning'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'real-time object detection'; single-page record limit reached.
- semantic_scholar failed for 'YOLO detector': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.
- semantic_scholar: incomplete discovery window for 'open-vocabulary object detection'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'visual representation learning'; single-page record limit reached.

## Highly Relevant

### [GenCOPE: Syn2Real Generalized Category-Level Object Pose Estimation for Robotic Picking](https://arxiv.org/abs/2610.01758v1)

- **Authors:** Jian Liu, Wei Sun, Zhenqi Dai, Hui Yang, Jian Xiao, Nicu Sebe, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (96/100)
- **Reason:** Studies pose estimation or keypoint localization.
- **Tags:** pose, 3d-vision, synthetic-data
- **Abstract summary:** Category-level object pose estimation (COPE), capable of generalizing to intra-class unknown objects, has become a core technique for robotic 3D scene understanding. However, existing COPE methods still require labor-intensive recollection of real-world training data for novel object categories, which limits their s...

### [Towards Automatic Video Annotation with ASH: Zero-Shot Open-Vocabulary Multi-Object Tracking and Segmentation](https://arxiv.org/abs/2610.01022v1)

- **Authors:** Arash Rocky, Q. M. Jonathan Wu
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (96/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation, tracking
- **Abstract summary:** Memory-attention-based Video Instance Segmentation (VIS) methods have demonstrated strong zero-shot tracking capability, yet their substantial memory requirements confine them to short video clips and their single-prompt inference design makes multi-category open-vocabulary tracking computationally prohibitive. This...

### [When Does Geometric View Synthesis Help Wine Label Retrieval? A Public One-Shot Benchmark Across Self-Supervised and Vision-Language Backbones](https://arxiv.org/abs/2609.33359)

- **Authors:** Yueh-Cheng Huang
- **Date:** 2026-09-27
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation, vision-transformer, vision-language
- **Abstract summary:** Geometric view synthesis can expand a single wine-label photograph into a training set, but its value with pretrained image encoders is unclear. We study this on a public WineSensed-derived benchmark of 1,000 classes, one enrollment photograph per class, and 4,295 real queries. With the earlier DINO vision transform...

### [Dyna3: VLM-Guided Training-Free 4D Reconstruction via Depth Foundation Models](https://arxiv.org/abs/2610.01286v1)

- **Authors:** Xinhao Xiang, Weiyang Li, Zhijie Zheng, Abhijeet Rastogi, Jiawei Zhang
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (95/100)
- **Reason:** Studies pose estimation or keypoint localization.
- **Tags:** pose, 3d-vision, depth, vision-language
- **Abstract summary:** Recent depth foundation models like Depth Anything 3 (DA3) achieve remarkable multi-view depth estimation but assume static 3D scenes, limiting their applicability to real-world dynamic environments. Existing training-free 4D methods like Easi3R and VGGT4D rely on correspondence-trained backbones whose attention enc...

### [OneStreamer: Unifying Perception, Memory, and Proactive Response in Streaming Video Interaction](https://arxiv.org/abs/2610.01762v1)

- **Authors:** Xiangyu Zeng, Yuandong Yang, Zhiqiu Zhang, Yuhan Zhu, Xinhao Li, Qingyi Si, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (94/100)
- **Reason:** Studies visual representation learning or large visual encoders.
- **Tags:** visual-representation, efficient-vision
- **Abstract summary:** Streaming video LLMs must retain evidence before its relevance to future tasks is known and respond when sufficient evidence becomes available. The challenge is to form reusable factual memory without compromising real-time perception. We introduce OneStreamer, which jointly learns query-independent evidence recordi...

### [CrossGMN: Graph Metanetworks for Cross-Architecture Weight-Space Transformations](https://arxiv.org/abs/2610.01649v1)

- **Authors:** Adir Dayan, Yam Eitan, Haggai Maron
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (93/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, visual-representation, efficient-vision
- **Abstract summary:** Weight-space networks operate directly on parameters of other neural networks, enabling tasks such as predicting model properties, editing trained models, and generating weights. Weight-space symmetries such as neuron permutations make equivariance a key design principle. However, existing equivariant weight-space a...

### [VASC: Value-Aware Sparse Attention with Cross-Layer Memory for Efficient 3D Reconstruction](https://arxiv.org/abs/2610.01013v1)

- **Authors:** Junyi Wu, Fanqing Kong, Leyang Chen, Shaoqiu Zhang, Yulun Zhang
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (93/100)
- **Reason:** Studies pose estimation or keypoint localization.
- **Tags:** pose, 3d-vision
- **Abstract summary:** Feed-forward 3D vision models such as VGGT have achieved remarkable progress, unifying camera estimation and dense scene reconstruction in a single pass. However, their quadratic global attention makes long image sequences expensive, while existing sparse methods may favor highly attended yet value-redundant regions...

### [Anti-Persona: Disrupting Unauthorized Identity Binding and Recognition in Personalized Vision--Language Models](https://arxiv.org/abs/2610.01944v1)

- **Authors:** Abhishek Basu, Fahad Shamshad, Karthik Nandakumar
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual representation learning or large visual encoders.
- **Tags:** visual-representation
- **Abstract summary:** Few-shot personalization enables large vision--language models (LVLMs) to learn user-specific visual concepts for applications such as personalized retrieval and subject-aware querying. However, it also creates a privacy risk: an adversary can bind a target identity from a few reference images and subsequently detec...

### [ARROW: Arbitrary Reconstruction and Tracking of 4D Observations in the Wild](https://arxiv.org/abs/2610.01314v1)

- **Authors:** Ilya Fradlin, Christian Schmidt, Jens Piekenbrinck, Karim Knaebel, Gonzalo Martin Garcia, Bastian Leibe
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies 3D vision, depth estimation, or geometric visual understanding.
- **Tags:** 3d-vision
- **Abstract summary:** Dynamic scenes may be captured by a moving camera, multiple video streams, or images taken at different times. These observations reveal complementary aspects of scene geometry and motion, yet bringing them together requires establishing correspondence across viewpoints, capture times, and visibility changes. We int...

### [Attribution Gaps in Zero-Training LLM+OVOD Pipelines: A Fine-Grained Analysis of the CAAP--SNAP Discrepancy](https://arxiv.org/abs/2609.32567)

- **Authors:** Yu-Feng Yen
- **Date:** 2026-09-26
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** yolo, benchmark
- **Abstract summary:** LAOD and similar zero-training LLM+open-vocabulary-detector (OVOD) pipelines score two things separately: class-agnostic localization accuracy (CAAP) and semantic naming accuracy (SNAP). The two consistently diverge, and nobody has asked why. This paper asks why, on the full 5,000-image COCO-Val split (27,273 detect...

### [Combining General and Domain-Specific Pretext Tasks for Brain MR Image Segmentation](https://arxiv.org/abs/2609.30708)

- **Authors:** Tasneem Nasser, Susanne Schmid, Roberto Souza, Naser El-Sheimy
- **Date:** 2026-09-25
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation
- **Abstract summary:** A key challenge in medical image analysis is the scarcity of large annotated datasets for specific populations and diseases. As deep learning models rely heavily on labeled data, effective transfer learning strategies are needed to reduce the dependence on manual annotations. Self-supervised learning has emerged as...

### [Curvature Under Attack in hZACH-ViT: Gauge Symmetry, Boundary Saturation, and Adversarial Failure](https://arxiv.org/abs/2610.00680v1)

- **Authors:** Athanasios Angelakis, Marta Gomez-Barrero
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** Curvature is often treated as an intrinsic property of a representation, although its empirical effect also depends on coordinate scale, learned logit temperature, and numerical safeguards. We study this interaction in hZACH-ViT, a compact Vision Transformer with Euclidean, Poincare, and spherical prototype heads. T...

### [FFBL-Coop: Association-Decoupled Cooperative 3D Multi-Object Tracking](https://arxiv.org/abs/2610.01750v1)

- **Authors:** Haoxin Wu, Xiaokai Bai
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies multi-object or visual object tracking.
- **Tags:** tracking
- **Abstract summary:** Cooperative 3D tracking must integrate complementary observations across agents and time while maintaining consistent identities. When evidence integration and identity inheritance share a matching decision, errors arising from cross-view appearance differences and spatial misalignment can compromise both feature fu...

### [Lang3DSeg: Annotation-Free Open-Vocabulary 3D Segmentation with Point Transformers](https://arxiv.org/abs/2610.00855v1)

- **Authors:** Cigdem Kokenoz, Amir Salarpour, Alkim Domeke, Christopher Salas, Pedram MohajerAnsari, Long Cheng, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation, vision-language, benchmark, metrics
- **Abstract summary:** Accurate 3D semantic perception is critical for safe autonomous navigation. However, supervised LiDAR segmentation remains tied to closed taxonomies and to the cost of point-wise manual annotation. Open-vocabulary methods avoid that cost by projecting the output of 2D vision-language models onto LiDAR and distilling...

### [Latent-Foresight: End-to-End Learning Predictable Representations for Latent World Models](https://arxiv.org/abs/2610.01942v1)

- **Authors:** Efstathios Karypidis, Spyros Gidaris, Nikos Komodakis
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual representation learning or large visual encoders.
- **Tags:** visual-representation
- **Abstract summary:** Predicting the future evolution of a scene is a fundamental capability for world modeling. Recent work has shown that operating in the feature space of Vision Foundation Models (VFMs) yields semantically rich representations that support diverse future scene understanding tasks. However, existing approaches rely on...

### [LiteReality-Agent: An Agentic System for Interactable 3D Indoor Scene Reconstruction](https://arxiv.org/abs/2610.01863v1)

- **Authors:** Zhening Huang, Yueyan Li, Johnathan Chiu, Xiaoyang Lyu, Matt Zhou, Yuxin Yao, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies 3D vision, depth estimation, or geometric visual understanding.
- **Tags:** 3d-vision
- **Abstract summary:** We present LiteReality-Agent, an agentic system for reconstructing real indoor environments as realistic, articulated, and simulation-ready 3D scenes from RGB-D scans. At its core, LiteReality-Agent formulates 3D reconstruction as a coding problem, in which a coding agent gathers evidence using specialised tools and...

### [MVDG: Efficient Multi-view 3D Disambiguation on Unconstrained Real-World Images](https://arxiv.org/abs/2610.01098v1)

- **Authors:** Hanyuan Xiao, Gonglin Chen, Haolin Xiong, Wenbin Teng, Haiwei Chen, Yajie Zhao
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies 3D vision, depth estimation, or geometric visual understanding.
- **Tags:** 3d-vision
- **Abstract summary:** Illusory matches between distinct yet visually similar 3D surfaces--doppelgangers--remain a fundamental obstacle for large-scale, in-the-wild 3D reconstruction and visual localization. Prior work mitigates this issue with pairwise classifiers, but this design limits multi-view contextual reasoning and incurs O(n^2)...

### [Open Vocabulary Word Recognition From Transcribed Bangla Texts](https://arxiv.org/abs/2610.01134v1)

- **Authors:** Faias Satter, Sk. Md. Masudul Ahsan
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection
- **Abstract summary:** An optical character recognition (OCR) can scan a paper and extract text using technology, making people's jobs easier. While various OCR systems are available in the software industry, finding a reliable equivalent solution for Bangla takes much work. When it comes to handwritten texts, the situation is much more u...

### [PACT: End-to-End Learning of Human Pose, Contacts, and Forces from Video](https://arxiv.org/abs/2610.00451v1)

- **Authors:** Rikhat Akizhanov, Yangsong Zhang, Nikolai Kaliazin, Peter Wolf, Yoshihiko Nakamura, Pascal Fua, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual representation learning or large visual encoders.
- **Tags:** visual-representation
- **Abstract summary:** Human motion, environmental contacts, and interaction forces are governed by common physical laws, yet existing approaches typically separate visual pose reconstruction from contact and force estimation. This separation limits joint reasoning and can propagate errors between stages. We introduce PACT, an end-to-end...

### [RelationVGGT: Visual Geometry Transformers for 3D Spatial Relation Segmentation](https://arxiv.org/abs/2610.00970v1)

- **Authors:** Minsu Kim, Jaesung Choe, Jiwoo Lee, Yu-Chiang Frank Wang, Seon Joo Kim
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies 3D vision, depth estimation, or geometric visual understanding.
- **Tags:** 3d-vision
- **Abstract summary:** Recent advances in 3D reconstruction have progressed from per-scene optimization to feed-forward inference, and semantic scene understanding has followed suit -- yet existing methods remain confined to object-centric perception, neglecting spatial relations between objects. We formulate 3D spatial relation segmentat...

### [Semantic RGB--Depth Based Surgical Skill Assessment in Microscopic Stereo Videos](https://arxiv.org/abs/2610.01205v1)

- **Authors:** Jecia Z. Y. Mao, Sue M. Cho, Francis X. Creighton, Deepa Galaiya, Russell H. Taylor, Manish Sahu
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies 3D vision, depth estimation, or geometric visual understanding.
- **Tags:** 3d-vision
- **Abstract summary:** Objective assessment of microsurgical technical skill is essential for competency-based training and quality assurance, yet existing video-based approaches predominantly rely on RGB images and therefore overlook the 3D spatial relationships that characterize instrument-anatomy interactions. Although stereo operating...

### [The hidden advantage of mask resampling: a theory of masked autoencoders](https://arxiv.org/abs/2610.01578v1)

- **Authors:** Jorge Medina Moreira, Lorenzo Bardone, Lenka Zdeborová
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** Why can masked prediction learn useful representations that unmasked reconstruction misses? We study this question in a high-dimensional model of a masked autoencoder (MAE) trained on data with shared latent structure and heterogeneous noise. We prove that masked linear reconstruction can recover the latent feature...

### [Two Routes to the Middle: Placement Search and Brain Readouts Converge on Where Continual Learners Should Specialize](https://arxiv.org/abs/2610.01590v1)

- **Authors:** Yuan Huang, Zihan Chen, Runbin Zhang, Hongwei Ding, Changzeng Fu, Shiqi Zhao
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, benchmark
- **Abstract summary:** Continual learners that keep a task-specific adapter in every block of a pre-trained vision transformer accumulate storage linearly with the number of tasks; keeping task-specific adapters in only a few blocks curbs this growth but raises the question of where to place them. We investigate this question from two per...

### [FlashBack: Knowing When to Remember in Streaming Vision-Language Models](https://arxiv.org/abs/2610.01192v1)

- **Authors:** Yi Chen, MingMing Yu, Rui-Qi Wang, Boran Wang, Xiaohang Cao, Chu Tang, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** relevant (89/100)
- **Reason:** Studies efficient or real-time visual inference.
- **Tags:** vision-language, efficient-vision
- **Abstract summary:** Streaming vision-language models must process continuously growing video streams under a bounded compute budget, creating a persistent tension between real-time perception and long-term memory. Retrieving historical information provides a natural remedy, yet historical recall is not uniformly beneficial: unnecessary...

## Maybe Relevant

### [A Multi-Agent Framework for Explainable Brain Tumour Instance Segmentation and Clinical Report Generation Using ASIO-Optimised YOLO Architectures](https://doi.org/10.21203/rs.3.rs-10468605/v1)

- **Authors:** Shrikant Manikarao Mahindrakar, Yudhishthir Raut, Snehankita Majalekar, Kamlesh Arun Meshram, Sagar Dhanraj Pande, Vivek Jog
- **Date:** 2026-09-28
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** yolo, segmentation
- **Abstract summary:** No abstract available.

### [CLoSeR: Closing the Loop for Long-Context Streaming Reconstruction](https://arxiv.org/abs/2610.01927v1)

- **Authors:** Moyang Li, Zihan Zhu, Wei Zhang, Marc Pollefeys, Daniel Barath
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: uses an existing detector or model without a clearly general method contribution.
- **Tags:** 3d-vision
- **Abstract summary:** Feedforward foundation models have recently shown remarkable 3D reconstruction capabilities. However, existing models exhibit large tracking drift in long-context streaming reconstruction due to error accumulation. In this paper, we revisit loop closure with streaming reconstruction foundation models to enable accur...

### [Concept Driven Domain Adaptation: Finding an Abstract Needle in a Haystack](https://arxiv.org/abs/2610.00973v1)

- **Authors:** Haiming Zhao, Tai Wang, Kun Zhang, Xicheng Peng, Zhiyang Li
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: uses an existing detector or model without a clearly general method contribution.
- **Tags:** visual-representation, vision-language
- **Abstract summary:** Science teachers frequently search for documentary excerpts not by describing what appears on screen, but by querying the abstract concepts they intend to teach. This use case exposes a limitation of existing language-based video moment retrieval methods, which typically assume that queries describe observable event...

### [Cracks-YOLO: an improved YOLOv5 tongue crack detection method based on switchable atrous convolution and transformer](https://doi.org/10.3389/fmed.2026.1901533)

- **Authors:** Miaomiao Ding, Meiyi Wu, Bochen Shen, Huangbo Lin, Shaoyang Men
- **Date:** 2026-09-29
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** yolo, visual-representation
- **Abstract summary:** Introduction Tongue diagnosis is a vital component of Traditional Chinese Medicine (TCM), with cracked tongue serving as a key diagnostic indicator. Although deep learning techniques have advanced TCM tongue image recognition, existing methods for cracked tongue detection still face challenges of low accuracy and sl...

### [FedCKA: Representation-Guided Layer Personalization for Federated 3D Perception Across Driving Domains](https://arxiv.org/abs/2610.01510v1)

- **Authors:** Jolle Verhoog, Ali Burak Ünal, Holger Caesar
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, benchmark
- **Abstract summary:** Robust perception in intelligent vehicles demands 3D object detectors that remain dependable under domain shifts, such as changes in time of day, location, or weather. However, due to costly annotation and rare shifts, some environments lack sufficient data to train a standalone detector. Federated learning offers a...

### [FedMAD: Modulation-Aware Directional Aggregation for Federated Learning in Remote Sensing Image Classification](https://arxiv.org/abs/2610.00693v1)

- **Authors:** Barış Büyüktaş, Begüm Demir
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** visual-representation
- **Abstract summary:** Federated learning (FL) has recently attracted increasing attention in remote sensing (RS) since it enables collaborative model training across decentralized RS image archives without requiring direct access to local data. However, FL performance significantly degrades when the data distributions between clients are...

### [FiVOS: A Fish Segmentation Algorithm Based on Interactive Video Object Segmentation and Filter Enhancement](https://arxiv.org/abs/2610.01480v1)

- **Authors:** Yuqing Duan, Song Zhang, Shili Zhao, Daoliang Li, Ran Zhao
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation
- **Abstract summary:** With the continuous expansion of aquaculture, precise and efficient monitoring of fish behavior has become increasingly critical for improving farming efficiency and reducing economic losses. In particular, with the ongoing enhancement of computational capabilities in deep learning models, vision-based fish segmenta...

### [From Image Latent Space to Fuzzy Rules: Interpretable Analysis of Gastrointestinal Foundation Model](https://arxiv.org/abs/2610.00414v1)

- **Authors:** Michael D. Vasilakakis, Dimitris K. Iakovidis
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** vision-transformer, synthetic-data, benchmark
- **Abstract summary:** Foundation models pretrained on large-scale datasets demonstrate strong transferability to medical imaging tasks. However, understanding how their latent representations encode clinically relevant information remains an open challenge in safety-critical domains. This study proposes a prototype-based fuzzy-rule frame...

### [Geometric Similarity in VLM Low-Level Vision Representations](https://arxiv.org/abs/2610.00848v1)

- **Authors:** Shao-Jun Xia, Huixin Zhang, Zhen Lei, Anlan Sun, Yuner Zhang, Xiaoyang Chen
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** backbone, vision-language
- **Abstract summary:** Vision-language models (VLMs) have emerged as powerful candidates for universal vision backbones, with representative architectures including autoregressive (AR) models and diffusion transformers (DiTs). Yet, adapting them efficiently for all-in-one low-level image restoration remains a challenge. Crucially, the fie...

### [HierGF: Hierarchical Gaussian Fields via Geometry-perception Message Passing for Sparse-view 3D Reconstruction](https://arxiv.org/abs/2610.01056v1)

- **Authors:** Bi'an Du, Zhimin Zhang, Daizong Liu, Baoquan Chen, Wei Hu
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: robotics or driving system where the vision contribution is not clearly the subject.
- **Tags:** 3d-vision
- **Abstract summary:** Sparse view 3D reconstruction is an important and common scenario in multimedia applications, such as augmented reality/virtual reality (AR/VR) content creation, cultural heritage digitization, and certain robotic applications, where only a limited number of randomly captured views may be available. However, sparse...

### [Localisation-Aware Uncertainty for Pretrained Object Detection](https://arxiv.org/abs/2610.01409v1)

- **Authors:** Charmaine Barker, Daniel Bethell, Simos Gerasimou
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: uses an existing detector or model without a clearly general method contribution.
- **Tags:** object-detection
- **Abstract summary:** Reliable uncertainty estimation is essential for deploying object detectors when distribution/covariate shift and adversarial attacks may occur. Existing approaches often require detector retraining, architectural modification, or repeated inference, which may be infeasible or incur significant overheads. We introdu...

### [OptimusMesh: Compact Autoregressive Mesh Generation from Point Clouds via Sparse Latent Pivots](https://arxiv.org/abs/2610.01148v1)

- **Authors:** Mazhar Iqbal, Naoya Chiba, Xuanmeng Sha, Tomohiro Mashita, Yuki Uranishi
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** 3d-vision
- **Abstract summary:** Generating compact and geometrically faithful 3D meshes directly from point clouds remains a fundamental challenge. Point clouds are unordered and sparse, whereas meshes exhibit irregular structure and varying topology. As a result, many existing approaches rely on implicit representations followed by surface extrac...

### [PhysVista: Benchmarking Physical Intelligence in VLMs via a Perception-Reasoning-Assessment Loop](https://arxiv.org/abs/2610.00559v1)

- **Authors:** Xinge Peng, Yiting Lu, Tianwu Zhi, Wen Wen, Jianzhao Liu, Xin Li, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** visual-representation, vision-language
- **Abstract summary:** Vision-Language Models (VLMs) have shown strong multimodal reasoning capabilities, yet whether they truly capture the physical consistency underlying real-world dynamics remains unclear. Existing benchmark paradigms often suffer from fragmented evaluation, focusing on isolated cognitive stages while overlooking the...

### [Real-time recognition model of 3D workpiece for transmission tower based on uniseg3d and vision-inertia fusion](https://doi.org/10.21595/jme.2026.26085)

- **Authors:** Zeyu Li, Yalong Zhao, Xiaowei Sun, Nan Jiang, Te Li, Dalue Xue
- **Date:** 2026-09-27
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** 3d-vision, efficient-vision
- **Abstract summary:** To tackle the challenges existing in point cloud segmentation for transmission tower components-specifically, weak small-target perception, blurred boundaries, poor cross-scene adaptability, and insufficient real-time performance-this study develops a real-time recognition model by integrating LiDAR-IMU with UniSeg3...

### [Tumor Tissues FLIM Image Segmentation Dataset: Human Tumors and Xenograft Mouse Models.](https://doi.org/10.6084/m9.figshare.34003191.v1)

- **Authors:** Garance Boesinger, Victoria Fay
- **Date:** 2026-09-26
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation
- **Abstract summary:** Dataset DescriptionThis dataset contains the data associated with the study "The role of spatial resolution in cellular-scale fluorescence lifetime imaging deep-learning segmentation of head and neck cancer cryosections", which investigates deep learning-based segmentation of FLIM tumor tissue images using different...

### [Tumor Tissues FLIM Image Segmentation Dataset: Human Tumors and Xenograft Mouse Models.](https://doi.org/10.6084/m9.figshare.34003191.v2)

- **Authors:** Garance Boesinger, Victoria Fay
- **Date:** 2026-09-26
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation
- **Abstract summary:** Dataset DescriptionThis dataset contains the data associated with the study "The role of spatial resolution in cellular-scale fluorescence lifetime imaging deep-learning segmentation of head and neck cancer cryosections", which investigates deep learning-based segmentation of FLIM tumor tissue images using different...

### [Tumor Tissues FLIM Image Segmentation Dataset: Human Tumors and Xenograft Mouse Models.](https://doi.org/10.6084/m9.figshare.34003191)

- **Authors:** Garance Boesinger, Victoria Fay
- **Date:** 2026-09-26
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation
- **Abstract summary:** Dataset DescriptionThis dataset contains the data associated with the study "The role of spatial resolution in cellular-scale fluorescence lifetime imaging deep-learning segmentation of head and neck cancer cryosections", which investigates deep learning-based segmentation of FLIM tumor tissue images using different...

### [Uncertainty-Guided Handshake: Efficient Human-in-the-Loop Refinement for Surgical-Grade Glioma Segmentation](https://arxiv.org/abs/2610.01452v1)

- **Authors:** Samuel Hart, Ahmad Yahya, Ahmed Karam Eldaly
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation
- **Abstract summary:** While state-of-the-art automated models for medical image segmentation achieve high mean performance, they frequently suffer from localized, catastrophic failures that preclude safe clinical deployment, particularly in neuro-oncology. Interactive segmentation frameworks mitigate this by incorporating human oversight...

### [UniTrackPLA: Unified Panorama-Language-Action Model for Instruction-Guided Navigation and Dynamic Person Tracking](https://arxiv.org/abs/2610.00878v1)

- **Authors:** Pengfei Qi, Haoran Lin, Sizhuang Chen, Kai Luo, Sirui Zhang, Xinqi Liu, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: robotics or driving system where the vision contribution is not clearly the subject.
- **Tags:** visual-representation, vision-language
- **Abstract summary:** General-purpose embodied robots should support both navigation toward language-specified destinations and dynamic person tracking under arbitrary initial target azimuths. However, existing methods typically rely on forward-facing observations and address these tasks with separate policies, limiting omnidirectional p...

### [3DROID: A Renderable 3D Gaussian Dataset with Measured Per-Scene Reliability](https://arxiv.org/abs/2610.01744v1)

- **Authors:** Wonguen Cho, Junhoo Lee, Nojun Kwak
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** 3d-vision
- **Abstract summary:** Robot manipulation models primarily reason from 2D observations while acting in the 3D physical world. To bridge this gap, recent work has augmented robot data with geometric priors such as depth, point clouds, and 3D trajectories, while renderable 3D Gaussian representations provide another promising form of 3D sup...

### [Machine Translation for Sign Languages](https://arxiv.org/abs/2610.00881v1)

- **Authors:** Ozge Mercanoglu Sincan, Anton Pelykh, Edward Fish, Harry Walsh, JianHe Low, Karahan Sahin, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** pose
- **Abstract summary:** Sign language machine translation has progressed substantially over the past decade, evolving from isolated sign recognition to end-to-end translation systems. Advances in pose estimation, transformer architectures, and large-scale dataset collection have driven progress, yet challenges remain. Datasets are limited...

### [World Motion Models: Flexible Sequence Modeling of SE(3) Trajectories](https://arxiv.org/abs/2610.01742v1)

- **Authors:** Jiahui Lei, Qianqian Wang, Trevor Darrell, Angjoo Kanazawa
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** 3d-vision
- **Abstract summary:** Equipping artificial agents with spatial intelligence requires a comprehensive generative prior over the dynamic 3D world. We propose World Motion Models (WMMs) that capture "what was, is, and will be where across time" via sparse SE(3) pose trajectories. WMMs are built on the observation that elements of dynamic sc...

### [A Cascaded Multimodal Deep Learning Framework for PET/CT Lesion Segmentation with Metabolic Screening and Dual-Encoder Networks](https://doi.org/10.1007/978-3-032-39895-6_8)

- **Authors:** Alison Corrêa Mendes, Darlan B. P. Quintanilha, Anselmo Cardoso de Paiva, Ramsey Derek Badawi, Vivek Swarnakar, Cláudio de Souza Baptista
- **Date:** 2026-09-30
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** No abstract available.

### [A Survey on End-to-End Autonomous Driving Training from the Perspectives of Data, Strategy, and Platform](https://arxiv.org/abs/2610.00926v1)

- **Authors:** Chengkai Xu, Yiming Cui, Jiaqi Liu, Yicheng Guo, Cheng Qin, Geyuan Zhang, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Autonomous driving is a cornerstone technology for the future of intelligent transportation, where end-to-end learning has emerged as a transformative paradigm that directly maps multimodal sensory inputs to driving actions through unified differentiable models. While offering advantages, the effectiveness of end-to...

### [A2Z GameSpec-Bench: How Faithfully Can Coding Agents Generate Games from Game Design Specifications?](https://arxiv.org/abs/2609.39564v1)

- **Authors:** Seonho Lee, Wonryeol Jeong, Alberto Cereser, Inha Kang, Hyeonjong Kim, Seungmin Kwak, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Delegating complete application development to coding agents requires preserving the intended design rather than simply producing plausible outputs through naive prompting. Game development provides a demanding testbed, as long-form Game Design Documents (GDDs) describe requirements that must work together across ga...

### [AiSearch: Interactive Multi-Modal Search with VLMs](https://arxiv.org/abs/2610.01389v1)

- **Authors:** Ali Koksal, Mei Chee Leong, Vicky Sintunata, Ching Ling Chin, Wee Teck Fong
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Modern retrieval systems must both be automated and interactive, allowing users to search and refine results in real time. We present AiSearch, a flexible multimodal retrieval framework that leverages the zero shot capabilities of Vision Language Models (VLMs) for natural language search over images and videos. AiSe...

### [ALFRED: Requirement-driven development of an open-source mobile manipulator for long-term plant monitoring](https://arxiv.org/abs/2610.01477v1)

- **Authors:** Ciarán Miceal Johnson, Christopher Quail, Garry Ellard, Alistair McConnell, Steve Tonneau, Fernando Auat Cheein
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Tracking seasonal change in crops and forests requires observing the same plants repeatedly. Ground robots can do this at close range, and a manipulator gives their sensors more viewpoints. Yet the robots behind long-term field datasets are rarely released with their design files, and how a robot's own structure lim...

### [Architectural Sampling: Test-Time Scaling via Computational Diversity in Frozen Vision-Language Models](https://arxiv.org/abs/2610.01687v1)

- **Authors:** Akshit Singh, Shyam Marjit, Wei Lin, Leonid Karlinsky, M. Jehanzeb Mirza
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Test-time scaling often seeks better answers by sampling multiple responses from a frozen model, yet conventional temperature sampling generates every candidate along the same fixed computation path. We introduce architectural sampling, a training-free method that generates candidates through distinct forward comput...

### [ATI-VLA: Action-Centric Predictive Vision-Language-Action Models via Actionable Alignment Then Adaptive Injection](https://arxiv.org/abs/2610.01741v1)

- **Authors:** Yijie Zhu, Rui Shao, Jie He, Wei Li, Bo Zhao, Yelin Wang, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Predictive Vision-Language-Action (VLA) models aim to improve robotic manipulation via future observation or world dynamics forecasting. However, existing approaches often fail to realize this potential and underperform direct action prediction models. We argue that these limitations stem from modality misalignment...

### [Beyond Domain-Level Adaptation: Margin-Oriented Semantic-Appearance Interaction Correction for Personalized Federated Vision-Language Models](https://arxiv.org/abs/2610.01625v1)

- **Authors:** Wentao Yue, Qingyu Mao, Tianyou Lai, Ahmed M. Abdelmoniem, Qilei Li
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Federated parameter-efficient fine-tuning enables distributed clients to adapt pretrained vision-language models without sharing raw data or updating the full backbone. Its effectiveness, however, is limited by domain heterogeneity across clients. Existing personalized methods separate globally shared knowledge from...

### [Beyond Leaderboard Scores: A Deployment-Focused Protocol for Interpretable Tracking Evaluation in Pedestrian-Centric Environments](https://arxiv.org/abs/2610.01682v1)

- **Authors:** Dominik Wojcikiewicz, Diego Paez-Granados
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** edge-deployment
- **Abstract summary:** Mobile robots operating among pedestrians need trajectories that become available quickly, remain spatially credible through missed observations, preserve identity, and fit within an embedded computing budget. Aggregate tracking scores provide limited insight into when and how trajectories fail, while varying detect...

### [Bootstrapping Video Interaction Generation with Synthetic State Transitions](https://arxiv.org/abs/2610.01039v1)

- **Authors:** Jiho Jang, Jinyoung Kim, Nojun Kwak, Kyungjune Kim
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** synthetic-data
- **Abstract summary:** While recent video generative models can synthesize high-fidelity videos, they struggle to portray plausible physical interactions and the resulting state transitions, a critical bottleneck for applications in robotics and VR/AR. To address this, we introduce a framework to generate a scalable synthetic dataset of c...

### [CineMR: Tool-Integrated Vision-Language Reasoning for Quantitative Cardiac MRI Assessment](https://arxiv.org/abs/2610.01166v1)

- **Authors:** Kunyang Li, Hai Nguyen, Joshua Lowe, Chenguang Zhao, Peace C. Madueme, Mehdi Hedjazi Moghari, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Cardiovascular magnetic resonance (CMR), including cine imaging, is a reference standard for the noninvasive assessment of cardiac morphology and ventricular function. Cine CMR interpretation integrates qualitative visual assessment with quantitative measurements of ventricular volumes, ejection fraction, myocardial...

### [CoEvolve: Construct-to-Edit Visual Grounding with Bidirectional State Refinement](https://arxiv.org/abs/2610.01710v1)

- **Authors:** Dongwei Sun, Yujie Zhang, Bowen Yao, Pei Liu, Jing Yao, Xiangyong Cao
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Visual grounding localizes an object described by language with a bounding box. Most multimodal grounding models compress target identification, spatial reasoning, and boundary estimation into one terminal prediction. Free-form rationales make reasoning linguistically explicit but do not necessarily expose measurabl...

### [Continual Concept Erasure in Diffusion Models by Suppressing Cross-Edit Interference](https://arxiv.org/abs/2610.01989v1)

- **Authors:** Yongliang Wu, Haori Lu, Jinqi Luo, Wei Cao, Xingyu Zhu, Yaoyao Liu
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: touches vision, but the excluded framing leaves the visual contribution unclear.
- **Tags:** vision-adjacent
- **Abstract summary:** Concept erasure removes copyright-protected, privacy-sensitive, or otherwise undesirable concepts from pretrained text-to-image diffusion models to support content governance and compliance. As erasure requests arrive over time, models must remove new targets without undoing prior erasures. Existing methods do not c...

### [Controllable Multi-label Video Safety Detection via Adaptive Tversky Policy Optimization](https://arxiv.org/abs/2610.02019v1)

- **Authors:** Guangyu Yang, Jingbiao Mei, Mingsheng Sun, Jinghong Chen, Yingtong Bu, Pengda Qin, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** The rapid growth of video-based social media has increased users' exposure to harmful content, creating a need for reliable automated video safety detection. Although recent Vision-Language Models (VLMs) show strong video understanding capabilities, existing harmful video detection systems face two key limitations:...

### [CtrlWAM: Controllable World Action Models with Aligned Intent and Foresight](https://arxiv.org/abs/2610.00859v1)

- **Authors:** Chensheng Peng, Wenhao Ding, Ran Tian, Zewei Zhou, Jef Packer, Maximilian Igl, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** World action models (WAMs) jointly predict actions (intent) and visual future (foresight). Standard training adds noise to recorded actions and video simultaneously, but such training paradigms introduce a mismatch: perturbed actions imply counterfactual future visual, while the noised video remains tied to the GT r...

### [Discrete Annotation, Continuous Preference: Rethinking Supervision for Accurate and Generalizable Aesthetic Image Cropping](https://arxiv.org/abs/2610.00582v1)

- **Authors:** Ziqing Zhang, Xiao Liu, Kai Liu, Jianze Li, Weihang Zhang, Linghe Kong, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Aesthetic image cropping aims to identify the optimal crop of an image in terms of aesthetics and composition. While supervision based on annotated data is fundamental, the field has been hindered by a long-standing problem: existing datasets suffer from (1) human subjectivity and (2) rigid discreteness confined to...

### [DiVid: Diagnosing Dimension-Specific Diversity Collapse in Video Generation Models](https://arxiv.org/abs/2610.01661v1)

- **Authors:** Huanran Hu, Zihui Ren, Dingyi Yang, Zhinan Song, Guozheng Wu, Tiezheng Ge, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Despite remarkable progress, video generation models often produce highly similar outputs when repeatedly sampled from the same prompt, limiting their usefulness for creative exploration. Existing diversity evaluations primarily rely on global scalar metrics, which obscure where diversity collapses in the spatiotemp...

### [Do MLLM Judges Judge the Edit? Auditing Bias in Image Editing Evaluation with Verified Quality Preservation](https://arxiv.org/abs/2610.01670v1)

- **Authors:** Yuan Huang, Zirui Song, Xiuying Chen
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Multimodal large language models (MLLMs) are increasingly used as automated judges for instruction-based image editing and as reward signals for model training. However, systematically auditing whether these judges are influenced by cues irrelevant to editing quality is challenging because visual interventions may t...

### [EndoLive: Real-Time Style Transfer for Endoscopic Endonasal Skull Base Surgical Video](https://arxiv.org/abs/2610.01956v1)

- **Authors:** Griffin Hurt, Calvin Brinkman
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Complex surgical procedures around critical anatomy, such as the endoscopic endonasal skull base surgery, requires significant practice and training on the part of the surgeon before they are allowed to perform the operation on a live patient. This training in typically done in cadaveric specimens, due to them conta...

### [Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens](https://arxiv.org/abs/2610.01939v1)

- **Authors:** Ruiyang Si, Jianxin Bi, Shunyu Yang, Rui Ni, Wenbo Huang, Qiang Wang, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Vision language model (VLM) agents can control robots through visual feedback and action primitives, but repeated model invocations and redundant observations incur substantial token overhead. We introduce PyRUA-Lean, an interactive code-execution framework that couples feedback-driven primitive composition with sel...

### [Flow Matching Reinforcement for 3D Mesh Generation via Dynamic Homing Optimization](https://arxiv.org/abs/2610.01233v1)

- **Authors:** Zhen Zhou, Zhiwei Ning, Puhua Jiang, Sheng Zhang, Yifei Tang, Jie Yang, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Flow matching is central to 3D generation, yet in practice its reinforcement learning (RL) methods are largely adapted from 2D visual generation. Representative DPO-, GRPO-, and NFT-style objectives, when applied to negative trajectories, mainly steer predicted velocities away from the corresponding directions witho...

### [Form and Void: Entangled Composition through an Autonomous AI Agent](https://arxiv.org/abs/2610.02045v1)

- **Authors:** Shiwen Wang, Jian Yang, Xu Wang, Xincan Wang, Weiming Dong
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: touches vision, but the excluded framing leaves the visual contribution unclear.
- **Tags:** vision-adjacent
- **Abstract summary:** Positive and negative space is a fundamental principle in visual composition, supporting visually coherent forms and layered semantic relationships. Generating such compositions is challenging because it requires coordinated control over two semantic concepts that share a common boundary. Although recent text-to-ima...

### [FORTE: Adaptive Scoring and Exact Keyframe Selection for Long-Video Question Answering](https://arxiv.org/abs/2610.00573v1)

- **Authors:** Haifeng Huang, Biyin Xu, Chunsheng Xin, Yang Li
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Query-aware keyframe selection enables multimodal large language models (MLLMs) to process long videos using only a small set of question-relevant frames. Existing score-based methods, however, typically search within a fixed, uniformly sampled candidate pool, preventing evidence outside this pool from ever being se...

### [From Pixels to Policy: A Multi-Agent System for Intervention and Geo-Spatial Decision Support](https://arxiv.org/abs/2610.01870v1)

- **Authors:** Hosam Elgendy, Utkarsh Mall
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: touches vision, but the excluded framing leaves the visual contribution unclear.
- **Tags:** vision-adjacent
- **Abstract summary:** Urban environments are shaped by design choices with long-term implications for health, safety, and quality of life, yet evaluating proposed interventions remains costly, time-consuming, and often impractical. Existing geospatial vision methods largely focus on monitoring urban indicators from aerial and street-view...

### [From Reasoning Failures to Composable Video Spatial Intelligence](https://arxiv.org/abs/2610.01999v1)

- **Authors:** Pengzhan Sun, Junbin Xiao, Ramanathan Rajaraman, Shiu-hong Kao, Angela Yao
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Spatial reasoning benchmarks evaluate vision-language models across diverse tasks, but task-level scores do not reveal which underlying capabilities account for success or failure. Each task requires recovering spatial evidence, representing geometry, and reasoning over it. We disentangle these capabilities by compa...

### [Frozen Scenes, Shifting Winners: Configuration Fragility in Text-to-3D Evaluation](https://arxiv.org/abs/2610.00447v1)

- **Authors:** Anson Y. Lam, Shuqing Li, Michael R. Lyu
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Can a text-to-3D leaderboard change when every generated scene stays fixed? We audit this question for rendered-image evaluation, where camera settings and caption wording become part of the measurement protocol. Across 300 frozen scenes from six generators, we vary eight render and caption factors for 19 alignment...

### [Fusing Visual and Textual Representations via Multi-layer Fusing Transformers for Vietnamese Visual Question Answering](https://arxiv.org/abs/2610.01637v1)

- **Authors:** Cong Phu Nguyen, Huy Tien Nguyen, Tung Le
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** In recent decades, artificial intelligence has made significant progress in understanding and interacting with images. One of the important applications of this technology is Visual Question Answering (VQA), a research field that requires computers to understand and answer questions about images in a natural manner....

### [FutureWorlds: Learning Robotic World Models from Alternative Futures](https://arxiv.org/abs/2610.01019v1)

- **Authors:** Hao Wu, Shengju Qian, Weiyan Wang, Fan Xu, Fan Zhang, Yuanpeng He, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Robotic world models predict action-conditioned future scenes, providing a foundation for understanding action outcomes. However, turning alternative predictions into useful learning signals remains challenging: similar candidates limit informative quality comparisons, while diverging trajectories require persistent...

### [Generative Cinematographer: Composing Camera and Object Motion in 3D](https://arxiv.org/abs/2610.02180v1)

- **Authors:** Jiahan Zhang, Chaohao Yang, Namitha Guruprasad, Vivekjyoti Banerjee, Trong-Tung Nguyen, Alan Yuille, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Current controllable video generation systems often rely on 2D motion trajectories or sparse drag signals for object motion. These controls are ambiguous because the same 2D trajectory can correspond to different 3D motions, especially when the camera and objects move simultaneously. We present Generative Cinematogr...

### [GeoLatent: Geometry-Guided Latent Structuring with Routed Optimization for 3D Reasoning](https://arxiv.org/abs/2610.02091v1)

- **Authors:** Yakun Zhu, Yi Bin, Yujuan Ding, Zheng Wang, Pengpeng Zeng, Duo Peng, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Despite progress in vision-language models, 3D spatial reasoning from 2D images remains challenging. Text-based methods describe intermediate geometry with discrete tokens, limiting fidelity for continuous spatial relations. Continuous latents offer richer representations, but a single latent type does not explicitl...

### [GIFTBench: Diagnosing Generalization in Image Forgery Localization and Informing Model Design](https://arxiv.org/abs/2610.01778v1)

- **Authors:** Baoke Dou, Ziye Wang, Hao Wang, Guoqing Cai, Wende Tan, Chenyang Si, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Reliable evaluation of image forgery localization (IFL) requires assessing models under diverse distribution changes, yet existing benchmarks often cover limited manipulation conditions or entangle multiple factors in cross-dataset evaluation. Consequently, aggregate performance provides an incomplete view of locali...

### [Harnessing Vision-Language Models for Perceptual Quality Assessment and Autonomous Content Adjustment in Augmented Reality](https://arxiv.org/abs/2610.00677v1)

- **Authors:** Elias Rotondo, Lin Duan, Yanming Xiu, Sangjun Eom, Conrad Li, Maria Gorlatova
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Advancements in augmented reality (AR) continue to foster innovative solutions, facilitating novel methodologies within educational systems, healthcare delivery, and risk-mitigation protocols. However, optimizing for end-user immersion and comfort remains challenging, as AR head-mounted displays contend with constra...

### [HAWK: Rethinking Multimodal Drafting for Speculative Decoding](https://arxiv.org/abs/2610.00623v1)

- **Authors:** Wenhan Yang, Anirudh Rao, Ashwin Chandra
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Speculative decoding has achieved substantial lossless speedups for LLMs, but remains less effective for large vision-language models (LVLMs), where lightweight drafters struggle to use rich multimodal information. A second limitation is that standard distillation supervises the drafter only along the original train...

### [Hybrid Attention Transformers for Multi-Spectral Satellite Super-Resolution](https://doi.org/10.31224/8320)

- **Authors:** Naman Sharma
- **Date:** 2026-09-26
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** efficient-vision
- **Abstract summary:** Spaceborne optical imaging missions, such as the European Space Agency's Copernicus Sentinel-2 constellation, provide vital multi-spectral observations worldwide, yet optical aperture diffraction limits native Ground Sampling Distance (GSD) to 10 m across visible and near-infrared (VNIR) bands. Traditional Single-Im...

### [Hybrid Transformer-Mamba for Weakly Supervised Volumetric Medical Segmentation](https://doi.org/10.1007/978-3-032-38069-2_28)

- **Authors:** Yiheng Lyu, Xu Lian, Coen Arrow, Mohammed Bennamoun, Farid Boussaïd, Girish Dwivedi
- **Date:** 2026-09-25
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** No abstract available.

### [Just Align $\bm{x}$: Aligning Predictions, Not Representations](https://arxiv.org/abs/2610.00600v1)

- **Authors:** Yuyao Zhang, Yuwei Hu, Ziyang Mai, Yu-Wing Tai
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** benchmark
- **Abstract summary:** Representation alignment has become an effective way to accelerate diffusion training, but its benefits do not transfer reliably to pixel-space clean-image prediction. In JiT, we find that auxiliary feature alignment can improve access to semantic features while reducing access to image variation needed for clean-im...

### [Learning from Failure: Leveraging Unreliable Predictions in Semi-Supervised Real-World Adverse Weather Removal](https://arxiv.org/abs/2610.02051v1)

- **Authors:** Cap Dang Xuan Kiet, Tat-Jen Cham
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Adverse weather image restoration aims to recover images degraded by rain, haze, snow, and other weather-induced artifacts, thereby improving the robustness of outdoor vision systems. Existing unified restoration models exhibit limited generalization to real-world scenes due to their reliance on synthetic supervisio...

### [MapLightning: Online Vectorized HD Map Construction with 1D Map Tokens](https://arxiv.org/abs/2610.01905v1)

- **Authors:** Shen Zheng, Anurag Ghosh, Mani Ramanagopal, Srinivasa Narasimhan
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** efficient-vision, benchmark
- **Abstract summary:** Online vectorized HD map construction is essential for scaling safe autonomous driving and requires accurate, real-time inference. Prior methods typically rely on dense bird's-eye-view (BEV) grids as the intermediate representation. We propose \textit{MapLightning}, which replaces the dense BEV grid with a compact s...

### [MIRTO: a registration-gated, multiverse-tested evaluation protocol for unsupervised anomaly segmentation in brain MRI](https://arxiv.org/abs/2610.02136v1)

- **Authors:** Negin Kafee Hernashki, Soumick Chatterjee
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Unsupervised anomaly detection (UAD) methods for brain MRI are ranked by a single score, yet that score rests on choices that are rarely reported: how each anomaly map is aligned with the reference, how and on which data the threshold is set, and which false-positive budget, metric, aggregation and lesion definition...

### [MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs](https://arxiv.org/abs/2610.01434v1)

- **Authors:** Xudong Wang, Hao Wu, Haozhe Hu, Peiran Yin, Xinghao Chen, Yunpu Ma, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** efficient-vision
- **Abstract summary:** Multimodal large language models (MLLMs) incur substantial inference costs when processing long visual-textual sequences. While existing operation compression methods exploit modality-level redundancy, they largely treat computation within attention heads and shared feed-forward network (FFN) channels as unified uni...

### [NarrativeFlow: Flow-Based Vision-Language-Action Model Using Robot Velocity Fields](https://arxiv.org/abs/2610.00981v1)

- **Authors:** Shota Kobayashi, Koki Seno, Daichi Yashima, Komei Sugiura
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** We focus on language-conditioned flow-based manipulation, where robot flows (robot velocity fields) serve as embodiment-agnostic, motion-centric representations for leveraging data collected from multiple robot platforms. This task is crucial because language-conditioned manipulation is essential for practical robot...

### [Not All Error Yields to Scale: Where Scaling Stops in Vision-Language Inference](https://arxiv.org/abs/2610.01640v1)

- **Authors:** Xinye Zhao, Yunkai Dang, Yunchen Wu, Wenbin Li
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Vision-language models (VLMs) face a fixed-budget trade-off between processing more visual information for fine-grained perception and using a larger language backbone for complex reasoning. Existing studies do not tell us which combination of backbone size and input resolution to deploy, especially in high-resoluti...

### [Paying for Too Many Tokens? Valid and Cost-Efficient Multimodal LLM Annotation with Simple Heuristics](https://arxiv.org/abs/2610.00809v1)

- **Authors:** Zhixi Zhu, Kristina Gligoric
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Vision-Language Models (VLMs) enable video annotation at scale, but costs accumulate quickly: processing a typical 60-second short-form video at one frame per second requires millions of tokens. To reduce costs, researchers rely on heuristics such as sampling a subset of frames, compressing videos into image grids,...

### [PhaseAT: Fourier Phase Adversarial Training for Medical Image Domain Generalization](https://arxiv.org/abs/2610.01807v1)

- **Authors:** Ahmed Sharshar, Asif Hanif, Naveen Kumar Kummari, Mohammad Yaqub, Mohsen Guizan
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Reliable clinical deployment of deep medical image models is hindered by distribution shifts across scanners, sites, and acquisition protocols. Existing domain generalization (DG) methods often focus on style or intensity diversification, but they can still leave networks dependent on domain-specific texture correla...

### [PhysicsLENS: Diagnosing Physical Property Blindness in Video Generation Models](https://arxiv.org/abs/2610.01162v1)

- **Authors:** Isaiah Milkey, Som Sagar, Aditya Taparia, Xinyuan Liu, Jiqing Wen, Ransalu Senanayake
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Reliable video world models could provide scalable predictive environments for robot learning, planning, and evaluation. However, generated robot videos can violate physical principles and complete tasks through physically implausible behavior, limiting their reliability for robot learning and planning. Current vide...

### [RASteer: Retain-Aware Activation Steering for Concept Erasure in Diffusion Models](https://arxiv.org/abs/2610.01969v1)

- **Authors:** Yongliang Wu, Haori Lu, Yulun Wu, Jinqi Luo, Xingyu Zhu, Yaoyao Liu
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: touches vision, but the excluded framing leaves the visual contribution unclear.
- **Tags:** vision-adjacent
- **Abstract summary:** Concept erasure aims to remove a target concept, such as a copyrighted style, a recognizable character, or unsafe content, from a pretrained text-to-image diffusion model while preserving its ability to generate other content. Existing activation steering methods build an erasure direction mainly from the target con...

### [Retrospective Open-Vocabulary Memory for Long-Term Object Search](https://arxiv.org/abs/2610.00330v1)

- **Authors:** Jiaming Wang, Zhiwei Xue, Chen Jizhuo, Peng Shiqi, Harold Soh
- **Date:** 2026-09-29
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Long-term object search requires learning where objects usually appear from repeated but uneven observations of a changing environment. We formulate retrospective open-vocabulary memory as probabilistic inference from censored observations, where the key idea is to reason with evidence per opportunity: a detection o...

### [Revisiting Cross-Reconstruction for Generalizable Deepfake Detection](https://arxiv.org/abs/2610.01544v1)

- **Authors:** Bingjian Yang, Shilei Zhao, Zheng Wang
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Existing image forgery detectors often suffer from generalization to unseen manipulation methods due to the limited ability to capture transferable forensic cues. Recent cross-reconstruction based methods attempt to improve generalization through semantic-artifact disentanglement, but typically align heterogeneous a...

### [RIQE: a NIQE-style reference model for Computed Tomography](https://arxiv.org/abs/2610.00384v1)

- **Authors:** Fabio Mattiussi
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** The Natural Image Quality Evaluator (NIQE) scores an image by its statistical distance from a model fitted on pristine images, and its distributed model is fitted on photographs. We release the Radiology Image Quality Evaluator (RIQE), a NIQE-style model fitted on 3,792 full-dose slices from 158 patients of the publ...

### [Scores That Hold, Benchmarks That Leak: Measuring Dataset Contamination in Public Brain-Tumor MRI Classification](https://arxiv.org/abs/2610.00421v1)

- **Authors:** Bhanu Prakash Vangala, Sowmya Guda, Latha Peddi, Navya Vangala
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Automated classification of brain tumors from MRI is a heavily published application of deep learning in medical imaging, with reported accuracies on public benchmarks routinely exceeding 98%. However, accuracy does not capture a critical dimension of benchmark quality: dataset integrity, defined as the independence...

### [ShelfChange3D: Object-Level 3D Change Detection for Retail Shelf Monitoring](https://arxiv.org/abs/2610.01283v1)

- **Authors:** Lingyi Zhou, Yunke Wang, Mengyu Zheng, Wenbo Wang, Zijian Wang, Chang Xu
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Reliable shelf monitoring is an important capability for retail automation, yet existing out-of-stock detection methods mainly operate in image space and lack metric 3D localization for downstream robotic systems. We formulate shelf monitoring as object-level 3D change detection: given two RGB-D observations capture...

### [SIEVE: Selective attention-value Suppression for Vision-Language Models Unlearning](https://arxiv.org/abs/2610.01962v1)

- **Authors:** Si Qi Goh, Cap Dang Xuan Kiet, Tat-Jen Cham, Kwok-Yan Lam
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** The ability of vision-language models (VLMs) to associate visual identities with biographical information creates a need for selective unlearning of personally identifiable information (PII) while preserving permitted knowledge about the same individual. This setting is challenging because both sensitive and retaine...

### [Skeleton-and-Strategy Prompting: Training-Free Negation Understanding for Vision-Language Models](https://arxiv.org/abs/2610.01180v1)

- **Authors:** Yuliang Cai, Mohammad Rostami, Jesse Thomason
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Despite the strong performance of Vision-Language Models (VLMs) on a wide range of visual question answering (VQA) tasks, these models consistently struggle to understand negation and produce incorrect answers when questions involve negated clauses. To address this limitation, we propose Skeleton-and-Strategy Prompt...

### [Surface-volume self-supervised representation learning of brain MRI for genetic discovery](https://arxiv.org/abs/2610.02114v1)

- **Authors:** Tian Xia, Nuo Chen, Zihao Zhu, Huiwen Han, Ziqian Xie, Zhiwen Fan, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Existing genome-wide association studies (GWAS) of brain imaging provide predefined or deep-learning-derived imaging phenotypes, yet these phenotypes come from either volumetric scans or cortical surface meshes, so each captures only part of the heritable variation in brain anatomy. Here we introduce MEVA (Mesh-Enha...

### [Synthetic training for long-tail haemorrhagic lesion segmentation in data-scarce settings](https://arxiv.org/abs/2610.01542v1)

- **Authors:** Yuan Cao, Sumeet Dash, Antonia Zachariadis, Stefanie Schreiber, Katja Neumann, Jose Bernal
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Cerebral microbleeds (CMBs) and cortical superficial siderosis (cSS) are imaging markers of cerebral small vessel disease, but their automated segmentation is limited by the scarcity of positive cases and voxel-level annotations. We propose a synthetic training framework for long-tail haemorrhagic lesion segmentatio...

### [Task-Adaptive Grounded 3D-Programmers Using 2D VLMs](https://arxiv.org/abs/2610.02021v1)

- **Authors:** Arman Raayatsanati, Sombit Dey, Anna-Maria Halacheva, Jan-Nico Zaech, Luc Van Gool, Danda Pani Paudel
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Recent vision-language models (VLMs) exhibit remarkable generalization and reasoning abilities, yet 3D understanding in these models is limited by data scale, training diversity, and reasoning capacity. Instead of naively extending these models into 3D, we take a different approach: we enable powerful 2D VLMs to ope...

### [The Impact of Processing Parameters on High-Accuracy Measurements in UAV Photogrammetry](https://arxiv.org/abs/2610.01438v1)

- **Authors:** Paweł Ćwiąkała, Edyta Puniach, Elżbieta Pastucha, Wojciech Gruszczyński
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Unmanned aerial vehicle (UAV) photogrammetry is increasingly used in applications requiring high accuracy, such as determining ground surface changes caused by landslides, mining, or microrelief transformation. While acquisition strategies have been widely studied, the influence of the processing workflow-particular...

### [The RSNA Intracranial Aneurysm (RSNA-ICA) Dataset](https://arxiv.org/abs/2610.01135v1)

- **Authors:** Maria Correia de Verdier, Rachit Saluja, Jason Sho, Maryam Vabarizad, Rennie Yung-Chieh Chen, Uyen N. T. Nguyen, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Intracranial aneurysm rupture is associated with substantial morbidity and mortality, yet aneurysm detection remains challenging, particularly for small lesions and on routine non-angiographic imaging examinations. To support the development and evaluation of artificial intelligence (AI) algorithms for intracranial...

### [Token-Level Video Reinforcement Learning](https://arxiv.org/abs/2610.01973v1)

- **Authors:** Yifan Wang, Gordon Guocheng Qian, Yanyu Li, Anil Kag, Yun Fu
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Reinforcement learning (RL) for video generation usually assigns one scalar reward to an entire sampled video. Yet a video is not uniformly flawed: some visual tokens may already satisfy the prompt, whereas others require correction. A scalar reward cannot localize errors, causing optimization to perturb satisfactor...

### [Towards Reliable Vision-Language Models for Autonomous Driving](https://arxiv.org/abs/2610.01531v1)

- **Authors:** Manasa Mariam Mammen, Priyanka Mary Mammen, Zafer Kayatas, Stefan Wagner
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Vision-Language models (VLMs) are increasingly being explored in autonomous driving for tasks such as scene understanding, driving reasoning, decision-making, and end-to-end driving. As their role becomes more prominent, ensuring their robustness and reliability is increasingly important. In real-world conditions, v...

### [Towards Subject Consistency over Dynamic Subject Sets in Video Generation](https://arxiv.org/abs/2610.01052v1)

- **Authors:** Tongcheng Zhang, Jun Zhu, Jianfei Chen
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** We argue that as video generation extends to longer durations, subject consistency should be evaluated over \textit{dynamic subject sets}. We therefore introduce \textbf{DynSC-Eval}, an evaluation framework that dynamically tracks eligible subjects throughout their visible lifespans and measures local continuity and...

### [Unsupervised Domain Adaptation for Enhanced Radiometer Image Precipitation Estimation using Conditional Flow Matching](https://arxiv.org/abs/2610.01890v1)

- **Authors:** Victor Enescu, Assaad Zeghina, Matthieu Meignin, Nicolas Viltard, Cécile Mallet
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Deep generative networks have recently achieved unprecedented performance in precise image and video editing using sophisticated textual prompts. However, the effectiveness of such models heavily depends on access to very large supervised and annotated image datasets, which can be very difficult to obtain. This is p...

### [VETO: Video Efficient Token Optimization for Vision Language Models](https://arxiv.org/abs/2610.01785v1)

- **Authors:** Gueter Josmy Faure, Hao Ping Wang, Min-Hung Chen, Winston H. Hsu
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Processing long videos with Vision-Language Models (VLMs) is bottlenecked by the quadratic cost of visual tokens, making long-form inference prohibitively expensive. While single-axis compression methods mitigate this, they hit a hard efficiency floor because they treat spatial and temporal redundancy independently....

### [Video Generation Models: A Survey of Post-Training and Alignment](https://arxiv.org/abs/2610.00812v1)

- **Authors:** Chaoyu Li, Xiaoyi Gu, Yogesh Kulkarni, Eun Woo Im, Mohammadmahdi Honarmand, Zeyu Wang, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Video generation has rapidly progressed from short, low-quality clips to high-resolution, long-duration sequences with complex spatiotemporal dynamics. Despite strong generative priors learned through large-scale pretraining, pretrained video models often fail to reliably follow human intent, maintain temporal coher...

### [VideoEvolve: Evolving Agent Harnesses for Video Temporal Grounding](https://arxiv.org/abs/2610.01766v1)

- **Authors:** Bingjun Luo, Yuhuan Fan, Jialin Guo, Siqi Li
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Video temporal grounding aims to localize events in videos from natural-language queries. For agents built around frozen video-language models, the harness determines how queries guide temporal predictions and how those predictions are refined. Manually refining these harnesses requires diagnosing grounding failures...

### [VIEScore2: Unified Image Evaluation with Spatially Grounded Explanations](https://arxiv.org/abs/2610.00994v1)

- **Authors:** Xianda Du, Max Ku, Weiming Ren, Zhi Rui Tam, Chunlin Ren, Ping Nie, et al.
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** synthetic-data
- **Abstract summary:** Existing synthetic image evaluators typically provide only a scalar quality score and do not identify the image regions that support it. We introduce VIEScore2, a unified evaluator for image generation and editing tasks with optional conditioning images. VIEScore2 represents an image as an N x N grid and jointly pre...

### [VisionQ: VLM-as-a-Judge Taxonomy, Dataset and Benchmark for Qualitative Analysis in Computer Vision](https://arxiv.org/abs/2610.00666v1)

- **Authors:** Vu Dinh Xuan, Duc-Hai Nguyen, Minh-Dung Dao, Vu Quynh Giao, Quang Hong Nguyen, Binh-Son Hua, et al.
- **Date:** 2026-09-30
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Qualitative comparison figures are central evidence in computer vision papers, and vision-language models (VLMs) are increasingly used to judge them. Yet existing benchmarks score only scalar quality or overall preference, so a judge can be rewarded for picking the preferred image for the wrong visual reason. We int...

### [Weather-Aware Domain Adaptation for Street-View Weather Recognition](https://arxiv.org/abs/2610.02000v1)

- **Authors:** Hossein Maghsoumi, George Atia, Yaser P. Fallah
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Adverse conditions such as rain, snow, fog, and dust remain challenging for camera-based perception in autonomous driving. We study multi-class weather recognition from street-view images under domain shift, where most available training data come from non-street-view sources that differ markedly from real driving s...

### [When the Judge Acts: Auditing VLM-Guided Image Selection on Culturally Situated Prompts](https://arxiv.org/abs/2610.01243v1)

- **Authors:** Huichan Seo
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-language
- **Abstract summary:** Vision-language models (VLMs) increasingly act as judges that pick the best of several generated images, so their choices decide what users see. Such judges are usually validated by score agreement with human ratings, not by the images they return. We audit VLM judges as decision-makers: on 300 culturally situated p...

### [Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes](https://arxiv.org/abs/2610.02117v1)

- **Authors:** Sophia Sirko-Galouchenko, Monika Wysoczanska, Andrei Bursuc, Nicolas Thome, Spyros Gidaris
- **Date:** 2026-10-01
- **Source:** arxiv
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** On-policy self-distillation has recently emerged as an effective approach for improving language-model reasoning by supervising students with a frozen or EMA version of themselves that receives privileged information. Its application to multimodal large language models (MLLMs), however, remains largely unexplored. R...
