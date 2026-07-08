# Paper Scout Live Smoke Report - 2026-07-08

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 776
- **Candidates fetched:** 628
- **Unique papers:** 412
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Success
- Queries attempted: 26
- Raw records: 626
- Converted candidates: 626
- Sample title: Checklist Rubric-Driven Iterative Control for Mitigating Context Drift in Deep Research Agents
- Sample source ID: W7167079006
- Sample URL: https://doi.org/10.14801/jkiit.2026.24.6.1
- Sample published date: 2026-06-30
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 7
- Raw records: 150
- Converted candidates: 2
- Sample title: Clarus: Coordinating Autonomous Research Agents toward Web-Scale Scientific Collaboration
- Sample source ID: e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample URL: https://www.semanticscholar.org/paper/e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample published date: 2026-06-29
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 46
- maybe: 41
- irrelevant: 325

## Top Relevant Or Maybe Papers

- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.29981
- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.29981
- **One Reflection Is Not Enough: Self-Correcting Autonomous Research via Multi-Hypothesis Failure Attribution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.48550/arxiv.2606.31478
- **One Reflection Is Not Enough: Self-Correcting Autonomous Research via Multi-Hypothesis Failure Attribution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2606.31478
- **Socratic agents for autonomous scientific discovery in high-dimensional physical systems** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.26722
- **Socratic agents for autonomous scientific discovery in high-dimensional physical systems** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.26722
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.31273
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.31273

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- semantic_scholar (HTTP/API error) for `AI scientist`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- doi:10.14801/jkiit.2026.24.6.1: openalex:W7167079006, openalex:W7167079006
- doi:10.21203/rs.3.rs-9701113/v1: openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095
- doi:10.5281/zenodo.20822051: openalex:W7165792392, openalex:W7165792392, openalex:W7165792392
- openalex:W7166901874: openalex:W7166901874, openalex:W7166901874, openalex:W7166901874, openalex:W7166901874
- doi:10.48550/arxiv.2606.29746: openalex:W7166706750, openalex:W7166706750, openalex:W7166706750
- doi:10.1098/rsos.251988: openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127
- doi:10.1038/s42256-026-01266-0: openalex:W7167041027, openalex:W7167041027
- doi:10.1111/1462-2920.70353: openalex:W7166115436, openalex:W7166115436, openalex:W7166115436, openalex:W7166115436, openalex:W7166115436
- doi:10.64898/2026.06.24.734302: openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207
- doi:10.3390/buildings16132569: openalex:W7166510832, openalex:W7166510832, openalex:W7166510832, openalex:W7166510832, openalex:W7166510832, openalex:W7166510832
- doi:10.26434/chemrxiv.15005137/v1: openalex:W7165775338, openalex:W7165775338
- doi:10.1016/j.neucom.2026.134438: openalex:W7167341239, openalex:W7167341239
- doi:10.1007/s10791-026-10231-9: openalex:W7167417706, openalex:W7167417706, openalex:W7167417706
- openalex:W7167155010: openalex:W7167155010, openalex:W7167155010
- doi:10.5281/zenodo.21140610: openalex:W7167075364, openalex:W7167075364
- doi:10.5281/zenodo.21140609: openalex:W7167092641, openalex:W7167092641
- doi:10.1038/s44386-026-00054-5: openalex:W4391940875, openalex:W4391940875, openalex:W4391940875, openalex:W4391940875, openalex:W4391940875
- openalex:W7166900994: openalex:W7166900994, openalex:W7166900994, openalex:W7166900994
- openalex:W7166399911: openalex:W7166399911, openalex:W7166399911, openalex:W7166399911
- doi:10.5281/zenodo.21169943: openalex:W7167259055, openalex:W7167259055, openalex:W7167259055
- doi:10.5281/zenodo.21185277: openalex:W7167351490, openalex:W7167351490, openalex:W7167351490
- openalex:W7167446164: openalex:W7167446164, openalex:W7167446164, openalex:W7167446164, openalex:W7167446164
- doi:10.1186/s40712-026-00517-7: openalex:W7167076631, openalex:W7167076631
- openalex:W7166902620: openalex:W7166902620, openalex:W7166902620
- doi:10.1527/tjsai.41-4_c-p102: openalex:W7166873740, openalex:W7166873740
- arxiv:2606.30246: semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1, semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- doi:10.48550/arxiv.2606.30246: openalex:W7166673172, openalex:W7166673172, openalex:W7166673172, openalex:W7166673172
- openalex:W7166901356: openalex:W7166901356, openalex:W7166901356, openalex:W7166901356
- doi:10.1145/3822503: openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992
- doi:10.17605/osf.io/ugkv5: openalex:W7167026573, openalex:W7167026573, openalex:W7167026573, openalex:W7167026573, openalex:W7167026573
- doi:10.1007/s11633-026-1667-4: openalex:W4404990867, openalex:W4404990867
- doi:10.55041/isjem08120: openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914
- doi:10.5281/zenodo.21222350: openalex:W7167479016, openalex:W7167479016, openalex:W7167479016
- doi:10.26192/q4qyq: openalex:W2810130361, openalex:W2810130361, openalex:W2810130361, openalex:W2810130361
- doi:10.4018/979-8-2600-2601-4.ch004: openalex:W7165782897, openalex:W7165782897
- doi:10.5281/zenodo.20826452: openalex:W7165735928, openalex:W7165735928, openalex:W7165735928
- doi:10.5281/zenodo.20826453: openalex:W7165744339, openalex:W7165744339, openalex:W7165744339
- openalex:W7167379873: openalex:W7167379873, openalex:W7167379873
- doi:10.48550/arxiv.2607.02329: openalex:W7167276670, openalex:W7167276670
- doi:10.1016/j.aei.2026.104988: openalex:W7167512922, openalex:W7167512922, openalex:W7167512922
- doi:10.1080/23311975.2026.2692205: openalex:W7165951177, openalex:W7165951177
- doi:10.48550/arxiv.2606.31478: openalex:W7166808931, openalex:W7166808931
- openalex:W7167155031: openalex:W7167155031, openalex:W7167155031
- doi:10.35784/acs_9272: openalex:W7166850898, openalex:W7166850898
- doi:10.5281/zenodo.20822771: openalex:W7165797887, openalex:W7165797887
- doi:10.5281/zenodo.20822770: openalex:W7165755467, openalex:W7165755467
- doi:10.1145/3815572.3815744: openalex:W7166153882, openalex:W7166153882, openalex:W7166153882, openalex:W7166153882, openalex:W7166153882
- doi:10.5281/zenodo.20839771: openalex:W7165910312, openalex:W7165910312, openalex:W7165910312
- doi:10.5281/zenodo.20839770: openalex:W7165842336, openalex:W7165842336, openalex:W7165842336
- doi:10.5281/zenodo.21040068: openalex:W7166593969, openalex:W7166593969, openalex:W7166593969
- doi:10.5281/zenodo.21040067: openalex:W7166534811, openalex:W7166534811, openalex:W7166534811, openalex:W7166534811
- openalex:W7166900081: openalex:W7166900081, openalex:W7166900081
- doi:10.48550/arxiv.2606.30111: openalex:W7166698998, openalex:W7166698998
- doi:10.1007/s10115-026-02806-1: openalex:W4406880911, openalex:W4406880911, openalex:W4406880911, openalex:W4406880911
- openalex:W7167154310: openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310
- openalex:W7166901100: openalex:W7166901100, openalex:W7166901100, openalex:W7166901100
- openalex:W7166900713: openalex:W7166900713, openalex:W7166900713, openalex:W7166900713, openalex:W7166900713
- doi:10.48550/arxiv.2606.31229: openalex:W7166805631, openalex:W7166805631, openalex:W7166805631, openalex:W7166805631
- doi:10.5281/zenodo.18275969: openalex:W7124536980, openalex:W7124536980
- doi:10.5281/zenodo.21117754: openalex:W7166881449, openalex:W7166881449, openalex:W7166881449
- doi:10.5281/zenodo.18746522: openalex:W7131123480, openalex:W7131123480
- doi:10.5281/zenodo.21080396: openalex:W7166650293, openalex:W7166650293, openalex:W7166650293
- doi:10.5281/zenodo.21080395: openalex:W7166665405, openalex:W7166665405, openalex:W7166665405
- openalex:W7166399708: openalex:W7166399708, openalex:W7166399708
- doi:10.23093/fsi.2026.59.2.167: openalex:W7167019350, openalex:W7167019350
- doi:10.6082/324p4-ymb14: openalex:W7165772541, openalex:W7165772541
- doi:10.6082/gep96-ycs43: openalex:W7165788481, openalex:W7165788481
- openalex:W7167380583: openalex:W7167380583, openalex:W7167380583
- doi:10.48550/arxiv.2607.01639: openalex:W7167205772, openalex:W7167205772
- openalex:W7167154699: openalex:W7167154699, openalex:W7167154699
- doi:10.48550/arxiv.2606.31273: openalex:W7166831674, openalex:W7166831674
- openalex:W7166399684: openalex:W7166399684, openalex:W7166399684
- openalex:W7167154245: openalex:W7167154245, openalex:W7167154245, openalex:W7167154245
- doi:10.1038/s43016-026-01380-7: openalex:W7167273491, openalex:W7167273491
- openalex:W7166399511: openalex:W7166399511, openalex:W7166399511, openalex:W7166399511
- doi:10.48550/arxiv.2606.26722: openalex:W7166151766, openalex:W7166151766
- openalex:W7166400267: openalex:W7166400267, openalex:W7166400267
- doi:10.1007/s10489-026-07340-9: openalex:W7166833661, openalex:W7166833661
- doi:10.65140/gimn202601.19: openalex:W7165758059, openalex:W7165758059
- doi:10.26192/q4qyy: openalex:W2811413344, openalex:W2811413344
- doi:10.21203/rs.3.rs-9819774/v1: openalex:W7166694999, openalex:W7166694999, openalex:W7166694999, openalex:W7166694999, openalex:W7166694999
- openalex:W7167380899: openalex:W7167380899, openalex:W7167380899
- doi:10.5194/epsc2026-276: openalex:W7167024696, openalex:W7167024696, openalex:W7167024696
- doi:10.26434/chemrxiv.15005228/v1: openalex:W7166062973, openalex:W7166062973, openalex:W7166062973, openalex:W7166062973
- doi:10.1016/j.trc.2026.105818: openalex:W4416434619, openalex:W4416434619
- doi:10.3389/fcpxs.2026.1800335: openalex:W7167408981, openalex:W7167408981
- openalex:W7166901650: openalex:W7166901650, openalex:W7166901650
- doi:10.48550/arxiv.2606.29116: openalex:W7166673129, openalex:W7166673129
- doi:10.31462/jcemi.2026.721: openalex:W7166811136, openalex:W7166811136
- doi:10.1145/3750555.3811883: openalex:W7165730392, openalex:W7165730392
- doi:10.1145/3805760.3814889: openalex:W7160617091, openalex:W7160617091
- doi:10.3233/shti260874: openalex:W7167079121, openalex:W7167079121
- openalex:W7167380417: openalex:W7167380417, openalex:W7167380417
- doi:10.5281/zenodo.20848833: openalex:W7165849592, openalex:W7165849592
- doi:10.5281/zenodo.20848834: openalex:W7165859569, openalex:W7165859569
- doi:10.17605/osf.io/7dvcp: openalex:W7166299976, openalex:W7166299976
- openalex:W7167379880: openalex:W7167379880, openalex:W7167379880
- openalex:W7167379885: openalex:W7167379885, openalex:W7167379885
- openalex:W7167290022: openalex:W7167290022, openalex:W7167290022
- doi:10.21981/gfzt-hb86: openalex:W7167361824, openalex:W7167361824
- doi:10.21981/ke2k-gd71: openalex:W7167019083, openalex:W7167019083
- doi:10.21981/axzb-pv51: openalex:W7165867525, openalex:W7165867525
- doi:10.21981/rz3e-kb86: openalex:W7167230525, openalex:W7167230525
- openalex:W7165706373: openalex:W7165706373, openalex:W7165706373
- doi:10.1016/j.inffus.2026.104579: openalex:W4414875577, openalex:W4414875577
