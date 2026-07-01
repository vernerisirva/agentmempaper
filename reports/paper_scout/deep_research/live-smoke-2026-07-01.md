# Paper Scout Live Smoke Report - 2026-07-01

- **CI mode:** True
- **Sources attempted:** 3
- **Sources succeeded:** 0
- **Sources failed:** 3
- **Raw records:** 0
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
- Error: HTTP/API error: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error

### openalex

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-06-17&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable

### semantic_scholar

- Status: Failed
- Queries attempted: 1
- Raw records: 0
- Converted candidates: 0
- Error: HTTP/API error: http error for https://api.semanticscholar.org/graph/v1/paper/search?query=deep+research+agent&limit=25&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds: request failed after 3 attempts: HTTP Error 500: Internal Server Error


## Decisions

- relevant: 0
- maybe: 0
- irrelevant: 0

## Top Relevant Or Maybe Papers

- None

## Source Failures

- arxiv (HTTP/API error) for `deep research agent`: http error for https://export.arxiv.org/api/query?search_query=all%3A%22deep+research+agent%22&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending: request failed after 3 attempts: HTTP Error 429: Unknown Error
- semantic_scholar (HTTP/API error) for `deep research agent`: http error for https://api.semanticscholar.org/graph/v1/paper/search?query=deep+research+agent&limit=25&fields=paperId%2Ctitle%2Cabstract%2Curl%2Cyear%2CpublicationDate%2Cauthors%2CexternalIds: request failed after 3 attempts: HTTP Error 500: Internal Server Error
- openalex (HTTP/API error) for `deep research agent`: http error for https://api.openalex.org/works?search=deep+research+agent&filter=from_publication_date%3A2026-06-17&per-page=25: request failed after 3 attempts: HTTP Error 503: Service Unavailable

## Deduplication Examples

- No duplicates found.
