"""The committed Switchbox CSL style renders organization abbreviations."""

import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(shutil.which("quarto") is None, reason="quarto not installed")
CSL = Path(__file__).resolve().parents[2] / "reports" / "chicago-author-date-switchbox.csl"

BIB = """references:
  - id: madpu_Docket23150Order_2024
    author:
      - family: Massachusetts Department of Public Utilities
    author-short: MA DPU
    issued: 2024
    title: "Docket 23-150: Order"
    type: report
  - id: madpu_Docket2380Order_2024
    author:
      - family: Massachusetts Department of Public Utilities
    author-short: MA DPU
    issued: 2024
    title: "Docket 23-80: Order"
    type: report
  - id: shah_DesigningBetterRates_2026
    author:
      - family: Shah
        given: Amar
    issued: 2026
    title: Designing Better Rates
    type: report
"""


def test_abbreviation_in_text_and_bibliography(tmp_path):
    (tmp_path / "refs.yaml").write_text(BIB, encoding="utf-8")
    (tmp_path / "doc.md").write_text(
        "@madpu_Docket23150Order_2024 says.\n\n[@madpu_Docket23150Order_2024, 4]\n\n[-@madpu_Docket2380Order_2024]\n\n"
        "[@shah_DesigningBetterRates_2026; @madpu_Docket2380Order_2024]\n",
        encoding="utf-8",
    )
    out = subprocess.run(
        [
            "quarto",
            "pandoc",
            "doc.md",
            "--citeproc",
            "--bibliography",
            "refs.yaml",
            "--csl",
            str(CSL),
            "-t",
            "plain",
            "--wrap=none",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "MA DPU (2024a) says." in out
    assert "(MA DPU 2024a, 4)" in out
    assert "(2024b)" in out
    assert "(Shah 2026; MA DPU 2024b)" in out
    assert "Massachusetts Department of Public Utilities (MA DPU). 2024a." in out
    assert "Shah, Amar. 2026." in out
