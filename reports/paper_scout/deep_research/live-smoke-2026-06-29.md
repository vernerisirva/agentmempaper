# Paper Scout Live Smoke Report - 2026-06-29

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 2
- **Sources failed:** 1
- **Raw records:** 1281
- **Candidates fetched:** 638
- **Unique papers:** 429
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
- Raw records: 631
- Converted candidates: 631
- Sample title: Agent-Fence: Mapping Security Vulnerabilities Across Deep Research Agents
- Sample source ID: W7165677059
- Sample URL: https://doi.org/10.1609/aaaiss.v9i1.42945
- Sample published date: 2026-06-23
- Abstract: yes

### semantic_scholar

- Status: Success
- Queries attempted: 26
- Raw records: 650
- Converted candidates: 7
- Sample title: Open Research Online
- Sample source ID: b3744d7d35aded35a345f13c6be4defa9ce3a914
- Sample URL: https://www.semanticscholar.org/paper/b3744d7d35aded35a345f13c6be4defa9ce3a914
- Sample published date: unknown
- Abstract: no


## Decisions

- relevant: 45
- maybe: 52
- irrelevant: 332

## Top Relevant Or Maybe Papers

- **Socratic agents for autonomous scientific discovery in high-dimensional physical systems** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.48550/arxiv.2606.26722
- **Socratic agents for autonomous scientific discovery in high-dimensional physical systems** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://arxiv.org/abs/2606.26722
- **Cybernetics After Prompt Engineering: SkillOpt, AutoResearch, and the Governance of Externalized State** (relevant, 95/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.5281/zenodo.20705508
- **Why Sense Matters: Answer-Key Leakage and the Specification Boundary in Agentic Citation Verification** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.5281/zenodo.20710741
- **Why Sense Matters: Answer-Key Leakage and the Specification Boundary in Agentic Citation Verification** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.5281/zenodo.20710740
- **VERIFY-DD: An Evidence-Grounded Agentic AI Framework for Hallucination Detection and Mitigation in LLM-Assisted Drug Discovery** (relevant, 93/100): Studies source-grounded research workflows, citation verification, or evidence-backed research reports. https://doi.org/10.25258/ijddt.16.54s.157
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/gep96-ycs43
- **Towards Reliable AI Scientists** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.6082/324p4-ymb14
- **Tool Use and "AI Scientists"** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.59350/7zgzc-yk365
- **Tool Use and "AI Scientists"** (relevant, 93/100): Studies AI-scientist or scientific-discovery agents. https://doi.org/10.59350/2y9n3-6vk07

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

## Deduplication Examples

- doi:10.1609/aaaiss.v9i1.42945: openalex:W7165677059, openalex:W7165677059, openalex:W7165677059, openalex:W7165677059, openalex:W7165677059, openalex:W7165677059
- openalex:W7165063777: openalex:W7165063777, openalex:W7165063777, openalex:W7165063777
- doi:10.48550/arxiv.2606.17029: openalex:W7164941083, openalex:W7164941083
- openalex:W7165220055: openalex:W7165220055, openalex:W7165220055, openalex:W7165220055, openalex:W7165220055, openalex:W7165220055
- doi:10.48550/arxiv.2606.18648: openalex:W7165173206, openalex:W7165173206, openalex:W7165173206, openalex:W7165173206, openalex:W7165173206
- doi:10.5281/zenodo.20822051: openalex:W7165792392, openalex:W7165792392, openalex:W7165792392
- doi:10.4171/ecr/23/11: openalex:W4403444398, openalex:W4403444398, openalex:W4403444398
- doi:10.1038/s41598-026-57117-w: openalex:W4390572748, openalex:W4390572748
- openalex:W7165423777: openalex:W7165423777, openalex:W7165423777
- openalex:W7165219111: openalex:W7165219111, openalex:W7165219111
- doi:10.48550/arxiv.2606.19893: openalex:W7165377301, openalex:W7165377301
- doi:10.48550/arxiv.2606.17458: openalex:W7165028274, openalex:W7165028274
- openalex:W7165423976: openalex:W7165423976, openalex:W7165423976
- doi:10.48550/arxiv.2606.20122: openalex:W7165359052, openalex:W7165359052
- openalex:W7165220203: openalex:W7165220203, openalex:W7165220203, openalex:W7165220203, openalex:W7165220203
- doi:10.48550/arxiv.2606.18191: openalex:W7165059973, openalex:W7165059973, openalex:W7165059973, openalex:W7165059973
- doi:10.26434/chemrxiv.15005137/v1: openalex:W7165775338, openalex:W7165775338
- doi:10.1145/3821637: openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855, openalex:W4387724855
- openalex:W7165818466: openalex:W7165818466, openalex:W7165818466, openalex:W7165818466
- doi:10.48550/arxiv.2606.21401: openalex:W7165642208, openalex:W7165642208
- doi:10.17869/enu.236998: openalex:W1641964597, openalex:W1641964597, openalex:W1641964597, openalex:W1641964597, openalex:W1641964597, openalex:W1641964597
- doi:10.5281/zenodo.20729328: openalex:W7165023922, openalex:W7165023922, openalex:W7165023922
- doi:10.5281/zenodo.20729329: openalex:W7165027671, openalex:W7165027671, openalex:W7165027671
- doi:10.1201/9781003667766-2: openalex:W7165651067, openalex:W7165651067
- openalex:W7166399911: openalex:W7166399911, openalex:W7166399911
- doi:10.1145/3822503: openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992, openalex:W4414989992
- doi:10.5281/zenodo.20775223: openalex:W7165458917, openalex:W7165458917
- doi:10.5281/zenodo.20775222: openalex:W7165461832, openalex:W7165461832
- openalex:W7165817655: openalex:W7165817655, openalex:W7165817655, openalex:W7165817655, openalex:W7165817655, openalex:W7165817655
- doi:10.48550/arxiv.2606.22610: openalex:W7165659369, openalex:W7165659369, openalex:W7165659369, openalex:W7165659369
- doi:10.5281/zenodo.20602943: openalex:W7164043641, openalex:W7164043641, openalex:W7164043641
- doi:10.5281/zenodo.20711464: openalex:W7164930570, openalex:W7164930570, openalex:W7164930570
- doi:10.5281/zenodo.20732895: openalex:W7165003960, openalex:W7165003960, openalex:W7165003960
- doi:10.5281/zenodo.20732894: openalex:W7164990913, openalex:W7164990913, openalex:W7164990913
- openalex:W7166252298: openalex:W7166252298, openalex:W7166252298, openalex:W7166252298
- doi:10.48550/arxiv.2606.25198: openalex:W7165885460, openalex:W7165885460, openalex:W7165885460
- doi:10.5281/zenodo.20345041: openalex:W7162104229, openalex:W7162104229
- doi:10.5281/zenodo.20751654: openalex:W7165186180, openalex:W7165186180
- doi:10.3390/electronics15122740: openalex:W7165680161, openalex:W7165680161, openalex:W7165680161, openalex:W7165680161
- doi:10.5281/zenodo.20712333: openalex:W7164889905, openalex:W7164889905
- doi:10.5281/zenodo.20712334: openalex:W7164957846, openalex:W7164957846
- doi:10.3389/fphy.2026.1700712: openalex:W4399911812, openalex:W4399911812, openalex:W4399911812, openalex:W4399911812, openalex:W4399911812, openalex:W4399911812, openalex:W4399911812, openalex:W4399911812, openalex:W4399911812, openalex:W4399911812, openalex:W4399911812
- doi:10.4018/979-8-2600-2601-4.ch004: openalex:W7165782897, openalex:W7165782897
- doi:10.5281/zenodo.20718644: openalex:W7164915659, openalex:W7164915659, openalex:W7164915659
- doi:10.5281/zenodo.20718643: openalex:W7164890501, openalex:W7164890501, openalex:W7164890501
- doi:10.5281/zenodo.20826453: openalex:W7165744339, openalex:W7165744339, openalex:W7165744339
- doi:10.5281/zenodo.20826452: openalex:W7165735928, openalex:W7165735928, openalex:W7165735928
- doi:10.7771/3067-4883.2198: openalex:W7164899438, openalex:W7164899438, openalex:W7164899438
- openalex:W7163840128: openalex:W7163840128, openalex:W7163840128
- doi:10.22399/ijcesen.5339: openalex:W7165008770, openalex:W7165008770
- doi:10.1145/3815572.3815744: openalex:W7166153882, openalex:W7166153882, openalex:W7166153882, openalex:W7166153882, openalex:W7166153882
- doi:10.5281/zenodo.20839770: openalex:W7165842336, openalex:W7165842336, openalex:W7165842336
- doi:10.5281/zenodo.20839771: openalex:W7165910312, openalex:W7165910312, openalex:W7165910312
- doi:10.64898/2026.06.15.732409: openalex:W7165359770, openalex:W7165359770, openalex:W7165359770, openalex:W7165359770
- doi:10.5281/zenodo.20792042: openalex:W7165544293, openalex:W7165544293, openalex:W7165544293
- doi:10.5281/zenodo.20792041: openalex:W7165564166, openalex:W7165564166, openalex:W7165564166
- doi:10.5281/zenodo.20780689: openalex:W7165490738, openalex:W7165490738
- doi:10.1007/s10614-026-11371-2: openalex:W7166181976, openalex:W7166181976
- doi:10.5281/zenodo.20780709: openalex:W7165476017, openalex:W7165476017
- doi:10.1145/3805689.3806504: openalex:W4399695245, openalex:W4399695245, openalex:W4399695245
- doi:10.1145/3805689.3812399: openalex:W7155637802, openalex:W7155637802
- doi:10.1007/s10462-026-11590-x: openalex:W4403662649, openalex:W4403662649, openalex:W4403662649, openalex:W4403662649, openalex:W4403662649
- doi:10.1007/s11831-026-10675-8: openalex:W7164841116, openalex:W7164841116, openalex:W7164841116, openalex:W7164841116
- openalex:W7166399708: openalex:W7166399708, openalex:W7166399708
- doi:10.6082/324p4-ymb14: openalex:W7165772541, openalex:W7165772541
- doi:10.6082/gep96-ycs43: openalex:W7165788481, openalex:W7165788481
- openalex:W7165816672: openalex:W7165816672, openalex:W7165816672, openalex:W7165816672, openalex:W7165816672
- doi:10.48550/arxiv.2606.22859: openalex:W7165656922, openalex:W7165656922, openalex:W7165656922
- doi:10.5281/zenodo.20767717: openalex:W7165386155, openalex:W7165386155
- doi:10.5281/zenodo.20767716: openalex:W7165376786, openalex:W7165376786
- doi:10.5281/zenodo.20703439: openalex:W7164814671, openalex:W7164814671
- doi:10.5281/zenodo.20776924: openalex:W7165456080, openalex:W7165456080
- doi:10.5281/zenodo.20776925: openalex:W7165447087, openalex:W7165447087
- openalex:W7166399511: openalex:W7166399511, openalex:W7166399511, openalex:W7166399511, openalex:W7166399511
- doi:10.48550/arxiv.2606.26722: openalex:W7166151766, openalex:W7166151766
- doi:10.54254/2755-2721/2026.34758: openalex:W7165647483, openalex:W7165647483
- doi:10.1145/3744256.3812580: openalex:W7165139125, openalex:W7165139125
- doi:10.5281/zenodo.20819646: openalex:W7165649371, openalex:W7165649371
- doi:10.5281/zenodo.20819647: openalex:W7165612077, openalex:W7165612077
- doi:10.65140/gimn202601.19: openalex:W7165758059, openalex:W7165758059
- doi:10.21203/rs.3.rs-9819693/v1: openalex:W7165119815, openalex:W7165119815
- openalex:W7165423553: openalex:W7165423553, openalex:W7165423553
- doi:10.21203/rs.3.rs-10126259/v1: openalex:W7165734347, openalex:W7165734347
- doi:10.1016/j.ssaho.2026.103144: openalex:W7165478177, openalex:W7165478177
- doi:10.5281/zenodo.20802608: openalex:W7165682185, openalex:W7165682185
- doi:10.5281/zenodo.20802609: openalex:W7165670352, openalex:W7165670352
- doi:10.5281/zenodo.20724440: openalex:W7165035955, openalex:W7165035955
- doi:10.5281/zenodo.20777809: openalex:W7165451331, openalex:W7165451331
- openalex:W7165818408: openalex:W7165818408, openalex:W7165818408, openalex:W7165818408
- doi:10.48550/arxiv.2606.21959: openalex:W7165623149, openalex:W7165623149
- openalex:W7165218563: openalex:W7165218563, openalex:W7165218563
- openalex:W7165818581: openalex:W7165818581, openalex:W7165818581
- openalex:W7165818093: openalex:W7165818093, openalex:W7165818093
- doi:10.25258/ijddt.16.54s.157: openalex:W7165192912, openalex:W7165192912
- doi:10.31234/osf.io/xnvak_v2: openalex:W7165453853, openalex:W7165453853
- doi:10.5281/zenodo.20777489: openalex:W7165446464, openalex:W7165446464
- doi:10.5281/zenodo.20777488: openalex:W7165460456, openalex:W7165460456
- doi:10.12701/jyms.2026.43.40: openalex:W7165027501, openalex:W7165027501, openalex:W7165027501
- doi:10.26434/chemrxiv.15005228/v1: openalex:W7166062973, openalex:W7166062973, openalex:W7166062973, openalex:W7166062973
- doi:10.1016/j.trc.2026.105818: openalex:W4416434619, openalex:W4416434619
- doi:10.1145/3808045.3808062: openalex:W4415090786, openalex:W4415090786
- doi:10.5281/zenodo.20777159: openalex:W7165458005, openalex:W7165458005
- doi:10.5281/zenodo.20777160: openalex:W7165459457, openalex:W7165459457
- doi:10.5281/zenodo.20711194: openalex:W7164881849, openalex:W7164881849
- doi:10.5281/zenodo.20711195: openalex:W7164940065, openalex:W7164940065
- doi:10.26434/chemrxiv.15004907/v1: openalex:W7165141875, openalex:W7165141875
- doi:10.1145/3750555.3811883: openalex:W7165730392, openalex:W7165730392
- openalex:W7165816698: openalex:W7165816698, openalex:W7165816698
- doi:10.48550/arxiv.2606.21168: openalex:W7165652028, openalex:W7165652028
- doi:10.5281/zenodo.20848833: openalex:W7165849592, openalex:W7165849592
- doi:10.5281/zenodo.20848834: openalex:W7165859569, openalex:W7165859569
- doi:10.17605/osf.io/7dvcp: openalex:W7166299976, openalex:W7166299976
- doi:10.3389/frai.2026.1808378: openalex:W7165119238, openalex:W7165119238
- openalex:W7165424024: openalex:W7165424024, openalex:W7165424024
- doi:10.22214/ijraset.2026.81730: openalex:W7165519270, openalex:W7165519270
- doi:10.21981/axzb-pv51: openalex:W7165867525, openalex:W7165867525
- doi:10.22214/ijraset.2026.81271: semantic_scholar:ca6f3fedea6bc87ba962cd84917b9bafa40565fd, openalex:W7165767214
- doi:10.1145/3770855.3818954: openalex:W7165740203, openalex:W7165740203
