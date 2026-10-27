import pytest

from lib.sources.docket_titles import docket_title


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Gas Long-Term Plan (Case 22-G-0610)", "Docket 22-G-0610: Gas Long-Term Plan"),
        (
            "Direct Testimony of Revenue Requirements Panel (Cases 22-E-0317, 22-G-0318, 22-E-0319 and 22-G-0320)",
            "Docket 22-E-0317: Direct Testimony of Revenue Requirements Panel",
        ),
        (
            "Revenue Requirements Panel Exhibits (Case 23-E-0418; Case 23-G-0419)",
            "Docket 23-E-0418: Revenue Requirements Panel Exhibits",
        ),
        ("Cases 25-E-0375 and 25-E-0379: Revenue Allocation", "Docket 25-E-0375: Revenue Allocation"),
        ("Order Adopting Targets (CASE 18-M-0084)", "Docket 18-M-0084: Order Adopting Targets"),
        ("D.P.U. 25-55: Direct Testimony of Richard D. Chin", "Docket 25-55: Direct Testimony of Richard D. Chin"),
        (
            "Rewiring America Comments on DPU 26-72 (Unitil Compliance Filing)",
            "Docket 26-72: Rewiring America Comments (Unitil Compliance Filing)",
        ),
        (
            "Direct Testimony of Ned W. Allis (Exh LU-NWA-1, D.P.U. 25-08)",
            "Docket 25-08: Direct Testimony of Ned W. Allis (Exh LU-NWA-1)",
        ),
        ("Docket No. 26-05-10 - CLP Rate Case Application", "Docket 26-05-10: CLP Rate Case Application"),
        ("Docket 25-0084 Ameren Final Order", "Docket 25-0084: Ameren Final Order"),
        (
            "Docket CI-23-117 (Gas IRP): Order Establishing Framework",
            "Docket CI-23-117: Order Establishing Framework (Gas IRP)",
        ),
        ("ConEd Broadcast Memo for 25-E-0072", "Docket 25-E-0072: ConEd Broadcast Memo"),
        ("Filing Summary - Electric Rate Case 25-E-0072", "Docket 25-E-0072: Filing Summary - Electric Rate Case"),
        ("Future of Gas Proceeding, Docket No. 24-0158", "Docket 24-0158: Future of Gas Proceeding"),
        ("Docket 25-08: Order on Seasonal Heat Pump Rates", None),
        ("Summary of Rates: Last Resort Service (R.I.P.U.C. No. 2096)", None),
        ("Maryland PSC Order No. 91461", None),
        ("2018 CARIS Phase 2 Base Case Assumptions", None),
    ],
)
def test_docket_title(title: str, expected: str | None) -> None:
    assert docket_title(title) == expected


def test_docket_from_number_field() -> None:
    data = {"reportNumber": "PGL Ex. 2.0, Docket No. 24-0081"}
    assert docket_title("Peoples Gas and the SMP History", data) == "Docket 24-0081: Peoples Gas and the SMP History"
    assert docket_title("Annual Report", {"reportNumber": "NREL/TP-5500-83063"}) is None
