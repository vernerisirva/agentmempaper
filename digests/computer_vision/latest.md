# Latest Paper Scout Digest

Latest daily digest: [2026-09-22](2026-09-22.md).

# Paper Scout Digest - 2026-09-22

## Run Summary

- **Run ID:** 2
- **Candidates fetched:** 100
- **New unique papers:** 93
- **Relevant:** 28
- **Maybe relevant:** 60
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

### [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872v3)

- **Authors:** Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, Sergey Zagoruyko
- **Date:** 2020-05-26
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Studies DETR-family or query-based object detection.
- **Tags:** object-detection, detr, segmentation, benchmark
- **Abstract summary:** We present a new method that views object detection as a direct set prediction problem. Our approach streamlines the detection pipeline, effectively removing the need for many hand-designed components like a non-maximum suppression procedure or anchor generation that explicitly encode our prior knowledge about the t...

### [Decoder-Agnostic Token Merging for Vision Transformers: A Systematic Study of G2TM](https://arxiv.org/abs/2609.18279)

- **Authors:** Victor Bercy, Martyna Poreba, Michal Szczepanski, Samia Bouchafa
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** relevant (98/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation, vision-transformer, visual-representation, efficient-vision, benchmark
- **Abstract summary:** Vision Transformers (ViTs) have achieved state-of-the-art performance across a range of computer vision tasks, mainly thanks to the self-attention mechanism. However, its complexity, increasing quadratically with the number of tokens, remains the major obstacle to ViT efficiency and deployment at scale. Token mergin...

### [Multi-Stream Deep Learning Framework for Real-Time Dangerous Behavior Detection and Defect Recognition in Power Systems](https://doi.org/10.3233/atde260887)

- **Authors:** Xiaoming Chen, Yifeng Liu, Pengcheng Wang, Jingwen Li, Jing Zhou, Yuqian Wang, et al.
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (98/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, pose, efficient-vision, metrics
- **Abstract summary:** The operational safety of modern power systems faces threats from infrastructure degradation and human procedural violations. Traditional monitoring lacks real-time prevention and neglects Safety Ergonomics principles regarding human attention decay, leading to “Inattentional Blindness.” This paper proposes “SafeGri...

### [Segment Anything](https://arxiv.org/abs/2304.02643v1)

- **Authors:** Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, et al.
- **Date:** 2023-04-05
- **Source:** arxiv
- **Relevance:** relevant (96/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation, visual-representation
- **Abstract summary:** We introduce the Segment Anything (SA) project: a new task, model, and dataset for image segmentation. Using our efficient model in a data collection loop, we built the largest segmentation dataset to date (by far), with over 1 billion masks on 11M licensed and privacy respecting images. The model is designed and tr...

### [Self-supervised knowledge distillation for few-shot single-stage 3D object detection](https://doi.org/10.1016/j.compeleceng.2026.111522)

- **Authors:** Alok Kumar Tiwari, Charu Gandhi, Prateek Singhal, Madan Singh, Rajesh Dwivedi
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection, 3d-vision, efficient-vision, benchmark
- **Abstract summary:** Conventional deep learning models for 3D object detection require a large number of annotated bounding boxes and substantial computational resources, which limit their applicability in data- and resource-constrained autonomous driving scenarios. To address this challenge, this paper proposes SSD-KD, a self-supervise...

### [Multi-output classification of dental implant placement parameters in the posterior maxilla from CBCT images using a two-stage vision transformer framework](https://doi.org/10.1038/s41598-026-70962-z)

- **Authors:** Nattamon Wachirasakulchai, Raweewan Arayasantiparb, Tharathip Kulchotirat, Kiatanant Boonsiriseth, Pobploy Petchmedyai, Penporn Luangchana, et al.
- **Date:** 2026-09-20
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, efficient-vision
- **Abstract summary:** Implant placement in the posterior edentulous maxilla is clinically challenging due to anatomical variability, limited residual bone height, and maxillary sinus pneumatization. Conventional planning relies heavily on clinician experience and manual radiographic interpretation, leading to variability and subjectivity...

### [The Generalization Gap in Deep Learning for Wound Image Segmentation: A PRISMA 2020 Systematic Review of Internal versus External Validation](https://doi.org/10.5281/zenodo.22859249)

- **Authors:** Rokeya Akter
- **Date:** 2026-09-20
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation
- **Abstract summary:** No abstract available.

### [The Generalization Gap in Deep Learning for Wound Image Segmentation: A PRISMA 2020 Systematic Review of Internal versus External Validation](https://doi.org/10.5281/zenodo.22859250)

- **Authors:** Rokeya Akter
- **Date:** 2026-09-20
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation
- **Abstract summary:** No abstract available.

## Maybe Relevant

### [Accuracy- and Real-Time-Aware 4D Radar Preprocessing for Autonomous Driving Perception Systems](https://arxiv.org/abs/2609.18542)

- **Authors:** Woo-Jin Jung, Dong-Hee Paek, Jeong-Su Park, Seung-Hyun Kong
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: robotics or driving system where the vision contribution is not clearly the subject.
- **Tags:** object-detection, 3d-vision, edge-deployment
- **Abstract summary:** 4D radar has emerged as a promising next-generation sensor for improving the robustness of autonomous driving perception systems because of its stable sensing capability under adverse weather conditions. However, deploying 4D radar in embedded environments with limited hardware resources requires radar-representatio...

### [DRerio LogAI: an open-source, GPU-free platform for automated tracking and behavioural analysis of adult zebrafish (Danio rerio)](https://doi.org/10.5281/zenodo.22783436)

- **Authors:** Marco Antônio Sant'Ana Camargos, Percília Cardoso Giaquinto
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** yolo, tracking
- **Abstract summary:** DRerio LogAI is an open-source desktop platform for automated tracking, closed-loop stimulation and behavioural analysis of adult zebrafish (Danio rerio). It combines YOLOv11 detection, BYTETracker multi-object tracking and Intel OpenVINO inference in an event-driven architecture, and runs GPU-free on integrated gra...

### [HBB2OBB: Horizontal to Oriented Bounding Box Conversion and Evaluation Tool](https://doi.org/10.5281/zenodo.22817652)

- **Authors:** Róbert Fónod
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, segmentation, benchmark
- **Abstract summary:** HBB2OBB converts horizontal (axis-aligned) bounding boxes (HBBs) into oriented (rotated) bounding boxes (OBBs) by using existing HBB annotations as prompts for segmentation models from the SAM (Segment Anything Model) family. It targets object detection tasks where objects appear at arbitrary orientations, such as a...

### [Quantum Vision Ai For Pediatric Urological Screening Using Hybrid Quantum Machine Learning](https://doi.org/10.38142/jisdb.v5i3.2116)

- **Authors:** Joko Pitoyo, Jahrizal, Fajri Marindra Siregar, Nyoto Nyoto, Rizaldi Putra, Nicholas Renaldo
- **Date:** 2026-09-21
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer
- **Abstract summary:** Pediatric urological disorders require timely recognition to reduce the risk of persistent functional, reproductive, and psychosocial consequences, yet screening still depends heavily on clinician-led visual examination. This study develops and evaluates Quantum Vision AI, a child-safe intelligent screening platform...

### [ResLRP: The Role of Residual Cancellation in Attribution Instability in Vision Transformers](https://arxiv.org/abs/2609.17152)

- **Authors:** Jim Berend, Reduan Achtibat, Daniel Schäffer, Alexander Binder, Wojciech Samek, Sebastian Lapuschkin, et al.
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer, vision-language
- **Abstract summary:** Vision Transformers (ViTs) are central to most modern vision models, yet obtaining input attributions that are fine-grained, faithful, and stable remains challenging. Layer-wise Relevance Propagation (LRP) has been adapted to transformer attention, but in ViTs it often produces noisy, unfaithful explanations. We sho...

### [YOLO27: An Overview of Dual-Scale Architecture and Query-Based Real-Time Computer Vision](https://doi.org/10.6084/m9.figshare.33916828.v3)

- **Authors:** Ranjan Sapkota
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: robotics or driving system where the vision contribution is not clearly the subject.
- **Tags:** object-detection, yolo, segmentation, pose, depth, edge-deployment, benchmark
- **Abstract summary:** This study presents a comprehensive overview of Ultralytics YOLO27 (also called as YOLOv27), examining its scale-adaptive architecture, detection mechanisms, preliminary performance, and implications for real-time computer vision. Unlike conventional YOLO families that largely scale common architectures across model...

### [A COMPUTER VISION APPROACH TO MILITARY OBJECT RECOGNITION](https://doi.org/10.68302/std2026.vol3.154)

- **Authors:** Krasimir Ognyanov Slavyanov
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** visual-representation
- **Abstract summary:** This research described is focused on computer vision tools implemented for detection of a particular military object (or many objects) in a observed scene, given a reference image(s) of the object(s). An algorithm for detecting a specific object based on finding point correspondences between the reference and the t...

### [BenSParX: A robust explainable machine learning framework for Parkinson’s disease detection from Bengali conversational speech](https://doi.org/10.1016/j.artmed.2026.103538)

- **Authors:** Riad Hossain, Muhammad Ashad Kabir, Arat Ibne Golam Mowla, Animesh Roy, Ranjit Kumar Ghosh
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Parkinson's disease (PD) poses a growing global health challenge, with Bangladesh experiencing a notable rise in PD-related mortality. Early detection of PD remains particularly challenging in resource-constrained settings, where voice-based analysis has emerged as a promising non-invasive and cost-effective alterna...
