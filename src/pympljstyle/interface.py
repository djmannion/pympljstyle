import typing
import contextlib

import matplotlib as mpl

import pympljstyle.base


def apply_style(
    journal_name: str,
    width: str,
    height: str = "1.5 widths",
    content_type: str = "combination",
    with_opinionated_defaults: bool = True,
) -> contextlib.AbstractContextManager[None]:

    style = get_style(
        journal_name=journal_name,
        width=width,
        height=height,
        content_type=content_type,
        with_opinionated_defaults=with_opinionated_defaults,
    )

    context = mpl.rc_context(rc=style)

    return context


def get_style(
    journal_name: str,
    width: str,
    height: str = "1.5 widths",
    content_type: str = "combination",
    with_opinionated_defaults: bool = True,
) -> dict[str, typing.Any]:

    JournalStyle = pympljstyle.base.registry[journal_name]  # noqa: N806

    journal_style = JournalStyle(width=width, height=height, content_type=content_type)

    if with_opinionated_defaults:
        rc_params = pympljstyle.base.get_defaults()
    else:
        rc_params = {}

    rc_params |= journal_style.rcParams

    return rc_params


def get_registered_journals() -> tuple[str, ...]:

    return tuple(
        JournalStyle.info() for JournalStyle in pympljstyle.base.registry.values()
    )
