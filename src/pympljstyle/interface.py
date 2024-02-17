import typing

import pympljstyle.base


def apply_style(
    journal_name: str,
    width: str,
    height: str = "1.5 widths",
) -> dict[str, typing.Any]:

    JournalStyle = pympljstyle.base.registry[journal_name]  # noqa: N806

    journal_style = JournalStyle(width=width, height=height)

    rc_params = journal_style.rcParams

    return rc_params
