from lib.sources import checks


def org_item(name, short=None, **fields):
    data = {"creators": [{"creatorType": "author", "name": name}], "title": "Docket 23-150: Order", "date": "2024"}
    if short:
        data["extra"] = f"tex.shortauthor: {short}"
    return data | fields


def codes(findings):
    return {(f.code, f.key) for f in findings}


def test_clean_entry_has_no_findings():
    entries = [("madpu_Docket23150Order_2024", org_item("Massachusetts Department of Public Utilities", "MA DPU"))]
    assert checks.run_checks(entries) == []


def test_short_form_conflicts():
    entries = [
        ("bug_GAAP_2024", org_item("Brooklyn Union Gas Company", "BUG")),
        ("kedny_GAAP_2024", org_item("Brooklyn Union Gas Company", "KEDNY")),
        ("ng_A_2024", org_item("National Grid", "NG")),
        ("ng_B_2024", org_item("Northern Illinois Gas Company", "NG")),
    ]
    found = {f.code for f in checks.run_checks(entries)}
    assert {"FULL_NAME_SEVERAL_SHORT_FORMS", "SHORT_FORM_SEVERAL_NAMES"} <= found


def test_name_shape_errors():
    entries = [
        ("dpu_Docket23150Order_2024", org_item("DPU")),
        (
            "company_Statement_2022",
            {
                "creators": [{"creatorType": "author", "firstName": "Boston Gas", "lastName": "Company"}],
                "title": "Statement",
                "date": "2022",
            },
        ),
        ("eldringhoff_Testimony_2026", org_item("Polly Eldringhoff", title="Testimony", date="2026")),
    ]
    found = codes(checks.run_checks(entries))
    assert ("AUTHOR_IS_ABBREVIATION", "dpu_Docket23150Order_2024") in found
    assert ("ORG_AS_TWO_FIELD_NAME", "company_Statement_2022") in found
    assert ("PERSON_IN_ONE_FIELD", "eldringhoff_Testimony_2026") in found


def test_publisher_repeating_author_and_duplicate_keys():
    item = org_item("ISO New England", "ISO-NE", publisher="ISO New England", title="Regulation Clearing", date="2025")
    found = codes(checks.run_checks([("isone_RegulationClearing_2025", item), ("isone_RegulationClearing_2025", item)]))
    assert ("PUBLISHER_REPEATS_AUTHOR", "isone_RegulationClearing_2025") in found
    assert ("DUPLICATE_KEY", "isone_RegulationClearing_2025") in found


def test_multi_org_short_form_must_join_members():
    nyseg = org_item("New York State Electric & Gas", "NYSEG")
    rge = org_item("Rochester Gas and Electric", "RG&E")
    joint = org_item("New York State Electric & Gas", "NYSEG, RG&E")
    joint["creators"].append({"creatorType": "author", "name": "Rochester Gas and Electric"})
    found = codes(checks.run_checks([("nyseg_A_2024", nyseg), ("rge_A_2024", rge), ("nyseg_B_2024", joint)]))
    assert ("MULTI_ORG_SHORT_FORM", "nyseg_B_2024") in found


def test_key_warnings():
    entries = [
        ("dpu_Docket23150Order_2024", org_item("Massachusetts Department of Public Utilities", "MA DPU")),
        (
            "madpu_ExhibitSeasonalHP_nd",
            org_item("Massachusetts Department of Public Utilities", "MA DPU", title="Exhibit Seasonal HP", date=""),
        ),
        (
            "eia_HeatingOilPropanePrices_2025",
            org_item(
                "U.S. Energy Information Administration",
                "EIA",
                title="Heating Oil and Propane Prices",
                date="2024",
                citationKey="eia_HeatingOilPropanePrices_2024",
            ),
        ),
        ("_HousingDataProfiles_", {"creators": [], "title": "Housing Data Profiles"}),
    ]
    found = codes(checks.run_checks(entries))
    assert ("KEY_NOT_CANONICAL", "dpu_Docket23150Order_2024") in found
    assert ("UNDATED_KEY", "madpu_ExhibitSeasonalHP_nd") in found
    assert ("PIN_DIFFERS_FROM_NATIVE_KEY", "eia_HeatingOilPropanePrices_2025") in found
    assert ("NO_CREATOR", "_HousingDataProfiles_") in found
    assert ("KEY_NOT_CITABLE", "_HousingDataProfiles_") in found


def test_key_not_citable_matches_pandoc_emphasis():
    for key in ("_HousingDataProfiles_", "_MA_BenefitMatrix_2025_", "_247400d338814d7bb28d343316b26494_"):
        assert checks.key_not_citable(key), key
    for key in (
        "_DirectTestimonyRevenue_2022",
        "_RhodeIsland2024_a",
        "__c",
        "baker_ICCReplacesControversial_",
        "madpu_Docket23150Order_2024",
    ):
        assert not checks.key_not_citable(key), key


def test_chicago_join():
    assert checks.chicago_join(["NYSEG", "RG&E"]) == "NYSEG and RG&E"
    assert (
        checks.chicago_join(["Nicor Gas", "Peoples Gas", "North Shore Gas"])
        == "Nicor Gas, Peoples Gas, and North Shore Gas"
    )
    assert checks.chicago_join(["A", "B", "C", "D"]) == "A et al."


def test_legal_acronym_names_are_not_abbreviations():
    data = {"creators": [{"creatorType": "author", "name": "RMI"}], "title": "T", "date": "2024"}
    codes = {f.code for f in checks.run_checks([("rmi_T_2024", data)])}
    assert "AUTHOR_IS_ABBREVIATION" not in codes
