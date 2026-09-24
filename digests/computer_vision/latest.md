# Latest Paper Scout Digest

Latest daily digest: [2026-09-24](2026-09-24.md).

# Paper Scout Digest - 2026-09-24

## Run Summary

- **Run ID:** 4
- **Candidates fetched:** 100
- **New unique papers:** 97
- **Relevant:** 20
- **Maybe relevant:** 68
- **Irrelevant:** 12
- **Source summary:** openalex: 100, semantic_scholar: 0

## Source Warnings

- arxiv failed for 'all:object and all:detection': http error for https://export.arxiv.org/api/query?search_query=all%3Aobject+and+all%3Adetection&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:"real-time object detection"': http error for https://export.arxiv.org/api/query?search_query=all%3A%22real-time+object+detection%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:"yolo"': http error for https://export.arxiv.org/api/query?search_query=all%3A%22yolo%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:open and all:vocabulary and all:object and all:detection': http error for https://export.arxiv.org/api/query?search_query=all%3Aopen+and+all%3Avocabulary+and+all%3Aobject+and+all%3Adetection&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:vision and all:transformer': http error for https://export.arxiv.org/api/query?search_query=all%3Avision+and+all%3Atransformer&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'cat:cs.cv': http error for https://export.arxiv.org/api/query?search_query=cat%3Acs.cv&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex: incomplete discovery window for 'real-time object detection'; single-page record limit reached.
- openalex: incomplete discovery window for 'yolo object detector'; single-page record limit reached.
- openalex: incomplete discovery window for 'vision transformer image recognition'; single-page record limit reached.
- openalex: incomplete discovery window for 'image segmentation deep learning'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'real-time object detection'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'yolo detector'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'open-vocabulary object detection'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'visual representation learning'; single-page record limit reached.

## Highly Relevant

### [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640v5)

- **Authors:** Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi
- **Date:** 2015-06-08
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, efficient-vision
- **Abstract summary:** We present YOLO, a new approach to object detection. Prior work on object detection repurposes classifiers to perform detection. Instead, we frame object detection as a regression problem to spatially separated bounding boxes and associated class probabilities. A single neural network predicts bounding boxes and cla...

### [A deep learning-assisted whole-cell biosensor for catechol monitoring: Synergizing BphC recognition with a multi-feature fusion vision transformer](https://doi.org/10.1016/j.talanta.2026.130638)

- **Authors:** Xiaoyan Qi, Guoqiang Sun, Yuzhi Xue, Yan Liang, Pingyu Wang, Fangling Ning, et al.
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** No abstract available.

### [A deep learning-expert hybrid framework for interpreting interior and architectural design styles in cultural heritage contexts](https://doi.org/10.1080/00038628.2026.2737179)

- **Authors:** Dung Nguyen, Van-Tung Nguyen, Giang Bui
- **Date:** 2026-09-22
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** This study investigates how artificial intelligence (AI) supports the interpretation of interior and architectural design styles (IADS) through a hybrid framework that combines deep learning, expert evaluation, and explainable AI. A diverse set of customized deep learning models, including EfficientNetB3, ResNet50,...

## Maybe Relevant

### [PART: Learning 3D Part Assembly and Retrieval with Transformers](https://arxiv.org/abs/2609.19872)

- **Authors:** Rucha Bao, Wenzheng Wu, Chucheng Xiang, Zhongyuan Liu, Yuan Liu, Jinxin Dong, et al.
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (59/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** pose
- **Abstract summary:** 3D assembly is fundamental to modern manufacturing and digital content creation. In this paper, we present PART, a unified transformer-based framework for 3D part retrieval and assembly: given a target shape and a part library, PART automatically selects the appropriate parts and predicts their 6-DoF poses to recons...

### [A Lightweight PCB Defect Detection Method Based on Heterogeneous Feature Enhancement and Discrepancy-Guided Fusion](https://doi.org/10.3390/s26185984)

- **Authors:** Yujie Pei, Xuehong Gao, Shenyuan Gao, Yongchang Zhang, Ying Liu, Guozhong Huang, et al.
- **Date:** 2026-09-21
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo
- **Abstract summary:** Accurate detection of small and weak defects is essential for ensuring the manufacturing quality and operational reliability of printed circuit boards (PCBs). Existing detectors, however, remain constrained by insufficient fine-grained feature representation, interference from repetitive conductive backgrounds, loca...

### [Hybridnav: A Hybrid Approach to Zero-Shot Object Detection with Adaptive Exploration for Autonomous Reconnaissance](https://doi.org/10.4271/2026-01-7517)

- **Authors:** Hemanth Indurthi, Eric Martinson
- **Date:** 2026-09-22
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: robotics or driving system where the vision contribution is not clearly the subject.
- **Tags:** object-detection
- **Abstract summary:** Autonomous reconnaissance in unknown or contested environments demands robust perception systems capable of identifying diverse objects without prior training data. This paper presents HybridNAV, a hybrid framework that combines multiple foundation models with an adaptive navigation system for zero-shot object detec...

### [RViTCANet: a multimodal network for UAV recognition based on millimeter wave radar RCS data](https://doi.org/10.1007/s40747-026-02526-7)

- **Authors:** Hongyu Gao, Yujie Huo, Ahmad Najmi Bin Amerhaider Nuar, Junkun Hong
- **Date:** 2026-09-22
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer
- **Abstract summary:** Precise recognition of low-altitude UAVs is critical for airspace security, yet current radar cross section (RCS)-based multimodal methods face challenges regarding limited local receptive fields, rigid temporal modeling, and inefficient fusion strategies, especially when dealing with nonlinear scattering patterns,...

### [HACI-Net: A Hybrid Attention and Channel Interaction Network for Food Image Recognition](https://doi.org/10.21203/rs.3.rs-10598219/v1)

- **Authors:** Zhiyong Xiao, Chaoliang Liu, Zhaohong Deng
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** visual-representation
- **Abstract summary:** No abstract available.

### [A calibrated multi-scale transformer-based dual deep convolutional neural network framework for robust parasitic egg recognition across diverse microscopy conditions](https://doi.org/10.1016/j.compeleceng.2026.111492)

- **Authors:** Muhammad Bilal Zia, Xujuan Zhou, Raj Gururajan, Ka Ching Chan
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** The accurate identification of parasitic eggs in microscopic images remains a persistent challenge in both clinical and veterinary diagnostics. Existing manual examination techniques, while effective, are time-consuming, error prone, and difficult to standardize across diverse laboratory settings. Existing automated...
