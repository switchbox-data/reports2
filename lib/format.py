"""String formatting for report narrative prose.

These turn values exported by an analysis notebook into the text an
``index.qmd`` drops inline. They do no computation.
"""

from __future__ import annotations

from collections.abc import Iterable

MONTH_NAMES = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December",
}


def pct(x: float, accuracy: int = 0) -> str:
    """Format a fraction as a percent string, e.g. ``0.43`` -> ``"43%"``."""
    return f"{x * 100:,.{accuracy}f}%"


def month_list(months: Iterable[str]) -> str:
    """Join month abbreviations as prose.

    ``["Jun", "Jul", "Aug"]`` -> ``"June, July, and August"``.
    """
    names = [MONTH_NAMES.get(m, m) for m in months]
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]
