import typing
import abc

import pint

import pympljstyle.base


@pympljstyle.base.journal
class ProcRoyalSocB(pympljstyle.base.BaseJournal):

    name = "proc_b"

    def add_custom_settings(self) -> None:

        dpi = {
            "halftone": 300,
            "combination": 500,
            "line": 1000,
        }

        self._rc_params["savefig.dpi"] = dpi[self._content_type]

    def add_custom_units(self) -> None:
        self._ureg.define(
            "column = 100 mm; offset: -10 = col"
        )
