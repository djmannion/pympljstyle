import typing

import pint

import pympljstyle.base


# indicate the attributes available in the Base journal
class HasBaseProtocol(typing.Protocol):
    @property
    def _rc_params(self) -> dict[str, typing.Any]: ...
    @property
    def _content_type(self) -> str: ...
    @property
    def _ureg(self) -> pint.registry.UnitRegistry: ...


# this can be used for general Elsevier journals
class ElsevierMixin:

    def add_custom_settings(self: HasBaseProtocol) -> None:

        dpi = {
            "halftone": 300,
            "combination": 500,
            "line": 1000,
        }

        self._rc_params["savefig.dpi"] = dpi[self._content_type]

    def add_custom_units(self: HasBaseProtocol) -> None:
        self._ureg.define("column = 100 mm; offset: -10 = col")


@pympljstyle.base.add_journal
class Cortex(ElsevierMixin, pympljstyle.base.BaseJournal):

    name = "cortex"
    journal_name = "Cortex"
    custom_units = ("1 column", "1.5 columns", "2 columns")


@pympljstyle.base.add_journal
class JNeurophys(pympljstyle.base.BaseJournal):

    name = "j_neurophys"
    journal_name = "Journal of Neurophysiology"
    custom_units = ("single", "double", "full")

    def add_custom_settings(self) -> None:

        dpi = {
            "halftone": 300,
            "combination": 600,
            "line": 1200,
        }

        self._rc_params["savefig.dpi"] = dpi[self._content_type]

    def add_custom_units(self) -> None:
        self._ureg.define("single = 8.9 cm")
        self._ureg.define("double = 12 cm")
        self._ureg.define("full = 18 cm")
