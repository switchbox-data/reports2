"""Build the provenance table for the MD BGE direct testimony (Maryland PSC Case No. 9888).

For every figure, table and computed number in the filed testimony PDF, records its
page/line and a GitHub permalink (at the ``md_bge_submission`` tag) to the notebook cell
that generates it.

The setup cell reads ``cache/*.pkl``. Those must come from the notebooks rendered at the
tag, not from a later render, so render them in a worktree and point the build at it::

    git worktree add --detach ../worktrees/reports2_md_bge_submission md_bge_submission
    cd ../worktrees/reports2_md_bge_submission && uv sync --frozen
    cd reports/md_hp_rates
    for n in rs_release_comp representative_home delivery_mc analysis_bills_only incremental_fair_default; do
        QUARTO_PYTHON=$PWD/../../.venv/bin/python quarto render notebooks/$n.qmd --to html
    done
    # then, from this repo's reports/md_hp_rates:
    just fetch-source velez_Docket9888Direct_2026  # the filed PDF, next to its extract
    just provenance-direct <worktree>/reports/md_hp_rates

Outputs (in this directory):

- ``pdf_lines.json``: the PDF indexed by printed page, margin line, footnote and caption
- ``provenance.csv``: one row per artifact (type, location, what it is, link)
- ``provenance_review.csv``: internal checks (never shown in the Word document)
- ``provenance.md`` / ``md_bge_direct_provenance.docx``: the document to send
"""

from __future__ import annotations

import os
from pathlib import Path

from lib.provenance import Hardcoded, KnownDifference, Link, ProvenanceConfig
from lib.provenance.build import main
from lib.provenance.config import GITHUB_RDP_BLOB, GITHUB_RDP_TREE
from lib.provenance.runs import check_runs

TAG = "md_bge_submission"
"""Annotated tag on reports2 (the testimony and notebooks as filed) and on rate-design-platform
(the commit pinned in ``batch_config.yaml``, ``RDP_REF``)."""
RDP_PIN = "1b456954"
BATCH_PREFIX = "switchbox/cairo/outputs/hp_rates/md/bge/md_20260910_w_rhp/"
MC_TYPES = ("dist_and_sub_tx", "bulk_tx")

PATH_HERE = Path(__file__).resolve().parent
PATH_REPORT = PATH_HERE.parents[1]
PATH_REPO = PATH_REPORT.parents[1]
PATH_RDP = Path(os.environ.get("PATH_RDP", PATH_REPO.parent / "rate-design-platform"))

NAMESPACES = {
    "r": "representative_home",
    "m": "delivery_mc",
    "b": "analysis_bills_only",
    "fc": "incremental_fair_default",
}

NOTEBOOK_BLURBS = {
    "representative_home": (
        "Typical home's usage and bills",
        "Monthly electricity use, bills and grid costs for the average gas-heated and fossil-fuel-heated "
        "BGE home, before and after it installs a heat pump.",
    ),
    "delivery_mc": (
        "When the grid is under strain",
        "Which hours of the year drive new transmission and distribution costs, and how large those costs are.",
    ),
    "analysis_bills_only": (
        "Bill changes across all homes",
        "How many gas-heated homes would see their bills rise or fall after installing a heat pump, "
        "under Schedule R, Schedule RD and the proposed Schedule R-HP.",
    ),
    "incremental_fair_default": (
        "Fixed charge alternative",
        "The fixed charge that would remove the overpayment if the volumetric charges were lowered instead.",
    ),
    "expert_testimony": (
        "The testimony itself",
        "The text of the testimony, including its tables.",
    ),
}

INTRO = f"""\
This document lists every figure, table and calculated number in the Direct Testimony of
Juan-Pablo Velez (Maryland PSC Case No. 9888), and links each one to the code that produced it.
Figures, tables and numbers each have their own table, in the order they appear in the testimony.

- **Location** gives the page and line number in the testimony as filed. Items that appear
  more than once are listed once, with every place they appear.
- The second column gives the figure or table title, or for numbers, a short quote with the
  number in bold.
- **Where it's generated** links to the block of code that produces the item. Our analysis is
  written as notebooks: documents that explain each step in plain language next to the code
  that carries it out. Each link opens the exact lines on GitHub, frozen at the version used for
  the testimony (labeled `{TAG}`), so the links will keep pointing to the same code.
"""

DIST_DOC = "context/methods/marginal_costs/md_bge_dist_mc_methodology.md"
BULK_DOC = "context/methods/marginal_costs/md_bulk_transmission.md"


def rdp_blob(path: str, lines: tuple[int, int] | None = None) -> str:
    anchor = f"#L{lines[0]}-L{lines[1]}" if lines else ""
    return f"{GITHUB_RDP_BLOB}/{TAG}/{path}{anchor}"


def rdp_link(path: str, lines: tuple[int, int]) -> Link:
    return Link(f"{Path(path).name}_{lines[0]}-{lines[1]}", rdp_blob(path, lines))


def rdp_links() -> list[str]:
    tariffs = "rate_design/hp_rates/md/config/tariffs/electric"
    return [
        "**Hourly cost of new distribution capacity**: "
        f"[explanation]({rdp_blob(DIST_DOC)}), "
        f"[code]({rdp_blob('utils/data_prep/marginal_costs/generate_utility_tx_dx_mc.py')}).",
        "**Hourly cost of new bulk transmission capacity**: "
        f"[explanation]({rdp_blob(BULK_DOC)}), "
        f"[code]({rdp_blob('utils/data_prep/marginal_costs/generate_bulk_tx_mc.py')}).",
        f"**Bill simulation for every modeled home**: [code]({rdp_blob('rate_design/hp_rates/run_scenario.py')}).",
        "**The rates we simulated** (Schedule R, Schedule RD and Schedule R-HP): "
        f"[rate definitions]({GITHUB_RDP_TREE}/{TAG}/{tariffs}).",
        "**How we built Schedule R-HP**: "
        f"[rate inputs]({rdp_blob(f'{tariffs}/custom_rates/bge_rhp_flat.yaml')}), "
        f"[code]({rdp_blob('utils/pre/create_custom_flat_tariff.py')}).",
    ]


DIST_36_NOTE = (
    "the dist/sub-tx MC file the runs used (reproduced exactly at the RDP pin) sums to $35.21/kW-year, "
    "which rounds to $35; the RDP methodology doc also says ~$36"
)

HARDCODED = [
    Hardcoded("$57.74", "giving a 2025 effective rate of approximately $57.74/kW-year", rdp_link(BULK_DOC, (167, 179))),
    Hardcoded("$57.74", "Multiplying the $57.74/kW-year figure", rdp_link(BULK_DOC, (167, 179))),
    Hardcoded("8,610", "The remaining 8,610 hours", rdp_link(BULK_DOC, (340, 352))),
    Hardcoded("$36", "yielding approximately $36/kW-year", rdp_link(DIST_DOC, (30, 43)), DIST_36_NOTE),
    Hardcoded("$36", "the annualized cost (~$36/kW-year)", rdp_link(DIST_DOC, (30, 43)), DIST_36_NOTE),
]

KNOWN_DIFFERENCES = [
    KnownDifference(
        "$256",
        "$257",
        "edited in Word after rendering: $2,946 - $2,690 from Figure 16's rounded bar labels; "
        "the code's unrounded difference is $256.54",
    ),
    KnownDifference(
        "$359",
        "$365",
        "edited in Word after rendering; the code and the filed Figure 12 give $365 ($1,018 - $653); "
        "the source of $359 is not known",
    ),
]

CONFIG = ProvenanceConfig(
    tag=TAG,
    path_repo=PATH_REPO,
    report_rel="reports/md_hp_rates",
    path_pdf=PATH_REPO / "context/sources/md_hp_rates/Johnston - VIA ELECTRONIC FILING.pdf",
    path_extract=PATH_REPO / "context/sources/md_hp_rates/mdpuc_9888_direct_testimony_velez.md",
    namespaces=NAMESPACES,
    notebook_blurbs=NOTEBOOK_BLURBS,
    title="Where the testimony's figures, tables and numbers come from",
    subtitle="Direct Testimony of Juan-Pablo Velez, Maryland PSC Case No. 9888",
    intro=INTRO,
    docx_name="md_bge_direct_provenance.docx",
    platform_links=rdp_links(),
    hardcoded=HARDCODED,
    known_differences=KNOWN_DIFFERENCES,
    run_checks=lambda review: check_runs(
        review, batch_prefix=BATCH_PREFIX, path_rdp=PATH_RDP, rdp_pin=RDP_PIN, mc_types=MC_TYPES
    ),
)

if __name__ == "__main__":
    main(CONFIG, PATH_HERE, "Build the provenance table for the MD BGE direct testimony.")
