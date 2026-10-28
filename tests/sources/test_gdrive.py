"""Drive upload reuses an existing file (found by appProperties or ID), checks md5, and shares once."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from lib.data import gsheets
from lib.sources import gdrive


def fake_service(listing=None, perms=None, created=None):
    svc = MagicMock()
    svc.files.return_value.list.return_value.execute.return_value = {"files": listing or []}
    svc.files.return_value.create.return_value.execute.return_value = created or {"id": "NEW1", "md5Checksum": "m1"}
    svc.permissions.return_value.list.return_value.execute.return_value = {"permissions": perms or []}
    return svc


@pytest.fixture(autouse=True)
def _folder(monkeypatch, tmp_path):
    monkeypatch.setenv("GDRIVE_PUBLIC_FOLDER_ID", "ROOT")
    book = tmp_path / "model.xlsx"
    book.write_bytes(b"PK workbook")
    return book


def test_new_upload_creates_folder_file_and_permission(monkeypatch, _folder):
    svc = fake_service()
    monkeypatch.setattr(gdrive, "service", lambda: svc)
    monkeypatch.setattr("googleapiclient.http.MediaFileUpload", lambda *a, **k: object())
    result = gdrive.upload(_folder, "ma_hp_rates", "madpu_X_2025", "m1")
    assert result == gdrive.DriveFile("NEW1", "https://drive.google.com/file/d/NEW1/view", "m1")
    created = [c.kwargs.get("body") for c in svc.files.return_value.create.call_args_list]
    assert any(b.get("mimeType") == gdrive.FOLDER_MIME and b["parents"] == ["ROOT"] for b in created)
    file_body = next(b for b in created if "appProperties" in b)
    assert file_body["appProperties"] == {"citekey": "madpu_X_2025", "md5": "m1"}
    perm = svc.permissions.return_value.create.call_args.kwargs["body"]
    assert perm["type"] == "anyone" and perm["role"] == "reader"


def test_existing_public_file_is_reused_without_creating_anything(monkeypatch, _folder):
    svc = fake_service(listing=[{"id": "OLD1", "md5Checksum": "m1"}], perms=[{"type": "anyone", "role": "reader"}])
    monkeypatch.setattr(gdrive, "service", lambda: svc)
    result = gdrive.upload(_folder, "ma_hp_rates", "madpu_X_2025", "m1")
    assert result.id == "OLD1"
    svc.files.return_value.create.assert_not_called()
    svc.permissions.return_value.create.assert_not_called()


def test_existing_private_file_gets_shared(monkeypatch, _folder):
    svc = fake_service(listing=[{"id": "OLD1", "md5Checksum": "m1"}], perms=[])
    monkeypatch.setattr(gdrive, "service", lambda: svc)
    gdrive.upload(_folder, "ma_hp_rates", "madpu_X_2025", "m1")
    svc.permissions.return_value.create.assert_called_once()


def test_md5_mismatch_is_an_error(monkeypatch, _folder):
    svc = fake_service(listing=[{"id": "OLD1", "md5Checksum": "different"}])
    monkeypatch.setattr(gdrive, "service", lambda: svc)
    with pytest.raises(RuntimeError, match="expected m1"):
        gdrive.upload(_folder, "ma_hp_rates", "madpu_X_2025", "m1")


def test_query_values_are_escaped():
    assert gdrive._q("it's a \\ test") == "it\\'s a \\\\ test"


def test_service_uses_the_cached_google_login(monkeypatch):
    seen = {}

    def fake_creds(scopes=None):
        seen["scopes"] = scopes
        return "creds"

    monkeypatch.setattr(gsheets, "get_user_credentials", fake_creds)
    monkeypatch.setattr("googleapiclient.discovery.build", lambda *a, **k: seen.update(args=a, kwargs=k) or "svc")
    gdrive.service.cache_clear()
    assert gdrive.service() == "svc"
    gdrive.service.cache_clear()
    assert seen["args"] == ("drive", "v3") and seen["kwargs"]["credentials"] == "creds"
    assert seen["scopes"] == gdrive.SCOPES == ["https://www.googleapis.com/auth/drive"]


def test_missing_login_tells_the_user_to_run_google_login(monkeypatch, tmp_path):
    monkeypatch.setattr(gsheets, "_gspread_token_path", lambda: tmp_path / "none.json")
    gdrive.service.cache_clear()
    with pytest.raises(gsheets.GoogleLoginRequired, match="just google-login"):
        gdrive.service()
    gdrive.service.cache_clear()


def test_get_user_credentials_refreshes_a_stale_token(monkeypatch, tmp_path):
    token = {
        "refresh_token": "r",
        "client_id": "id",
        "client_secret": "s",
        "token_uri": "https://oauth2.googleapis.com/token",
        "scopes": ["https://www.googleapis.com/auth/drive"],
    }
    path = tmp_path / "token.json"
    path.write_text(json.dumps(token))
    monkeypatch.setattr(gsheets, "_gspread_token_path", lambda: path)
    refreshed = []

    def fake_refresh(self, request):
        refreshed.append(self)
        self.token = "access"

    monkeypatch.setattr("google.oauth2.credentials.Credentials.refresh", fake_refresh)
    creds = gsheets.get_user_credentials(gdrive.SCOPES)
    assert refreshed and creds.token == "access" and creds.refresh_token == "r"


def test_whoami_reports_folder_and_shared_drive(monkeypatch):
    svc = MagicMock()
    svc.files.return_value.get.return_value.execute.return_value = {"id": "ROOT", "name": "Public", "driveId": "D1"}
    monkeypatch.setattr(gdrive, "service", lambda: svc)
    assert gdrive.whoami() == {"folder": "Public", "id": "ROOT", "shared_drive": True}
