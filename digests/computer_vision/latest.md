# Latest Paper Scout Digest

Latest daily digest: [2026-09-28](2026-09-28.md).

# Paper Scout Digest - 2026-09-28

## Run Summary

- **Run ID:** 7
- **Candidates fetched:** 25
- **New unique papers:** 25
- **Relevant:** 8
- **Maybe relevant:** 13
- **Irrelevant:** 4
- **Source summary:** openalex: 25, semantic_scholar: 0

## Source Warnings

- arxiv failed for 'all:object and all:detection': http error for https://export.arxiv.org/api/query?search_query=all%3Aobject+and+all%3Adetection&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:"real-time object detection"': http error for https://export.arxiv.org/api/query?search_query=all%3A%22real-time+object+detection%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:"yolo"': http error for https://export.arxiv.org/api/query?search_query=all%3A%22yolo%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:open and all:vocabulary and all:object and all:detection': http error for https://export.arxiv.org/api/query?search_query=all%3Aopen+and+all%3Avocabulary+and+all%3Aobject+and+all%3Adetection&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'all:vision and all:transformer': http error for https://export.arxiv.org/api/query?search_query=all%3Avision+and+all%3Atransformer&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'cat:cs.cv': http error for https://export.arxiv.org/api/query?search_query=cat%3Acs.cv&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex failed for 'real-time object detection': http error for https://api.openalex.org/works?search=real-time+object+detection&filter=from_publication_date%3A2026-09-21&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable
- openalex failed for 'yolo object detector': http error for https://api.openalex.org/works?search=yolo+object+detector&filter=from_publication_date%3A2026-09-21&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable
- openalex: incomplete discovery window for 'vision transformer image recognition'; single-page record limit reached.
- openalex failed for 'image segmentation deep learning': http error for https://api.openalex.org/works?search=image+segmentation+deep+learning&filter=from_publication_date%3A2026-09-21&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable
- semantic_scholar: incomplete discovery window for 'real-time object detection'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'yolo detector'; single-page record limit reached.
- semantic_scholar: incomplete discovery window for 'open-vocabulary object detection'; single-page record limit reached.
- semantic_scholar failed for 'visual representation learning': Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Highly Relevant

### [Vision–language guided semantic-geometric transformer for memory-efficient 3D scene understanding](https://doi.org/10.3389/frai.2026.1945529)

- **Authors:** Licheng Liu, Yu Li, Fuyong Liu
- **Date:** 2026-09-25
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies visual representation learning or large visual encoders.
- **Tags:** visual-representation, 3d-vision
- **Abstract summary:** Recent 3D Transformers have become a dominant framework for point-cloud segmentation by modeling spatial context in sparse 3D scenes. However, geometry and color alone provide limited high-level semantic cues, especially for cluttered boundary regions, visually similar objects, and long-tail categories. To address t...

### [Cloud-Based Facial Expression Recognition Using Squeeze Vision Transformer](https://doi.org/10.26437/2pdqpg59)

- **Authors:** S. Al-Darraji, A. J. Jalil
- **Date:** 2026-09-26
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, efficient-vision
- **Abstract summary:** Purpose: This paper presents and evaluates a cloud-oriented facial expression recognition (FER) system built on a compact, squeeze-style Vision Transformer, and assesses its suitability as an accurate, resource-efficient modelling layer for cloud and edge-cloud deployment. Design/Methodology/Approach: A pretrained V...

### [INRA-Transformer: A Multi-Scale Hybrid Vision Transformer for Precise Seismic Deformation Mapping of the 6.1 Mw Sındırgı Earthquake](https://doi.org/10.21203/rs.3.rs-10777482/v1)

- **Authors:** İlyas Aslan
- **Date:** 2026-09-25
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** No abstract available.

### [NS-ATTENTION: Newton-Schulz Transformations of Attention Outputs in Vision Transformers](https://arxiv.org/abs/2609.27735)

- **Authors:** Xiaohe Jiang, Guoqiang Zhang, Tianjin Huang, Ronghui Mu
- **Date:** 2026-09-23
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, efficient-vision
- **Abstract summary:** Newton-Schulz (NS) iteration has recently been used in the Muon optimizer to transform update matrices during the training of large language models. Motivated by its spectral effect, we investigate applying NS directly to Transformer attention representations. We introduce Newton-Schulz Attention (NS-Attn.), a param...

## Maybe Relevant

### [Automated Multi-Class Skin Cancer Classification Using Vision Transformers](https://doi.org/10.33411/ijist/2008)

- **Authors:** Wasim Habib, Salman Ilahi Siddiqui, Bilal Ur Rehman, Mohammad Usman Ali Khan, Sahibzada Muhammad Faheem
- **Date:** 2026-09-23
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer, visual-representation
- **Abstract summary:** Automated analysis of dermoscopic images can support the assessment of skin lesions; however, reliable multi-class classification remains challenging due to visual similarity among diagnoses, class imbalance, and variations across image sources. This study presents a Vision Transformer (ViT-B/16)-based pipeline for...

### [Deep Learning-Based Segmentation, Action, and Phase Recognition in Laparoscopic Cholecystectomy: A Review](https://doi.org/10.62762/jaib.2026.698089)

- **Authors:** Hafsa Gulzar, Muhammad Bilal, Muhammad Zubair Nawaz, Muhammad Yaqub, Chayut Bunterngchit
- **Date:** 2026-09-22
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation, vision-transformer
- **Abstract summary:** The integration of artificial intelligence into biomedical image analysis represents a paradigm shift in clinical decision support and surgical informatics. Laparoscopic cholecystectomy (LC) is a widely performed minimally invasive procedure but remains technically challenging due to limited visibility, anatomical v...

### [Lightweight Vision Transformer-Based U-Net for Brain Tumor Segmentation from MRI](https://arxiv.org/abs/2609.29785)

- **Authors:** Sheekar Banerjee, Md. Srabon Chowdhury, Md. Mahbub Hasan Akash, Ishtiak Al Mamoon
- **Date:** 2026-09-24
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation, vision-transformer, metrics
- **Abstract summary:** Accurate brain tumor segmentation from Magnetic Resonance Imaging is essential for diagnosis, treatment planning, and surgical guidance. Although Convolutional Neural Networks, particularly UNet, have achieved significant success in medical image segmentation, they often struggle to capture the long-range spatial de...

### [SegDINO: Introducing Multi-scale Structure Into DINO for Efficient Medical Image Segmentation](https://doi.org/10.1007/978-3-032-38085-2_48)

- **Authors:** Sicheng Yang, Hongqiu Wang, Zhaohu Xing, Sixiang Chen, Qiuxia Yang, Yize Mao, et al.
- **Date:** 2026-09-26
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation
- **Abstract summary:** No abstract available.

### [Task-Induced Riemannian Metrics for Vision Transformer Feature Spaces](https://arxiv.org/abs/2609.27988)

- **Authors:** Andrew Bond, Ege Erdem Ozlu, Tuna Çimen, Ilkin Umut Melanlioglu, Tolga Birdal, Erkut Erdem, et al.
- **Date:** 2026-09-23
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer, efficient-vision
- **Abstract summary:** Methods operating on Vision Transformer (ViT) feature spaces typically rely on Euclidean distance or cosine similarity. This assumes that every direction is equally meaningful, but there is no reason to believe the true task geometry has this property. The task-sensitive geometry of the feature space is given by the...

### [Transcribing Lines of Handwritten Text Using TrOCR: An Encoder-Decoder Model Based on Pre-Trained Image and Text Transformers](https://doi.org/10.5201/ipol.2026.587)

- **Authors:** Natalia Bottaioli, Daniel Parres, Yung-Hsin Chen
- **Date:** 2026-09-24
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: uses an existing detector or model without a clearly general method contribution.
- **Tags:** vision-transformer
- **Abstract summary:** This article focuses on analyzing several aspects of the handwritten text recognition (HTR) models belonging to the TrOCR family introduced by Minghao Li et al. in [TrOCR: Transformerbased Optical Character Recognition with Pre-trained Models, AAAI Conference on Artificial Intelligence, 2023].The TrOCR models are de...

### [X-Edit: Exact, Explicit, and Explainable Null-Space Editing for Medical Vision Transformers](https://doi.org/10.1007/978-3-032-38079-1_59)

- **Authors:** Yuanye Liu, Siyuan Zhou, Ke Zhang, Lei Li, Wei Chen, Xiahai Zhuang
- **Date:** 2026-09-25
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer
- **Abstract summary:** No abstract available.
