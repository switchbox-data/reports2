"""The citation-key rule, tested on items from the Switchbox library."""

import pytest

from lib.sources import citekeys


def org(name, short=None, title="Docket 23-150: Order", date="2024-06-24", key="ITEM0001", **extra_fields):
    item = {"key": key, "creators": [{"creatorType": "author", "name": name}], "title": title, "date": date}
    if short:
        item["extra"] = f"tex.shortauthor: {short}"
    return item | extra_fields


def person(last, first="A.", title="Some Title Here", date="2024", key="ITEM0002", **extra_fields):
    creators = [{"creatorType": "author", "firstName": first, "lastName": last}]
    return {"key": key, "creators": creators, "title": title, "date": date} | extra_fields


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        (org("Massachusetts Department of Public Utilities", "MA DPU"), "madpu_Docket23150Order_2024"),
        (
            org("ISO New England", "ISO-NE", title="Five-Minute Regulation Clearing Prices (Final)", date="2025"),
            "isone_FiveMinuteRegulationClearing_2025",
        ),
        (
            org("Eversource Connecticut", "CL&P", title="Docket 26-05-10: Exhibit CLP-MCOS-1", date="2026-05-28"),
            "clp_Docket260510Exhibit_2026",
        ),
        (
            org("Orange and Rockland Utilities", "O&R", title="2018 Marginal Cost of Service Study", date="2019"),
            "or_2018MarginalCost_2019",
        ),
        (org("Rochester Gas and Electric", "RG&E", title="Rate Case Filing", date="2025"), "rge_RateCaseFiling_2025"),
        (
            org("Boston Gas Company", title="Statement of Operating Revenues", date="2022"),
            "bostongascompany_StatementOperatingRevenues_2022",
        ),
        (org("National Grid", title="Gas Customer Connection", date="2022"), "nationalgrid_GasCustomerConnection_2022"),
        (
            person(
                "Borenstein",
                "Severin",
                title="Should 'Energy Hogs' Shoulder More of the Utility Cost Burden?",
                date="8/2024",
            ),
            "borenstein_ShouldEnergyHogs_2024",
        ),
        (
            person(
                "Pérez-Arriaga",
                "José Ignacio",
                title="Regulatory Framework for an Evolving Electricity Sector",
                date="2017",
            ),
            "perezarriaga_RegulatoryFrameworkEvolving_2017",
        ),
        (person("Rábago", "Karl", title="The Value of Solar", date="2013"), "rabago_ValueSolar_2013"),
        (
            person("Gallo Cassarino", "Tiziano", title="Hydrogen Production", date="2018"),
            "gallocassarino_HydrogenProduction_2018",
        ),
        (person("O'Shaughnessy", "Eric", title="Solar Prices", date="2020"), "oshaughnessy_SolarPrices_2020"),
        (
            person("Esquivel-Elizondo", "Sofia", title="Wide Range in Estimates", date="2023"),
            "esquivelelizondo_WideRangeEstimates_2023",
        ),
        (
            person("van Benthem", "Arthur", title="Learning-by-Doing and the Optimal Solar Policy", date="2008"),
            "vanbenthem_LearningbyDoingOptimalSolar_2008",
        ),
        (person("King, Jr.", "Martin", title="Strength to Love", date="1963"), "king_StrengthLove_1963"),
        (
            person("Brattle", title="New York\u2019s Grid Flexibility Potential - Volume 2", date="01/2025"),
            "brattle_NewYorksGrid_2025",
        ),
        (
            person("Sergici", "Sanem", title="Heat Pump\u2013Friendly Cost-Based Rate Designs", date="1/2023"),
            "sergici_HeatPumpFriendly_2023",
        ),
        (
            person("Smith", title="U.S. Rates 2.0: Q&A on Low-Income Programs", date="March 3, 2021"),
            "smith_USRates20_2021",
        ),
        (person("Smith", title="Low-Income Q&A", date=""), "smith_LowIncomeQA_nd"),
        (person("Smith", title="<i>CELT</i> report about kWh", date="2025"), "smith_CELTReportKWh_2025"),
    ],
)
def test_base_key(item, expected):
    assert citekeys.base_key(item) == expected


def test_statute_and_case_fields():
    statute = {
        "key": "S1",
        "creators": [{"creatorType": "author", "name": "State of New York"}],
        "nameOfAct": "Environmental Conservation Law, Article 75",
        "dateEnacted": "2020-01-03",
    }
    case = {
        "key": "C1",
        "creators": [{"creatorType": "author", "name": "New York Public Service Commission"}],
        "caseName": "Energy Affordability Proceeding (14-M-0565)",
        "dateDecided": "2016-05-20",
    }
    assert citekeys.base_key(statute) == "stateofnewyork_EnvironmentalConservationLaw_2020"
    assert citekeys.base_key(case) == "newyorkpublicservicecommission_EnergyAffordabilityProceeding_2016"


def test_first_creator_prefers_authors_then_editors():
    item = person("Editor", title="A Book", date="2020")
    item["creators"] = [
        {"creatorType": "editor", "firstName": "E", "lastName": "Editor"},
        {"creatorType": "author", "firstName": "A", "lastName": "Author"},
    ]
    assert citekeys.base_key(item) == "author_Book_2020"


def test_multiple_organizations_use_first_short_form():
    item = org("New York State Electric & Gas", "NYSEG and RG&E", title="Rate Case Exhibits", date="2025")
    item["creators"].append({"creatorType": "author", "name": "Rochester Gas and Electric"})
    assert citekeys.base_key(item) == "nyseg_RateCaseExhibits_2025"
    item["extra"] = "tex.shortauthor: Nicor Gas, Peoples Gas, and North Shore Gas"
    assert citekeys.author_part(item["creators"], citekeys.short_form(item)) == "nicorgas"


def test_no_creator_raises():
    with pytest.raises(citekeys.NoCreatorError):
        citekeys.base_key({"key": "X", "creators": [], "title": "T", "date": "2024"})


@pytest.mark.parametrize(
    ("key", "item", "expected"),
    [
        ("madpu_Docket23150Order_2024", org("Massachusetts Department of Public Utilities", "MA DPU"), True),
        ("madpu_Docket23150Order_2024b", org("Massachusetts Department of Public Utilities", "MA DPU"), True),
        ("dpu_Docket23150Order_2024", org("Massachusetts Department of Public Utilities", "MA DPU"), False),
        ("madpu_docket23150order_2024", org("Massachusetts Department of Public Utilities", "MA DPU"), True),
        ("madpu_Docket23150Order_24", org("Massachusetts Department of Public Utilities", "MA DPU"), False),
        ("madpu_Docket23150Order_", org("Massachusetts Department of Public Utilities", "MA DPU"), False),
        (
            "isone_CeltReport_2025",
            org(
                "ISO New England",
                "ISO-NE",
                title="Capacity, Energy, Loads, and Transmission (CELT) report",
                date="2025",
            ),
            False,
        ),
        (
            "isone_CELTReport_2025",
            org(
                "ISO New England",
                "ISO-NE",
                title="Capacity, Energy, Loads, and Transmission (CELT) report",
                date="2025",
                shortTitle="CELT report",
            ),
            True,
        ),
        ("Designing_better_rates_shah_2026", person("Shah", title="Designing Better Rates", date="2026"), False),
        ("zotero-item-3604", person("Dakss", date="2026"), False),
        (
            "madpu_ExhibitSeasonalHP_nd",
            org("Massachusetts Department of Public Utilities", "MA DPU", title="Exhibit Seasonal HP", date=""),
            True,
        ),
    ],
)
def test_conforms(key, item, expected):
    assert citekeys.conforms(key, item) is expected


def test_propose_key_takes_first_free_suffix():
    item = org("Massachusetts Department of Public Utilities", "MA DPU")
    assert citekeys.propose_key(item, set()) == "madpu_Docket23150Order_2024"
    taken = {"madpu_Docket23150Order_2024", "madpu_Docket23150Order_2024a"}
    assert citekeys.propose_key(item, taken) == "madpu_Docket23150Order_2024b"


def test_suffix_sequence_continues_past_z():
    seq = list(zip(range(29), citekeys.suffixes(), strict=False))
    assert [s for _, s in seq][:3] == ["", "a", "b"]
    assert [s for _, s in seq][26:29] == ["z", "aa", "ab"]


def test_assign_keys_collisions_follow_filing_date_and_keep_conforming_keys():
    exhibits = [
        org("Eversource Connecticut", "CL&P", title="Docket 26-05-10: Exhibit CLP-B", date="2026-07-14", key="B"),
        org("Eversource Connecticut", "CL&P", title="Docket 26-05-10: Exhibit CLP-A", date="2026-05-28", key="A"),
        org("Eversource Connecticut", "CL&P", title="Docket 26-05-10: Exhibit CLP-C", date="2026-08", key="C"),
        org("Eversource Connecticut", "CL&P", title="Docket 26-05-10: Exhibit CLP-D", date="2026-06-01", key="D"),
    ]
    current = {"B": "eversource_Docket260510Exhibit_2026", "D": "clp_Docket260510Exhibit_2026c"}
    assert citekeys.assign_keys(exhibits, current) == {
        "D": "clp_Docket260510Exhibit_2026c",
        "A": "clp_Docket260510Exhibit_2026",
        "B": "clp_Docket260510Exhibit_2026a",
        "C": "clp_Docket260510Exhibit_2026b",
    }


def test_assign_keys_duplicate_current_key_first_comes_first():
    vol1 = person("Brattle", title="New York\u2019s Grid Flexibility Potential - Volume 1", date="2025-01-10", key="V1")
    vol2 = person("Brattle", title="New York\u2019s Grid Flexibility Potential - Volume 2", date="2025-01-10", key="V2")
    keys = citekeys.assign_keys([vol1, vol2], {"V1": "brattle_NewYorksGrid_2025a", "V2": "brattle_NewYorksGrid_2025a"})
    assert keys == {"V1": "brattle_NewYorksGrid_2025a", "V2": "brattle_NewYorksGrid_2025"}


def test_assign_keys_respects_reserved():
    item = org("Massachusetts Department of Public Utilities", "MA DPU")
    assert citekeys.assign_keys([item], {}, reserved={"madpu_Docket23150Order_2024"}) == {
        "ITEM0001": "madpu_Docket23150Order_2024a"
    }
