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


def test_all_styles() -> None:

    for journal_name in pympljstyle.registry:

        if journal_name == "custom_test":
            continue

        _ = pympljstyle.get_style(
            journal_name=journal_name,
            width="1cm",
        )
