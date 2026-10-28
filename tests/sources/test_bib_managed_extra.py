"""The public-copy lines ingest writes to Extra never reach references.yaml."""

from __future__ import annotations

from lib.sources import bib

EXTRA = (
    "Citation Key: madpu_Docket2555Order_2025\n"
    "tex.shortauthor: MA DPU\n"
    "DocumentCloud ID: 12345\n"
    "Google Drive ID: 1AbC\n"
    "Wayback URL: https://web.archive.org/web/2026/https://x.org\n"
    "_eprint: 2410.04540"
)


def test_managed_lines_are_stripped_from_the_csl_note():
    item = {
        "key": "A1",
        "data": {"key": "A1", "itemType": "report", "extra": EXTRA, "citationKey": ""},
        "csljson": {"id": "1/A1", "type": "report", "title": "Order", "note": EXTRA},
    }
    record, _ = bib.build_record(item, "madpu_Docket2555Order_2025")
    assert record["note"] == "_eprint: 2410.04540"
    assert record["author-short"] == "MA DPU"


def test_note_disappears_when_only_managed_lines_remain():
    only = EXTRA.split("\n_eprint")[0]
    item = {
        "key": "A1",
        "data": {"key": "A1", "itemType": "report", "extra": only, "citationKey": ""},
        "csljson": {"id": "1/A1", "type": "report", "title": "Order", "note": only},
    }
    record, _ = bib.build_record(item, "madpu_Docket2555Order_2025")
    assert "note" not in record
