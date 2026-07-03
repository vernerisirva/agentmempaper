# Paper Scout Live Smoke Report - 2026-07-03

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 1279
- **Candidates fetched:** 639
- **Unique papers:** 420
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable

### openalex

- Status: Success
- Queries attempted: 26
- Raw records: 629
- Converted candidates: 629
- Sample title: Agent-Fence: Mapping Security Vulnerabilities Across Deep Research Agents
- Sample source ID: W7165677059
- Sample URL: https://doi.org/10.1609/aaaiss.v9i1.42945
- Sample published date: 2026-06-23
- Abstract: yes

### semantic_scholar

- Status: Success
- Queries attempted: 26
- Raw records: 650
- Converted candidates: 10
- Sample title: Clarus: Coordinating Autonomous Research Agents toward Web-Scale Scientific Collaboration
- Sample source ID: e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample URL: https://www.semanticscholar.org/paper/e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- Sample published date: 2026-06-29
- Abstract: yes


## Decisions

- relevant: 43
- maybe: 49
- irrelevant: 328

## Top Relevant Or Maybe Papers

- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://www.semanticscholar.org/paper/8b5edab1fd875d24c9aed5f088f6ea3656bdd78c
- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.29981
- **Hephaestus: Toward a Cybersecurity AI Scientist** (relevant, 98/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.29981
- **One Reflection Is Not Enough: Self-Correcting Autonomous Research via Multi-Hypothesis Failure Attribution** (relevant, 96/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.48550/arxiv.2606.31478
- **Socratic agents for autonomous scientific discovery in high-dimensional physical systems** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.26722
- **Socratic agents for autonomous scientific discovery in high-dimensional physical systems** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.26722
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **The Calibration Turn in AI-Assisted Research: A Conceptual and Methodological Framework for Evidence-Licensed Claims** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.31273
- **Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. I. Uncertainty Quantification, ML on Therapeutic Data Commons, and Agent-Based Modeling** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.64898/2026.06.24.734302

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable

## Deduplication Examples

- doi:10.1609/aaaiss.v9i1.42945: openalex:W7165677059, openalex:W7165677059, openalex:W7165677059, openalex:W7165677059, openalex:W7165677059, openalex:W7165677059
- doi:10.5281/zenodo.20822051: openalex:W7165792392, openalex:W7165792392, openalex:W7165792392
- doi:10.48550/arxiv.2606.29746: openalex:W7166706750, openalex:W7166706750, openalex:W7166706750
- openalex:W7166901874: openalex:W7166901874, openalex:W7166901874, openalex:W7166901874
- doi:10.1098/rsos.251988: openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127, openalex:W4417090127
- doi:10.4171/ecr/23/11: openalex:W4403444398, openalex:W4403444398, openalex:W4403444398
- doi:10.1038/s41598-026-57117-w: openalex:W4390572748, openalex:W4390572748
- doi:10.1111/1462-2920.70353: openalex:W7166115436, openalex:W7166115436, openalex:W7166115436, openalex:W7166115436, openalex:W7166115436
- doi:10.64898/2026.06.24.734302: openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207, openalex:W7166456207
- doi:10.26434/chemrxiv.15005137/v1: openalex:W7165775338, openalex:W7165775338
- doi:10.1145/3821637: openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855
- openalex:W7165818466: openalex:W7165818466, openalex:W7165818466, openalex:W7165818466, openalex:W7165818466
- doi:10.48550/arxiv.2606.21401: openalex:W7165642208, openalex:W7165642208
- doi:10.17869/enu.236998: openalex:W1641964597, openalex:W1641964597, openalex:W1641964597, openalex:W1641964597, openalex:W1641964597, openalex:W1641964597
- doi:10.1201/9781003667766-2: openalex:W7165651067, openalex:W7165651067
- openalex:W7166399911: openalex:W7166399911, openalex:W7166399911
- doi:10.4018/979-8-3693-5638-8.ch049: openalex:W7165359508, openalex:W7165359508
- doi:10.3390/computers15070401: openalex:W7165680067, openalex:W7165680067
- openalex:W7165818408: openalex:W7165818408, openalex:W7165818408, openalex:W7165818408, openalex:W7165818408, openalex:W7165818408
- doi:10.62762/ticps.2026.591816: openalex:W7166450520, openalex:W7166450520
- openalex:W7166900994: openalex:W7166900994, openalex:W7166900994
- doi:10.48550/arxiv.2606.26246: openalex:W7166194145, openalex:W7166194145
- doi:10.48550/arxiv.2606.29920: openalex:W7166663127, openalex:W7166663127
- doi:10.4018/979-8-3373-7082-8.ch005: openalex:W7166854929, openalex:W7166854929
- openalex:W7165816711: openalex:W7165816711, openalex:W7165816711, openalex:W7165816711
- arxiv:2606.30246: semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1, semantic_scholar:e665c4bbc454de8ffcf98bd92f6da212cf3780b1
- openalex:W7166901356: openalex:W7166901356, openalex:W7166901356, openalex:W7166901356
- doi:10.48550/arxiv.2606.30246: openalex:W7166673172, openalex:W7166673172, openalex:W7166673172, openalex:W7166673172
- doi:10.1145/3822503: openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992
- doi:10.5281/zenodo.20775222: openalex:W7165461832, openalex:W7165461832
- doi:10.5281/zenodo.20775223: openalex:W7165458917, openalex:W7165458917
- openalex:W7165817655: openalex:W7165817655, openalex:W7165817655, openalex:W7165817655, openalex:W7165817655, openalex:W7165817655, openalex:W7165817655
- doi:10.48550/arxiv.2606.22610: openalex:W7165659369, openalex:W7165659369, openalex:W7165659369, openalex:W7165659369
- openalex:W7166252298: openalex:W7166252298, openalex:W7166252298, openalex:W7166252298
- doi:10.48550/arxiv.2606.25198: openalex:W7165885460, openalex:W7165885460, openalex:W7165885460
- doi:10.3390/electronics15122740: openalex:W7165680161, openalex:W7165680161, openalex:W7165680161, openalex:W7165680161
- doi:10.26192/q4qyq: openalex:W2810130361, openalex:W2810130361, openalex:W2810130361, openalex:W2810130361
- doi:10.4018/979-8-2600-2601-4.ch004: openalex:W7165782897, openalex:W7165782897
- doi:10.5281/zenodo.20826452: openalex:W7165735928, openalex:W7165735928, openalex:W7165735928
- doi:10.5281/zenodo.20826453: openalex:W7165744339, openalex:W7165744339, openalex:W7165744339
- doi:10.1080/23311975.2026.2692205: openalex:W7165951177, openalex:W7165951177, openalex:W7165951177
- openalex:W7165816936: openalex:W7165816936, openalex:W7165816936
- doi:10.48550/arxiv.2606.31478: openalex:W7166808931, openalex:W7166808931
- doi:10.1201/9781003743774-10: openalex:W7165521704, openalex:W7165521704
- doi:10.48550/arxiv.2606.22774: openalex:W7165619005, openalex:W7165619005
- openalex:W7165973403: openalex:W7165973403, openalex:W7165973403
- doi:10.5281/zenodo.20822771: openalex:W7165797887, openalex:W7165797887
- doi:10.1038/s41598-026-45593-z: openalex:W7165956966, openalex:W7165956966
- doi:10.5281/zenodo.20822770: openalex:W7165755467, openalex:W7165755467
- doi:10.1145/3815572.3815744: openalex:W7166153882, openalex:W7166153882, openalex:W7166153882, openalex:W7166153882, openalex:W7166153882
- doi:10.5281/zenodo.20839771: openalex:W7165910312, openalex:W7165910312, openalex:W7165910312
- doi:10.5281/zenodo.20839770: openalex:W7165842336, openalex:W7165842336, openalex:W7165842336
- doi:10.5281/zenodo.21040067: openalex:W7166534811, openalex:W7166534811, openalex:W7166534811, openalex:W7166534811
- doi:10.5281/zenodo.21040068: openalex:W7166593969, openalex:W7166593969, openalex:W7166593969, openalex:W7166593969
- openalex:W7166900081: openalex:W7166900081, openalex:W7166900081
- doi:10.64898/2026.06.15.732409: openalex:W7165359770, openalex:W7165359770, openalex:W7165359770, openalex:W7165359770
- doi:10.48550/arxiv.2606.30111: openalex:W7166698998, openalex:W7166698998
- doi:10.5281/zenodo.20792042: openalex:W7165544293, openalex:W7165544293, openalex:W7165544293
- doi:10.5281/zenodo.20792041: openalex:W7165564166, openalex:W7165564166, openalex:W7165564166
- doi:10.48550/arxiv.2606.31229: openalex:W7166805631, openalex:W7166805631, openalex:W7166805631
- doi:10.1145/3805689.3806504: openalex:W4399695245, openalex:W4399695245, openalex:W4399695245
- doi:10.1145/3805689.3812399: openalex:W7155637802, openalex:W7155637802
- doi:10.5281/zenodo.21080396: openalex:W7166650293, openalex:W7166650293, openalex:W7166650293
- doi:10.5281/zenodo.21080395: openalex:W7166665405, openalex:W7166665405, openalex:W7166665405
- openalex:W7166399708: openalex:W7166399708, openalex:W7166399708
- doi:10.5281/zenodo.20799847: openalex:W7165523892, openalex:W7165523892
- doi:10.6082/324p4-ymb14: openalex:W7165772541, openalex:W7165772541
- doi:10.6082/gep96-ycs43: openalex:W7165788481, openalex:W7165788481
- openalex:W7165816672: openalex:W7165816672, openalex:W7165816672, openalex:W7165816672
- doi:10.48550/arxiv.2606.22859: openalex:W7165656922, openalex:W7165656922, openalex:W7165656922
- doi:10.48550/arxiv.2606.31273: openalex:W7166831674, openalex:W7166831674
- doi:10.5281/zenodo.20767716: openalex:W7165376786, openalex:W7165376786
- doi:10.5281/zenodo.20767717: openalex:W7165386155, openalex:W7165386155
- doi:10.5281/zenodo.20776924: openalex:W7165456080, openalex:W7165456080
- openalex:W7166399511: openalex:W7166399511, openalex:W7166399511, openalex:W7166399511
- doi:10.48550/arxiv.2606.26722: openalex:W7166151766, openalex:W7166151766
- doi:10.54254/2755-2721/2026.34758: openalex:W7165647483, openalex:W7165647483
- openalex:W7166400267: openalex:W7166400267, openalex:W7166400267
- doi:10.1145/3744256.3812580: openalex:W7165139125, openalex:W7165139125
- doi:10.5281/zenodo.20819646: openalex:W7165649371, openalex:W7165649371
- doi:10.5281/zenodo.20819647: openalex:W7165612077, openalex:W7165612077
- doi:10.1007/s10489-026-07340-9: openalex:W7166833661, openalex:W7166833661
- doi:10.65140/gimn202601.19: openalex:W7165758059, openalex:W7165758059
- doi:10.26192/q4qyy: openalex:W2811413344, openalex:W2811413344
- doi:10.21203/rs.3.rs-9819693/v1: openalex:W7165119815, openalex:W7165119815
- doi:10.1016/j.ssaho.2026.103144: openalex:W7165478177, openalex:W7165478177
- doi:10.5281/zenodo.20802608: openalex:W7165682185, openalex:W7165682185
- doi:10.5281/zenodo.20802609: openalex:W7165670352, openalex:W7165670352
- doi:10.48550/arxiv.2606.21959: openalex:W7165623149, openalex:W7165623149
- doi:10.5281/zenodo.20777544: openalex:W7165444033, openalex:W7165444033
- doi:10.5281/zenodo.20777543: openalex:W7165446266, openalex:W7165446266
- openalex:W7165818581: openalex:W7165818581, openalex:W7165818581
- openalex:W7165818093: openalex:W7165818093, openalex:W7165818093
- doi:10.1038/s41746-026-02888-9: openalex:W7165172255, openalex:W7165172255, openalex:W7165172255
- doi:10.31234/osf.io/xnvak_v2: openalex:W7165453853, openalex:W7165453853
- doi:10.5281/zenodo.20777489: openalex:W7165446464, openalex:W7165446464
- doi:10.5281/zenodo.20777488: openalex:W7165460456, openalex:W7165460456
- doi:10.5281/zenodo.3406497: openalex:W4400118483, openalex:W4400118483, openalex:W4400118483
- doi:10.1145/3805689.3806728: openalex:W7165663364, openalex:W7165663364
- doi:10.26434/chemrxiv.15005228/v1: openalex:W7166062973, openalex:W7166062973, openalex:W7166062973, openalex:W7166062973
- doi:10.1016/j.trc.2026.105818: openalex:W4416434619, openalex:W4416434619
- doi:10.5281/zenodo.21117753: openalex:W7166870415, openalex:W7166870415
- doi:10.5281/zenodo.21117754: openalex:W7166881449, openalex:W7166881449
- doi:10.1145/3808045.3808062: openalex:W4415090786, openalex:W4415090786
- doi:10.5281/zenodo.20777160: openalex:W7165459457, openalex:W7165459457
- doi:10.5281/zenodo.20777159: openalex:W7165458005, openalex:W7165458005
- doi:10.48550/arxiv.2606.29116: openalex:W7166673129, openalex:W7166673129
- openalex:W7166901650: openalex:W7166901650, openalex:W7166901650
- doi:10.31462/jcemi.2026.721: openalex:W7166811136, openalex:W7166811136
- doi:10.1145/3750555.3811883: openalex:W7165730392, openalex:W7165730392
- openalex:W7165816698: openalex:W7165816698, openalex:W7165816698
- doi:10.48550/arxiv.2606.21168: openalex:W7165652028, openalex:W7165652028
- doi:10.5281/zenodo.20848833: openalex:W7165849592, openalex:W7165849592
- doi:10.5281/zenodo.20848834: openalex:W7165859569, openalex:W7165859569
- doi:10.17605/osf.io/7dvcp: openalex:W7166299976, openalex:W7166299976
- openalex:W7165973254: openalex:W7165973254, openalex:W7165973254
- doi:10.22214/ijraset.2026.81730: openalex:W7165519270, openalex:W7165519270
- doi:10.21981/axzb-pv51: openalex:W7165867525, openalex:W7165867525
- doi:10.22214/ijraset.2026.81271: semantic_scholar:ca6f3fedea6bc87ba962cd84917b9bafa40565fd, openalex:W7165767214
