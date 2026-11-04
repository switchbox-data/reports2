"""Index rows are upserted by file path: reruns never duplicate."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.sources import indexes

GLOBAL = """# Context index

## domain/

| File | Use when |
| ---- | ---- |
| a.md | Domain. |

## sources/

Primary sources.

| File | Use when working on … |
| ---- | ---- |
| `bonbright_1960/` (directory) | Bonbright. |
| ma_hp_rates/older.md | Older document. |

## code/

Code notes.
"""

FOLDER = """# MA

Intro.

| File | Docket / filed | What it is and why it is here |
| ---- | ---- | ---- |
| `older.xlsx` | 25-55; 2025-04-17 | Original model. |

After the table.
"""


@pytest.fixture
def readme(tmp_path: Path) -> Path:
    path = tmp_path / "README.md"
    path.write_text(GLOBAL)
    return path


def test_add_then_update_then_unchanged(readme):
    assert indexes.upsert_global_row("ma_hp_rates/new.md", "New order.", readme) == "added"
    assert indexes.upsert_global_row("ma_hp_rates/new.md", "New order.", readme) == "unchanged"
    assert indexes.upsert_global_row("ma_hp_rates/new.md", "New order, revised.", readme) == "updated"
    text = readme.read_text()
    assert text.count("ma_hp_rates/new.md") == 1
    lines = text.splitlines()
    new_row = lines.index("| ma_hp_rates/new.md | New order, revised. |")
    assert lines[new_row - 1] == "| ma_hp_rates/older.md | Older document. |"
    assert "| a.md | Domain. |" in lines  # the other table is untouched
    assert "## code/" in lines


def test_directory_row_covers_files_in_that_folder(readme):
    assert indexes.upsert_global_row("bonbright_1960/ch01.md", "Chapter 1.", readme) == "covered"
    assert "ch01" not in readme.read_text()
    assert indexes.has_global_row("bonbright_1960/ch01.md", readme)
    assert not indexes.has_global_row("ma_hp_rates/none.md", readme)


def test_pipes_and_newlines_in_descriptions_are_escaped(readme):
    indexes.upsert_global_row("ma_hp_rates/p.md", "Rates | tariffs\nand bills.", readme)
    assert "| ma_hp_rates/p.md | Rates \\| tariffs and bills. |" in readme.read_text()


def test_folder_row_matches_the_tables_columns(tmp_path):
    path = tmp_path / "README.md"
    path.write_text(FOLDER)
    assert indexes.upsert_folder_row(path, "new.md", ["25-55; 2025-06-01", "Order.", "extra"]) == "added"
    assert indexes.upsert_folder_row(path, "new.md", ["25-55; 2025-06-01", "Order.", "extra"]) == "unchanged"
    assert indexes.upsert_folder_row(path, "new.md", ["25-55; 2025-06-01", "Order, revised."]) == "updated"
    text = path.read_text()
    assert text.count("`new.md`") == 1 and "After the table." in text
    rows = [line for line in text.splitlines() if line.startswith("| `new.md`")]
    assert rows == ["| `new.md` | 25-55; 2025-06-01 | Order, revised. |"]
    indexes.upsert_folder_row(path, "short.md", ["only-one"])
    assert "| `short.md` | only-one |  |" in text or "| `short.md` | only-one |  |" in path.read_text()


def test_global_row_in_another_section_is_replaced_not_duplicated(readme):
    readme.write_text(GLOBAL + "\n## dockets/\n\n| File | Use |\n| ---- | ---- |\n| ma_hp_rates/x.md | Old. |\n")
    assert indexes.upsert_global_row("ma_hp_rates/x.md", "New.", readme) == "updated"
    text = readme.read_text()
    assert text.count("ma_hp_rates/x.md") == 1 and "| ma_hp_rates/x.md | New. |" in text


def test_workbook_stub_replaces_the_row_naming_the_workbook(readme):
    readme.write_text(GLOBAL.replace("ma_hp_rates/older.md", "ma_hp_rates/older.xlsx"))
    assert indexes.upsert_global_row("ma_hp_rates/older.md", "Model.", readme) == "updated"
    text = readme.read_text()
    assert "older.xlsx" not in text and "| ma_hp_rates/older.md | Model. |" in text


def test_folder_row_in_a_later_file_table_is_replaced(tmp_path):
    path = tmp_path / "README.md"
    path.write_text(
        FOLDER + "\n### Orders\n\n| File | Docket / filed | What |\n| ---- | ---- | ---- |\n| `order.md` | 1 | Old. |\n"
    )
    assert indexes.upsert_folder_row(path, "order.md", ["1", "New."]) == "updated"
    assert indexes.upsert_folder_row(path, "older.md", ["25-55; 2025-04-17", "Model."]) == "updated"
    text = path.read_text()
    assert text.count("`order.md`") == 1 and "| `order.md` | 1 | New. |" in text
    assert "older.xlsx" not in text and text.count("`older.md`") == 1


def test_folder_without_a_file_table_is_an_error(tmp_path):
    path = tmp_path / "README.md"
    path.write_text("# Nothing here\n")
    with pytest.raises(ValueError):
        indexes.upsert_folder_row(path, "x.md", ["a"])
