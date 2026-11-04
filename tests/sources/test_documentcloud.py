"""DocumentCloud wrapper with a fake client: polling, errors, find by citekey."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from lib.sources import documentcloud


class FakeDoc:
    def __init__(self, status, access="public"):
        self.status, self.access, self.id = status, access, 1
        self.canonical_url = "https://www.documentcloud.org/documents/1-x"
        self.saved = False

    def save(self):
        self.saved = True


class FakeClient:
    """``documents.get`` walks through ``statuses`` (the last one repeats), like a document being processed."""

    def __init__(self, statuses=("success",), search=None, access="public"):
        self.uploads, self._statuses, self._access, self.docs = [], list(statuses), access, []
        self.documents = SimpleNamespace(
            upload=self._upload, get=self._get, search=lambda q: search or [], delete=lambda i: None
        )
        self.projects = SimpleNamespace(get_or_create_by_title=lambda t: (SimpleNamespace(id=55), True))

    def _get(self, doc_id):
        status = self._statuses.pop(0) if len(self._statuses) > 1 else self._statuses[0]
        doc = FakeDoc(status, self._access)
        self.docs.append(doc)
        return doc

    def _upload(self, path, **kw):
        self.uploads.append((path, kw))
        return SimpleNamespace(id=7)


@pytest.fixture
def client(monkeypatch):
    def install(c):
        monkeypatch.setattr(documentcloud, "client", lambda: c)
        return c

    return install


def test_upload_tags_the_citekey_and_project(client, tmp_path):
    c = client(FakeClient())
    pdf = tmp_path / "a.pdf"
    pdf.write_bytes(b"%PDF")
    doc_id = documentcloud.start_upload(pdf, "Title", "MA DPU", "Desc", "ma_hp_rates", "madpu_X_2025")
    assert doc_id == 7
    kwargs = c.uploads[0][1]
    assert kwargs["data"] == {"citekey": ["madpu_X_2025"]} and kwargs["project"] == 55 and kwargs["access"] == "public"


def test_wait_polls_until_success_and_returns_the_canonical_url(client):
    client(FakeClient(["pending", "readable", "success"]))
    sleeps = []
    url = documentcloud.wait_until_ready(1, sleep=sleeps.append, poll_seconds=2)
    assert url == "https://www.documentcloud.org/documents/1-x" and sleeps == [2, 2]


def test_wait_makes_a_private_document_public(client):
    c = client(FakeClient(["success"], access="private"))
    documentcloud.wait_until_ready(1, sleep=lambda _: None)
    assert c.docs[-1].access == "public" and c.docs[-1].saved


def test_wait_raises_on_processing_error(client):
    client(FakeClient(["pending", "error"]))
    with pytest.raises(documentcloud.UploadError):
        documentcloud.wait_until_ready(1, sleep=lambda _: None)


def test_wait_times_out(client):
    client(FakeClient(["pending"]))
    with pytest.raises(TimeoutError):
        documentcloud.wait_until_ready(1, timeout=0.0, sleep=lambda _: None)


def test_find_by_citekey_checks_the_tag(client):
    match = SimpleNamespace(id=3, data={"citekey": ["madpu_X_2025"]})
    other = SimpleNamespace(id=4, data={"citekey": ["madpu_Y_2025"]})
    client(FakeClient(search=[other, match]))
    assert documentcloud.find_by_citekey("madpu_X_2025") is match
    assert documentcloud.find_by_citekey("nope") is None


def test_missing_credentials_name_the_variables(monkeypatch):
    documentcloud.client.cache_clear()
    for name in ("DOCUMENTCLOUD_USERNAME", "DOCUMENTCLOUD_PASSWORD"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(documentcloud.env, "load_env", lambda: None)
    with pytest.raises(Exception, match="DOCUMENTCLOUD_USERNAME"):
        documentcloud.client()


def test_whoami_resolves_an_organization_id(client):
    org = SimpleNamespace(name="Switchbox", verified_journalist=True)
    c = client(
        SimpleNamespace(
            user_id=3,
            users=SimpleNamespace(get=lambda i: SimpleNamespace(name="Pipeline", organization=9)),
            organizations=SimpleNamespace(get=lambda i: org if i == 9 else None),
        )
    )
    assert documentcloud.whoami() == {"user": "Pipeline", "organization": "Switchbox", "verified": True}
    assert c.user_id == 3
