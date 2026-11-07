"""Build the provenance table for the MD BGE surrebuttal testimony (Maryland PSC Case No. 9888).

The surrebuttal repeats many numbers from the direct testimony (documented by
``provenance/direct``); this lists only the new analysis: the ResStock rerun of the
average-home comparison (``representative_home_rebuttal``, namespace ``s``), in Table 1 and
the sentences built on it. Each item gets its page/line and a GitHub permalink, at the
``md_bge_surrebuttal`` tag, to the notebook cell that generates it.

The setup cell reads ``cache/*.pkl``, which must come from the notebooks as of the tag, so run it
against a worktree checked out and rendered at the tag::

    just fetch-source velez_Docket9888Surrebuttal_2026  # the filed PDF, next to its extract
    git worktree add <worktree> md_bge_surrebuttal      # then render the notebooks there
    just provenance-surrebuttal <worktree>/reports/md_hp_rates

Outputs (in this directory):

- ``pdf_lines.json``: the PDF indexed by printed page, margin line, footnote and caption
- ``provenance.csv``: one row per artifact (type, location, what it is, link)
- ``provenance_review.csv``: internal checks (never shown in the Word document)
- ``provenance.md`` / ``md_bge_surrebuttal_provenance.docx``: the document to send
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from lib.provenance import Link, ProvenanceConfig
from lib.provenance.build import main
from lib.provenance.config import GITHUB_RDP_BLOB
from lib.provenance.resolve import Notebook, cell_for_line, find_var_line, load_notebook
from lib.provenance.runs import check_runs

TAG = "md_bge_surrebuttal"
"""Annotated tag on reports2 (the surrebuttal and notebooks as filed). The ResStock rerun reads the
same CAIRO batch as the direct testimony, so platform links use the direct testimony's
``md_bge_submission`` tag on rate-design-platform (the commit pinned in ``batch_config.yaml``)."""
RDP_TAG = "md_bge_submission"
RDP_PIN = "1b456954"
BATCH_PREFIX = "switchbox/cairo/outputs/hp_rates/md/bge/md_20260910_w_rhp/"
MC_TYPES = ("dist_and_sub_tx", "bulk_tx")

PATH_HERE = Path(__file__).resolve().parent
PATH_REPORT = PATH_HERE.parents[1]
PATH_REPO = PATH_REPORT.parents[1]
PATH_RDP = Path(os.environ.get("PATH_RDP", PATH_REPO.parent / "rate-design-platform"))

NAMESPACES = {
    "d": "representative_home",
    "s": "representative_home_rebuttal",
    "b": "analysis_bills_only",
}

NOTEBOOK_BLURBS = {
    "representative_home_rebuttal": (
        "Typical home, simulated with ResStock",
        "The average fossil-fuel-heated BGE home's electricity use, charges and grid costs, measured on the same "
        "ResStock homes before and after a heat pump retrofit instead of with BGE's customer data.",
    ),
    "surrebuttal_testimony": (
        "The testimony itself",
        "The text of the testimony, including its tables.",
    ),
}

INTRO = f"""\
This document lists the new analysis in the Surrebuttal Testimony of Juan-Pablo Velez
(Maryland PSC Case No. 9888): the table and calculated numbers that rerun the direct testimony's
average-home comparison with ResStock, and links each one to the code that produced it. Numbers
the surrebuttal repeats from the direct testimony are listed in the direct testimony's
provenance document and are not repeated here.

- **Location** gives the page and line number in the testimony as filed. Items that appear more
  than once are listed once, with every place they appear.
- The second column gives the table title, or for numbers, a short quote with the number in bold.
- **Where it's generated** links to the block of code that produces the item. Our analysis is
  written as notebooks: documents that explain each step in plain language next to the code
  that carries it out. Each link opens the exact lines on GitHub, frozen at the version used for
  the testimony (labeled `{TAG}`), so the links will keep pointing to the same code.
"""


def rdp_blob(path: str) -> str:
    return f"{GITHUB_RDP_BLOB}/{RDP_TAG}/{path}"


PLATFORM_LINKS = [
    f"**Bill simulation for every modeled home**: [code]({rdp_blob('rate_design/hp_rates/run_scenario.py')}).",
    "**Hourly cost of new distribution and transmission capacity**: "
    f"[code]({rdp_blob('utils/data_prep/marginal_costs/generate_utility_tx_dx_mc.py')}), "
    f"[code]({rdp_blob('utils/data_prep/marginal_costs/generate_bulk_tx_mc.py')}).",
]


def mc_delta_resolver(code: str, testimony: Notebook, cfg: ProvenanceConfig) -> Link | None:
    """``mc_delta(ns)`` (setup-cell helper): the change in delivery marginal cost from ``ns``'s notebook."""
    m = re.search(r"\bmc_delta\((\w+)\)", code)
    if m is None or m.group(1) not in cfg.namespaces:
        return None
    nb = load_notebook(cfg, cfg.namespaces[m.group(1)])
    line = find_var_line(nb, "all_fossil_annual_mc_delivery_after")
    return None if line is None else cfg.notebook_link(nb.name, *cell_for_line(nb, line))


CONFIG = ProvenanceConfig(
    tag=TAG,
    path_repo=PATH_REPO,
    report_rel="reports/md_hp_rates",
    path_pdf=PATH_REPO / "context/sources/md_hp_rates/2026-11-02 9888_CCAN Surrebuttal Testimony.pdf",
    path_extract=PATH_REPO / "context/sources/md_hp_rates/mdpuc_9888_surrebuttal_testimony_velez.md",
    namespaces=NAMESPACES,
    notebook_blurbs=NOTEBOOK_BLURBS,
    title="Where the surrebuttal's new analysis comes from",
    subtitle="Surrebuttal Testimony of Juan-Pablo Velez, Maryland PSC Case No. 9888",
    intro=INTRO,
    docx_name="md_bge_surrebuttal_provenance.docx",
    qmd_name="surrebuttal_testimony.qmd",
    platform_links=PLATFORM_LINKS,
    resolvers=[mc_delta_resolver],
    include_namespaces=frozenset({"s"}),
    # The lower of the two overcharges prints the direct testimony's $359, documented there.
    exclude_codes=frozenset(
        {"dollar(min(d.all_fossil_annual_total_overcharge, s.all_fossil_annual_total_overcharge))"}
    ),
    run_checks=lambda review: check_runs(
        review, batch_prefix=BATCH_PREFIX, path_rdp=PATH_RDP, rdp_pin=RDP_PIN, mc_types=MC_TYPES
    ),
)

if __name__ == "__main__":
    main(CONFIG, PATH_HERE, "Build the provenance table for the MD BGE surrebuttal testimony.")
