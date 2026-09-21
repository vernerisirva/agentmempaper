# Latest Paper Scout Digest

Latest daily digest: [2026-09-21](2026-09-21.md).

# Paper Scout Digest - 2026-09-21

## Run Summary

- **Run ID:** 3
- **Candidates fetched:** 100
- **New unique papers:** 93
- **Relevant:** 25
- **Maybe relevant:** 62
- **Irrelevant:** 13
- **Source summary:** openalex: 100

## Source Warnings

- arxiv failed for 'object detection': http error for https://export.arxiv.org/api/query?search_query=all%3Aobject+AND+all%3Adetection&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'real-time object detection': http error for https://export.arxiv.org/api/query?search_query=all%3A%22real-time+object+detection%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'YOLO': http error for https://export.arxiv.org/api/query?search_query=all%3A%22YOLO%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'open-vocabulary object detection': http error for https://export.arxiv.org/api/query?search_query=all%3Aopen+AND+all%3Avocabulary+AND+all%3Aobject+AND+all%3Adetection&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'vision transformer': http error for https://export.arxiv.org/api/query?search_query=all%3Avision+AND+all%3Atransformer&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- arxiv failed for 'cs.CV': http error for https://export.arxiv.org/api/query?search_query=cat%3Acs.CV&start=0&max_results=300&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex: incomplete discovery window for 'real-time object detection'; single-page record limit reached.
- openalex: incomplete discovery window for 'YOLO object detector'; single-page record limit reached.
- openalex: incomplete discovery window for 'vision transformer image recognition'; single-page record limit reached.
- openalex: incomplete discovery window for 'image segmentation deep learning'; single-page record limit reached.
- semantic_scholar failed for 'real-time object detection': Semantic Scholar returned HTTP 429. Configure SEMANTIC_SCHOLAR_API_KEY for higher rate limits. The run continued with other sources.
- semantic_scholar failed for 'YOLO detector': Semantic Scholar returned HTTP 429. Configure SEMANTIC_SCHOLAR_API_KEY for higher rate limits. The run continued with other sources.
- semantic_scholar failed for 'open-vocabulary object detection': Semantic Scholar returned HTTP 429. Configure SEMANTIC_SCHOLAR_API_KEY for higher rate limits. The run continued with other sources.
- semantic_scholar failed for 'visual representation learning': Semantic Scholar returned HTTP 429. Configure SEMANTIC_SCHOLAR_API_KEY for higher rate limits. The run continued with other sources.

## Highly Relevant

### [DETRs Beat YOLOs on Real-time Object Detection](https://arxiv.org/abs/2304.08069v3)

- **Authors:** Yian Zhao, Wenyu Lv, Shangliang Xu, Jinman Wei, Guanzhong Wang, Qingqing Dang, et al.
- **Date:** 2023-04-17
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, detr, efficient-vision, benchmark
- **Abstract summary:** The YOLO series has become the most popular framework for real-time object detection due to its reasonable trade-off between speed and accuracy. However, we observe that the speed and accuracy of YOLOs are negatively affected by the NMS. Recently, end-to-end Transformer-based detectors (DETRs) have provided an alter...

### [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872v3)

- **Authors:** Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, Sergey Zagoruyko
- **Date:** 2020-05-26
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Studies DETR-family or query-based object detection.
- **Tags:** object-detection, detr, segmentation, benchmark
- **Abstract summary:** We present a new method that views object detection as a direct set prediction problem. Our approach streamlines the detection pipeline, effectively removing the need for many hand-designed components like a non-maximum suppression procedure or anchor generation that explicitly encode our prior knowledge about the t...

### [Mask R-CNN](https://arxiv.org/abs/1703.06870v3)

- **Authors:** Kaiming He, Georgia Gkioxari, Piotr Dollár, Ross Girshick
- **Date:** 2017-03-20
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection, segmentation, pose, efficient-vision, benchmark
- **Abstract summary:** We present a conceptually simple, flexible, and general framework for object instance segmentation. Our approach efficiently detects objects in an image while simultaneously generating a high-quality segmentation mask for each instance. The method, called Mask R-CNN, extends Faster R-CNN by adding a branch for predi...

### [RAD-YOLO: a lightweight edge-deployed visual measurement method for small-object detection in UAV imagery](https://doi.org/10.1088/2631-8695/aea8d5)

- **Authors:** Shuai Nie, Jiajian Yang, Xin He, Yuhua Qi, Yanqing Hou
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, backbone, efficient-vision, edge-deployment, metrics
- **Abstract summary:** Abstract Reliable visual measurement of small objects in unmanned aerial vehicle (UAV) imagery is challenging because targets often have low spatial resolution, dense spatial distribution, partial occlusion and strong background clutter. These factors reduce localisation accuracy and make real-time inference on embe...

### [Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030v2)

- **Authors:** Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, et al.
- **Date:** 2021-03-25
- **Source:** arxiv
- **Relevance:** relevant (100/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection, segmentation, vision-transformer, backbone, visual-representation, benchmark, metrics
- **Abstract summary:** This paper presents a new vision Transformer, called Swin Transformer, that capably serves as a general-purpose backbone for computer vision. Challenges in adapting Transformer from language to vision arise from differences between the two domains, such as large variations in the scale of visual entities and the hig...

### [YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors](http://arxiv.org/abs/2207.02696)

- **Authors:** Chien-Yao Wang, Alexey Bochkovskiy, Hong-Yuan Mark Liao
- **Date:** 2022-07-06
- **Source:** openalex
- **Relevance:** relevant (100/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, detr, vision-transformer, efficient-vision, benchmark
- **Abstract summary:** YOLOv7 surpasses all known object detectors in both speed and accuracy in the range from 5 FPS to 160 FPS and has the highest accuracy 56.8% AP among all known real-time object detectors with 30 FPS or higher on GPU V100. YOLOv7-E6 object detector (56 FPS V100, 55.9% AP) outperforms both transformer-based detector S...

### [A study on edge-based object detection in complex scenarios using a lightweight YOLO model](https://doi.org/10.1117/12.3122610)

- **Authors:** Shaoxian Li, Yingying Wei, Tao Li
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, efficient-vision, edge-deployment
- **Abstract summary:** Recent advances in artificial intelligence (AI) and intelligent algorithms have promoted the shift of object detection from cloud-based processing to real-time local perception on edge devices. To address the challenges of scale variation, occlusion interference, complex backgrounds and limited edge computing resour...

### [Cross-scale semantic calibration for lightweight object detection in complex indoor scenes](https://doi.org/10.1088/1361-6501/aea924)

- **Authors:** Jiajie Cui, Xiaojun Wang, Ye Liu
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Studies DETR-family or query-based object detection.
- **Tags:** object-detection, detr, efficient-vision, benchmark
- **Abstract summary:** Abstract Addressing the problems that lightweight detection model in complex indoor scenes suffer from degradation of shallow feature representation after parameter compression, suppression of small-object responses by high-level semantics during multi-scale fusion, and unstable classification confidence under dense...

### [YOLO9000: Better, Faster, Stronger](http://arxiv.org/abs/1612.08242)

- **Authors:** Joseph Redmon, Ali Farhadi
- **Date:** 2016-12-25
- **Source:** openalex
- **Relevance:** relevant (99/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, efficient-vision, benchmark
- **Abstract summary:** We introduce YOLO9000, a state-of-the-art, real-time object detection system that can detect over 9000 object categories. First we propose various improvements to the YOLO detection method, both novel and drawn from prior work. The improved model, YOLOv2, is state-of-the-art on standard detection tasks like PASCAL V...

### [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640v5)

- **Authors:** Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi
- **Date:** 2015-06-08
- **Source:** arxiv
- **Relevance:** relevant (99/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, efficient-vision
- **Abstract summary:** We present YOLO, a new approach to object detection. Prior work on object detection repurposes classifiers to perform detection. Instead, we frame object detection as a regression problem to spatially separated bounding boxes and associated class probabilities. A single neural network predicts bounding boxes and cla...

### [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497v3)

- **Authors:** Shaoqing Ren, Kaiming He, Ross Girshick, Jian Sun
- **Date:** 2015-06-04
- **Source:** arxiv
- **Relevance:** relevant (97/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection, efficient-vision, benchmark
- **Abstract summary:** State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (R...

### [Deformable DETR: Deformable Transformers for End-to-End Object Detection](http://arxiv.org/abs/2010.04159)

- **Authors:** Xizhou Zhu, Weijie Su, Lewei Lu, Bin Li, Xiaogang Wang, Jifeng Dai
- **Date:** 2020-10-08
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies DETR-family or query-based object detection.
- **Tags:** object-detection, detr, benchmark
- **Abstract summary:** DETR has been recently proposed to eliminate the need for many hand-designed components in object detection while demonstrating good performance. However, it suffers from slow convergence and limited feature spatial resolution, due to the limitation of Transformer attention modules in processing image feature maps....

### [DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection](http://arxiv.org/abs/2203.03605)

- **Authors:** Hao Zhang, Feng Li, Shilong Liu, Lei Zhang, Hang Su, Jun Zhu, et al.
- **Date:** 2022-03-07
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies DETR-family or query-based object detection.
- **Tags:** object-detection, detr, benchmark
- **Abstract summary:** We present DINO (\textbf{D}ETR with \textbf{I}mproved de\textbf{N}oising anch\textbf{O}r boxes), a state-of-the-art end-to-end object detector. % in this paper. DINO improves over previous DETR-like models in performance and efficiency by using a contrastive way for denoising training, a mixed query selection method...

### [Image Recognition Technology of Multi-Modal Data Processing in Intelligent Document Management System](https://doi.org/10.3233/atde260845)

- **Authors:** Jiaxin Lin, Ruiqi Li, Yuetian Huang, Yongjiao Yang, Zeqi Zhu, Qing Lu
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, visual-representation, efficient-vision, metrics
- **Abstract summary:** With the continuous advancement of digital office and intelligent archives construction, traditional document management methods have been difficult to adapt to the needs of high-precision analysis and high concurrent processing of multi-source heterogeneous documents. Focusing on the intelligent document management...

### [LD-IoU: A Novel Lorentzian Distance-based Localization Loss for Enhanced Bounding-box Regression with Faster Convergence in YOLOv8-based Knee Osteoarthritis Detection](https://doi.org/10.22266/ijies2026.1031.24)

- **Authors:** Mustafa Radif, Manar Joundy Hazar, Zahraa Ibrahim Abed, Saif Aamer Fadhil
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, metrics
- **Abstract summary:** Knee osteoarthritis (KOA) is one of the most prevalent musculoskeletal disorders, making accurate and automated knee joint detection essential for computer-aided diagnosis.Although YOLO-based object detectors have demonstrated promising performance, most existing approaches rely on the conventional Intersection over...

### [MS-RTDETR: Leveraging Multi-Scale Feature Enhancement and Query Refinement for Small Object Detection](https://doi.org/10.21203/rs.3.rs-10852974/v1)

- **Authors:** Na Sun, Fang Niu, Yujiao Chen, Bing Liu, Xiaoguang Wang, Tianping Li
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies DETR-family or query-based object detection.
- **Tags:** object-detection, detr
- **Abstract summary:** No abstract available.

### [YOLO-MDIR: a YOLO network based on multidirectional convolution for infrared object detection](https://doi.org/10.1117/12.3121343)

- **Authors:** Z. Zhang, J. Deng, H. Wang, H. Zhang, L. Liu, C. Zhang, et al.
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, metrics
- **Abstract summary:** Infrared imaging offers significant advantages over visible-light imaging in real-world applications, performing robustly under night time, adverse weather, low illumination, and smoky or dusty conditions. However, it suffers from critical limitations, including lack of color information, low signal-to-noise ratios...

### [YOLO-TDH: An object detection framework for power transmission line inspection](https://doi.org/10.1016/j.aei.2026.105273)

- **Authors:** Baoye Song, Shihao Zhao, Weibo Liu, Yani Xue
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (96/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo
- **Abstract summary:** Coupled with vision-based inspection techniques, unmanned aerial vehicles (UAVs) have been extensively applied to power transmission line inspection. UAV images typically cover a wide field of view, they often contain complex backgrounds in power transmission line inspection, which make the accurate detection and lo...

### [YOLOv4: Optimal Speed and Accuracy of Object Detection](https://arxiv.org/abs/2004.10934v1)

- **Authors:** Alexey Bochkovskiy, Chien-Yao Wang, Hong-Yuan Mark Liao
- **Date:** 2020-04-23
- **Source:** arxiv
- **Relevance:** relevant (96/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, efficient-vision, benchmark, metrics
- **Abstract summary:** There are a huge number of features which are said to improve Convolutional Neural Network (CNN) accuracy. Practical testing of combinations of such features on large datasets, and theoretical justification of the result, is required. Some features operate on certain models exclusively and for certain problems exclu...

### [YOLOX: Exceeding YOLO Series in 2021](https://arxiv.org/abs/2107.08430v2)

- **Authors:** Zheng Ge, Songtao Liu, Feng Wang, Zeming Li, Jian Sun
- **Date:** 2021-07-18
- **Source:** arxiv
- **Relevance:** relevant (96/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo, efficient-vision, edge-deployment, benchmark
- **Abstract summary:** In this report, we present some experienced improvements to YOLO series, forming a new high-performance detector -- YOLOX. We switch the YOLO detector to an anchor-free manner and conduct other advanced detection techniques, i.e., a decoupled head and the leading label assignment strategy SimOTA to achieve state-of-...

### [Deadline-Aware Hardening of Real-Time Object Detection Against Candidate-Inflation Latency Attacks](https://doi.org/10.21203/rs.3.rs-10938635/v1)

- **Authors:** Salah Gontara, Selem Trabelsi, Khaled Ben Khalifa
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** relevant (94/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection, efficient-vision
- **Abstract summary:** No abstract available.

### [FlexXNOR-OD: A Channel-Grouped XNOR-Based Variable-Precision Accelerator for Real-Time Edge Object Detection](https://doi.org/10.48175/ijarsct-38402)

- **Authors:** Budidha Sriman and D. Sateesh
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (94/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection, efficient-vision
- **Abstract summary:** Object detection at the edge requires a difficult balance among detection accuracy, deterministic latency, memory bandwidth, and energy consumption. Existing binarized accelerators replace multipliers with XNOR and population-count logic, but many designs use a fixed binary datapath or select precision only at the l...

### [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929v2)

- **Authors:** Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, et al.
- **Date:** 2020-10-22
- **Source:** arxiv
- **Relevance:** relevant (93/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, visual-representation, benchmark
- **Abstract summary:** While the Transformer architecture has become the de-facto standard for natural language processing tasks, its applications to computer vision remain limited. In vision, attention is either applied in conjunction with convolutional networks, or used to replace certain components of convolutional networks while keepi...

### [Deep Learning-Based Automated Medical Image Segmentation Algorithm](https://doi.org/10.3233/atde260940)

- **Authors:** Qinghui Guo, Zhandong Liu, Wentao Zeng
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (93/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation, visual-representation
- **Abstract summary:** Medical image segmentation is crucial for early disease diagnosis and precise treatment planning; however, its accuracy remains challenging due to factors such as blurred boundaries and morphological variations. This paper proposes a deep learning segmentation algorithm that integrates a boundary-aware loss function...

### [Object Surface Defect Segmentation using Vision Transformers and Hybrid Models](https://doi.org/10.63503/acset.109)

- **Authors:** Santhya C, VS Sneha Chowdary, Beaulah Jeyavathana
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (93/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, backbone, metrics
- **Abstract summary:** Detection of surface defects in the manufacturing industry is fundamental to maintain the quality of products and reduce waste production. Inspection processes are always affected by human error due to the nature of manual operations in manufacturing environments, particularly in cases of high production rates, whil...

### [QiT: Quantum-Inspired Transformer for Visual Recognition Task](https://arxiv.org/abs/2609.17789)

- **Authors:** Badri N. Patro, Vijay Agneeswaran
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (93/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, visual-representation, benchmark
- **Abstract summary:** Quantum machine learning offers a compelling representational perspective: angle-encoded states inhabit Hilbert spaces in which periodic similarities and interactions can be expressed naturally. Realizing this perspective for visual recognition remains difficult, however, because present quantum neural networks are...

### [Topology-Enhanced Vision Transformer for Complex Pattern Image Recognition: Intelligent Regional School Discrimination in Intangible Cultural Heritage Paper-Cutting](https://doi.org/10.3233/atde260815)

- **Authors:** Changzhe Zhou, Baikun Zhang, Weilin Cui, Jianyu Wang, Junyan Du, Bingyan Li
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (93/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, visual-representation
- **Abstract summary:** Complex pattern image recognition requires models to capture both global visual dependencies and structural attributes, including holes, connected regions, skeleton branches, contours, pattern density, and symmetry. To improve fine-grained artistic image classification, this paper proposes TTViT-FR, a topology-enhan...

### [A Comprehensive Survey of Quantum and Quantum-Inspired Image Segmentation in the Context of Modern Segmentation Methods](https://doi.org/10.21203/rs.3.rs-11007930/v1)

- **Authors:** Marie Gogolin, Yannick Werner, Alexander Geng, Paul Lukowicz, Ali Moghiseh, Maximilian Kiefer-Emmanouilidis
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation
- **Abstract summary:** No abstract available.

### [Architecture-Aware Structured Pruning for Parameter-Efficient Dense Small-Object Detection](https://doi.org/10.1007/978-3-032-38398-3_59)

- **Authors:** Rafael Subo A. Yap, Arren Matthew C. Antioquia
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection, efficient-vision
- **Abstract summary:** No abstract available.

### [Attention-enhanced vision transformer hashing for hybrid image retrieval](https://doi.org/10.1007/s44163-026-02163-6)

- **Authors:** Uyen Nguyen, Hoai Le Ba, Quynh Dao Thi Thuy
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer, efficient-vision, benchmark
- **Abstract summary:** Large-scale image retrieval requires compact representations without substantially sacrificing retrieval accuracy. However, Vision Transformer Hashing (VTS) concatenates all output tokens before hash projection, resulting in a high-dimensional hashing head with considerable model and memory overhead. We replace this...

### [BrainFocus: EEG-Guided ROI Selection for Efficient Vision-Language Models](https://arxiv.org/abs/2609.17443)

- **Authors:** Yihui Peng, G. Lu, Qinyu Chen
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** yolo, vision-language, efficient-vision, benchmark
- **Abstract summary:** Vision-language models (VLMs) achieve strong visual question answering (VQA) performance, but processing large cluttered images is computationally expensive when only a small region is relevant. Electroencephalography (EEG) signals, which capture human neural responses to visual stimuli, can provide a human-derived...

### [DE-SwinJSCC: dual-enhanced swin transformer for wireless image semantic transmission](https://doi.org/10.1038/s41598-026-66105-z)

- **Authors:** Xiangcheng Li, Jibin Lu, Dongri Ban, Youming Sun, Haiqiang Chen, Yunyi Liu
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** With the successful adoption of Transformer architectures in visual tasks, end-to-end joint source channel coding (JSCC) has emerged as a promising paradigm for high-resolution wireless semantic image transmission. However, existing Transformer-based approaches, particularly SwinJSCC, still suffer from several limit...

### [Directing Vision Transformer Attention to Emotion-Relevant Facial Regions for Facial Expression Recognition](https://doi.org/10.20944/preprints202609.1441.v1)

- **Authors:** Nusrat Jahan Tahira, Jangsik Sik Park
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** Facial expression recognition (FER) in unconstrained images is difficult because faces vary widely in pose, illumination, and occlusion, and several expressions are visually similar. Vision Transformers (ViTs) have recently set strong FER benchmarks, yet they share a structural limitation that every image patch is t...

### [Hybrid FAU-guided Vision Transformer for Deep Fake-based Presentation Attack Detection](https://doi.org/10.22266/ijies2026.1031.72)

- **Authors:** Bindiya A J, Anitha N
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** With the evolution of deep learning based fake face generation, it has become easier to launch presentation attacks on face based biometric authentication systems.Especially with ability of generative adversarial networks (GAN) to generate fake faces as close to original, it is necessary to design effective techniqu...

### [Segment Anything](https://arxiv.org/abs/2304.02643v1)

- **Authors:** Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, et al.
- **Date:** 2023-04-05
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies semantic, instance, panoptic, or promptable segmentation.
- **Tags:** segmentation
- **Abstract summary:** We introduce the Segment Anything (SA) project: a new task, model, and dataset for image segmentation. Using our efficient model in a data collection loop, we built the largest segmentation dataset to date (by far), with over 1 billion masks on 11M licensed and privacy respecting images. The model is designed and tr...

### [UAV-LiteDet: A Lightweight Small Object Detection Network for Low-Altitude UAV Scenarios](https://doi.org/10.54254/2755-2721/2026.36918)

- **Authors:** Yining Zhang
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies object-detection architecture, training, or evaluation.
- **Tags:** object-detection, edge-deployment
- **Abstract summary:** Vehicles and pedestrians in low-altitude UAV images usually present features such as small object scales, dense distribution, complex background textures and low contrast. Existing high-precision object detection models often have problems including a large number of parameters, high computational cost and difficult...

### [ViT-ConvGDNet: a vision transformer–MobileNet guided decoder network for robust copy-move forgery detection and localization](https://doi.org/10.1038/s41598-026-64920-y)

- **Authors:** Bhagvan Krishna Gupta, Abhishek Kumar Chouhan, Durgesh Singh, Sandeep S. Udmale, Ankur Pandey
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** relevant (91/100)
- **Reason:** Studies visual backbones or vision-transformer architecture.
- **Tags:** vision-transformer
- **Abstract summary:** Abstract Copy-move forgery is a common form of image manipulation where a portion of an image is copied and pasted back into the image. This is especially difficult to detect when the forgery has been done on copied areas that have undergone post-processing operations, e.g. rotation, scaling, blurring etc. We propos...

### [YOLOv3: An Incremental Improvement](https://arxiv.org/abs/1804.02767v1)

- **Authors:** Joseph Redmon, Ali Farhadi
- **Date:** 2018-04-08
- **Source:** arxiv
- **Relevance:** relevant (91/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** yolo
- **Abstract summary:** We present some updates to YOLO! We made a bunch of little design changes to make it better. We also trained this new network that's pretty swell. It's a little bigger than last time but more accurate. It's still fast though, don't worry. At 320x320 YOLOv3 runs in 22 ms at 28.2 mAP, as accurate as SSD but three time...

## Maybe Relevant

### [A Lightweight Remote Sensing Image Object Detection Model Based on Improved YOLOv8](https://doi.org/10.3233/atde260795)

- **Authors:** Ruiyang Guo
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, edge-deployment, metrics
- **Abstract summary:** Addressing the challenges of complex backgrounds, variable object scales, and constrained edge device deployment in remote sensing images, this paper proposes a lightweight detection model based on an improved YOLOv8s architecture. First, by constructing the Ghost-neck architecture, the original dense convolutional...

### [A REAL-TİME AI-DRİVEN AGRİCULTURAL ROVER INTEGRATİNG PLANT DİSEASE DETECTİON AND GEO-REFERENCED SOİL MOİSTURE ANALYSİS](https://doi.org/10.30546/emnaa.2026.02.28.123)

- **Authors:** Gasimov V.A., Dadashov F.H., Hasanov H.B., Huseynov N.E
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection
- **Abstract summary:** This paper presents an autonomous agricultural ground robot for real-time monitoring of plant health and soil moisture in large-scale crop fields.The proposed system integrates a deep learning-based perception subsystem with autonomous navigation and a custom ground control station (GCS) to enable continuous and geo...

### [Automated pancreatic cancer pathology image segmentation using deep learning to quantify lymphocyte stroma ratio](https://doi.org/10.1038/s41746-026-03207-y)

- **Authors:** Xiawei Li, Changming Lv, Haozhong Ma, Yongji Sun, Sien Hu, Tianyu Song, et al.
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation, vision-transformer
- **Abstract summary:** Pancreatic ductal adenocarcinoma (PDAC) exhibits profound tumor microenvironment heterogeneity, and conventional prognostic tools often fail to adequately quantify critical features like the lymphocyte-stroma ratio (LSR). Manual assessment of LSR is prone to variability and inefficiency, which limits its clinical ut...

### [Classification of Brain MRI Images with Vision Transformer: Improving Performance with New Layers and Parameter Optimization](https://doi.org/10.38016/jista.1779498)

- **Authors:** Rıfat AŞLIYAN, İclal Gör, Korhan Günel
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer
- **Abstract summary:** Recent advances in deep learning have revolutionized fields such as robotics, healthcare, and natural language processing. The Vision Transformer (ViT), which operates on self-attention block, has emerged as an alternative to Convolutional Neural Networks. In this study, an improved ViT architecture is proposed for...

### [Clothing Classification using Vision Transformer, Efficient-NET and CNN](https://doi.org/10.63503/acset.132)

- **Authors:** B. Suvarna, Kilaru Chaitanya, Appikatla Jaswanth
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer
- **Abstract summary:** Clothing classification is an important task in computer vision. It has key uses in fashion retail, inventory management, and recommendation systems. This paper presents a deep learning framework for clothing classification. It compares Vision Transformer (ViT), EfficientNet, and Convolutional Neural Networks (CNN)....

### [Constellation Dataset: Benchmarking High-Altitude Object Detection for an Urban Intersection](https://doi.org/10.1007/s11263-026-03029-1)

- **Authors:** Mehmet Kerem Türkcan, Chengbo Zang, Sanjeev Narasimhan, Gyung Hyun Je, Bo Yu, Mahshid Ghasemi, et al.
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, edge-deployment
- **Abstract summary:** Abstract As smart cities evolve, privacy-preserving edge processing at traffic intersections has become essential for real-time safety applications while reducing data transmission and centralized computation. High-altitude cameras with on-device inference provide an optimal solution that respects privacy while deli...

### [CRFTrans: A recursive vision transformer reformulating the mean-field inference in conditional random field for medical image segmentation](https://doi.org/10.1016/j.neunet.2026.109621)

- **Authors:** Zhendi Gong, Guoping Qiu, Xin Chen
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation, vision-transformer
- **Abstract summary:** Transformers have recently revolutionised medical image segmentation, achieving state-of-the-art (SOTA) performance in many clinical applications. However, prevailing architectures relying on cascaded Transformer layers (e.g., 12-layer Vision Transformer) face practical limitations, leading to high computational cos...

### [Deep Learning for Medical Imaging Analysis](https://doi.org/10.1002/9781394477623.ch1)

- **Authors:** Amrita, Khalil Haruna Aminu, M Muhammad, Ibrahim Nayaya Isah
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, visual-representation
- **Abstract summary:** Deep neural network mimics human brain neuronic structure, activity, and behavior. It is greatly influenced by the convoluted system and functional excitable cells in the human cerebrum. The neurons are combined together to analyze and process information. The core of deep learning (DL) is the artificial neural netw...

### [Deep learning-based detection and counting of wheat seeds: Comparative benchmarking of YOLO models](https://doi.org/10.56612/ijaaeb.v6i1.249)

- **Authors:** Faisal Shahzad, Hafiza Ayesha Arshad, Habib‐ur‐Rehman Athar, Israr Hanif, Iqra Shokat, Ayesha Maryam, et al.
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, efficient-vision, metrics
- **Abstract summary:** Automated wheat-seed detection and counting play important roles in high-throughput plant phenotyping, seed characterization, and agricultural research. Conventional manual counting is labor-intensive, time-consuming, and susceptible to human error when processing large numbers of seed samples. Recent advances in de...

### [DRerio LogAI: an open-source, GPU-free platform for automated tracking and behavioural analysis of adult zebrafish (Danio rerio)](https://doi.org/10.5281/zenodo.22783436)

- **Authors:** Marco Antônio Sant'Ana Camargos, Percília Cardoso Giaquinto
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** yolo, tracking
- **Abstract summary:** DRerio LogAI is an open-source desktop platform for automated tracking, closed-loop stimulation and behavioural analysis of adult zebrafish (Danio rerio). It combines YOLOv11 detection, BYTETracker multi-object tracking and Intel OpenVINO inference in an event-driven architecture, and runs GPU-free on integrated gra...

### [EC-YOLO: a real-time object detection framework for minute bone tumors in X-ray imaging](https://doi.org/10.1038/s41598-026-71477-3)

- **Authors:** Yu Zhang, Lizhu Zhang, Huiqiang Meng
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, backbone, efficient-vision
- **Abstract summary:** Accurate early diagnosis of bone tumors is crucial for optimizing clinical treatment protocols and improving patient prognosis. However, traditional manual evaluation of X-ray images is constrained by blurred lesion boundaries, high missed-detection rates for minute lesions, and insufficient adaptability to multi-sc...

### [EHDS-YOLO: a lightweight side-scan sonar object detection model for intelligent underwater inspection in marine ranching](https://doi.org/10.1007/s10499-026-02666-0)

- **Authors:** Zejin Liu, Yiming Zhang, Yanqiang Yang, Bang Wen, Yida Sha, Yuanshan Lin
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo
- **Abstract summary:** No abstract available.

### [FH-YOLO: a cross-stage stabilized framework for underwater benthic object detection](https://doi.org/10.1038/s41598-026-67759-5)

- **Authors:** Mengya Ma, Zhangwei Yu, Changan Ren
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo
- **Abstract summary:** Underwater object detection is challenged by light attenuation, scattering, and severe appearance degradation, which introduce instability across different stages of the detection pipeline. To address this issue, we propose FH-YOLO, a cross-stage stabilized framework designed to improve detection robustness under de...

### [Frequency-oriented adaptive real-time object detector for cluttered traffic scenes](https://doi.org/10.1038/s41467-026-76346-1)

- **Authors:** Ziqi Li, Tao Gao, Shutao Li, Ting Chen, Yisheng An, Yuanbo Wen, et al.
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, benchmark
- **Abstract summary:** Given the growing demand for traffic object detection in autonomous driving, achieving both efficiency and accuracy on in-vehicle platforms remains challenging. To address this issue, we propose a Frequency-Oriented Adaptive Detector for vehicle-mounted intelligent traffic object detection. It integrates high- and l...

### [From Pixels to Semantics: Edge AI for UAV-Based Critical Infrastructure Inspection](https://arxiv.org/abs/2609.18448)

- **Authors:** Reza Farahani, Naser Hossein Motlagh, Zoha Azimi, Christian Timmerer, Lorenzo Carnevale, Sasu Tarkoma, et al.
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, vision-language, edge-deployment, benchmark
- **Abstract summary:** Critical infrastructure assets such as bridges, tunnels, dams, and power line networks require timely and scalable inspection. While conventional manual inspection remains costly and hazardous, unmanned aerial vehicle (UAV)-based inspection has emerged as an efficient alternative for monitoring difficult-to-access s...

### [HBB2OBB: Horizontal to Oriented Bounding Box Conversion and Evaluation Tool](https://doi.org/10.5281/zenodo.22817652)

- **Authors:** Róbert Fónod
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, segmentation, benchmark
- **Abstract summary:** HBB2OBB converts horizontal (axis-aligned) bounding boxes (HBBs) into oriented (rotated) bounding boxes (OBBs) by using existing HBB annotations as prompts for segmentation models from the SAM (Segment Anything Model) family. It targets object detection tasks where objects appear at arbitrary orientations, such as a...

### [HBB2OBB: Horizontal to Oriented Bounding Box Conversion and Evaluation Tool](https://doi.org/10.5281/zenodo.22774765)

- **Authors:** Róbert Fónod
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, segmentation, benchmark
- **Abstract summary:** HBB2OBB converts horizontal (axis-aligned) bounding boxes (HBBs) into oriented (rotated) bounding boxes (OBBs) by using existing HBB annotations as prompts for segmentation models from the SAM (Segment Anything Model) family. It targets object detection tasks where objects appear at arbitrary orientations, such as a...

### [HemaViT: transformer-based deep learning for automated non-invasive anemia detection using conjunctival imaging](https://doi.org/10.1038/s41598-026-70965-w)

- **Authors:** Gourishetty Sindhusha, Rupesh K. Mishra, R. Jegadeesan
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer, backbone
- **Abstract summary:** Abstract Anemia is a common hematological disorder that requires timely diagnosis to reduce the risk of severe health complications, particularly in resource-limited healthcare settings. This study proposes HemaViT, a transformer-based deep learning framework for automated, non-invasive detection of anemia from conj...

### [Hybrid Deep Learning and Semantic Segmentation Framework for Colon Cancer Screening in Endoscopic Images](https://doi.org/10.3991/ijoe.v22i09.61119)

- **Authors:** E. N. Srivani, G. Seshikala
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation, visual-representation
- **Abstract summary:** The rising global population, lifestyle changes, and altered dietary habits have contributed to an increase in gastrointestinal diseases, including colon cancer, necessitating robust computer-aided diagnosis (CAD) systems for early detection and clinical decision-making. This paper proposes a deep semantic segmentat...

### [ImDUSTRY5-1.5K: A Public Benchmark Dataset for Industrial Object Detection in Real Production Environments](https://doi.org/10.5281/zenodo.22791206)

- **Authors:** K. R. Gurbanov, Latafat A. Gardashova, Cedric Bobenrieth, Nathalie Al Makdessi, Grégoire Chabrol, Samy Rima, et al.
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo
- **Abstract summary:** v3 — anonymised release (September 2026) Use this version. v1 and v2 contain the images before anonymization, and v1 also carries a superseded, incomplete annotation pass. What changed from v2: – Faces that appeared incidentally were irreversibly blurred in 33 images: a printed photograph of a young child pinned on...

### [ImDUSTRY5-1.5K: A Public Benchmark Dataset for Industrial Object Detection in Real Production Environments](https://doi.org/10.5281/zenodo.19045784)

- **Authors:** K. R. Gurbanov, Latafat Gardashova, Cedric Bobenrieth, Nathalie Al Makdessi, Grégoire Chabrol, Samy Rima, et al.
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo
- **Abstract summary:** v3 — anonymised release (September 2026) Use this version. v1 and v2 contain the images before anonymization, and v1 also carries a superseded, incomplete annotation pass. What changed from v2: – Faces that appeared incidentally were irreversibly blurred in 33 images: a printed photograph of a young child pinned on...

### [Improving individual cattle identification for livestock management systems using vision transformer embeddings and FAISS](https://doi.org/10.1038/s41598-026-71106-z)

- **Authors:** Shiekhah AL-Binali, Abrar Alamoudi, Abdulrahman Javaid
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer, visual-representation
- **Abstract summary:** Abstract The growing demand for cattle products has created an urgent need for large-scale farms equipped with automated management systems to ensure sustainable and efficient livestock farming practices. One critical challenge is the accurate identification of individual cattle, as errors in identification can nega...

### [IRA-YOLO: Inter-Class Relation Attention for PPE Detection in Industrial Scenes](https://doi.org/10.3390/s26185882)

- **Authors:** Ran Zhao, Haoran Duan, Xiaodong Liu, Nan Xu, Du Junlin, Pei Zhou
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, efficient-vision
- **Abstract summary:** Personal protective equipment (PPE) detection in industrial scenes is a joint classification-and-localization problem complicated by partial occlusion, scale variation, and background clutter. PPE categories also follow structured physical relations; for example, helmets are normally associated with heads and gloves...

### [Learning Adaptive Gated Fusion of Convolutional and Transformer Features for Generalizable Medical Image Classification](https://doi.org/10.21203/rs.3.rs-10799468/v1)

- **Authors:** Palvi Gupta, Himani Tyagi, Nidhi Gupta
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** visual-representation
- **Abstract summary:** No abstract available.

### [LIGHTWEIGHT REAL-TIME OBJECT DETECTION FOR ASSISTIVE VISION SYSTEMS USING YOLOV3-TINY AND OPENCV](https://doi.org/10.30574/wjaets.2026.20.3.0437)

- **Authors:** Idris Wakil Ibrahim, Aishatu Ibrahim Birma, Ahmed Umar, Ahmad Suleiman Bello
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, efficient-vision, edge-deployment
- **Abstract summary:** This paper presents the development of a lightweight, real-time object detection system specifically designed to assist visually impaired individuals in identifying surrounding objects, thereby improving navigation and personal safety. Utilizing the YOLOv3-tiny model integrated with OpenCV, the system captures and p...

### [LUMA-YOLO: A Lightweight and Illumination-Adaptive Object Detector for Low-Light Autonomous Driving](https://doi.org/10.1007/s13369-026-11660-w)

- **Authors:** Mingkun Feng, Chengjie Li, Zhixue Zhang
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: robotics or driving system where the vision contribution is not clearly the subject.
- **Tags:** object-detection, yolo
- **Abstract summary:** No abstract available.

### [Optimization-Oriented Hybrid Visual Perception Architecture for Safety-Aware Pedestrian and Animal Detection in Autonomous Urban Mobility](https://doi.org/10.3390/math14183368)

- **Authors:** Bayan Sheikh Omar, Önder Yakut
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, efficient-vision
- **Abstract summary:** Reliable visual perception is essential for autonomous urban mobility, where dense traffic, severe occlusion, low illumination, and heterogeneous object distributions challenge pedestrian and animal detection. This study proposes an optimization-oriented hybrid visual perception architecture that formulates visual p...

### [Privacy preserving federated learning for brain tumor segmentation using multi institutional MRI data](https://doi.org/10.1038/s41598-026-69042-z)

- **Authors:** B. Sanjeev, G. Deepika, Sreedhar Kollem, Gangaiah Perugu, Chennaiah Kate, K. Pushpa Rani
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** segmentation
- **Abstract summary:** Federated brain tumor segmentation using privacy-preserving deep learning has emerged as a promising approach to address the challenges of data scarcity, data heterogeneity, and patient privacy in multi-institutional medical imaging research. Conventional deep learning methods for brain tumor segmentation typically...

### [Relative Position Encoding-Enhanced Vision Transformer for Image-Level Defect Classification in Manufacturing Textured-Surface Inspection](https://doi.org/10.4108/eetsis.13596)

- **Authors:** Jiamin Liu, Yuhui Sun
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer
- **Abstract summary:** INTRODUCTION: In textile and textured-surface manufacturing, visual defects in woven fabrics, leather-like materials, tiles, and grid products directly influence product grading, downstream cutting, assembly reliability, after-sales repair, and supply-chain delivery stability. Weak defects embedded in repetitive tex...

### [Research Progress on Semantic Segmentation in Lumbar Degenerative Diseases.](https://pubmed.ncbi.nlm.nih.gov/42733950)

- **Authors:** Yu-Tong Ji, Chuan-Tao Wang, Hai-Liang Xia, Jiliang Zhai
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** segmentation
- **Abstract summary:** With the continuous advancement of medical imaging technologies,deep learning-based semantic segmentation has emerged as a key methodology in medical image analysis,achieving substantial progress in recent years.In particular,these techniques have demonstrated remarkable effectiveness in the automated identification...

### [Revisiting Inductive Bias in Vision Transformers: A Comparative Analysis of Transfer Learning and Training from Scratch on CIFAR-10](https://doi.org/10.63503/acset.115)

- **Authors:** Arya Putatunda, Pranshu Kumar, Praveen, Akash Karan
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: uses an existing detector or model without a clearly general method contribution.
- **Tags:** vision-transformer, benchmark
- **Abstract summary:** This paper is a comparative study of transfer learning and training from scratch on CIFAR-10, and of the relationship between inductive bias and vision transformers. Vision Transformers (ViT) are a relatively new form of potent alternative to Convolutional Neural Networks (CNNs) in the field of computer vision. Howe...

### [Road Rockfall Detection by Integrating Feature Engineering with YOLO and Cascade Decision Fusion](https://doi.org/10.3390/app16189209)

- **Authors:** Zhiqing Qin, Tao Niu, Caijin Lu, Yongsheng Dai, Xiantao Liu, Peng Peng, et al.
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo
- **Abstract summary:** In roadside surveillance imagery, shadows, vegetation, vehicles, exposed pavement, and water stains may exhibit local textures and morphological characteristics similar to those of rockfalls, causing a standalone You Only Look Once (YOLO) real-time object detector to generate frequent false-positive detections. To a...

### [SAGA-YOLO: A High-Accuracy Detector for SAR Aircraft in Complex Environments](https://doi.org/10.13164/re.2026.0442)

- **Authors:** Q. Guo, H. D. Zhao, W. J. Wang, W. K. Zhang
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** yolo, backbone, metrics
- **Abstract summary:** Synthetic Aperture Radar (SAR), utilizing its ability to actively transmit microwave signals, is widely used for military aircraft target reconnaissance and aviation safety monitoring. However, the complex background of ground-based aircraft targets, combined with the coherent imaging characteristics of SAR, results...

### [Smart Home Assistant Rover Robot with Voice Control and Object Detection](https://doi.org/10.5281/zenodo.22826182)

- **Authors:** shabesh S
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: uses an existing detector or model without a clearly general method contribution.
- **Tags:** object-detection, yolo, efficient-vision
- **Abstract summary:** This paper presents a Smart Home Assistant Rover Robot with Voice Control and Object Detection, designed to provide intelligent assistance and remote monitoring in a home environment. The system integrates a mobile robotic platform with wireless control, voice-based commands, and real-time object detection using com...

### [Smart Home Assistant Rover Robot with Voice Control and Object Detection](https://doi.org/10.5281/zenodo.22826183)

- **Authors:** shabesh S
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: uses an existing detector or model without a clearly general method contribution.
- **Tags:** object-detection, yolo, efficient-vision
- **Abstract summary:** This paper presents a Smart Home Assistant Rover Robot with Voice Control and Object Detection, designed to provide intelligent assistance and remote monitoring in a home environment. The system integrates a mobile robotic platform with wireless control, voice-based commands, and real-time object detection using com...

### [Traffic Signal Detection Algorithm Based on Dual-GAM Improved YOLO26 under Nighttime Conditions](https://doi.org/10.70267/cai.v3n4.8298)

- **Authors:** Chongtao Hu
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** object-detection, yolo, efficient-vision, metrics
- **Abstract summary:** The environmental recognition of autonomous vehicles depends much on real-time object detection, and identifying small traffic signals in low-light conditions during the night is a difficult problem. The size of traffic signals is small and vulnerable to the disruption caused by street lights and the lights of vehic...

### [Trajectory-guided detection and feature reuse for infrared object tracking based on YOLOv8–DeepSORT](https://doi.org/10.1117/12.3120555)

- **Authors:** Zhezhi Zou, Chuangang Xu, Yuexing Wang
- **Date:** 2026-09-19
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** yolo
- **Abstract summary:** Infrared object tracking is widely used in intelligent surveillance and autonomous perception systems due to its robustness under low-illumination and adverse environmental conditions. However, conventional YOLOv8–DeepSORT frameworks exhibit limited performance in infrared scenarios because of weak thermal contrast,...

### [Translating deep learning innovations into clinical medical imaging practice](https://doi.org/10.1007/s10462-026-11714-3)

- **Authors:** Alireza Norouziazad, Razieh Salahandish
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** visual-representation, vision-language
- **Abstract summary:** Deep learning (DL) has fundamentally transformed medical imaging, enabling unprecedented advancements in image quality, automated detection, and diagnostic precision. Despite these technical achievements, a significant translational gap persists between algorithmic development and robust clinical deployment. Unlike...

### [WT-STCA-ViT: Window-transform synergistic spectro-temporal channel attention Vision Transformer for robust bearing fault diagnosis](https://doi.org/10.1093/jcde/qwag081)

- **Authors:** Qian Gu, Chaoyang Weng, W. Huang, Baochun Lu
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** vision-transformer
- **Abstract summary:** Abstract Reliable bearing fault diagnosis under variable operating conditions and severe noise remains challenging because empirically selected time-frequency front ends may produce degraded representations, while generic attention mechanisms lack explicit sensitivity to fault-related spectral structures. To address...

### [YOLO-CBNet: A robust attention-enhanced detection framework for underwater fish recognition in aquaculture environments](https://doi.org/10.1371/journal.pone.0341525)

- **Authors:** Mahdi Hamzaoui, Leila Bousbia, Mohamed Ould-Elhassen Aoueileyine, Imen Filali, Ridha Bouallegue
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** yolo, backbone
- **Abstract summary:** The accurate identification of fish species remains a pivotal challenge in aquaculture, as it directly influences population management, health monitoring, and overall production efficiency. Yet, underwater environments often present difficult conditions such as reduced visibility, suspended particles, and uneven li...

### [YOLOv11-based real-time weed detection and autonomous precision spraying for hilly agriculture](https://doi.org/10.1038/s41598-026-71788-5)

- **Authors:** Ritika Mehra, Vikas Thapa, Rituraj Jain, Kamal Upreti, Govind Panwar, Simon Kasahun Bekele
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain without a clearly general method contribution.
- **Tags:** yolo
- **Abstract summary:** Weeds are a major hazard to agricultural production and ecology in the hilly areas of Uttarakhand, India. Traditional weed management methods use blanket spraying of herbicides, which is very expensive, polluting, and unrealistic in steep slope areas where machines cannot reach. This study addresses this issue by re...

### [A COMPUTER VISION APPROACH TO MILITARY OBJECT RECOGNITION](https://doi.org/10.68302/std2026.vol3.154)

- **Authors:** Krasimir Slavyanov
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** visual-representation
- **Abstract summary:** This research described is focused on computer vision tools implemented for detection of a particular military object (or many objects) in a observed scene, given a reference image(s) of the object(s). An algorithm for detecting a specific object based on finding point correspondences between the reference and the t...

### [Automated Diagnosis of Ear Disorders from Otoscopic Images using Hybrid Deep Learning and Multi-Stage Segmentation](https://doi.org/10.38094/jastt72771)

- **Authors:** Jagmeet Kaur, Puneet Kumar
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** backbone
- **Abstract summary:** Effective diagnosis of ear disorders with the help of otoscopic images can enhance the health care of ENT disorders, especially in resourcelimited areas. In this study, deep learning algorithms are applied to five common ear conditions, namely Acute Otitis Media, Chronic Otitis Media, Cerumen Impaction, Myringoscler...

### [Developments in Underwater Image Processing and Computer Vision for Intelligent Maritime Surveillance](https://doi.org/10.1201/9781003674870-6)

- **Authors:** Tarun Kumar Vashishth, Vikas Sharma, Sarika Jain, M. K. Sharma, Shahanawaj Ahamad, Sachin Tomar
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** visual-representation
- **Abstract summary:** The subaquatic environment presents a lot of challenges to image processing and computer vision through light degradation and absorption, light scattering, turbidity, and color distortion. These characteristics effectively eliminate visibility and fidelity in visual perceptual tasks that support the important featur...

### [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193v2)

- **Authors:** Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, et al.
- **Date:** 2023-04-14
- **Source:** arxiv
- **Relevance:** maybe (51/100)
- **Reason:** Review candidate: vision-related, but the methodological contribution to computer vision is not clear.
- **Tags:** vision-transformer
- **Abstract summary:** The recent breakthroughs in natural language processing for model pretraining on large quantities of data have opened the way for similar foundation models in computer vision. These models could greatly simplify the use of images in any system by producing all-purpose visual features, i.e., features that work across...

### [5G-Driven UAV Intelligence: Real-Time Tile Defect Detection in Mobile Networks](https://doi.org/10.1007/s11036-026-02529-1)

- **Authors:** Ang-Hsun Tsai, Yu-Ting Tai, Yu-Quan Lin
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** No abstract available.

### [A Hybrid 2D-3D Deep Learning Framework with Size-Aware Attention for Multi-Task Pulmonary Nodule Detection and Segmentation in CT Images](https://doi.org/10.1201/9781042037759-60)

- **Authors:** Shailendra Sikarwar, Mohd Farman Ali, Maad M. Mijwil, Ketki Patel
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Early detection of pulmonary nodules in CT scans is an important factor in improving the outcome of lung cancer patients. This research introduces an innovative dual deep learning system which combines two-dimensional (2D) and three-dimensional (3D) convolutional neural networks to detect and segment nodules simulta...

### [Detection and classification of thyroid diseases using ultrasound images through deep learning techniques](https://doi.org/10.11591/ijece.v16i5.pp2806-2818)

- **Authors:** Kamal Subedi, Akash Kumar Yadav, Lochan Paudel
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Thyroid diseases remain one of the significant public health issues around the world, with thyroid nodules estimated to be prevalent among approximately 30 to 50% of the adult population through ultrasound imaging screening processes. Determination of the nature of the thyroid nodules in a patient's body is vital fo...

### [Edge AI and IoT-Enabled Livestock Intrusion Detection and Automated Farm Protection Using YOLOv8s and MQTT-Enabled Event Notification](https://doi.org/10.21203/rs.3.rs-10780057/v1)

- **Authors:** CALEB OLUGBENGA OLADEPO, Akorede Bello Abeeb, Habeebullahi Opemipo Akinleye
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** No abstract available.

### [EHFRNT: A Boundary-Aware Hybrid Deep Learning Framework with Fuzzy Clustering and Transformer for Segmentation-Guided Skin Lesion Classification](https://doi.org/10.1007/s40010-026-01218-8)

- **Authors:** Christy Grace Manuvel Antony, Diwan Baskaran
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** No abstract available.

### [FDFormer: frequency difference-guided transformer for change detection in heterogeneous remote sensing images](https://doi.org/10.1038/s41598-026-71812-8)

- **Authors:** Fuping Huang, Jinwei Luo, Xinhui Cao, Jiaming Gong, Yanchun He, Xingping Liu
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Abstract Heterogeneous change detection (HCD) is a current hot topic in the field of remote sensing, as it can capture changed areas at the same geographical location using bi-temporal remote sensing images from different sensors. The primary challenge in HCD stems from the inherent domain shift between heterogeneou...

### [Journal of Communication and Information Systems](https://doi.org/10.14209/jcis)

- **Authors:** Unknown authors
- **Date:** 2026-09-16
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** With the increasing tendency of incorporating technology into environments and activities in everyday life, new methods are being proposed to better integrate devices and mankind.Networks designed for monitoring areas through video and image systems are being implemented in several applications.Recent studies have s...

### [Method for Improving the Accuracy of Brain Tumors Segmentation in MRI Images](https://doi.org/10.1007/978-3-032-37933-7_33)

- **Authors:** Ngan Khanh Dinh Nguyen, Sinh Van Nguyen, Thong Dinh Nguyen
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** No abstract available.

### [Near-Real-Time Wildfire Segmentation and Brightness Temperature Estimation from Geostationary Satellite Imagery Using Deep Learning](https://doi.org/10.20944/preprints202603.0342.v2)

- **Authors:** Ryota Yagi, Mukul Badhan, Majid Bavandpour, Kasra Shamsaei, Dani Or, G. Bebis, et al.
- **Date:** 2026-09-14
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** Monitoring the progression of wildfires in near-real-time is essential for active-fire situational awareness and emergency response management. Current satellite-based wildfire monitoring systems face a trade-off between temporal and spatial resolution. Geostationary satellites such as the Geostationary Operational...

### [Self-eXplainable AI for medical image analysis: A survey and new outlooks](https://doi.org/10.1016/j.inffus.2026.104791)

- **Authors:** Junlin Hou, Sicen Liu, Yequan Bie, Hongmei Wang, Andong Tan, Luyang Luo, et al.
- **Date:** 2026-09-15
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** No abstract available.

### [Title: AN EDGE-DEPLOYABLE LIGHTWEIGHT DEEP LEARNING DIAGNOSTIC FRAMEWORK FOR MULTI-CLASS LUNG CANCER CLASSIFICATION AND STAGING Abstract: Lung cancer is one of the main causes of cancer-related deaths worldwide and needs to be diagnosed in its early and clinical stages with the help of accurate and efficient diagnostic systems that can be used in clinical settings. In this study, a lightweight deep learning framework, called LiteSOS-Net, is proposed to classify lung cancer types and predict the TNM stage from CT images simultaneously. The proposed pipeline combines pre-processing, Attention U-Net segmentation, and a ShuffleNet-based classification backbone with the Osprey algorithm for efficient feature learning. The results of a substanti (Preprint)](https://doi.org/10.2196/preprints.112270)

- **Authors:** C Venkatesh Sr, Shashi Kant Gupta, Diaa Salama AbdElminaam, Deema Mohammed Alsekait, Abdallah Mohammad Abualkishik
- **Date:** 2026-09-17
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** efficient-vision, edge-deployment
- **Abstract summary:** BACKGROUND Lung cancer is one of the leading causes of cancer-related deaths worldwide. Early and accurate diagnosis, along with reliable clinical-stage assessment, is essential for effective treatment planning and improved patient outcomes. However, conventional diagnostic approaches can be time-consuming and may h...

### [UNETI Road Damage Segmentation Dataset](https://doi.org/10.5281/zenodo.22830366)

- **Authors:** Hang Anh Le, Viet Hoa Bui, Duc Co Tran, Manh Huan Do, Thi Hai Yen Nguyen, Thi Thuy Linh Tran, et al.
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** A dataset of Vietnamese road-surface images with instance-segmentation labels for three common damage types, intended for research on the detection, segmentation, and severity estimation of road damage using deep learning. All images were collected by the research team on several roads in northern Vietnam (Hanoi, Ni...

### [UNETI Road Damage Segmentation Dataset](https://doi.org/10.5281/zenodo.22830365)

- **Authors:** Hang Anh Le, Viet Hoa Bui, Duc Co Tran, Manh Huan Do, Thi Hai Yen Nguyen, Thi Thuy Linh Tran, et al.
- **Date:** 2026-09-18
- **Source:** openalex
- **Relevance:** maybe (45/100)
- **Reason:** Review candidate: adjacent to computer vision, but no vision method is clearly studied.
- **Tags:** vision-adjacent
- **Abstract summary:** A dataset of Vietnamese road-surface images with instance-segmentation labels for three common damage types, intended for research on the detection, segmentation, and severity estimation of road damage using deep learning. All images were collected by the research team on several roads in northern Vietnam (Hanoi, Ni...
