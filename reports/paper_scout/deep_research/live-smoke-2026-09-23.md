# Paper Scout Live Smoke Report - 2026-09-23

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 1
- **Sources failed:** 2
- **Raw records:** 100
- **Candidates fetched:** 0
- **Unique papers:** 0
- **State initialized:** True
- **Idempotency passed:** True

## Sources

### arxiv

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-09-09&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

### semantic_scholar

- Status: Success - zero results
- Queries attempted: 4
- Raw records: 100
- Converted candidates: 0


## Decisions

- relevant: 0
- maybe: 0
- irrelevant: 0

## Top Relevant Or Maybe Papers

- None

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3Adeep+AND+all%3Aresearch+AND+all%3Aagent&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 406: Not Acceptable
- openalex (HTTP/API error) for `deep research agent`: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-09-09&per-page=25: request failed after 3 attempts: HTTP Error 429: Too Many Requests

## Deduplication Examples

- No duplicates found.
