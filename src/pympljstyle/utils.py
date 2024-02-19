


def apply_dropped_spines(ax, amount_pt: int | float = 10) -> None:

    for spine in ax.spines.values():
        spine.set_position(("outward", amount_pt))
