# Paper Scout Live Smoke Report - 2026-07-11

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 725
- **Candidates fetched:** 627
- **Unique papers:** 384
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
- Raw records: 625
- Converted candidates: 625
- Sample title: FORGE: Research-Trajectory Hijacking Attacks on Deep Research Agents
- Sample source ID: W7167747000
- Sample URL: https://arxiv.org/abs/2607.04718
- Sample published date: 2026-07-06
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 5
- Raw records: 100
- Converted candidates: 2
- Sample title: Clarus: Coordinating Autonomous Research Agents toward Web-Scale Scientific Collaboration
- Sample source ID: e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample URL: https://www.semanticscholar.org/paper/e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample published date: 2026-06-29
- Abstract: yes
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 49
- maybe: 35
- irrelevant: 300

## Top Relevant Or Maybe Papers

- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.29981
- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.29981
- **One Reflection Is Not Enough: Self-Correcting Autonomous Research via Multi-Hypothesis Failure Attribution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://arxiv.org/abs/2606.31478
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.31273
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.31273
- **Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. I. Uncertainty Quantification, ML on Therapeutic Data Commons, and Agent-Based Modeling** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.64898/2026.06.24.734302
- **Quantum Category-Theoretic Inference and Sheaf Cohomology for Automated Scientific Discovery in Systems Biology** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21193355
- **Quantum Category-Theoretic Inference and Sheaf Cohomology for Automated Scientific Discovery in Systems Biology** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21193204

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- semantic_scholar (HTTP/API error) for `automated research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- openalex:W7167747000: openalex:W7167747000, openalex:W7167747000, openalex:W7167747000, openalex:W7167747000, openalex:W7167747000, openalex:W7167747000
- doi:10.48550/arxiv.2607.04718: openalex:W7167627630, openalex:W7167627630, openalex:W7167627630, openalex:W7167627630
- doi:10.14801/jkiit.2026.24.6.1: openalex:W7167079006, openalex:W7167079006
- doi:10.21203/rs.3.rs-9701113/v1: openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095
- openalex:W7166901874: openalex:W7166901874, openalex:W7166901874, openalex:W7166901874, openalex:W7166901874
- doi:10.48550/arxiv.2606.29746: openalex:W7166706750, openalex:W7166706750, openalex:W7166706750
- openalex:W7167748531: openalex:W7167748531, openalex:W7167748531, openalex:W7167748531, openalex:W7167748531
- doi:10.48550/arxiv.2607.02927: openalex:W7167594425, openalex:W7167594425, openalex:W7167594425
- doi:10.1098/rsos.251988: openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127
- doi:10.1016/j.patter.2026.101610: openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464
- doi:10.1038/s42256-026-01266-0: openalex:W7167041027, openalex:W7167041027
- doi:10.1038/s41524-026-02205-8: openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561
- doi:10.64898/2026.06.24.734302: openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207
- doi:10.3390/buildings16132569: openalex:W7166510832, openalex:W7166510832, openalex:W7166510832, openalex:W7166510832
- doi:10.17869/enu.277667: openalex:W1939736137, openalex:W1939736137, openalex:W1939736137, openalex:W1939736137, openalex:W1939736137, openalex:W1939736137, openalex:W1939736137
- doi:10.48550/arxiv.2607.06489: openalex:W7167667392, openalex:W7167667392
- openalex:W7167855656: openalex:W7167855656, openalex:W7167855656
- doi:10.1016/j.neucom.2026.134438: openalex:W7167341239, openalex:W7167341239
- doi:10.4018/979-8-2600-0116-5.ch009: openalex:W7167849768, openalex:W7167849768
- doi:10.1007/s10791-026-10231-9: openalex:W7167417706, openalex:W7167417706, openalex:W7167417706
- openalex:W7167155010: openalex:W7167155010, openalex:W7167155010
- openalex:W7167748459: openalex:W7167748459, openalex:W7167748459, openalex:W7167748459, openalex:W7167748459, openalex:W7167748459
- doi:10.5281/zenodo.21140609: openalex:W7167092641, openalex:W7167092641
- doi:10.5281/zenodo.21140610: openalex:W7167075364, openalex:W7167075364
- openalex:W7166900994: openalex:W7166900994, openalex:W7166900994, openalex:W7166900994
- arxiv:2606.30246: semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1, semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- doi:10.48550/arxiv.2606.30246: openalex:W7166673172, openalex:W7166673172, openalex:W7166673172
- openalex:W7166901356: openalex:W7166901356, openalex:W7166901356, openalex:W7166901356
- openalex:W7167446164: openalex:W7167446164, openalex:W7167446164
- doi:10.1126/science.adz4351: openalex:W7167845123, openalex:W7167845123, openalex:W7167845123, openalex:W7167845123, openalex:W7167845123
- doi:10.4018/979-8-3373-7665-3.ch001: openalex:W7167627441, openalex:W7167627441, openalex:W7167627441, openalex:W7167627441
- doi:10.17605/osf.io/ugkv5: openalex:W7167026573, openalex:W7167026573, openalex:W7167026573, openalex:W7167026573, openalex:W7167026573
- doi:10.5281/zenodo.21222324: openalex:W7167526061, openalex:W7167526061, openalex:W7167526061, openalex:W7167526061, openalex:W7167526061
- doi:10.1007/s11633-026-1667-4: openalex:W4404990867, openalex:W4404990867
- doi:10.1177/25152459261454231: openalex:W7167794015, openalex:W7167794015
- doi:10.55041/isjem08120: openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914
- doi:10.5281/zenodo.21222350: openalex:W7167479016, openalex:W7167479016, openalex:W7167479016
- doi:10.26192/q4qyq: openalex:W2810130361, openalex:W2810130361, openalex:W2810130361, openalex:W2810130361
- doi:10.1145/3828752: openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589
- openalex:W7167379873: openalex:W7167379873, openalex:W7167379873
- doi:10.48550/arxiv.2607.02329: openalex:W7167276670, openalex:W7167276670
- doi:10.1016/j.aei.2026.104988: openalex:W7167512922, openalex:W7167512922, openalex:W7167512922
- doi:10.5281/zenodo.21279239: openalex:W7167826843, openalex:W7167826843
- doi:10.5281/zenodo.21279240: openalex:W7167814960, openalex:W7167814960
- doi:10.21203/rs.3.rs-10220882/v1: openalex:W7167719533, openalex:W7167719533, openalex:W7167719533, openalex:W7167719533, openalex:W7167719533
- openalex:W7167747186: openalex:W7167747186, openalex:W7167747186
- openalex:W7167155031: openalex:W7167155031, openalex:W7167155031
- openalex:W7166900081: openalex:W7166900081, openalex:W7166900081
- doi:10.48550/arxiv.2606.30111: openalex:W7166698998, openalex:W7166698998
- doi:10.5281/zenodo.21040067: openalex:W7166534811, openalex:W7166534811, openalex:W7166534811, openalex:W7166534811
- doi:10.5281/zenodo.21040068: openalex:W7166593969, openalex:W7166593969, openalex:W7166593969
- doi:10.1007/s10115-026-02806-1: openalex:W4406880911, openalex:W4406880911, openalex:W4406880911, openalex:W4406880911, openalex:W4406880911
- openalex:W7167154310: openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310
- doi:10.48550/arxiv.2606.31229: openalex:W7166805631, openalex:W7166805631, openalex:W7166805631, openalex:W7166805631
- doi:10.5281/zenodo.18275969: openalex:W7124536980, openalex:W7124536980
- doi:10.5281/zenodo.21117754: openalex:W7166881449, openalex:W7166881449, openalex:W7166881449
- doi:10.5281/zenodo.18746522: openalex:W7131123480, openalex:W7131123480
- doi:10.1038/s44386-026-00054-5: openalex:W4391940875, openalex:W4391940875, openalex:W4391940875
- openalex:W7167855827: openalex:W7167855827, openalex:W7167855827
- doi:10.48550/arxiv.2607.05435: openalex:W7167692845, openalex:W7167692845
- doi:10.5281/zenodo.21080395: openalex:W7166665405, openalex:W7166665405, openalex:W7166665405
- doi:10.5281/zenodo.21080396: openalex:W7166650293, openalex:W7166650293, openalex:W7166650293
- doi:10.1080/0142159x.2026.2681971: openalex:W7167577748, openalex:W7167577748
- doi:10.6082/324p4-ymb14: openalex:W7165772541, openalex:W7165772541
- doi:10.6082/gep96-ycs43: openalex:W7165788481, openalex:W7165788481
- doi:10.1093/bioinformatics/btag227: openalex:W7167635513, openalex:W7167635513
- openalex:W7167380583: openalex:W7167380583, openalex:W7167380583
- doi:10.48550/arxiv.2607.01639: openalex:W7167205772, openalex:W7167205772
- openalex:W7167154699: openalex:W7167154699, openalex:W7167154699
- openalex:W7167747562: openalex:W7167747562, openalex:W7167747562
- doi:10.48550/arxiv.2606.31273: openalex:W7166831674, openalex:W7166831674
- doi:10.48550/arxiv.2607.04293: openalex:W7167618004, openalex:W7167618004
- openalex:W7167154245: openalex:W7167154245, openalex:W7167154245
- doi:10.1038/s43016-026-01380-7: openalex:W7167273491, openalex:W7167273491
- doi:10.48550/arxiv.2607.03863: openalex:W7167612321, openalex:W7167612321, openalex:W7167612321
- openalex:W7167855751: openalex:W7167855751, openalex:W7167855751, openalex:W7167855751
- doi:10.1098/rsif.2026.0043: openalex:W7167603384, openalex:W7167603384
- doi:10.48550/arxiv.2607.05682: openalex:W7167668015, openalex:W7167668015, openalex:W7167668015
- openalex:W7167854942: openalex:W7167854942, openalex:W7167854942, openalex:W7167854942
- doi:10.1007/s10489-026-07340-9: openalex:W7166833661, openalex:W7166833661
- doi:10.3390/medicina62071243: openalex:W7166470482, openalex:W7166470482
- doi:10.26192/q4qyy: openalex:W2811413344, openalex:W2811413344
- doi:10.21203/rs.3.rs-9819774/v1: openalex:W7166694999, openalex:W7166694999, openalex:W7166694999, openalex:W7166694999, openalex:W7166694999
- openalex:W7167380899: openalex:W7167380899, openalex:W7167380899
- doi:10.5194/epsc2026-276: openalex:W7167024696, openalex:W7167024696, openalex:W7167024696
- openalex:W7166901650: openalex:W7166901650, openalex:W7166901650
- doi:10.48550/arxiv.2606.29116: openalex:W7166673129, openalex:W7166673129
- doi:10.31462/jcemi.2026.721: openalex:W7166811136, openalex:W7166811136
- openalex:W7167747256: openalex:W7167747256, openalex:W7167747256
- doi:10.1145/3805760.3814889: openalex:W7160617091, openalex:W7160617091
- openalex:W7167154092: openalex:W7167154092, openalex:W7167154092
- doi:10.3233/shti260874: openalex:W7167079121, openalex:W7167079121
- doi:10.1038/s41746-026-02978-8: openalex:W7167574952, openalex:W7167574952
- doi:10.1038/s41377-026-02385-4: openalex:W7166578122, openalex:W7166578122
- openalex:W7167747490: openalex:W7167747490, openalex:W7167747490
- openalex:W7167155179: openalex:W7167155179, openalex:W7167155179
- openalex:W7167379880: openalex:W7167379880, openalex:W7167379880
- openalex:W7167379885: openalex:W7167379885, openalex:W7167379885
- openalex:W7167290022: openalex:W7167290022, openalex:W7167290022
- doi:10.21981/ke2k-gd71: openalex:W7167019083, openalex:W7167019083
- doi:10.21981/gfzt-hb86: openalex:W7167361824, openalex:W7167361824
- doi:10.21981/rz3e-kb86: openalex:W7167230525, openalex:W7167230525
- doi:10.1016/j.inffus.2026.104579: openalex:W4414875577, openalex:W4414875577
