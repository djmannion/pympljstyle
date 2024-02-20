import matplotlib.pyplot as plt

import pympljstyle


def test_initial_reg() -> None:
    assert len(pympljstyle.get_registered_journals()) > 0


def test_rc_params() -> None:

    style = pympljstyle.get_style(
        journal_name="cortex",
        width="1 col",
    )

    assert style != {}


def test_rc_params_set() -> None:

    start_rc_params = dict(plt.rcParams)

    with pympljstyle.apply_style(
        journal_name="cortex",
        width="1 col",
    ):

        curr_rc_params = dict(plt.rcParams)

        assert curr_rc_params != start_rc_params

    end_rc_params = dict(plt.rcParams)

    assert start_rc_params == end_rc_params
