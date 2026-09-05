from __future__ import annotations

import json
import logging
import socket
import ssl
import time
from dataclasses import dataclass, field
from typing import ClassVar
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

LOGGER = logging.getLogger(__name__)


class HttpRequestError(RuntimeError):
    def __init__(self, kind: str, url: str, message: str) -> None:
        super().__init__(f"{kind} error for {url}: {message}")
        self.kind = kind
        self.url = url
        self.message = message


@dataclass
class HttpClient:
    timeout_seconds: int = 30
    retries: int = 3
    pause_seconds: float = 1.0
    min_interval_seconds: float = 0.0
    _last_request_at: float = field(default=0.0, init=False, repr=False)
    request_count: int = field(default=0, init=False)
    retry_count: int = field(default=0, init=False)
    _provider_last: ClassVar[dict[str, float]] = {}

    def get_text(self, url: str, params: dict[str, str | int] | None = None, headers: dict[str, str] | None = None) -> str:
        full_url = _with_params(url, params)
        return self._request("GET", full_url, None, headers)

    def post_json(self, url: str, payload: dict[str, object], headers: dict[str, str] | None = None) -> str:
        body = json.dumps(payload).encode("utf-8")
        request_headers = {"Content-Type": "application/json", **(headers or {})}
        return self._request("POST", url, body, request_headers)

    def _request(self, method: str, url: str, body: bytes | None, headers: dict[str, str] | None) -> str:
        last_error: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                self._throttle(url)
                self.request_count += 1
                self.retry_count += int(attempt > 1)
                self._last_request_at = time.monotonic()
                self._provider_last[urlsplit(url).netloc] = self._last_request_at
                request = Request(
                    url,
                    data=body,
                    headers={"User-Agent": "paper-scout/0.1", **(headers or {})},
                    method=method,
                )
                with urlopen(request, timeout=self.timeout_seconds) as response:
                    self._last_request_at = time.monotonic()
                    return response.read().decode("utf-8")
            except (HTTPError, URLError, TimeoutError) as exc:
                last_error = exc
                LOGGER.warning("HTTP %s failed on attempt %s/%s for %s: %s", method, attempt, self.retries, url, exc)
                if attempt < self.retries:
                    time.sleep(self.pause_seconds * attempt)
        kind = _classify_request_error(last_error)
        message = str(last_error) if last_error else "unknown request failure"
        raise HttpRequestError(kind, url, f"request failed after {self.retries} attempts: {message}") from last_error

    def _throttle(self, url: str) -> None:
        host = urlsplit(url).netloc
        provider_interval = {"export.arxiv.org": 3.0, "api.semanticscholar.org": 1.0}.get(host, 0.0)
        interval = max(self.min_interval_seconds, provider_interval)
        last = max(self._last_request_at, self._provider_last.get(host, 0.0))
        if interval > 0 and last:
            remaining = interval - (time.monotonic() - last)
            if remaining > 0:
                time.sleep(remaining)


def _with_params(url: str, params: dict[str, str | int] | None) -> str:
    if not params:
        return url
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{urlencode(params)}"


def _classify_request_error(error: Exception | None) -> str:
    if isinstance(error, HTTPError):
        return "http"
    if isinstance(error, URLError):
        reason = error.reason
        if isinstance(reason, (ssl.SSLError, ssl.CertificateError)):
            return "tls"
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return "timeout"
        text = str(reason).lower()
        if "certificate verify failed" in text or "ssl" in text or "tls" in text:
            return "tls"
        if "timed out" in text or "timeout" in text:
            return "timeout"
        return "network"
    if isinstance(error, (TimeoutError, socket.timeout)):
        return "timeout"
    return "network"
