from lib.sources import extra, org_apply


def _plan(**kw):
    before = {"itemType": "report", "creators": [{"creatorType": "author", "name": "DPU"}], "date": "2024"}
    after = {
        **before,
        "creators": [{"creatorType": "author", "name": "Massachusetts Department of Public Utilities"}],
        "institution": "",
        "date": "2024-03-05",
        "citationKey": "old_Key_2024",
        "extra": "tex.shortauthor: MA DPU",
    }
    return {"action": "update", "key": "madpu_Order_2024", "before": before, "after": after, **kw}


def test_target_data_pins_key_and_clears_native() -> None:
    data = org_apply.target_data(_plan())
    assert data is not None
    assert extra.get(data["extra"], extra.CITATION_KEY) == "madpu_Order_2024"
    assert extra.get(data["extra"], extra.SHORTAUTHOR) == "MA DPU"
    assert data["citationKey"] == ""
    assert org_apply.target_data(_plan(action="duplicate")) is None


def test_preview_csl_redoes_changed_variables_only() -> None:
    p = _plan()
    p["before"]["institution"] = "DPU"
    csl = {
        "id": "x",
        "author": [{"literal": "DPU"}],
        "publisher": "DPU",
        "issued": {"date-parts": [[2024]]},
        "URL": "u",
    }
    out = org_apply.preview_csl(csl, p["before"], p["after"])
    assert out["author"] == [{"literal": "Massachusetts Department of Public Utilities"}]
    assert "publisher" not in out
    assert out["issued"] == {"date-parts": [[2024, 3, 5]]}
    assert out["URL"] == "u"
