import json
import unittest

from paper_scout.fetchers.arxiv import ArxivFetcher, parse_arxiv_feed
from paper_scout.fetchers.openalex import OpenAlexFetcher, parse_openalex_works
from paper_scout.fetchers.semantic_scholar import SemanticScholarFetcher, parse_semantic_scholar_results


class FakeHttp:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get_text(self, url, params=None, headers=None):
        self.calls.append((url, params or {}, headers or {}))
        return self.payload


class PaperScoutFetchersTest(unittest.TestCase):
    def test_parses_arxiv_feed(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <entry>
            <id>http://arxiv.org/abs/2601.12345v2</id>
            <updated>2026-01-03T00:00:00Z</updated>
            <published>2026-01-01T00:00:00Z</published>
            <title>Long-Term Memory for LLM Agents</title>
            <summary>Persistent memory for language agents.</summary>
            <author><name>Ada Lovelace</name></author>
            <link href="http://arxiv.org/abs/2601.12345v2" rel="alternate" />
            <arxiv:doi xmlns:arxiv="http://arxiv.org/schemas/atom">10.48550/arXiv.2601.12345</arxiv:doi>
          </entry>
        </feed>"""

        papers = parse_arxiv_feed(xml)

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].arxiv_id, "2601.12345")
        self.assertEqual(papers[0].doi, "10.48550/arXiv.2601.12345")

    def test_arxiv_search_with_diagnostics_reports_raw_record_count(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <entry>
            <id>http://arxiv.org/abs/2606.12345v1</id>
            <published>2026-06-25T00:00:00Z</published>
            <updated>2026-06-25T00:00:00Z</updated>
            <title>Agent Memory Benchmark</title>
            <summary>Agent memory benchmark.</summary>
          </entry>
        </feed>"""

        result = ArxivFetcher(http=FakeHttp(xml)).search_with_diagnostics("agent memory", days=30, max_results=5)

        self.assertEqual(result.raw_count, 1)
        self.assertEqual(len(result.candidates), 1)
        self.assertEqual(result.candidates[0].source, "arxiv")

    def test_parses_semantic_scholar_results(self):
        payload = {
            "data": [
                {
                    "paperId": "S2",
                    "title": "Agent Memory Benchmark",
                    "abstract": "A benchmark.",
                    "url": "https://www.semanticscholar.org/paper/S2",
                    "year": 2026,
                    "publicationDate": "2026-01-02",
                    "authors": [{"name": "Ada Lovelace"}],
                    "externalIds": {"DOI": "10.1/example", "ArXiv": "2601.12345"},
                }
            ]
        }

        papers = parse_semantic_scholar_results(json.dumps(payload))

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].semantic_scholar_id, "S2")
        self.assertEqual(papers[0].arxiv_id, "2601.12345")

    def test_semantic_scholar_search_with_diagnostics_reports_raw_record_count(self):
        payload = {
            "data": [
                {
                    "paperId": "S2",
                    "title": "Agent Memory Benchmark",
                    "abstract": "A benchmark for agent memory.",
                    "url": "https://www.semanticscholar.org/paper/S2",
                    "publicationDate": "2026-06-25",
                    "authors": [{"name": "Ada Lovelace"}],
                }
            ]
        }

        result = SemanticScholarFetcher(http=FakeHttp(json.dumps(payload))).search_with_diagnostics("agent memory", days=30, max_results=5)

        self.assertEqual(result.raw_count, 1)
        self.assertEqual(len(result.candidates), 1)
        self.assertEqual(result.candidates[0].source, "semantic_scholar")

    def test_parses_openalex_works(self):
        payload = {
            "results": [
                {
                    "id": "https://openalex.org/W123",
                    "doi": "https://doi.org/10.1/example",
                    "title": "Agentic Memory Systems",
                    "publication_date": "2026-01-03",
                    "updated_date": "2026-01-04T00:00:00.000000",
                    "authorships": [
                        {"author": {"display_name": "Ada Lovelace"}},
                    ],
                    "abstract_inverted_index": {
                        "Persistent": [0],
                        "memory": [1],
                        "agents": [2],
                    },
                    "primary_location": {"landing_page_url": "https://example.test/openalex"},
                }
            ]
        }

        papers = parse_openalex_works(json.dumps(payload))

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].openalex_id, "W123")
        self.assertEqual(papers[0].doi, "10.1/example")
        self.assertEqual(papers[0].abstract, "Persistent memory agents")

    def test_openalex_search_with_diagnostics_reports_raw_record_count(self):
        payload = {
            "results": [
                {
                    "id": "https://openalex.org/W123",
                    "title": "Agentic Memory Systems",
                    "publication_date": "2026-06-25",
                    "authorships": [],
                    "primary_location": {"landing_page_url": "https://example.test/openalex"},
                }
            ]
        }

        result = OpenAlexFetcher(http=FakeHttp(json.dumps(payload))).search_with_diagnostics("agent memory", days=30, max_results=5)

        self.assertEqual(result.raw_count, 1)
        self.assertEqual(len(result.candidates), 1)
        self.assertEqual(result.candidates[0].source, "openalex")


if __name__ == "__main__":
    unittest.main()
