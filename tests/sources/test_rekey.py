from lib.sources import rekey


def test_rewrite_renames_citations_only() -> None:
    renames = {"old_A_2020": "new_A_2020", "new_A_2020": "other_B_2021", "o&r_X_2025": "or_X_2025"}
    text = (
        "See [@old_A_2020, p. 4; @new_A_2020] and -@{o&r_X_2025}.\n"
        "Email old_A_2020@x.org, code `@old_A_2020`, @fig-old_A_2020, [link](#ref-old_A_2020).\n"
        "```\n@old_A_2020\n```\n"
    )
    got, n = rekey.rewrite(text, renames)
    assert got == (
        "See [@new_A_2020, p. 4; @other_B_2021] and -@{or_X_2025}.\n"
        "Email old_A_2020@x.org, code `@old_A_2020`, @fig-old_A_2020, [link](#ref-new_A_2020).\n"
        "```\n@old_A_2020\n```\n"
    )
    assert n == 4


def test_renames_from_plan_sends_duplicates_to_the_kept_item() -> None:
    plans = [
        {"item": "A", "action": "update", "key": "a_New_2020", "old_keys": ["a_Old_2020"]},
        {"item": "B", "action": "duplicate", "duplicate_of": "A", "key": None, "old_keys": ["b_Old_2020"]},
        {"item": "C", "action": "update", "key": "c_Same_2020", "old_keys": ["c_Same_2020"]},
    ]
    assert rekey.renames_from_plan(plans) == {"a_Old_2020": "a_New_2020", "b_Old_2020": "a_New_2020"}


def test_table_skips_ambiguous_keys_so_reruns_are_safe(tmp_path) -> None:
    renames = {"k_2025": "k_2025a", "k_2025a": "k_2025", "old_X_2020": "new_X_2020"}
    path = tmp_path / "renames.csv"
    rekey.write_renames(renames, path)
    assert rekey.read_ambiguous(path) == {"k_2025", "k_2025a"}
    safe = rekey.read_renames(path)
    once, _ = rekey.rewrite("@old_X_2020 @k_2025", renames)
    assert once == "@new_X_2020 @k_2025a"
    assert rekey.rewrite(once, safe) == (once, 0)
