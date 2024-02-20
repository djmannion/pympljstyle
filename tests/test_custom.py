import pympljstyle


def test_add_custom() -> None:

    assert "custom_test" not in pympljstyle.registry

    @pympljstyle.add_journal
    class CustomTest(pympljstyle.BaseJournal):

        name = "custom_test"
        journal = "Custom Test"
        custom_units = ()

        def add_custom_settings(self) -> None:
            pass

        def add_custom_units(self) -> None:
            pass

    assert "custom_test" in pympljstyle.registry
