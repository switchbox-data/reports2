"""Web-page helpers: URL normalization, HTML to markdown, page metadata, Wayback Save Page Now (mocked)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import pytest
import requests

from lib.sources import webpage

PAGE = """<html><head><title>Heat pump rates explained | Example Institute</title>
<meta name="citation_author" content="Lopez, Ana"><meta name="citation_publication_date" content="2026-05-01">
<meta property="og:site_name" content="Example Institute"><meta name="citation_doi" content="10.1234/abc">
</head><body><nav>Home | About</nav><header>Site header</header>
<main><h1>Heat pump rates explained</h1><p>Winter rates <b>matter</b>.</p><ul><li>One</li><li>Two</li></ul></main>
<footer>Copyright</footer><script>track()</script></body></html>"""


@pytest.mark.parametrize(
    ("raw", "normal"),
    [
        ("http://WWW.Example.org/a/b/?utm_source=x&b=2&a=1#frag", "https://www.example.org/a/b?a=1&b=2"),
        ("https://example.org/", "https://example.org"),
        ("https://example.org/a?fbclid=zzz", "https://example.org/a"),
        ("https://example.org/a?id=7", "https://example.org/a?id=7"),
    ],
)
def test_normalize_url(raw, normal):
    assert webpage.normalize_url(raw) == normal


def test_html_to_markdown_drops_page_furniture():
    md = webpage.html_to_markdown(PAGE)
    assert md.startswith("# Heat pump rates explained")
    assert "**matter**" in md and "* One" in md
    for junk in ("Home | About", "Site header", "Copyright", "track()"):
        assert junk not in md


def test_page_metadata():
    meta = webpage.page_metadata(PAGE)
    assert meta == {
        "title": "Heat pump rates explained | Example Institute",
        "authors": ["Lopez, Ana"],
        "date": "2026-05-01",
        "site_name": "Example Institute",
        "doi": "10.1234/abc",
    }


class FakeSession:
    def __init__(self, post, statuses, playback=None):
        self._post, self._statuses, self.requests = post, list(statuses), []
        self._playback = playback or SimpleNamespace(status_code=200, headers={"x-archive-src": "spn2.warc.gz"})

    def head(self, url, headers=None, allow_redirects=True, timeout=None):
        self.requests.append(("head", url, headers, None))
        return self._playback

    def post(self, url, headers=None, data=None, timeout=None):
        self.requests.append(("post", url, headers, data))
        return self._post

    def get(self, url, headers=None, timeout=None, allow_redirects=True):
        self.requests.append(("get", url, headers, None))
        status = self._statuses.pop(0) if len(self._statuses) > 1 else self._statuses[0]
        return status if isinstance(status, SimpleNamespace) else SimpleNamespace(json=lambda: status)


def response(code=200, body=None, headers=None):
    return SimpleNamespace(
        status_code=code, json=lambda: body or {}, raise_for_status=lambda: None, headers=headers or {}
    )


@pytest.fixture
def keys(monkeypatch):
    monkeypatch.setenv("IA_ACCESS_KEY", "ak")
    monkeypatch.setenv("IA_SECRET_KEY", "sk")


@pytest.fixture
def no_keys(monkeypatch):
    monkeypatch.delenv("IA_ACCESS_KEY", raising=False)
    monkeypatch.delenv("IA_SECRET_KEY", raising=False)
    monkeypatch.setattr(webpage.env, "load_env", lambda: None)


def test_wayback_success_after_polling(keys):
    session = FakeSession(
        response(body={"job_id": "j1"}),
        [
            {"status": "pending"},
            {"status": "success", "timestamp": "20261028120000", "original_url": "https://x.org/a", "http_status": 200},
        ],
    )
    result = webpage.wayback_save("https://x.org/a", session=cast(Any, session), sleep=lambda _: None)
    assert result.ok and result.url == "https://web.archive.org/web/20261028120000/https://x.org/a"
    assert session.requests[0][2]["Authorization"] == "LOW ak:sk"  # authenticated when keys are set
    assert "capture_all" not in session.requests[0][3]  # SPN2 then refuses error pages itself
    assert not [r for r in session.requests if r[0] == "head"]  # http_status was enough


SNAPSHOT_404 = "https://web.archive.org/web/20261028182451/https://x.org/gone"


@pytest.mark.parametrize("code", [404, 410, 500, 503])
def test_wayback_capture_of_an_error_page_is_a_failure(keys, code):
    # Live SPN2 answers status "success" with the captured page's status in http_status.
    status = {
        "status": "success",
        "timestamp": "20261028182451",
        "original_url": "https://x.org/gone",
        "http_status": code,
    }
    session = FakeSession(response(body={"job_id": "j1"}), [status])
    result = webpage.wayback_save("https://x.org/gone", session=cast(Any, session), sleep=lambda _: None)
    assert not result.ok and not result.blocked
    assert result.url == SNAPSHOT_404 and f"HTTP {code}" in result.message and SNAPSHOT_404 in result.message


@pytest.mark.parametrize(
    ("playback", "ok"),
    [
        (SimpleNamespace(status_code=404, headers={"x-archive-src": "spn2.warc.gz"}), False),  # replayed 404
        (SimpleNamespace(status_code=404, headers={}), True),  # Wayback's own "not archived yet" page
        (SimpleNamespace(status_code=200, headers={"x-archive-src": "spn2.warc.gz"}), True),
    ],
)
def test_wayback_without_http_status_checks_the_replay(keys, playback, ok):
    status = {"status": "success", "timestamp": "20261028182451", "original_url": "https://x.org/gone"}
    session = FakeSession(response(body={"job_id": "j1"}), [status], playback=playback)
    result = webpage.wayback_save("https://x.org/gone", session=cast(Any, session), sleep=lambda _: None)
    assert result.ok is ok and not result.blocked and result.url == SNAPSHOT_404
    assert session.requests[-1][:2] == ("head", SNAPSHOT_404)


def test_wayback_anonymous_capture_of_an_error_page_is_a_failure(no_keys):
    playback = SimpleNamespace(status_code=404, headers={"x-archive-src": "spn2.warc.gz"})
    session = FakeSession(response(), [response(302, headers={"Location": SNAPSHOT_404})], playback=playback)
    result = webpage.wayback_save("https://x.org/gone", session=cast(Any, session), sleep=lambda _: None)
    assert not result.ok and not result.blocked and result.url == SNAPSHOT_404 and "HTTP 404" in result.message


def test_wayback_unreachable_replay_does_not_fail_the_capture(no_keys):
    class NoReplay(FakeSession):
        def head(self, *args, **kwargs):
            raise requests.ConnectionError("Connection refused")

    session = NoReplay(response(), [response(302, headers={"Location": SNAPSHOT_404})])
    result = webpage.wayback_save("https://x.org/gone", session=cast(Any, session), sleep=lambda _: None)
    assert result.ok and result.url == SNAPSHOT_404


def test_wayback_anonymous_uses_the_legacy_endpoint(no_keys):
    snapshot = "https://web.archive.org/web/20261028180628/https://x.org/a"
    session = FakeSession(response(), [response(302, headers={"Location": snapshot})])
    result = webpage.wayback_save("https://x.org/a", session=cast(Any, session), sleep=lambda _: None)
    assert result.ok and result.url == snapshot
    method, url, headers, _ = session.requests[0]
    assert (method, url) == ("get", "https://web.archive.org/save/https://x.org/a")
    assert "Authorization" not in headers
    assert session.requests[1][:2] == ("head", snapshot)  # the replay gives the captured page's status


def test_wayback_anonymous_failure(no_keys):
    session = FakeSession(response(), [response(523)])
    result = webpage.wayback_save("https://x.org/a", session=cast(Any, session), sleep=lambda _: None)
    assert not result.ok and "523" in result.message


def test_wayback_blocked_site(keys):
    session = FakeSession(
        response(body={"job_id": "j1"}),
        [{"status": "error", "status_ext": "error:blocked-robots", "message": "Blocked by robots.txt"}],
    )
    result = webpage.wayback_save("https://x.org/a", session=cast(Any, session), sleep=lambda _: None)
    assert not result.ok and result.blocked


def test_wayback_blocked_at_request_time(keys):
    # SPN2 answers excluded sites (e.g. archive.org itself) in the POST response, without a job.
    body = {"status": "error", "status_ext": "error:blocked-url", "message": "limitations archiving this site"}
    session = FakeSession(response(body=body), [])
    result = webpage.wayback_save("https://x.org/a", session=cast(Any, session), sleep=lambda _: None)
    assert not result.ok and result.blocked and "error:blocked-url" in result.message
    assert len(session.requests) == 1


@pytest.mark.parametrize("ext", ["error:http-status-500", "error:too-many-daily-captures", "error:blocked-client-ip"])
def test_wayback_other_error_is_not_blocked(keys, ext):
    session = FakeSession(
        response(body={"job_id": "j1"}), [{"status": "error", "status_ext": ext, "message": "Server error"}]
    )
    result = webpage.wayback_save("https://x.org/a", session=cast(Any, session), sleep=lambda _: None)
    assert not result.ok and not result.blocked and "Server error" in result.message


@pytest.mark.parametrize("code", [401, 403, 429])
def test_wayback_refusal(keys, code):
    result = webpage.wayback_save(
        "https://x.org/a", session=cast(Any, FakeSession(response(code), [])), sleep=lambda _: None
    )
    assert not result.ok and str(code) in result.message


def test_wayback_unreachable_is_a_clean_failure(keys):
    class Refusing(FakeSession):
        def post(self, *args, **kwargs):
            raise requests.ConnectionError("Connection refused")

    result = webpage.wayback_save("https://x.org/a", session=cast(Any, Refusing(response(), [])), sleep=lambda _: None)
    assert not result.ok and not result.blocked and "ConnectionError" in result.message


def test_wayback_gives_up_when_the_job_never_finishes(keys):
    session = FakeSession(response(body={"job_id": "j1"}), [{"status": "pending"}])
    result = webpage.wayback_save(
        "https://x.org/a", session=cast(Any, session), timeout_seconds=0.0, sleep=lambda _: None
    )
    assert not result.ok and "pending" in result.message
