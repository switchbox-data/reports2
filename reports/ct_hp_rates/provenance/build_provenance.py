"""Build the CIEC-1 provenance table for the CT Eversource testimony.

For every figure, table and computed number in the submitted testimony PDF,
records its page/line in the PDF and a GitHub permalink (at the
``ct_eversource_submission`` tag) to the notebook cell that generates it.

Outputs (in this directory):

- ``pdf_lines.json``: the PDF indexed by printed page, margin line, footnote and caption
- ``provenance.csv``: one row per artifact (type, location, what it is, link)
- ``provenance_review.csv``: internal checks (never shown in the Word document)
- ``provenance.md`` / ``ciec_1_provenance.docx``: the document sent to CIEC
"""

from __future__ import annotations

import os
from pathlib import Path

from lib.provenance import ProvenanceConfig, filed_constant_resolver
from lib.provenance.build import main
from lib.provenance.config import GITHUB_RDP_BLOB, GITHUB_RDP_TREE
from lib.provenance.runs import check_runs

TAG = "ct_eversource_submission"
RDP_PIN = "e97a3ca"
MC_TAGS = {
    "dist_and_sub_tx": ("mc/92366c905831", "utils/data_prep/marginal_costs/generate_utility_tx_dx_mc.py"),
    "bulk_tx": ("mc/1b1b329be68f", "utils/data_prep/marginal_costs/bulk_tx/generate_bulk_tx_mc.py"),
}
# The MC methodology docs at TAG misstate the bulk-tx dollar year; this commit on RDP main corrects them.
RDP_MC_DOCS_REF = "979af55635436ed27b829457fcced7c9ad43d34e"
BATCH_PREFIX = "switchbox/cairo/outputs/hp_rates/ct/ct_eversource/ct_20261015_a/"

PATH_HERE = Path(__file__).resolve().parent
PATH_REPORT = PATH_HERE.parent
PATH_REPO = PATH_REPORT.parents[1]
PATH_RDP = Path(os.environ.get("PATH_RDP", PATH_REPO.parent / "rate-design-platform"))

NAMESPACES = {
    "r": "representative_home",
    "m": "delivery_mc",
    "mc": "marginal_costs",
    "a": "analysis",
    "fc": "incremental_fair_default",
    "op": "overpayment",
    "th": "rate6_threshold",
    "fh": "feeder_headroom",
}

NOTEBOOK_BLURBS = {
    "representative_home": (
        "Typical home's usage and bills",
        "Monthly electricity use, bills and grid costs for the average fossil-fuel-heated home, "
        "before and after it installs a heat pump.",
    ),
    "delivery_mc": (
        "When the grid is under strain",
        "Which hours of the year drive new grid costs, and how large those costs are.",
    ),
    "marginal_costs": (
        "Cost of new grid capacity",
        "The cost of adding distribution and transmission capacity, drawn from the Company's filings.",
    ),
    "feeder_headroom": (
        "Spare grid capacity",
        "Each distribution feeder's peak demand compared with its capacity.",
    ),
    "overpayment": (
        "Overpayment across all homes",
        "How much each home that installs a heat pump would overpay for delivery under each rate.",
    ),
    "analysis": (
        "Bill changes by heating fuel",
        "How many homes would see their bills rise or fall under each rate.",
    ),
    "rate6_threshold": (
        "Rate 6's 700 kWh threshold",
        "How the 700 kWh winter threshold sorts each home's usage into discounted and undiscounted blocks.",
    ),
    "incremental_fair_default": (
        "Fixed charge alternative",
        "The fixed charge that would remove the overpayment if the volumetric rate were lowered instead.",
    ),
    "expert_testimony": (
        "The testimony itself",
        "The text of the testimony, including its tables and the filed Rate 1 charges it quotes.",
    ),
}

INTRO = f"""\
This document lists every figure, table and calculated number in the Direct Testimony of
Juan-Pablo Velez (Docket No. 26-05-10), and links each one to the code that produced it.
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


def rdp_links() -> list[str]:
    def blob(ref: str, path: str) -> str:
        return f"{GITHUB_RDP_BLOB}/{ref}/{path}"

    dist_tag, dist_path = MC_TAGS["dist_and_sub_tx"]
    bulk_tag, bulk_path = MC_TAGS["bulk_tx"]
    return [
        "**Hourly cost of new distribution capacity**: "
        f"[explanation]({blob(RDP_MC_DOCS_REF, 'context/methods/marginal_costs/ct_eversource_dist_mc_methodology.md')}), "
        f"[code]({blob(dist_tag, dist_path)}).",
        "**Hourly cost of new bulk transmission capacity**: "
        f"[explanation]({blob(RDP_MC_DOCS_REF, 'context/methods/marginal_costs/ct_bulk_transmission_marginal_cost.md')}), "
        f"[code]({blob(bulk_tag, bulk_path)}).",
        f"**Bill simulation for every modeled home**: [code]({blob(TAG, 'rate_design/hp_rates/run_scenario.py')}).",
        "**The rates we simulated** (Rate 1, Rate 6 and Rate HP): "
        f"[rate definitions]({GITHUB_RDP_TREE}/{TAG}/rate_design/hp_rates/ct/config/tariffs/electric).",
        "**How we derived Rate HP**: "
        f"[explanation]({blob(TAG, 'context/methods/tou_and_rates/icos_tariff_derivation.md')}), "
        f"[code]({blob(TAG, 'utils/mid/derive_icos_tariff.py')}).",
    ]


CONFIG = ProvenanceConfig(
    tag=TAG,
    path_repo=PATH_REPO,
    report_rel="reports/ct_hp_rates",
    path_pdf=PATH_REPO / "context/sources/ct_hp_rates/Direct Testimony of Juan-Pablo Velez - Docket No. 26-05-10.pdf",
    path_extract=PATH_REPO / "context/sources/ct_hp_rates/pura_260510_direct_testimony_clf_velez.md",
    namespaces=NAMESPACES,
    notebook_blurbs=NOTEBOOK_BLURBS,
    title="CIEC-1: Where the testimony's figures, tables and numbers come from",
    subtitle="Direct Testimony of Juan-Pablo Velez, Docket No. 26-05-10",
    intro=INTRO,
    docx_name="ciec_1_provenance.docx",
    platform_links=rdp_links(),
    resolvers=[filed_constant_resolver("FILED_")],
    run_checks=lambda review: check_runs(
        review, batch_prefix=BATCH_PREFIX, path_rdp=PATH_RDP, rdp_pin=RDP_PIN, mc_types=MC_TAGS
    ),
)

if __name__ == "__main__":
    main(CONFIG, PATH_HERE, "Build the CIEC-1 provenance table for the CT testimony.")
