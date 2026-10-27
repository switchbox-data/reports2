"""The library-cleanup review sheet: build its tabs, push them to Google Sheets and read answers back.

``build_tabs`` is pure (rows from the plan, clusters, conflicts, questions and cleanup actions), so
the CSV copies and the Google Sheet always match. Reviewers type only in the ``your_*`` columns;
``pull`` reads those back into ``decisions.json`` (cluster names and short forms, which ``orgs-plan``
applies) and ``answers.json`` (item verdicts, question and cleanup answers).
"""

from __future__ import annotations

import csv
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from lib.sources import citekeys, extra

Rows = list[list[Any]]

CLUSTER_COLS = [
    "cluster", "status", "kind", "proposed_full_name", "proposed_short_form", "short_form_source", "confidence",
    "names_in_library", "n_items", "n_cited_items", "evidence", "agent_notes", "flags", "batches",
    "your_full_name", "your_short_form", "your_kind", "your_comment",
]  # fmt: skip
ITEM_COLS = [
    "item", "scope", "cited_as", "old_keys", "new_key", "short_form", "key_check", "action", "authors_before",
    "authors_after", "changes", "flags", "title", "your_verdict", "your_comment",
]  # fmt: skip
KEY_COLS = ["item", "old_keys", "new_key", "short_form", "key_check", "key_changes", "cited_as", "title"]
LONG_KEY_COLS = [
    "author_part", "check", "first_author", "short_form", "n_items", "n_cited", "example_keys", "items",
    "your_short_form", "your_comment",
]  # fmt: skip
LONG_AUTHOR_PART = 4
QUESTION_COLS = ["id", "question", "options", "comes_up_in", "your_answer"]
CLEANUP_COLS = ["id", "needs_you", "type", "items", "description", "proposed_action", "your_answer"]
YOURS = ("your_full_name", "your_short_form", "your_kind", "your_comment", "your_verdict", "your_answer")
_CELL_MAX = 45_000  # Sheets rejects cells over 50,000 characters


def _cell(v: Any) -> Any:
    if isinstance(v, list | tuple | set):
        v = "\n".join(str(x) for x in v)
    if isinstance(v, str) and len(v) > _CELL_MAX:
        v = v[:_CELL_MAX] + " [truncated]"
    return "" if v is None else v


def _authors(creators: Iterable[Mapping[str, str]]) -> str:
    out = []
    for c in creators:
        name = c.get("name") or ", ".join(x for x in (c.get("lastName"), c.get("firstName")) if x)
        out.append(f"{name} ({c.get('creatorType', 'author')})")
    return "\n".join(out)


def short_form(p: Mapping[str, Any]) -> str:
    try:
        return extra.get(p["after"].get("extra"), extra.SHORTAUTHOR) or ""
    except extra.ExtraError:
        return ""


def _first_author(p: Mapping[str, Any]) -> Mapping[str, str] | None:
    ordered = citekeys._ordered_creators(p["after"].get("creators", []))
    return ordered[0] if ordered else None


def key_check(p: Mapping[str, Any]) -> str:
    """Why a key's author part is longer than four characters, or "" if it isn't."""
    if not p["key"] or len(p["key"].split("_", 1)[0]) <= LONG_AUTHOR_PART:
        return ""
    first = _first_author(p)
    if first is None:
        return "long author part"
    if citekeys._is_org(first):
        sf = short_form(p)
        return f"organization; short form {sf!r} is long" if sf else "organization without a short form"
    given, last = (first.get("firstName") or "").strip(), (first.get("lastName") or "").strip()
    if not given or " " in last or _MISSPLIT_GIVEN.search(given) or f"{given} {last}".casefold() in _ORG_AS_PERSON:
        return "person: check the name is split into first and last"
    return "long surname (probably fine)"


# A surname particle left in the given name ("Saif Al" + "Ghafri"), or a title ("Sen. Celina").
_MISSPLIT_GIVEN = re.compile(
    r"(?i)(?:\s(?:al|el|van|von|der|de|da|di|du|la|le|bin|ibn|st\.?)$)|^(?:sen|rep|dr|hon|mr|mrs|ms|prof)\.?\s"
)
_ORG_AS_PERSON = frozenset({"con edison"})


def cluster_rows(
    merged: Sequence[Mapping[str, Any]], groups: Sequence[Mapping[str, Any]], conflicts: Sequence[Mapping[str, Any]]
) -> Rows:
    by_group = {g["id"]: g for g in groups}
    conflicted = {c for x in conflicts for c in x["cluster"].split(", ")}
    rows: Rows = [CLUSTER_COLS]
    order = sorted(
        merged, key=lambda m: (not any(p["needs_decision"] for p in m["proposals"]), m["id"] not in conflicted, m["id"])
    )
    for m in order:
        props = m["proposals"]
        first = props[0]
        gs = [by_group[g] for g in m["groups"] if g in by_group]
        variants: dict[str, int] = {}
        for g in gs:
            for v, n in g["variants"].items():
                variants[v] = variants.get(v, 0) + n
        status = []
        if any(p["needs_decision"] for p in props):
            status.append("NEEDS YOUR DECISION")
        if m["id"] in conflicted:
            status.append("batches disagree")
        kind = "split" if m["split_into"] else first["kind"]
        full = (
            " | ".join(m["split_into"])
            if m["split_into"]
            else " | ".join(dict.fromkeys(p["canonical_full_name"] or "" for p in props))
        )
        rows.append([
            m["id"], "; ".join(status) or "ok", kind, full,
            " | ".join(dict.fromkeys(p["short_form"] or "" for p in props)).strip(" |"),
            first["short_form_source"], first["confidence"],
            "; ".join(f"{v} ({n})" for v, n in sorted(variants.items(), key=lambda x: -x[1])[:8]),
            len({i for g in gs for i in g["items"]}), sum(g["n_cited_items"] for g in gs),
            [f"\u201c{e['quote']}\u201d ({e['source']})" for p in props for e in p["evidence"][:2]],
            [p["notes"] for p in props if p["notes"]],
            sorted({f for p in props for f in p["flags"]}), m["batches"], "", "", "", "",
        ])  # fmt: skip
    return rows


def item_rows(plans: Sequence[Mapping[str, Any]]) -> Rows:
    rows: Rows = [ITEM_COLS]
    shown = [p for p in plans if p["changes"] or p["flags"] or p["key"] not in p["old_keys"]]
    shown.sort(key=lambda p: (not p["flags"], not p["cited"], p["item"]))
    for p in shown:
        rows.append([
            p["item"], p["scope"], p["cited"], p["old_keys"], p["key"] or "", short_form(p), key_check(p), p["action"],
            _authors(p["before"].get("creators", [])), _authors(p["after"].get("creators", [])),
            p["changes"], p["flags"], p["after"].get("title") or p["before"].get("title") or "", "", "",
        ])  # fmt: skip
    return rows


def key_rows(plans: Sequence[Mapping[str, Any]]) -> Rows:
    rows: Rows = [KEY_COLS]
    for p in sorted(plans, key=lambda p: (not p["cited"], p["key"] or "")):
        changed = "same" if p["key"] in p["old_keys"] else ("no key yet" if not p["key"] else "new")
        rows.append([
            p["item"], p["old_keys"], p["key"] or "", short_form(p), key_check(p), changed, p["cited"],
            p["after"].get("title") or "",
        ])  # fmt: skip
    return rows


def long_key_rows(plans: Sequence[Mapping[str, Any]]) -> Rows:
    """One row per author part over four characters, organizations without a short form first."""
    groups: dict[str, list[Mapping[str, Any]]] = {}
    for p in plans:
        if key_check(p):
            groups.setdefault(p["key"].split("_", 1)[0], []).append(p)
    order = ["organization without a short form", "person: check", "organization; short form", "long"]

    def rank(item: tuple[str, list[Mapping[str, Any]]]) -> tuple[int, int, str]:
        check = key_check(item[1][0])
        return (next(i for i, o in enumerate(order) if check.startswith(o)), -len(item[1]), item[0])

    rows: Rows = [LONG_KEY_COLS]
    for part, ps in sorted(groups.items(), key=rank):
        first = _first_author(ps[0]) or {}
        name = first.get("name") or ", ".join(x for x in (first.get("lastName"), first.get("firstName")) if x)
        rows.append([
            part, key_check(ps[0]), name, short_form(ps[0]), len(ps), sum(bool(p["cited"]) for p in ps),
            [p["key"] for p in ps[:3]], [p["item"] for p in ps], "", "",
        ])  # fmt: skip
    return rows


def question_rows(questions: Sequence[Mapping[str, Any]]) -> Rows:
    rows: Rows = [QUESTION_COLS]
    for q in questions:
        rows.append([q["id"], q["question"], q.get("options", []), q.get("comes_up_in", ""), ""])
    return rows


def cleanup_rows(actions: Sequence[Mapping[str, Any]]) -> Rows:
    rows: Rows = [CLEANUP_COLS]
    for a in actions:
        rows.append([
            a["id"],
            "yes" if a.get("needs_you") else "",
            a["type"],
            a.get("items", []),
            a["description"],
            a.get("proposed_action", ""),
            "",
        ])  # fmt: skip
    return rows


def summary_rows(
    plans: Sequence[Mapping[str, Any]], merged: Sequence[Mapping[str, Any]], n_questions: int, n_cleanup: int
) -> Rows:
    keyed = [p for p in plans if p["key"]]
    return [
        ["Switchbox Zotero cleanup: review"],
        [""],
        [
            "Nothing has been written to Zotero. Type only in the yellow your_* columns; blank means accept the proposal."
        ],
        ["1. Questions: answer each once; the answers apply everywhere the question comes up."],
        [
            "2. Clusters: one row per organization. Rows needing your decision are first. Edit your_full_name / your_short_form / your_kind to override."
        ],
        ["3. Items: every item whose metadata or key changes. your_verdict = reject to leave an item alone."],
        ["4. Citation keys: every new key, from scratch. Cited keys are rewritten in reports by rekey-refs."],
        ["5. Cleanup: duplicates, deletions and other one-off fixes."],
        [
            "6. Long keys: keys whose author part is over four characters. Give an organization a short form in your_short_form (it applies to all its items); for a person, say in your_comment if the name is split wrong."
        ],
        [""],
        ["items in Reports and Inbox", len(plans)],
        ["items with metadata changes", sum(bool(p["changes"]) for p in plans)],
        ["items flagged for a look", sum(bool(p["flags"]) for p in plans)],
        ["organization clusters", len(merged)],
        ["clusters needing your decision", sum(any(x["needs_decision"] for x in m["proposals"]) for m in merged)],
        ["keys assigned", len(keyed)],
        ["keys unchanged", sum(p["key"] in p["old_keys"] for p in keyed)],
        ["cited items whose key changes", sum(1 for p in keyed if p["cited"] and p["key"] not in p["old_keys"])],
        ["items to the trash (duplicates, empty)", sum(p["action"] != "update" for p in plans)],
        ["items still without an author (no key)", sum(p["action"] == "update" and not p["key"] for p in plans)],
        ["questions", n_questions],
        ["cleanup actions", n_cleanup],
    ]


def build_tabs(
    plans: Sequence[Mapping[str, Any]],
    merged: Sequence[Mapping[str, Any]],
    groups: Sequence[Mapping[str, Any]],
    conflicts: Sequence[Mapping[str, Any]],
    questions: Sequence[Mapping[str, Any]],
    cleanup: Sequence[Mapping[str, Any]],
) -> dict[str, Rows]:
    tabs = {
        "Summary": summary_rows(plans, merged, len(questions), len(cleanup)),
        "Questions": question_rows(questions),
        "Clusters": cluster_rows(merged, groups, conflicts),
        "Items": item_rows(plans),
        "Citation keys": key_rows(plans),
        "Long keys": long_key_rows(plans),
        "Cleanup": cleanup_rows(cleanup),
    }
    return {name: [[_cell(v) for v in row] for row in rows] for name, rows in tabs.items()}


def carry_answers(tabs: Mapping[str, Rows], previous: Mapping[str, Rows]) -> dict[str, Rows]:
    """``tabs`` with the reviewer columns filled from ``previous`` rows that have the same ID (first column)."""
    out: dict[str, Rows] = {}
    for name, rows in tabs.items():
        old = _records(previous[name]) if previous.get(name) else []
        by_id = {str(r[rows[0][0]]): r for r in old if rows[0][0] in r}
        header, *body = rows
        mine = [i for i, col in enumerate(header) if col in YOURS]
        new_body = []
        for row in body:
            row = row + [""] * (len(header) - len(row))
            prev = by_id.get(str(row[0]), {})
            for i in mine:
                if not str(row[i]).strip() and str(prev.get(header[i], "")).strip():
                    row[i] = prev[header[i]]
            new_body.append(row)
        out[name] = [header, *new_body]
    return out


def answers_as_tabs(decisions: Mapping[str, Mapping[str, Any]], other: Mapping[str, Any]) -> dict[str, Rows]:
    """The inverse of ``answers_from``: saved answers as minimal tabs, for ``carry_answers``."""
    clusters = set(decisions) | set(other.get("cluster_comments", {}))
    long_keys = set(other.get("long_key_comments", {}))
    return {
        "Clusters": [
            ["cluster", "your_full_name", "your_short_form", "your_kind", "your_comment"],
            *(
                [
                    c,
                    decisions.get(c, {}).get("full_name", ""),
                    decisions.get(c, {}).get("short_form", ""),
                    decisions.get(c, {}).get("kind", ""),
                    other.get("cluster_comments", {}).get(c, ""),
                ]
                for c in sorted(clusters)
            ),
        ],
        "Items": [
            ["item", "your_verdict", "your_comment"],
            *([i, v.get("verdict", ""), v.get("comment", "")] for i, v in other.get("items", {}).items()),
        ],
        "Questions": [["id", "your_answer"], *([k, v] for k, v in other.get("questions", {}).items())],
        "Cleanup": [["id", "your_answer"], *([k, v] for k, v in other.get("cleanup", {}).items())],
        "Long keys": [
            ["author_part", "your_comment"],
            *([k, other["long_key_comments"][k]] for k in sorted(long_keys)),
        ],
    }


def write_csvs(tabs: Mapping[str, Rows], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in tabs.items():
        with (out_dir / f"{name.lower().replace(' ', '_')}.csv").open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)


def push(tabs: Mapping[str, Rows], title: str, spreadsheet_id: str | None = None) -> str:
    """Create (or refresh) the Google Sheet and return its URL. Reviewer columns are highlighted."""
    from gspread.utils import ValueInputOption

    from lib.data import gsheets

    gc, _ = gsheets.get_gspread_client()
    sh = gc.open_by_key(spreadsheet_id) if spreadsheet_id else gc.create(title)
    for name, rows in tabs.items():
        n_cols = max(len(r) for r in rows)
        ws = gsheets.upsert_worksheet(sh, name, rows=len(rows) + 5, cols=n_cols)
        ws.update(
            values=[r + [""] * (n_cols - len(r)) for r in rows],
            range_name="A1",
            value_input_option=ValueInputOption.raw,
        )
        header = rows[0]
        requests: list[dict[str, Any]] = []
        if name != "Summary":
            requests.append({
                "updateSheetProperties": {
                    "properties": {"sheetId": ws.id, "gridProperties": {"frozenRowCount": 1}},
                    "fields": "gridProperties.frozenRowCount",
                }
            })  # fmt: skip
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": ws.id},
                    "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"}},
                    "fields": "userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment",
                }
            })  # fmt: skip
            requests.append({
                "updateDimensionProperties": {
                    "range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": n_cols},
                    "properties": {"pixelSize": 220},
                    "fields": "pixelSize",
                }
            })  # fmt: skip
        for i, col in enumerate(header):
            if col in YOURS:
                requests.append({
                    "repeatCell": {
                        "range": {"sheetId": ws.id, "startColumnIndex": i, "endColumnIndex": i + 1},
                        "cell": {"userEnteredFormat": {"backgroundColor": {"red": 1, "green": 0.96, "blue": 0.7}}},
                        "fields": "userEnteredFormat.backgroundColor",
                    }
                })  # fmt: skip
        requests.append({
            "repeatCell": {
                "range": {"sheetId": ws.id, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                "fields": "userEnteredFormat.textFormat.bold",
            }
        })  # fmt: skip
        sh.batch_update({"requests": requests})
    for ws in sh.worksheets():
        if ws.title not in tabs:
            sh.del_worksheet(ws)
    return sh.url


def _records(rows: Rows) -> list[dict[str, Any]]:
    header, *body = rows
    return [dict(zip(header, r + [""] * (len(header) - len(r)), strict=True)) for r in body]


def answers_from(tabs: Mapping[str, Rows]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """(decisions for ``orgs-plan``, everything else a reviewer typed) from the sheet's rows."""
    decisions: dict[str, dict[str, Any]] = {}
    for r in _records(tabs["Clusters"]):
        d: dict[str, Any] = {}
        if v := str(r["your_full_name"]).strip():
            d["full_name"] = v
        if v := str(r["your_short_form"]).strip():
            d["short_form"] = "" if v.lower() in ("none", "-") else v
        if v := str(r["your_kind"]).strip():
            d["kind"] = v
        if d:
            decisions[r["cluster"]] = d
    other: dict[str, Any] = {
        "cluster_comments": {r["cluster"]: r["your_comment"] for r in _records(tabs["Clusters"]) if r["your_comment"]},
        "items": {
            r["item"]: {"verdict": r["your_verdict"], "comment": r["your_comment"]}
            for r in _records(tabs["Items"])
            if r["your_verdict"] or r["your_comment"]
        },
        "questions": {r["id"]: r["your_answer"] for r in _records(tabs["Questions"]) if r["your_answer"]},
        "cleanup": {r["id"]: r["your_answer"] for r in _records(tabs["Cleanup"]) if r["your_answer"]},
        "short_forms": {
            r["first_author"]: str(r["your_short_form"]).strip()
            for r in _records(tabs.get("Long keys", [LONG_KEY_COLS]))
            if str(r["your_short_form"]).strip()
        },
        "long_key_comments": {
            r["author_part"]: r["your_comment"]
            for r in _records(tabs.get("Long keys", [LONG_KEY_COLS]))
            if r["your_comment"]
        },
    }
    return decisions, other


def pull(spreadsheet_id: str) -> dict[str, Rows]:
    from lib.data import gsheets

    sh = gsheets.open_sheet_by_id(spreadsheet_id)
    return {ws.title: ws.get_all_values() for ws in sh.worksheets()}


def load_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
