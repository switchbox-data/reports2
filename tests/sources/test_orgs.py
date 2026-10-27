from __future__ import annotations

from typing import Any

import pytest

from lib.sources import org_proposals, orgs


@pytest.mark.parametrize(
    ("raw", "norm"),
    [
        ("The Brooklyn Union Gas Company, Inc.", "brooklyn union gas company"),
        ("Orange & Rockland", "orange and rockland"),
        ("ISO-NE", "iso ne"),
        ("Rábago Energy LLC", "rabago energy"),
        ("National Grid (Upstate)", "national grid upstate"),
    ],
)
def test_normalize(raw: str, norm: str) -> None:
    assert orgs.normalize(raw) == norm


def test_acronyms_with_state_prefix() -> None:
    assert orgs.acronyms("massachusetts department of public utilities") == {"dpu", "madpu", "mdpu"}
    assert "nyserda" in orgs.acronyms("new york state energy research and development authority")
    assert orgs.acronyms("nyserda") == set()


@pytest.mark.parametrize(
    ("creator", "kind", "shape"),
    [
        ({"name": "Massachusetts Department of Public Utilities"}, "org", "single"),
        ({"name": "Jesse Dakss"}, "person", "single"),
        ({"name": "NYSEG / RG&E"}, "org", "single"),
        ({"firstName": "", "lastName": "NYSERDA"}, "org", "two"),
        ({"firstName": "Boston Gas", "lastName": "Company"}, "org", "two"),
        ({"firstName": "Ignacio", "lastName": "Pérez-Arriaga"}, "person", "two"),
        ({"firstName": "J.", "lastName": "NREL"}, "ambiguous", "two"),
    ],
)
def test_classify_creator(creator: dict[str, str], kind: str, shape: str) -> None:
    assert orgs.classify_creator(creator)[1:] == (kind, shape)


def _snap() -> dict[str, Any]:
    cols = [{"key": "R", "data": {"name": "Reports", "parentCollection": False}}]

    def item(key: str, **data: Any) -> dict[str, Any]:
        base = {"itemType": "report", "title": "T", "date": "2024", "creators": [], "collections": ["R"]}
        return {"key": key, "data": {**base, **data}}

    items = [
        item("A", creators=[{"creatorType": "author", "name": "MA DPU"}], citationKey="madpu_T_2024"),
        item(
            "B",
            creators=[{"creatorType": "author", "name": "Massachusetts Department of Public Utilities"}],
            publisher="MA DPU",
            citationKey="massachusettsdepartmentofpublicutilities_T_2024",
        ),
        item("C", citationKey="coned_T_2024"),
        item("D", creators=[{"creatorType": "author", "name": "ConEd"}], citationKey="coned_U_2024"),
        item("E", creators=[{"creatorType": "author", "name": "NYSEG / RG&E"}], citationKey="nyseg_T_2024"),
        item("F", creators=[{"creatorType": "author", "name": "NYSEG"}], citationKey="nyseg_U_2024"),
        item(
            "G",
            creators=[{"creatorType": "author", "firstName": "Ann", "lastName": "Smith"}],
            citationKey="smith_T_2024",
        ),
    ]
    return {"library_version": 1, "taken_at": "2026-10-27T00:00:00+00:00", "collections": cols, "items": items}


def test_extract_groups_and_edges() -> None:
    snap = _snap()
    mentions = orgs.extract(snap, {"coned_T_2024": 3})
    assert {m.kind for m in mentions if m.item == "G"} == {"person"}
    key_author = [m for m in mentions if m.role == "key_author"]
    assert [(m.item, m.text, m.cited) for m in key_author] == [("C", "coned", 3)]
    groups = orgs.group_mentions(mentions)
    by_norm = {g.norm: g for g in groups}
    assert by_norm["coned"].items == {"C", "D"}
    assert by_norm["ma dpu"].items == {"A", "B"}
    edges = orgs.candidate_edges(groups, mentions)
    reasons = {(by_norm_id(groups, e.a), by_norm_id(groups, e.b), e.reason) for e in edges}
    full = "massachusetts department of public utilities"
    assert (*sorted(("ma dpu", full)), "acronym") in {(*sorted(r[:2]), r[2]) for r in reasons}
    assert any(r[2] == "author_publisher" for r in reasons)
    assert any(r[2] == "split_part" and "nyseg" in r[:2] for r in reasons)
    comps = orgs.components(groups, edges)
    assert any({by_norm["ma dpu"].id, by_norm[full].id} <= set(c) for c in comps)


def by_norm_id(groups: list[orgs.OrgGroup], gid: str) -> str:
    return next(g.norm for g in groups if g.id == gid)


def test_split_parts_keeps_and_inside_names() -> None:
    known = {n: orgs.OrgGroup(id=n, norm=n) for n in ("nyseg", "rg and e", "national grid")}
    assert [p for p, _ in orgs.split_parts("NYSEG / RG&E", known)] == ["NYSEG", "RG&E"]
    assert orgs.split_parts("Public Service Electric and Gas Company", known) == []


def test_batches_never_split_a_component() -> None:
    assert orgs.batches([["a", "b", "c"], ["d"], ["e", "f"]], size=4) == [["a", "b", "c", "d"], ["e", "f"]]


def _cluster(**kw: Any) -> dict[str, Any]:
    base = {"groups": ["G1"], "kind": "organization", "canonical_full_name": "X", "confidence": "high"}
    return {**base, **kw}


def test_cluster_validation() -> None:
    ev = [{"quote": "q", "source": "s"}]
    org_proposals.Cluster.model_validate(_cluster(short_form="ICC", short_form_source="own_usage", evidence=ev))
    for bad in (
        _cluster(short_form="ICC", evidence=ev),
        _cluster(short_form="ICC", short_form_source="own_usage"),
        _cluster(short_form="DPU", short_form_source="own_usage", evidence=ev),
        _cluster(canonical_full_name=None),
    ):
        with pytest.raises(ValueError):
            org_proposals.Cluster.model_validate(bad)


def test_merge_coverage_same_as_and_names() -> None:
    p1 = org_proposals.BatchProposal(
        batch="B01",
        clusters=[
            org_proposals.Cluster.model_validate(_cluster(groups=["G1"], same_as_groups=["G9"])),
            org_proposals.Cluster.model_validate(_cluster(groups=["G2"], canonical_full_name="Y")),
        ],
    )
    p2 = org_proposals.BatchProposal(
        batch="B02",
        clusters=[
            org_proposals.Cluster.model_validate(_cluster(groups=["G9"])),
            org_proposals.Cluster.model_validate(_cluster(groups=["G8"], canonical_full_name="y")),
        ],
    )
    merged, problems = org_proposals.merge([p1, p2], {"B01": {"G1", "G2", "G3"}, "B02": {"G8", "G9"}})
    assert sorted(m.groups for m in merged) == [["G1", "G9"], ["G2", "G8"]]
    assert problems == ["B01: groups not assigned: G3"]
