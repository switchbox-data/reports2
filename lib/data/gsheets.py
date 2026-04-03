"""Google Sheets client with cached OAuth credentials."""

from __future__ import annotations

import json
import os
from pathlib import Path

import gspread
from dotenv import load_dotenv


def _gspread_token_path() -> Path:
    """Path for cached OAuth token; reuse to avoid browser prompt on every run."""
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path.home() / ".config"
    return base / "gspread" / "authorized_user_reports2.json"


def load_cached_token() -> dict | None:
    """Load cached gspread OAuth token from disk, or None if missing or invalid."""
    token_path = _gspread_token_path()
    if not token_path.exists():
        return None
    try:
        return json.loads(token_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save_cached_token(authorized_user: dict | str) -> None:
    """Persist gspread authorized_user token so the next run can skip the browser."""
    token_path = _gspread_token_path()
    token_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(authorized_user, dict):
        token_path.write_text(json.dumps(authorized_user, indent=2), encoding="utf-8")
    else:
        token_path.write_text(str(authorized_user), encoding="utf-8")


def get_gspread_client():
    """Return a gspread client using env credentials and cached token when possible.

    Loads G_* env vars (optionally from .env via load_dotenv()). Uses a cached
    token at ~/.config/gspread/authorized_user_reports2.json when present so
    the browser is only opened on first run or when the token is expired.

    Returns:
        Tuple of (gc, authorized_user) where gc is the gspread Client and
        authorized_user is the token dict/str returned by gspread (for persistence).
    """
    load_dotenv()
    app_creds = {
        "installed": {
            "client_id": os.getenv("G_CLIENT_ID"),
            "client_secret": os.getenv("G_CLIENT_SECRET"),
            "project_id": os.getenv("G_PROJECT_ID"),
            "auth_uri": os.getenv("G_AUTH_URI"),
            "token_uri": os.getenv("G_TOKEN_URI"),
            "redirect_uris": ["http://localhost"],
        }
    }
    saved_token = load_cached_token()
    if saved_token is not None:
        gc, authorized_user = gspread.oauth_from_dict(credentials=app_creds, authorized_user_info=saved_token)
    else:
        gc, authorized_user = gspread.oauth_from_dict(credentials=app_creds)
    if authorized_user:
        save_cached_token(authorized_user)
    return gc, authorized_user
