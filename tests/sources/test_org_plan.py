from __future__ import annotations

from typing import Any

import pytest

from lib.sources import cleanup, item_fixes, org_plan, org_proposals, orgs, review_sheet, snapshot


def _item(key: str, **data: Any) -> dict[str, Any]:
    base = {"itemType": "report", "title": "Gas Rate Study", "date": "2024", "creators": [], "collections": ["R"]}
    return {"key": key, "data": {**base, **data}}


def _snap() -> dict[str, Any]:
    items = [
        _item("A", creators=[{"creatorType": "author", "name": "MA DPU"}], citationKey="madpu_GasRateStudy_2024"),
        _item(
            "B",
            creators=[{"creatorType": "author", "name": "Massachusetts Department of Public Utilities"}],
            publisher="MA DPU",
            date="5/1/2024",
            citationKey="massachusettsdepartmentofpublicutilities_GasRateStudy_2024",
        ),
        _item("C", title="Rate Case", citationKey="coned_RateCase_2024"),
        _item("D", title="Joint Filing", creators=[{"creatorType": "author", "name": "NYSEG / RG&E"}]),
        _item(
            "E",
            title="Testimony",
            creators=[{"creatorType": "author", "name": "ConEd"}],
            citationKey="coned_Testimony_2024",
        ),
        _item("F", title="mag-gas-adjustment-factors", date=""),
    ]
    cols = [{"key": "R", "data": {"name": "Reports", "parentCollection": False}}]
    return {"library_version": 1, "taken_at": "2026-10-27T00:00:00+00:00", "collections": cols, "items": items}


def _cluster(groups: list[str], name: str | None, short: str | None = None, **kw: Any) -> org_proposals.Cluster:
    ev = [{"quote": "q", "source": "s"}] if short else []
    return org_proposals.Cluster.model_validate({
        "groups": groups, "kind": kw.pop("kind", "organization"), "canonical_full_name": name, "short_form": short,
        "short_form_source": "own_usage" if short else "none", "evidence": ev, "confidence": "high", **kw,
    })  # fmt: skip


def _setup() -> tuple[dict[str, Any], list[dict], list[dict], list[org_proposals.MergedCluster], list[dict]]:
    snap = _snap()
    mentions = [orgs.mention_dict(m) for m in orgs.extract(snap, {})]
    groups = [g.as_dict() for g in orgs.group_mentions(orgs.extract(snap, {}))]
    gid = {g["norm"]: g["id"] for g in groups}
    dpu = "Massachusetts Department of Public Utilities"
    coned = "Consolidated Edison Company of New York"
    clusters = [
        _cluster([gid["ma dpu"], gid[dpu.lower()]], dpu, "MA DPU"),
        _cluster(
            [gid["coned"]],
            coned,
            "ConEd",
            item_overrides=[
                {"item": "E", "role": "creator:author", "action": "assign", "to": ["NY DPS"], "reason": "Staff"}
            ],
        ),
        _cluster([gid["nyseg rg and e"]], "New York State Electric & Gas; Rochester Gas and Electric"),
    ]
    merged, problems = org_proposals.merge(
        [org_proposals.BatchProposal(batch="B01", clusters=clusters)], {"B01": {g["id"] for g in groups}}
    )
    assert problems == []
    key_rows = snapshot.key_map(snapshot.summarize(snap), [])
    return snap, mentions, groups, merged, key_rows


def test_segment_names_matches_known_names_only() -> None:
    known = ["NYSEG", "Rochester Gas and Electric", "National Grid New York"]
    assert org_proposals.segment_names("NYSEG and Rochester Gas and Electric", known) == known[:2]
    assert org_proposals.segment_names("Rochester Gas and Electric", known) is None
    assert org_proposals.segment_names("NYSEG and Unknown Co", known) is None


def test_merge_keeps_split_clusters_apart_and_reports_conflicts() -> None:
    a = _cluster(["G1"], "New York State Electric & Gas", "NYSEG")
    b = _cluster(["G2"], "New York State Electric & Gas and Rochester Gas and Electric", same_as_groups=["G1"])
    c = _cluster(["G3"], "Rochester Gas and Electric", "RG&E")
    d = _cluster(["G4"], "Lawrence Berkeley National Laboratory", "LBNL")
    e = _cluster(["G5"], "Lawrence Berkeley National Laboratory", "Berkeley Lab")
    merged, problems = org_proposals.merge(
        [org_proposals.BatchProposal(batch="B01", clusters=[a, b, c, d, e])], {"B01": {"G1", "G2", "G3", "G4", "G5"}}
    )
    assert problems == []
    split = [m for m in merged if m.split_into]
    assert [m.groups for m in split] == [["G2"]]
    assert split[0].split_into == ["New York State Electric & Gas", "Rochester Gas and Electric"]
    found = org_proposals.conflicts(merged)
    assert [(c.field, c.options) for c in found] == [("short_form", ["Berkeley Lab", "LBNL"])]


@pytest.mark.parametrize(
    ("raw", "iso"),
    [
        ("5/1/2025", "2025-05-01"),
        ("10/2023", "2023-10"),
        ("7-14-2026", "2026-07-14"),
        ("12.30.2024", "2024-12-30"),
        ("January 31, 2022", "2022-01-31"),
        ("December, 2022", "2022-12"),
        ("Sept. 5, 2023", "2023-09-05"),
        ("2025-05-07T21:30:00Z", "2025-05-07"),
        ("2024-08-15 8/15/24", "2024-08-15"),
        ("2024", "2024"),
        ("7/142026", None),
        ("13/2024", None),
    ],
)
def test_normalize_date(raw: str, iso: str | None) -> None:
    assert org_plan.normalize_date(raw) == iso


def test_joined_short_and_item_shortauthor() -> None:
    assert org_plan.joined_short(["A", "B", "C"]) == "A, B, and C"
    assert org_plan.joined_short(["A", "B", "C", "D"]) == "A et al."
    shorts = {"new york state electric & gas": "NYSEG", "rochester gas and electric": "RG&E"}
    orgs_only = [
        {"creatorType": "author", "name": "New York State Electric & Gas"},
        {"creatorType": "author", "name": "Rochester Gas and Electric"},
    ]
    assert org_plan.item_shortauthor(orgs_only, shorts) == "NYSEG and RG&E"
    smith = {"creatorType": "author", "firstName": "Ann", "lastName": "Smith"}
    assert org_plan.item_shortauthor([*orgs_only, smith], shorts) == "NYSEG and RG&E"
    assert org_plan.item_shortauthor([smith, *orgs_only], shorts) is None


def test_build_applies_clusters_overrides_and_keys_from_scratch() -> None:
    snap, mentions, groups, merged, key_rows = _setup()
    plans = {p.item: p for p in org_plan.build(snap, mentions, groups, merged, key_rows)}
    # Abbreviated author becomes the full name; the item gets the short form; keys are recomputed.
    assert plans["A"].after["creators"] == [
        {"creatorType": "author", "name": "Massachusetts Department of Public Utilities"}
    ]
    assert "tex.shortauthor: MA DPU" in plans["A"].after["extra"]
    assert {plans["A"].key, plans["B"].key} == {"madpu_GasRateStudy_2024", "madpu_GasRateStudy_2024a"}
    # A publisher that repeats the author is removed; the US date becomes ISO.
    assert plans["B"].after["publisher"] == ""
    assert plans["B"].after["date"] == "2024-05-01"
    # The old key's author part names the issuer of an item with no creator.
    assert plans["C"].after["creators"] == [
        {"creatorType": "author", "name": "Consolidated Edison Company of New York"}
    ]
    assert plans["C"].key == "coned_RateCase_2024"
    # One string naming two organizations becomes two creators.
    assert [c["name"] for c in plans["D"].after["creators"]] == [
        "New York State Electric & Gas",
        "Rochester Gas and Electric",
    ]
    # A per-item override beats the cluster.
    assert plans["E"].after["creators"] == [{"creatorType": "author", "name": "NY DPS"}]
    assert plans["F"].key is None and any("no author" in f for f in plans["F"].flags)


def test_build_applies_fixes_and_decisions() -> None:
    snap, mentions, groups, merged, key_rows = _setup()
    fix = item_fixes.ItemFix.model_validate({
        "item": "F", "organizations": ["National Grid Massachusetts Gas"], "date": "2025-03-01",
        "title": "Gas Adjustment Factors", "evidence": [{"quote": "q", "source": "s"}], "confidence": "high",
    })  # fmt: skip
    dpu_cluster = next(m.id for m in merged if m.proposals[0].short_form == "MA DPU")
    decisions = {dpu_cluster: {"short_form": "DPU-MA"}}
    plans = {p.item: p for p in org_plan.build(snap, mentions, groups, merged, key_rows, decisions, {"F": fix})}
    assert plans["F"].key == "nationalgridmassachusettsgas_GasAdjustmentFactors_2025"
    assert (plans["A"].key or "").startswith("dpuma_")


def test_rulings_override_clusters_and_fixes() -> None:
    snap, mentions, groups, merged, key_rows = _setup()
    rulings = {
        "A": {"reason": "Q05", "creators": ["Gannett Fleming"], "fields": {"institution": "MA DPU"}},
        "B": {"reason": "dup", "action": "duplicate", "duplicate_of": "A"},
        "E": {"reason": "people", "creators": [{"lastName": "Vu", "firstName": "Tiffany"}]},
    }
    plans = {p.item: p for p in org_plan.build(snap, mentions, groups, merged, key_rows, rulings=rulings)}
    assert plans["A"].key == "gannettfleming_GasRateStudy_2024"
    assert plans["A"].after["institution"] == "MA DPU"
    assert plans["B"].action == "duplicate" and plans["B"].key is None
    assert plans["E"].key == "vu_Testimony_2024"


@pytest.mark.parametrize(
    ("creator", "from_zotero", "expected"),
    [
        ({"name": "Roderick Go"}, True, {"firstName": "Roderick", "lastName": "Go"}),
        ({"name": "Roderick Go"}, False, {"name": "Roderick Go"}),
        ({"name": "Pigman, Margaret"}, False, {"firstName": "Margaret", "lastName": "Pigman"}),
        ({"name": "Kristin George Bagdanov"}, True, {"firstName": "Kristin", "lastName": "George Bagdanov"}),
        ({"name": "Gannett Fleming"}, True, {"name": "GFT"}),
        ({"name": "Potomac Edison"}, True, {"name": "Potomac Edison"}),
    ],
)
def test_canonical_creator(creator: dict, from_zotero: bool, expected: dict) -> None:
    got = org_plan.canonical_creator(
        {"creatorType": "author", **creator},
        {"gannett fleming": "GFT"},
        {"kristin george bagdanov": ("Kristin", "George Bagdanov")},
        from_zotero=from_zotero,
        not_people=frozenset({"potomac edison"}),
    )
    assert got == {"creatorType": "author", **expected}


def test_item_fix_validation() -> None:
    ev = [{"quote": "q", "source": "s"}]
    with pytest.raises(ValueError):
        item_fixes.ItemFix.model_validate({"item": "X", "date": "May 2024", "evidence": ev, "confidence": "high"})
    with pytest.raises(ValueError):
        item_fixes.ItemFix.model_validate({"item": "X", "evidence": ev, "confidence": "high"})
    item_fixes.ItemFix.model_validate({"item": "X", "action": "delete", "evidence": ev, "confidence": "high"})


def test_duplicate_sets_and_review_round_trip() -> None:
    snap, mentions, groups, merged, key_rows = _setup()
    snap["items"] += [
        {"key": "P1", "data": {"itemType": "attachment", "parentItem": "A", "md5": "abc"}},
        {"key": "P2", "data": {"itemType": "attachment", "parentItem": "B", "md5": "abc"}},
    ]
    plans = [p.__dict__ for p in org_plan.build(snap, mentions, groups, merged, key_rows)]
    dups = cleanup.duplicate_sets(snap, plans)
    assert [(d["reason"], sorted(d["items"])) for d in dups] == [("same attached file", ["A", "B"])]

    tabs = review_sheet.build_tabs(plans, [m.model_dump() for m in merged], groups, [], [], [])
    header = tabs["Clusters"][0]
    row = tabs["Clusters"][1]
    row[header.index("your_short_form")] = "none"
    decisions, other = review_sheet.answers_from(tabs)
    assert decisions == {row[0]: {"short_form": ""}}
    assert other["items"] == {}


@pytest.mark.parametrize(
    ("key", "creator", "extra_text", "expected"),
    [
        (
            "nyseg_Order_2024",
            {"name": "New York State Electric & Gas"},
            "tex.shortauthor: NYSEG",
            "organization; short form",
        ),
        ("eversourceconnecticut_X_2026", {"name": "Eversource Connecticut"}, "", "organization without a short form"),
        ("ghafri_X_2020", {"firstName": "Saif ZS Al", "lastName": "Ghafri"}, "", "person: check"),
        ("villanueva_X_2024", {"firstName": "Sen Celina", "lastName": "Villanueva"}, "", "person: check"),
        ("henchen_X_2025", {"firstName": "Mike", "lastName": "Henchen"}, "", "long surname"),
        ("vu_X_2025", {"firstName": "Tiffany", "lastName": "Vu"}, "", ""),
    ],
)
def test_key_check(key: str, creator: dict, extra_text: str, expected: str) -> None:
    plan = {"key": key, "after": {"creators": [{"creatorType": "author", **creator}], "extra": extra_text}}
    got = review_sheet.key_check(plan)
    assert got.startswith(expected) and (bool(got) == bool(expected))


def test_carry_answers_keeps_reviewer_columns_by_id() -> None:
    tabs = {"Questions": [["id", "question", "your_answer"], ["Q1", "new text", ""], ["Q2", "b", ""]]}
    previous = {"Questions": [["id", "question", "your_answer"], ["Q2", "b", "yes"], ["Q9", "gone", "x"]]}
    saved = review_sheet.answers_as_tabs({}, {"questions": {"Q1": "keep"}, "items": {}})
    got = review_sheet.carry_answers(review_sheet.carry_answers(tabs, previous), saved)
    assert got["Questions"] == [["id", "question", "your_answer"], ["Q1", "new text", "keep"], ["Q2", "b", "yes"]]


def test_table_short_forms_reads_subsidiary_table() -> None:
    md = """
| legal company | parent | full name | short form | key part |
| --- | --- | --- | --- | --- |
| The Connecticut Light and Power Company | Eversource | Eversource Connecticut | CL&P | `clp` |
| New England Power Company | National Grid | New England Power | NEP (verify) | `nep` |
| Eversource Energy | | Eversource | (none) | `eversource` |
"""
    assert org_plan.table_short_forms(md) == {"Eversource Connecticut": "CL&P", "New England Power": "NEP"}
