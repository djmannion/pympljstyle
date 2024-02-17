__version__ = "0.1"

import pympljstyle.journals  # noqa: F401

from .base import registry, BaseJournal

from .interface import apply_style, get_style, get_registered_journals

__all__ = (
    "apply_style",
    "get_style",
    "registry",
    "get_registered_journals",
    "BaseJournal",
)
