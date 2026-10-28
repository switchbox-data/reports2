"""Front-matter edits touch only the fields being changed; the body and comments survive."""

from __future__ import annotations

from lib.sources import frontmatter

REAL_SHAPED = """---
source: papuc_R-2024-3046523_20240320_st15_coleman_direct_ev_tou_rates_rs_rh_ra.pdf
docket: R-2024-3046523
utility: Duquesne Light Company
rate: RS, RH, RA
filing_date: March 20, 2024
filer: David C. Coleman, Manager, Rates and Regulatory Strategy, for Duquesne Light Company (Duquesne Light Statement No. 15)
document_type: testimony (direct)
pages_total: 26
extraction_scope: full
source_url: https://www.puc.pa.gov/pcdocs/1823419.pdf  # from the docket index, not the filing itself
original_pdf_path: /ebs/home/staging/pa_duquesne/papuc_st15.pdf
why_here: >
  Coleman testimony comparing proposed RA, RH and RS rates, including the
  argument that TOU is not cost-reflective for heat pump customers.
---

# Statement No. 15

Body with a --- rule below.

---

More text.
"""

IDS = {
    "citekey": "papuc_Docket20243046523Direct_2024",
    "zotero_item": "ABCD1234",
    "short_url": "https://pub.switch.box/papuc_Docket20243046523Direct_2024",
    "md5": "9b2c0123456789abcdef0123456789ab",
    "validated": "2026-10-28",
}


def test_round_trip_converts_legacy_fields_and_keeps_everything_else():
    out = frontmatter.to_flat(REAL_SHAPED, IDS)
    fm = frontmatter.parse(out)
    assert fm["source_file"].startswith("papuc_R-2024-3046523_20240320_st15")
    assert "source" not in fm and "original_pdf_path" not in fm
    assert {k: fm[k] for k in IDS} == IDS
    assert fm["docket"] == "R-2024-3046523" and fm["pages_total"] == 26 and fm["extraction_scope"] == "full"
    assert fm["why_here"].startswith("Coleman testimony comparing")
    # The author's inline comment and the body (including a horizontal rule) are untouched.
    assert "# from the docket index, not the filing itself" in out
    assert out.split("\n---\n", 1)[1] == REAL_SHAPED.split("\n---\n", 1)[1]


def test_new_ids_are_inserted_in_canonical_order():
    out = frontmatter.to_flat(REAL_SHAPED, IDS)
    keys = [
        line.split(":")[0] for line in out.split("\n---\n")[0].splitlines()[1:] if line and not line.startswith(" ")
    ]
    ids = [k for k in keys if k in frontmatter.ID_FIELDS]
    assert ids == [k for k in frontmatter.ID_FIELDS if k in ids]
    assert keys[0] == "source_file"


def test_conversion_is_idempotent():
    once = frontmatter.to_flat(REAL_SHAPED, IDS)
    assert frontmatter.to_flat(once, IDS) == once


def test_changed_value_keeps_the_inline_comment():
    out = frontmatter.edit(REAL_SHAPED, {"source_url": "https://www.puc.pa.gov/pcdocs/other.pdf"})
    assert "source_url: https://www.puc.pa.gov/pcdocs/other.pdf  # from the docket index" in out


def test_md5_and_zotero_item_are_quoted():
    out = frontmatter.edit(REAL_SHAPED, {"md5": "1e50000000000000000000000000001", "zotero_item": "12345678"})
    assert 'md5: "1e50000000000000000000000000001"' in out and 'zotero_item: "12345678"' in out
    assert frontmatter.parse(out)["zotero_item"] == "12345678"


def test_remove_and_rename_without_front_matter_raises(tmp_path):
    path = tmp_path / "plain.md"
    path.write_text("# no front matter\n")
    assert frontmatter.parse(path.read_text()) == {} and frontmatter.read(path) == {}
    try:
        frontmatter.update(path, {"citekey": "x"})
    except ValueError as e:
        assert "no front matter" in str(e)
    else:
        raise AssertionError("expected ValueError")


def test_update_writes_only_when_changed(tmp_path):
    path = tmp_path / "x.md"
    path.write_text(REAL_SHAPED)
    assert frontmatter.update(path, IDS, remove=("original_pdf_path",), rename={"source": "source_file"}) is True
    assert frontmatter.update(path, IDS) is False


def test_write_creates_canonical_order(tmp_path):
    path = tmp_path / "sub" / "stub.md"
    frontmatter.write(
        path, {"docket": "25-55", "citekey": "k_X_2025", "md5": "abc", "source_file": "m.xlsx"}, "# Title\n"
    )
    lines = path.read_text().splitlines()
    assert lines[1:5] == ["source_file: m.xlsx", "citekey: k_X_2025", 'md5: "abc"', "docket: 25-55"]
    assert path.read_text().endswith("---\n\n# Title\n")


def test_find_by_citekey_in_nested_folders(tmp_path):
    deep = tmp_path / "il_hp_rates" / "tou" / "comed"
    deep.mkdir(parents=True)
    (deep / "a.md").write_text("---\ncitekey: comed_A_2025\n---\n\nBody\n")
    (tmp_path / "b.md").write_text("---\ncitekey: other_B_2025\n---\n\nBody\n")
    (tmp_path / "README.md").write_text("---\ncitekey: comed_A_2025\n---\n")
    assert frontmatter.find_by_citekey("comed_A_2025", tmp_path) == deep / "a.md"
    assert frontmatter.find_by_citekey("missing", tmp_path) is None


def test_dates_parse_as_iso_strings():
    assert frontmatter.parse("---\nvalidated: 2026-10-28\nfiling_date: March 20, 2024\n---\n") == {
        "validated": "2026-10-28",
        "filing_date": "March 20, 2024",
    }
