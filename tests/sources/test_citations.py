from pathlib import Path

from lib.sources.citations import find_citations, report_sources

TEXT = """---
title: Test
nocite: |
  @nocite_Key_2020
---

Narrative @madpu_Docket23150Order_2024 says; see [@a_B_2020, p. 4; -@c_D_2021] and @{o&r_2018MarginalCost_2019}.
Trailing punctuation: @e_F_2022. Email name@switch.box and x@y.org are not citations.
Cross-refs @fig-bill-change and @tbl-rates are skipped; so is `@inline_Code_2020`.
Link: [see](#ref-g_H_2023).

```python
x = "@fenced_Code_2020"
```
"""


def test_find_citations():
    keys = [c.key for c in find_citations(TEXT)]
    assert keys == [
        "nocite_Key_2020",
        "madpu_Docket23150Order_2024",
        "a_B_2020",
        "c_D_2021",
        "o&r_2018MarginalCost_2019",
        "e_F_2022",
        "g_H_2023",
    ]


def test_line_numbers():
    by_key = {c.key: c.line for c in find_citations(TEXT)}
    assert by_key["madpu_Docket23150Order_2024"] == 7


def test_report_sources_excludes_rendered_output(tmp_path: Path):
    for rel in ("a/index.qmd", "a/notes.md", "a/docs/index.md", "a/_freeze/x.md", "a/cache/x.qmd", "a/plot.py"):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x")
    assert [p.relative_to(tmp_path).as_posix() for p in report_sources(tmp_path)] == ["a/index.qmd", "a/notes.md"]
