
import typing

import pympljstyle.journal


def apply_style(
    journal_name: str,
    width: "2 cols",
    height: "1.5 widths",
) -> None:

    JournalStyle = pympljstyle.journal.registry[journal_name]

    journal_style = JournalStyle(width=width, height=height)

    rc_params = journal_style.rcParams

    return rc_params
