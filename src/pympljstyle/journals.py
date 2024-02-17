
import pympljstyle.base


@pympljstyle.base.journal
class Cortex(pympljstyle.base.BaseJournal):

    name = "cortex"
    journal_name = "Cortex"

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


@pympljstyle.base.journal
class JNeurophys(pympljstyle.base.BaseJournal):

    name = "j_neurophys"
    journal_name = "Journal of Neurophysiology"

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
