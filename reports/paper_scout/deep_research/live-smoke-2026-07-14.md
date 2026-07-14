# Paper Scout Live Smoke Report - 2026-07-14

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 674
- **Candidates fetched:** 624
- **Unique papers:** 387
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
- Raw records: 624
- Converted candidates: 624
- Sample title: DeepResearch-9K: A Challenging Benchmark Dataset of Deep-Research Agent
- Sample source ID: W7165806706
- Sample URL: https://doi.org/10.1145/3805712.3808597
- Sample published date: 2026-07-10
- Abstract: yes

### semantic_scholar

- Status: Failed
- Queries attempted: 3
- Raw records: 50
- Converted candidates: 0
- Error: HTTP/API error: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.


## Decisions

- relevant: 38
- maybe: 33
- irrelevant: 316

## Top Relevant Or Maybe Papers

- **Which ‘AI scientist’ suits your lab? A guide for the perplexed** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.1038/d41586-026-02091-6
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.31273
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.31273
- **Quantum Category-Theoretic Inference and Sheaf Cohomology for Automated Scientific Discovery in Systems Biology** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21193355
- **Quantum Category-Theoretic Inference and Sheaf Cohomology for Automated Scientific Discovery in Systems Biology** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21193204
- **Quantum Category-Theoretic Inference and Sheaf Cohomology for Automated Scientific Discovery in Systems Biology** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21193131
- **Quantum Category-Theoretic Inference and Sheaf Cohomology for Automated Scientific Discovery in Systems Biology** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21184712
- **Quantum Category-Theoretic Inference and Sheaf Cohomology for Automated Scientific Discovery in Systems Biology** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.21184467

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- semantic_scholar (HTTP/API error) for `autonomous research agent`: Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources.

## Deduplication Examples

- doi:10.1145/3805712.3808597: openalex:W7165806706, openalex:W7165806706, openalex:W7165806706
- openalex:W7167747000: openalex:W7167747000, openalex:W7167747000, openalex:W7167747000, openalex:W7167747000, openalex:W7167747000, openalex:W7167747000
- doi:10.48550/arxiv.2607.04718: openalex:W7167627630, openalex:W7167627630, openalex:W7167627630, openalex:W7167627630
- doi:10.14801/jkiit.2026.24.6.1: openalex:W7167079006, openalex:W7167079006
- doi:10.21203/rs.3.rs-9701113/v1: openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095, openalex:W4391556095
- openalex:W7167748531: openalex:W7167748531, openalex:W7167748531, openalex:W7167748531, openalex:W7167748531
- doi:10.48550/arxiv.2607.02927: openalex:W7167594425, openalex:W7167594425, openalex:W7167594425
- doi:10.1098/rsos.251988: openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127
- doi:10.1016/j.patter.2026.101610: openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464, openalex:W4415286464
- doi:10.1038/s42256-026-01266-0: openalex:W7167041027, openalex:W7167041027
- doi:10.1038/s41524-026-02205-8: openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561, openalex:W7167678561
- doi:10.1371/journal.pone.0331638: openalex:W4413477882, openalex:W4413477882
- doi:10.1145/3805712.3809617: openalex:W7167895515, openalex:W7167895515
- doi:10.17869/enu.277667: openalex:W1939736137, openalex:W1939736137, openalex:W1939736137, openalex:W1939736137, openalex:W1939736137, openalex:W1939736137, openalex:W1939736137
- openalex:W7168054711: openalex:W7168054711, openalex:W7168054711, openalex:W7168054711
- openalex:W7168054992: openalex:W7168054992, openalex:W7168054992, openalex:W7168054992, openalex:W7168054992
- doi:10.48550/arxiv.2607.08662: openalex:W7167890363, openalex:W7167890363
- doi:10.48550/arxiv.2607.07820: openalex:W7167890036, openalex:W7167890036, openalex:W7167890036
- openalex:W7167855656: openalex:W7167855656, openalex:W7167855656
- doi:10.1080/02691728.2026.2682149: openalex:W7167513634, openalex:W7167513634, openalex:W7167513634
- doi:10.48550/arxiv.2607.06489: openalex:W7167667392, openalex:W7167667392
- doi:10.1016/j.neucom.2026.134438: openalex:W7167341239, openalex:W7167341239
- doi:10.4018/979-8-2600-0116-5.ch009: openalex:W7167849768, openalex:W7167849768
- doi:10.1145/3805712.3808374: openalex:W7167918833, openalex:W7167918833, openalex:W7167918833
- doi:10.1007/s10791-026-10336-1: openalex:W7167833660, openalex:W7167833660, openalex:W7167833660, openalex:W7167833660
- doi:10.1126/science.adz4351: openalex:W7167845123, openalex:W7167845123, openalex:W7167845123, openalex:W7167845123, openalex:W7167845123
- openalex:W7167446164: openalex:W7167446164, openalex:W7167446164
- doi:10.4018/979-8-3373-7665-3.ch001: openalex:W7167627441, openalex:W7167627441, openalex:W7167627441, openalex:W7167627441
- doi:10.17605/osf.io/ugkv5: openalex:W7167026573, openalex:W7167026573, openalex:W7167026573, openalex:W7167026573, openalex:W7167026573
- doi:10.5281/zenodo.21222324: openalex:W7167526061, openalex:W7167526061, openalex:W7167526061, openalex:W7167526061, openalex:W7167526061
- doi:10.5281/zenodo.21313591: openalex:W7168046980, openalex:W7168046980, openalex:W7168046980, openalex:W7168046980
- doi:10.5281/zenodo.21313592: openalex:W7168049151, openalex:W7168049151, openalex:W7168049151, openalex:W7168049151
- doi:10.1007/s11633-026-1667-4: openalex:W4404990867, openalex:W4404990867
- doi:10.1016/j.trc.2026.105852: openalex:W4403007104, openalex:W4403007104, openalex:W4403007104
- doi:10.1177/25152459261454231: openalex:W7167794015, openalex:W7167794015
- doi:10.55041/isjem08120: openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914, openalex:W7167360914
- doi:10.5281/zenodo.21222350: openalex:W7167479016, openalex:W7167479016, openalex:W7167479016
- doi:10.26192/q4qyq: openalex:W2810130361, openalex:W2810130361, openalex:W2810130361, openalex:W2810130361
- doi:10.1145/3828752: openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589, openalex:W4409048589
- openalex:W7167379873: openalex:W7167379873, openalex:W7167379873
- doi:10.48550/arxiv.2607.02329: openalex:W7167276670, openalex:W7167276670
- doi:10.1016/j.aei.2026.104988: openalex:W7167512922, openalex:W7167512922, openalex:W7167512922
- doi:10.5281/zenodo.21279240: openalex:W7167814960, openalex:W7167814960
- doi:10.65222/viral.2026.7.40.60: openalex:W7167934967, openalex:W7167934967, openalex:W7167934967
- doi:10.5281/zenodo.21306302: openalex:W7168038634, openalex:W7168038634
- doi:10.5281/zenodo.21318372: openalex:W7168082644, openalex:W7168082644
- doi:10.5281/zenodo.21318373: openalex:W7168099647, openalex:W7168099647
- doi:10.1007/s10115-026-02806-1: openalex:W4406880911, openalex:W4406880911, openalex:W4406880911, openalex:W4406880911, openalex:W4406880911
- openalex:W7167154310: openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310, openalex:W7167154310
- doi:10.48550/arxiv.2606.31229: openalex:W7166805631, openalex:W7166805631, openalex:W7166805631
- doi:10.5281/zenodo.18275969: openalex:W7124536980, openalex:W7124536980
- doi:10.5281/zenodo.21117754: openalex:W7166881449, openalex:W7166881449, openalex:W7166881449
- doi:10.5281/zenodo.18746522: openalex:W7131123480, openalex:W7131123480
- doi:10.1007/s00146-026-03174-8: openalex:W4410117633, openalex:W4410117633, openalex:W4410117633, openalex:W4410117633
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
- doi:10.7554/elife.105302.3: openalex:W4392898887, openalex:W4392898887
- doi:10.17645/si.12135: openalex:W7167845010, openalex:W7167845010
- openalex:W7167154699: openalex:W7167154699, openalex:W7167154699
- openalex:W7167747562: openalex:W7167747562, openalex:W7167747562
- doi:10.48550/arxiv.2606.31273: openalex:W7166831674, openalex:W7166831674
- doi:10.48550/arxiv.2607.04293: openalex:W7167618004, openalex:W7167618004
- openalex:W7167154245: openalex:W7167154245, openalex:W7167154245
- doi:10.1038/s43016-026-01380-7: openalex:W7167273491, openalex:W7167273491
- openalex:W7167855751: openalex:W7167855751, openalex:W7167855751, openalex:W7167855751, openalex:W7167855751
- doi:10.48550/arxiv.2607.03863: openalex:W7167612321, openalex:W7167612321
- openalex:W7167854942: openalex:W7167854942, openalex:W7167854942, openalex:W7167854942, openalex:W7167854942
- doi:10.1098/rsif.2026.0043: openalex:W7167603384, openalex:W7167603384
- doi:10.48550/arxiv.2607.05682: openalex:W7167668015, openalex:W7167668015, openalex:W7167668015
- openalex:W7167981654: openalex:W7167981654, openalex:W7167981654
- doi:10.1007/s10489-026-07340-9: openalex:W7166833661, openalex:W7166833661
- doi:10.26192/q4qyy: openalex:W2811413344, openalex:W2811413344
- doi:10.21203/rs.3.rs-9819774/v1: openalex:W7166694999, openalex:W7166694999, openalex:W7166694999, openalex:W7166694999, openalex:W7166694999
- doi:10.1016/j.dsm.2026.100195: openalex:W7168032443, openalex:W7168032443
- doi:10.5281/zenodo.21198322: openalex:W7167369189, openalex:W7167369189
- doi:10.5281/zenodo.21198323: openalex:W7167327078, openalex:W7167327078
- doi:10.5281/zenodo.21289028: openalex:W7167910996, openalex:W7167910996
- openalex:W7167748459: openalex:W7167748459, openalex:W7167748459
- openalex:W7167380899: openalex:W7167380899, openalex:W7167380899
- doi:10.5194/epsc2026-276: openalex:W7167024696, openalex:W7167024696, openalex:W7167024696
- doi:10.33774/coe-2026-vt9t2-v2: openalex:W7168016202, openalex:W7168016202
- doi:10.5281/zenodo.21301356: openalex:W7167956323, openalex:W7167956323
- doi:10.5281/zenodo.21301869: openalex:W7167973731, openalex:W7167973731
- doi:10.31462/jcemi.2026.721: openalex:W7166811136, openalex:W7166811136
- doi:10.5281/zenodo.21307399: openalex:W7168029277, openalex:W7168029277
- doi:10.5281/zenodo.21262688: openalex:W7167675082, openalex:W7167675082
- doi:10.1145/3805760.3814889: openalex:W7160617091, openalex:W7160617091
- doi:10.21203/rs.3.rs-10220882/v1: openalex:W7167719533, openalex:W7167719533, openalex:W7167719533
- openalex:W7167380417: openalex:W7167380417, openalex:W7167380417
- doi:10.1038/s41746-026-02978-8: openalex:W7167574952, openalex:W7167574952
- doi:10.1016/j.ipm.2026.105056: openalex:W7167904580, openalex:W7167904580
- openalex:W7167747490: openalex:W7167747490, openalex:W7167747490
- openalex:W7167155179: openalex:W7167155179, openalex:W7167155179
- openalex:W7167379880: openalex:W7167379880, openalex:W7167379880
- openalex:W7167379885: openalex:W7167379885, openalex:W7167379885
- openalex:W7167290022: openalex:W7167290022, openalex:W7167290022
- doi:10.21981/ke2k-gd71: openalex:W7167019083, openalex:W7167019083
- doi:10.21981/gfzt-hb86: openalex:W7167361824, openalex:W7167361824
- doi:10.21981/rz3e-kb86: openalex:W7167230525, openalex:W7167230525
- doi:10.1016/j.datak.2026.102627: openalex:W4405095248, openalex:W4405095248, openalex:W4405095248
- doi:10.1016/j.jaccedu.2026.101037: openalex:W4413236460, openalex:W4413236460
