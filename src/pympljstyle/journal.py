import typing
import abc

import pint


class BaseJournal(abc.ABC):

    def __init__(
        self,
        width: str,
        height: str,
        content_type: str = "combination",
    ) -> None:

        self._width_raw = width
        self._height_raw = height

        if content_type not in ["halftone", "combination", "line"]:
            raise ValueError("Unknown `content_type`")

        self._content_type = content_type

        self._ureg = pint.UnitRegistry(
            cache_folder=":auto:",
            autoconvert_offset_to_baseunit=True,
        )

        self._rc_params: dict[str, typing.Any] = {}

    @abc.abstractmethod
    def add_custom_units(self) -> None:
        pass

    @abc.abstractmethod
    def add_custom_settings(self) -> None:
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        return self.name

    def get_size(self, units: str = "inches") -> tuple[float, float]:

        width = self._ureg.Quantity(value=self._width_raw)

        self._ureg.define(
            f"width = 1 * {width.to('mm')} = w"
        )

        height = self._ureg.Quantity(value=self._height_raw)

        return tuple(
            dim.to(other=units).magnitude
            for dim in (width, height)
        )

    @property
    def rcParams(self) -> dict[str, typing.Any]:  # noqa: N802

        self.add_custom_settings()
        self.add_custom_units()

        figure_size_entry = {
            "figure.figsize": self.get_size(units="inches"),
        }

        return self._rc_params | figure_size_entry


registry: dict[str, type[BaseJournal]] = {}

T = typing.TypeVar("T", bound=BaseJournal)

def journal(cls: type[T]) -> type[T]:
    registry[str(cls.name)] = cls
    return cls


@journal
class ProcRoyalSocB(BaseJournal):

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
