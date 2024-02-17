__version__ = "0.1"

import pympljstyle.journals  # noqa: F401

from .base import registry

from .interface import apply_style

__all__ = ("apply_style", "registry")
