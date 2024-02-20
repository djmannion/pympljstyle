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

    @property
    @abc.abstractmethod
    def journal_name(self) -> str:
        return self.journal_name

    @property
    @abc.abstractmethod
    def custom_units(self) -> tuple[str, ...]:
        return self.custom_units

    @classmethod
    def info(cls) -> str:  # noqa: ANN102
        info_str = f'"{cls.name}": {cls.journal_name}'
        # explicit type verification because mypy gets confused by properties
        custom_units = cls.custom_units
        assert isinstance(custom_units, tuple)
        if len(custom_units) > 0:
            info_str += f' (custom units: {", ".join(custom_units)})'
        return info_str

    def get_size(self, units: str = "inches") -> tuple[float, float]:

        width = self._ureg.Quantity(value=self._width_raw)

        self._ureg.define(f"width = 1 * {width.to('mm')} = w")

        height = self._ureg.Quantity(value=self._height_raw)

        return tuple(dim.to(other=units).magnitude for dim in (width, height))

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


def add_journal(cls: type[T]) -> type[T]:
    registry[str(cls.name)] = cls
    return cls


def get_defaults() -> dict[str, typing.Any]:

    defaults = {
        # font sizes
        "font.size": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7,
        "legend.title_fontsize": 7,
        # other params
        "lines.linewidth": 1,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "figure.frameon": False,
        "font.sans-serif": [
            "Arial",
            "Nimbus Sans",
            "Nimbus Sans L",
            "Helvetica",
        ],
    }

    return defaults
