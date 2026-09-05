import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from paper_scout.config import DiscoveryQuery
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.http import HttpClient, HttpRequestError
from paper_scout.query_planner import build_query


class EngramRequestTests(unittest.TestCase):
    def test_http_attempt_and_retry_accounting(self):
        client = HttpClient(retries=3, pause_seconds=0)
        with patch('paper_scout.http.urlopen', side_effect=HTTPError('https://example.test', 429, 'limit', {}, None)), patch('paper_scout.http.time.sleep'):
            with self.assertRaises(HttpRequestError):
                client.get_text('https://example.test')
        self.assertEqual(client.request_count, 3)
        self.assertEqual(client.retry_count, 2)

    def test_throttle_shared_across_clients_for_same_provider(self):
        with patch.dict(HttpClient._provider_last, {'export.arxiv.org': 100}, clear=True), patch('paper_scout.http.time.monotonic', return_value=101), patch('paper_scout.http.time.sleep') as sleep:
            HttpClient()._throttle('https://export.arxiv.org/api/query')
            sleep.assert_called_once_with(2)

    def test_one_page_limit_and_incomplete_diagnostics_for_all_providers(self):
        payloads = {
            'arxiv': '<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>https://arxiv.org/abs/2601.07372</id><title>Fixture</title><published>2026-09-04</published></entry></feed>',
            'openalex': json.dumps({'results': [{'id': 'W1', 'title': 'Fixture'}]}),
            'semantic_scholar': json.dumps({'data': [{'paperId': 'S1', 'title': 'Fixture'}]}),
        }
        for cls in (ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher):
            with self.subTest(source=cls.source):
                class FakeHttp:
                    calls = 0
                    def get_text(self, *args, **kwargs):
                        self.calls += 1
                        return payloads[cls.source]
                http = FakeHttp()
                result = cls(http=http).search_planned_with_diagnostics(build_query(cls.source, DiscoveryQuery('conditional memory')), days=100000, max_results=1)
                self.assertEqual(http.calls, 1)
                self.assertEqual(result.page_count, 1)
                self.assertTrue(result.incomplete)

    def test_metadata_lookup_budget_shared_across_search_queries(self):
        class FakeHttp:
            metadata = 0
            def get_text(self, url, **kwargs):
                if 'export.arxiv' in url:
                    self.metadata += 1
                    return '<feed xmlns="http://www.w3.org/2005/Atom"/>'
                return json.dumps({'data': [{'paperId': str(i), 'title': 'Fixture', 'year': 2026, 'externalIds': {'ArXiv': f'2601.0000{i}'}} for i in range(3)]})
        http = FakeHttp()
        fetcher = SemanticScholarFetcher(http, max_metadata_requests=4)
        results = [fetcher.search_with_diagnostics('Engram', 100000, 25) for _ in range(4)]
        self.assertEqual(http.metadata, 4)
        self.assertEqual([r.metadata_requests for r in results], [3, 1, 0, 0])

    def test_config_selected_track_remains_compatible_without_track_flag(self):
        from contextlib import redirect_stdout
        import io
        from paper_scout.cli import main
        from paper_scout.site import SiteBuildResult
        with patch('paper_scout.cli.build_site', return_value=SiteBuildResult(True, 'test')) as build, redirect_stdout(io.StringIO()):
            self.assertEqual(main(['--config', 'config/tracks/engram.yaml', 'build-site']), 0)
        self.assertEqual(build.call_args.kwargs['relevance_profile'], 'engram')
        self.assertFalse(build.call_args.kwargs['enrich_dates'])

    def test_generated_file_guard_rejects_runtime_and_secrets_without_slug_false_positives(self):
        import importlib.util
        import tempfile
        script = Path(__file__).resolve().parents[1] / '.github/scripts/check_paper_scout_site.py'
        spec = importlib.util.spec_from_file_location('site_guard', script)
        guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / 'docs'
            docs.mkdir()
            (docs / 'leaked.sqlite3').write_text('synthetic runtime state')
            (docs / 'secret.txt').write_text('sk-' + 'A' * 40)  # Synthetic detector input, never a credential.
            (docs / 'safe.txt').write_text('risk-controlled-selection-for-an-agent-study')
            errors = guard.validate_site(root)
            self.assertTrue(any('runtime file' in e for e in errors))
            self.assertTrue(any('secret.txt' in e for e in errors))
            self.assertFalse(any('safe.txt' in e for e in errors))
        self.assertEqual(guard.validate_workflows(Path(__file__).resolve().parents[1]), [])
