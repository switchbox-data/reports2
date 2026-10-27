import pytest

from lib.sources.title_case import uncap_title

NAMES = ["The Brooklyn Union Gas Company", "Connecticut Light and Power Company"]


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("RATE RSH (RESIDENTIAL SERVICE HEATING)", "Rate RSH (Residential Service Heating)"),
        ("RESIDENTIAL NON-HEATING RATE R-1", "Residential Non-Heating Rate R-1"),
        (
            "PURA INVESTIGATION INTO DISTRIBUTION SYSTEM PLANNING",
            "PURA Investigation into Distribution System Planning",
        ),
        (
            "PROPOSAL OF NATIONAL GRID FOR LOW-TO-MODERATE INCOME PROGRAMS",
            "Proposal of National Grid for Low-to-Moderate Income Programs",
        ),
        (
            "SUPPLEMENTAL FILING OF THE BROOKLYN UNION GAS COMPANY d/b/a NATIONAL GRID NY AND THE KEYSPAN GAS EAST CORPORATION",
            "Supplemental Filing of The Brooklyn Union Gas Company d/b/a National Grid NY and the KeySpan Gas East Corporation",
        ),
        (
            "SELECTED ANNUAL FEDERAL POVERTY LEVEL and STATE MEDIAN INCOME GUIDELINES",
            "Selected Annual Federal Poverty Level and State Median Income Guidelines",
        ),
        ("LIHEAP Summary RI 2024", None),
        ("GAAP FINANCIAL STATEMENTS AND FERC FORM 1", "GAAP Financial Statements and FERC Form 1"),
        ("CLCPA PANEL EXHIBITS", "CLCPA Panel Exhibits"),
        ("NIAGARA MOHAWK POWER CORPORATION Direct Testimony", "Niagara Mohawk Power Corporation Direct Testimony"),
        ("Heat Pump Key Product Criteria | ENERGY STAR", None),
        ("Docket 25-08: Order on Seasonal Heat Pump Rates", None),
        ("SMART-DS", None),
    ],
)
def test_uncap_title(title: str, expected: str | None) -> None:
    assert uncap_title(title, NAMES, ["PURA"]) == expected


def test_library_acronyms() -> None:
    from lib.sources.title_case import library_acronyms

    assert library_acronyms(["Gas Long-Term Plan (LTP) for NFGDC", "RATE RSH SERVICE", "Criteria | ENERGY STAR"]) == {
        "LTP",
        "NFGDC",
    }
