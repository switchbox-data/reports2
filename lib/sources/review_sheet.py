"""The library-cleanup review sheet: build its tabs, push them to Google Sheets and read answers back.

``build_tabs`` is pure (rows from the plan, clusters, conflicts, questions and cleanup actions), so
the CSV copies and the Google Sheet always match. Reviewers type only in the ``your_*`` columns;
``pull`` reads those back into ``decisions.json`` (cluster names and short forms, which ``orgs-plan``
applies) and ``answers.json`` (item verdicts, question and cleanup answers).
"""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

Rows = list[list[Any]]

CLUSTER_COLS = [
    "cluster", "status", "kind", "proposed_full_name", "proposed_short_form", "short_form_source", "confidence",
    "names_in_library", "n_items", "n_cited_items", "evidence", "agent_notes", "flags", "batches",
    "your_full_name", "your_short_form", "your_kind", "your_comment",
]  # fmt: skip
ITEM_COLS = [
    "item", "scope", "cited_as", "old_keys", "new_key", "action", "authors_before", "authors_after", "changes",
    "flags", "title", "your_verdict", "your_comment",
]  # fmt: skip
KEY_COLS = ["item", "old_keys", "new_key", "key_changes", "cited_as", "title"]
QUESTION_COLS = ["id", "question", "options", "comes_up_in", "your_answer"]
CLEANUP_COLS = ["id", "type", "items", "description", "proposed_action", "your_answer"]
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
            p["item"], p["scope"], p["cited"], p["old_keys"], p["key"] or "", p["action"],
            _authors(p["before"].get("creators", [])), _authors(p["after"].get("creators", [])),
            p["changes"], p["flags"], p["after"].get("title") or p["before"].get("title") or "", "", "",
        ])  # fmt: skip
    return rows


def key_rows(plans: Sequence[Mapping[str, Any]]) -> Rows:
    rows: Rows = [KEY_COLS]
    for p in sorted(plans, key=lambda p: (not p["cited"], p["key"] or "")):
        changed = "same" if p["key"] in p["old_keys"] else ("no key yet" if not p["key"] else "new")
        rows.append([p["item"], p["old_keys"], p["key"] or "", changed, p["cited"], p["after"].get("title") or ""])
    return rows


def question_rows(questions: Sequence[Mapping[str, Any]]) -> Rows:
    rows: Rows = [QUESTION_COLS]
    for q in questions:
        rows.append([q["id"], q["question"], q.get("options", []), q.get("comes_up_in", ""), ""])
    return rows


def cleanup_rows(actions: Sequence[Mapping[str, Any]]) -> Rows:
    rows: Rows = [CLEANUP_COLS]
    for a in actions:
        rows.append([a["id"], a["type"], a.get("items", []), a["description"], a.get("proposed_action", ""), ""])
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
        [""],
        ["items in Reports and Inbox", len(plans)],
        ["items with metadata changes", sum(bool(p["changes"]) for p in plans)],
        ["items flagged for a look", sum(bool(p["flags"]) for p in plans)],
        ["organization clusters", len(merged)],
        ["clusters needing your decision", sum(any(x["needs_decision"] for x in m["proposals"]) for m in merged)],
        ["keys assigned", len(keyed)],
        ["keys unchanged", sum(p["key"] in p["old_keys"] for p in keyed)],
        ["cited items whose key changes", sum(1 for p in keyed if p["cited"] and p["key"] not in p["old_keys"])],
        ["items still without an author (no key)", len(plans) - len(keyed)],
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
        "Cleanup": cleanup_rows(cleanup),
    }
    return {name: [[_cell(v) for v in row] for row in rows] for name, rows in tabs.items()}


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
    }
    return decisions, other


def pull(spreadsheet_id: str) -> dict[str, Rows]:
    from lib.data import gsheets

    sh = gsheets.open_sheet_by_id(spreadsheet_id)
    return {ws.title: ws.get_all_values() for ws in sh.worksheets()}


def load_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
