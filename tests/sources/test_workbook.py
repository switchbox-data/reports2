from __future__ import annotations

from lib.sources import frontmatter, workbook


def test_size_limit_matches_the_commit_hook(tmp_path):
    small, big = tmp_path / "s.xlsx", tmp_path / "b.xlsx"
    small.write_bytes(b"x" * 600 * 1024)
    big.write_bytes(b"x" * (600 * 1024 + 1))
    assert not workbook.too_large(small) and workbook.too_large(big)
    assert not workbook.needs_decision(small, None)
    assert workbook.needs_decision(big, None)
    assert not workbook.needs_decision(big, True) and not workbook.needs_decision(big, False)


def test_copy_into_repo_is_idempotent(tmp_path):
    src, dest = tmp_path / "m.xlsx", tmp_path / "repo" / "sources" / "m.xlsx"
    src.write_bytes(b"PK data")
    assert workbook.copy_into_repo(src, dest) is True
    assert workbook.copy_into_repo(src, dest) is False
    src.write_bytes(b"PK changed")
    assert workbook.copy_into_repo(src, dest) is True and dest.read_bytes() == b"PK changed"


def test_stub_is_written_once_and_front_matter_refreshed(tmp_path):
    stub = tmp_path / "m.md"
    workbook.write_stub(stub, {"citekey": "k_M_2025", "repo_file": "m.xlsx"}, "Model", "Rate design model.")
    assert stub.read_text().endswith("# Model\n\nRate design model.\n")
    workbook.write_stub(stub, {"citekey": "k_M_2025", "repo_file": workbook.NOT_IN_REPO}, "Model", "ignored")
    text = stub.read_text()
    assert text.endswith("# Model\n\nRate design model.\n")
    assert frontmatter.parse(text)["repo_file"] == "not in repo: fetch from Zotero"
