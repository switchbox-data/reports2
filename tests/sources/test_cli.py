"""CLI wiring: session-start output, fetch, ingest exit codes and JSON, and the read-only helpers."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from lib.sources import cli, frontmatter, metadata, zotero
from tests.sources.conftest import make_card, use_repo_env


def pending_item(i=0):
    return zotero.PendingItem(f"K{i}", f"Title {i}", f"Author {i}", "2026", "not marked processed", ("ma_hp_rates",))


def test_pending_brief_is_one_line_and_silent_when_empty(monkeypatch, capsys):
    monkeypatch.setattr(zotero, "pending_items", lambda: [pending_item(i) for i in range(6)])
    assert cli.main(["pending", "--brief"]) == 0
    out = capsys.readouterr().out
    assert out.count("\n") == 1 and "6 source(s)" in out and "+2 more" in out
    monkeypatch.setattr(zotero, "pending_items", lambda: [])
    assert cli.main(["pending", "--brief"]) == 0
    assert capsys.readouterr().out == ""


def test_pending_brief_never_fails_without_credentials(monkeypatch, capsys):
    def boom():
        raise RuntimeError("ZOTERO_API_KEY is not set")

    monkeypatch.setattr(zotero, "pending_items", boom)
    assert cli.main(["pending", "--brief"]) == 0 and capsys.readouterr().out == ""
    assert cli.main(["pending", "--hook"]) == 0 and capsys.readouterr().out == ""
    assert cli.main(["pending"]) == 1


def test_pending_hook_emits_additional_context_json(monkeypatch, capsys):
    monkeypatch.setattr(zotero, "pending_items", lambda: [pending_item()])
    cli.main(["pending", "--hook"])
    payload = json.loads(capsys.readouterr().out)
    assert set(payload) == {"additional_context"} and "ingest-source" in payload["additional_context"]


def test_session_start_hook_script_answers_empty_json_without_a_venv(tmp_path):
    hook = tmp_path / ".cursor" / "hooks" / "sources-pending.sh"
    hook.parent.mkdir(parents=True)
    shutil.copy2(Path(__file__).parents[2] / ".cursor" / "hooks" / "sources-pending.sh", hook)
    stdin = json.dumps({"session_id": "s", "is_background_agent": False, "composer_mode": "agent"})
    done = subprocess.run([str(hook)], input=stdin, capture_output=True, text=True, timeout=10)
    assert done.returncode == 0 and json.loads(done.stdout) == {}
    assert not (tmp_path / ".venv").exists()


def test_fetch_downloads_next_to_the_extract(world, tmp_path, monkeypatch, capsys, repo):
    use_repo_env(monkeypatch, repo)
    extract = repo / "context" / "sources" / "ma_hp_rates" / "order.md"
    extract.write_text("---\ncitekey: madpu_X_2025\nmd5: abc\n---\n\nBody\n")
    key = world.add_item({"itemType": "document", "title": "T", "extra": "Citation Key: madpu_X_2025"})
    pdf = tmp_path / "order.pdf"
    pdf.write_bytes(b"%PDF data")
    zotero.attach_file(key, pdf)
    assert cli.main(["fetch", "madpu_X_2025"]) == 0
    out = Path(capsys.readouterr().out.strip())
    assert out == (extract.parent / "order.pdf").resolve() and out.read_bytes() == b"%PDF data"


def test_fetch_unknown_key(world, capsys):
    assert cli.main(["fetch", "nope_X_2025"]) == 1
    assert "No Zotero item" in capsys.readouterr().err


def write_card(path: Path, card: metadata.SourceMetadata) -> Path:
    metadata.dump(card, path)
    return path


def test_ingest_prints_json_per_document_and_exit_code(world, repo, pdf_file, monkeypatch, capsys, tmp_path):
    use_repo_env(monkeypatch, repo)
    monkeypatch.setattr("lib.sources.ingest.env.REPO_ROOT", repo)
    extract = repo / "context" / "sources" / "ma_hp_rates" / "madpu_25-55_order.md"
    extract.write_text("---\nsource: order.pdf\n---\n\nBody\n")
    card_path = write_card(tmp_path / "card.yaml", make_card())
    assert cli.main(["ingest", str(card_path), "--path-source", str(pdf_file)]) == 0
    report = json.loads(capsys.readouterr().out.strip().splitlines()[0])
    assert report["ok"] and report["processed"] and report["short_url"].startswith("https://pub.switch.box/")
    assert report["item_key"]


def test_ingest_extract_flag_requires_an_existing_extract(world, repo, monkeypatch, tmp_path, capsys):
    monkeypatch.setattr("lib.sources.cli.REPO_ROOT", repo)
    card_path = write_card(tmp_path / "card.yaml", make_card())
    assert cli.main(["ingest", str(card_path), "--extract"]) == 2
    assert "--extract needs an existing extract" in capsys.readouterr().err


def test_ingest_rejects_an_unfinished_draft_card(tmp_path, capsys):
    draft = tmp_path / "draft.yaml"
    draft.write_text(yaml.safe_dump({"item_type": "document", "title": "Docket 1: T"}))
    assert cli.main(["ingest", str(draft)]) == 2
    assert "citekey" in capsys.readouterr().err


def test_zotero_item_flag_needs_exactly_one_card(tmp_path, capsys):
    assert cli.main(["ingest", "a.yaml", "b.yaml", "--zotero-item", "K1"]) == 2


def test_org_and_dedupe_run_without_zotero(capsys, tmp_path):
    assert cli.main(["org", "National Grid", "--no-zotero"]) == 0
    assert "National Grid" in capsys.readouterr().out
    assert cli.main(["dedupe"]) == 2
    assert cli.main(["dedupe", "--url", "https://nowhere.example.org/x.pdf", "--no-zotero"]) == 0
    assert capsys.readouterr().out.strip() == "no matches"


def test_convert_frontmatter_is_a_dry_run_unless_applied(tmp_path, capsys):
    (tmp_path / "a.md").write_text("---\nsource: a.pdf\noriginal_pdf_path: /x/a.pdf\n---\n\nBody\n")
    assert cli.main(["convert-frontmatter", "--path-root", str(tmp_path)]) == 0
    assert "would change" in capsys.readouterr().out and "original_pdf_path" in (tmp_path / "a.md").read_text()
    cli.main(["convert-frontmatter", "--path-root", str(tmp_path), "--apply"])
    assert frontmatter.read(tmp_path / "a.md") == {"source_file": "a.pdf"}


def test_every_subcommand_has_help():
    for command in ("ingest", "fetch", "pending", "dedupe", "org", "status", "doctor", "check-card", "key"):
        with pytest.raises(SystemExit) as e:
            cli.main([command, "--help"])
        assert e.value.code == 0
