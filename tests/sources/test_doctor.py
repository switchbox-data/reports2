"""Doctor reports every check as pass/warn/fail with a fix hint; it never crashes on a missing Inbox or credential."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from lib.sources import doctor, env, zotero


@pytest.fixture
def no_env(monkeypatch):
    monkeypatch.setattr(env, "load_env", lambda: None)
    for names in env.VARIABLES.values():
        for name in names:
            monkeypatch.delenv(name, raising=False)


def collections(with_inbox):
    cols = [
        {"key": "REP", "data": {"name": "Reports", "parentCollection": False}},
        {"key": "MA", "data": {"name": "ma_hp_rates", "parentCollection": "REP"}},
    ]
    if with_inbox:
        cols.append({"key": "INBOX", "data": {"name": "Inbox", "parentCollection": False}})
    return cols


def fake_zotero(monkeypatch, write=True, with_inbox=True):
    access = {"groups": {"999": {"library": True, "write": write}}}
    monkeypatch.setenv("ZOTERO_GROUP_ID", "999")
    monkeypatch.setattr(zotero, "client", lambda: SimpleNamespace(key_info=lambda: {"access": access}))
    monkeypatch.setattr(zotero, "collections", lambda: collections(with_inbox))


def by_name(results):
    return {r.name: r for r in results}


def test_every_unset_variable_is_reported_with_a_hint(no_env):
    results = by_name(doctor.check_env())
    assert results["ZOTERO_API_KEY set"].level == doctor.FAIL
    assert "write and file access" in results["ZOTERO_API_KEY set"].hint
    assert results["IA_ACCESS_KEY set"].level == doctor.WARN  # Wayback works anonymously
    assert results["SOURCES_CONTACT_EMAIL set"].level == doctor.WARN
    assert len(results) == sum(len(v) for v in env.VARIABLES.values())
    assert all(r.hint for r in results.values())


def test_set_variables_pass_and_values_are_never_printed(monkeypatch):
    monkeypatch.setattr(env, "load_env", lambda: None)
    monkeypatch.setenv("ZOTERO_API_KEY", "super-secret-value")
    results = doctor.check_env()
    assert all("super-secret-value" not in r.line() for r in results)
    assert by_name(results)["ZOTERO_API_KEY set"].level == doctor.OK


def test_missing_inbox_is_reported_not_a_crash(monkeypatch):
    fake_zotero(monkeypatch, with_inbox=False)
    results = by_name(doctor.check_zotero())
    inbox = results["Zotero 'Inbox' collection"]
    assert inbox.level == doctor.WARN and "create a top-level collection named Inbox" in inbox.hint
    assert results["Zotero 'Reports' collection"].level == doctor.OK
    assert results["Zotero key can write"].level == doctor.OK


def test_read_only_key_fails_with_a_fix(monkeypatch):
    fake_zotero(monkeypatch, write=False)
    key = by_name(doctor.check_zotero())["Zotero key can write"]
    assert key.level == doctor.FAIL and "write access" in key.hint


def test_a_raising_check_becomes_a_failed_result(monkeypatch):
    monkeypatch.setattr(zotero, "client", lambda: (_ for _ in ()).throw(RuntimeError("no network")))
    results = doctor.check_zotero()
    assert results and all(r.level == doctor.FAIL and "no network" in r.detail for r in results)


def test_run_all_skips_service_checks_without_credentials(no_env, monkeypatch):
    monkeypatch.setattr(doctor, "check_tools", lambda: [doctor.Check("tools", doctor.OK)])
    monkeypatch.setattr(doctor, "check_pub", lambda: [doctor.Check("pub", doctor.OK)])
    names = {r.name for r in doctor.run_all()}
    assert "tools" in names and "pub" in names and "Zotero key can write" not in names


def test_line_shows_the_hint_only_for_problems():
    assert "fix:" in doctor.Check("x", doctor.FAIL, "broken", "do this").line()
    assert "fix:" not in doctor.Check("x", doctor.OK, "", "do this").line()


def test_tools_check_reports_missing_binaries(monkeypatch):
    monkeypatch.setattr(doctor.shutil, "which", lambda name: None)
    results = by_name(doctor.check_tools())
    assert results["quarto on PATH"].level == doctor.FAIL and results["yamlfmt on PATH"].level == doctor.FAIL


def test_pub_check_runs_a_dry_run_push(pub_remote):
    results = doctor.check_pub()
    assert results[0].level == doctor.OK
