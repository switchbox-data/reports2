"""Short links: 404.html is regenerated from links.json; a batch is one commit and one push."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess

import pytest

from lib.sources import shortlinks
from tests.sources.conftest import _git, remote_commits, remote_links


def embedded_links(html: str) -> dict[str, str]:
    m = re.search(r"var LINKS = (\{.*\});", html)
    assert m, "the map must be on one `var LINKS = {...};` line"
    return json.loads(m.group(1))


def test_404_embeds_the_sorted_map_on_one_line():
    html = shortlinks.render_404({"b_key": "https://b.example.org/", "a_key": "https://a.example.org/"})
    assert embedded_links(html) == {"a_key": "https://a.example.org/", "b_key": "https://b.example.org/"}
    assert list(embedded_links(html)) == ["a_key", "b_key"]
    assert "location.replace(target)" in html and "<noscript>" in html


def test_404_never_lets_a_value_break_out_of_the_script():
    hostile = "https://x.example.org/</script><script>alert(1)</script>?a=1&b=2"
    html = shortlinks.render_404({"k": hostile})
    assert html.count("</script>") == 2  # the two script blocks of the template, none from the value
    assert embedded_links(html)["k"] == hostile
    assert "innerHTML" not in html


def test_404_forwards_only_http_urls_and_ignores_prototype_keys():
    html = shortlinks.render_404({"k": "javascript:alert(1)"})
    assert "/^https?:\\/\\//i.test(target)" in html
    assert "hasOwnProperty.call(LINKS, key)" in html


@pytest.mark.parametrize("key", ["", "a/b", "../x", "has space", "-lead"])
def test_bad_keys_are_rejected(key):
    with pytest.raises(shortlinks.ShortLinkError):
        shortlinks.check_key(key)


@pytest.mark.parametrize("target", ["", "ftp://x.org/f", "javascript:alert(1)", "//x.org/a", "https://"])
def test_bad_targets_are_rejected(target):
    with pytest.raises(shortlinks.ShortLinkError):
        shortlinks.check_target(target)


def test_regenerate_rebuilds_404_from_links_json(tmp_path):
    (tmp_path / "links.json").write_text(json.dumps({"k": "https://x.example.org/"}))
    (tmp_path / "404.html").write_text("stale")
    assert shortlinks.regenerate(tmp_path) is True
    assert embedded_links((tmp_path / "404.html").read_text()) == {"k": "https://x.example.org/"}
    assert shortlinks.regenerate(tmp_path) is False


def test_batch_is_one_commit_and_one_push(pub_remote, tmp_path):
    before = remote_commits(pub_remote)
    batch = shortlinks.Batch()
    assert batch.add("k_a_2025", "https://a.example.org/") is True
    assert batch.add("k_b_2025", "https://b.example.org/") is True
    assert batch.add("k_a_2025", "https://a.example.org/") is False  # unchanged: no-op
    assert batch.publish() is True
    assert remote_commits(pub_remote) == before + 1
    links = remote_links(pub_remote, tmp_path)
    assert links["k_a_2025"] == "https://a.example.org/" and links["test"] == "https://switch.box/"
    html = subprocess.run(
        ["git", "--git-dir", str(pub_remote), "show", "main:404.html"], capture_output=True, text=True, check=True
    ).stdout
    assert embedded_links(html) == links


TRAILER = "Co-authored-by: Cursor <cursoragent@cursor.com>"


def inject_trailers(repo, tmp_path, monkeypatch):
    """Every route that adds a trailer to ``git commit``: a hook, and a PATH wrapper doing what Cursor's
    agent shell does (rewriting ``git commit`` to ``git commit --trailer ...``)."""
    hook = repo / ".git" / "hooks" / "prepare-commit-msg"
    hook.write_text(f'#!/bin/sh\nprintf "\\n{TRAILER}\\n" >> "$1"\n')
    hook.chmod(0o755)
    wrapper_dir = tmp_path / "bin"
    wrapper_dir.mkdir()
    real_git = shutil.which("git")
    wrapper = wrapper_dir / "git"
    wrapper.write_text(
        "#!/bin/sh\n"
        f'for a in "$@"; do [ "$a" = commit ] && exec {real_git} "$@" --trailer "{TRAILER}"; done\n'
        f'exec {real_git} "$@"\n'
    )
    wrapper.chmod(0o755)
    monkeypatch.setenv("PATH", f"{wrapper_dir}:{os.environ['PATH']}")
    probe = tmp_path / "probe"
    _git("init", "-q", str(probe))
    _git("commit", "-q", "--allow-empty", "-m", "probe", cwd=probe)
    assert (
        TRAILER
        in subprocess.run(
            ["git", "-C", str(probe), "log", "-1", "--format=%B"], capture_output=True, text=True, check=True
        ).stdout
    )  # the simulation works on a plain git commit


def remote_messages(bare):
    return subprocess.run(
        ["git", "--git-dir", str(bare), "log", "--format=%B%x00", "main"], capture_output=True, text=True, check=True
    ).stdout


def test_published_commits_carry_no_co_author_trailer(pub_remote, tmp_path, monkeypatch):
    batch = shortlinks.Batch()
    assert batch.repo is not None
    inject_trailers(batch.repo, tmp_path, monkeypatch)
    batch.add("k_a_2025", "https://a.example.org/")
    assert batch.publish() is True
    messages = remote_messages(pub_remote)
    assert "Add 1 short link: k_a_2025\n" in messages and "Co-authored-by" not in messages
    assert (
        subprocess.run(
            ["git", "-C", str(batch.repo), "status", "--porcelain"], capture_output=True, text=True, check=True
        ).stdout
        == ""
    )  # index and work tree match the new commit


def test_replayed_commit_after_a_rejected_push_carries_no_trailer(pub_remote, tmp_path, monkeypatch):
    batch = shortlinks.Batch()
    assert batch.repo is not None
    other = tmp_path / "other"
    subprocess.run(["git", "clone", str(pub_remote), str(other)], check=True, capture_output=True)
    shortlinks.save_links(other, {**shortlinks.load_links(other), "theirs_2025": "https://theirs.example.org/"})
    _git("add", ".", cwd=other)
    _git("commit", "-m", "theirs", cwd=other)
    _git("push", cwd=other)
    inject_trailers(batch.repo, tmp_path, monkeypatch)
    batch.add("mine_2025", "https://mine.example.org/")
    assert batch.publish() is True
    assert "Co-authored-by" not in remote_messages(pub_remote)
    assert set(remote_links(pub_remote, tmp_path)) >= {"theirs_2025", "mine_2025"}


def test_files_written_but_not_committed_are_published_by_a_rerun(pub_remote, tmp_path, monkeypatch):
    real = shortlinks._git

    def broken_commit(repo_path, *args, **kwargs):
        if args[:1] == ("commit-tree",):
            raise subprocess.CalledProcessError(1, "git commit-tree")
        return real(repo_path, *args, **kwargs)

    batch = shortlinks.Batch()
    batch.add("k_a_2025", "https://a.example.org/")
    monkeypatch.setattr(shortlinks, "_git", broken_commit)
    with pytest.raises(subprocess.CalledProcessError):
        batch.publish()
    monkeypatch.setattr(shortlinks, "_git", real)
    rerun = shortlinks.Batch()
    assert rerun.add("k_a_2025", "https://a.example.org/") is False  # already in the written links.json
    assert rerun.publish() is True
    assert "k_a_2025" in remote_links(pub_remote, tmp_path)


def test_publish_with_nothing_new_does_not_commit(pub_remote):
    before = remote_commits(pub_remote)
    batch = shortlinks.Batch()
    assert batch.add("test", "https://switch.box/") is False
    assert batch.publish() is False
    assert remote_commits(pub_remote) == before


def test_add_refuses_to_overwrite_but_repoint_moves(pub_remote, tmp_path):
    first = shortlinks.Batch()
    first.add("k_a_2025", "https://a.example.org/")
    first.publish()
    second = shortlinks.Batch()
    with pytest.raises(shortlinks.ShortLinkError):
        second.add("k_a_2025", "https://elsewhere.example.org/")
    assert second.repoint("k_a_2025", "https://web.archive.org/web/2026/https://a.example.org/") is True
    second.publish()
    assert remote_links(pub_remote, tmp_path)["k_a_2025"].startswith("https://web.archive.org/")


def test_clone_is_created_then_pulled(pub_remote, tmp_path):
    repo = shortlinks.ensure_clone()
    assert repo == shortlinks.clone_dir() and (repo / "links.json").exists()
    other = tmp_path / "other"
    subprocess.run(["git", "clone", str(pub_remote), str(other)], check=True, capture_output=True)
    shortlinks.save_links(other, {**shortlinks.load_links(other), "k_c_2025": "https://c.example.org/"})
    _git("add", ".", cwd=other)
    _git("commit", "-m", "someone else", cwd=other)
    _git("push", cwd=other)
    assert shortlinks.resolve("k_c_2025") == "https://c.example.org/"  # resolve() pulls first


def test_push_rejected_because_someone_else_pushed_first(pub_remote, tmp_path):
    batch = shortlinks.Batch()  # clones now
    other = tmp_path / "other"
    subprocess.run(["git", "clone", str(pub_remote), str(other)], check=True, capture_output=True)
    shortlinks.save_links(other, {**shortlinks.load_links(other), "theirs_2025": "https://theirs.example.org/"})
    _git("add", ".", cwd=other)
    _git("commit", "-m", "theirs", cwd=other)
    _git("push", cwd=other)
    batch.add("mine_2025", "https://mine.example.org/")
    assert batch.publish() is True
    links = remote_links(pub_remote, tmp_path)
    assert links["theirs_2025"] and links["mine_2025"]


def test_unpushed_commit_from_an_earlier_failed_run_is_pushed(pub_remote, tmp_path):
    batch = shortlinks.Batch()
    batch.add("k_a_2025", "https://a.example.org/")
    assert batch.repo is not None
    shortlinks.save_links(batch.repo, batch._links or {})
    _git("add", ".", cwd=batch.repo)
    _git("commit", "-m", "local only", cwd=batch.repo)
    rerun = shortlinks.Batch()
    assert rerun.get("k_a_2025") == "https://a.example.org/"
    assert rerun.add("k_a_2025", "https://a.example.org/") is False
    assert rerun.publish() is True
    assert "k_a_2025" in remote_links(pub_remote, tmp_path)
