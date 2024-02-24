# pympljstyle

A Python library for specifying and applying journal-specific styles to matplotlib figures.

## Installation

The library can be installed using `pip`:

```bash
pip install pympljstyle
```

## Usage

### Listing the available journals

The journals that have registered styles can be accessed using `get_registered_journals`:

```python
import pympljstyle
registered_journals = pympljstyle.get_registered_journals()
print(*registered_journals, sep="\n")
```

This shows the journal identifier followed by its complete title and any registered custom size units.

```output
"cortex": Cortex (custom units: 1 column, 1.5 columns, 2 columns)
"j_neurophys": Journal of Neurophysiology (custom units: single, double, full)
```

### Using a built-in style

To use a built-in style, first identify the relevant journal identifier as shown above.
Then, the width of the figure needs to be specified.
This can be in typical units like centimetres or inches, but many journal style definitions also support more journal-specific units like 'columns' or identifiers such as 'single' (the custom units that are supported by a particular journal style are shown in the output of `get_registered_journals`, as shown in the previous section).
The height of the figure can be specified using the same set of units, with the additional option of using a 'width' (or 'w') unit to allow for the height to be a multiple of the width (e.g., '0.5 widths').
Finally, the sort of content that will be shown in the figure can (optionally) be specified.
This is typically used by journal styles to identify the appropriate DPI to use when exporting the figure.
The available options are `halftone`, `combination` (the default), and `line`.

With the above information, the style for a particular journal can be applied using the `apply_style` context manager:

```python
import matplotlib.pyplot as plt
import pympljstyle

with pympljstyle.apply_style(
    journal_name="cortex",
    width="1.5 cols",
    height="0.5 widths",
    content_type="line",
):
    # the journal-specific styles are applied

# the settings are returned to their previous values
```

If you want to access the settings directly, rather than applying them to a context manager, you can use the `get_style` function.
This function has the same call signature of `apply_style`.

Note that these functions also set a few 'opinionated' settings that are not journal specific.
These can be disabled by setting the parameter `with_opinionated_defaults` to `False`.

### Specifying a new style

If the desired journal style is not present in the package, you can add your own specification of the journal style to the package registry.
For example, we can re-create the style for the journal Cortex that is present in the package.
To do so, first create a class that inherits from `pympljstyle.BaseJournal` and is decorated by `@pympljstyle.add_journal`:

```python
@pympljstyle.add_journal
class Cortex(pympljstyle.BaseJournal):
    ...
```

The key attributes that are inherited from `BaseJournal` are:

* `_rc_params`: the dictionary of custom matplotlib [`rcParams`](https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams) settings.
* `_content_type`: the user-specified type of content in the figure (`halftone`, `combination`, or `line`).
* `_ureg`: a [pint](https://pint.readthedocs.io/en/stable/index.html) [`UnitRegistry`](https://pint.readthedocs.io/en/stable/api/base.html#pint.UnitRegistry) instance.

This class is required to have three class attributes:

* `name`: a journal identifier, typically in snake case.
* `journal_name`: the complete journal title.
* `custom_units`: a tuple of strings that describes the custom size units that are available for the journal.

For Cortex, this looks like:

```python
@pympljstyle.add_journal
class Cortex(pympljstyle.BaseJournal):

    name = "cortex"
    journal_name = "Cortex"
    custom_units = ("1 column", "1.5 columns", "2 columns")
```

The class is also required to have two methods:

* `add_custom_settings`: where custom entries into `self._rc_params` are made.
* `add_custom_units`: where custom units are defined.

For Cortex, the custom setting that we will use is their specification for the DPI of saved figures.
Because that is dependent on the content type, we will use the `_content_type` variable to set the appropriate DPI value in `_rc_params`:

```python
@pympljstyle.add_journal
class Cortex(pympljstyle.BaseJournal):

    name = "cortex"
    journal_name = "Cortex"
    custom_units = ("1 column", "1.5 columns", "2 columns")

    def add_custom_settings(self) -> None:

        dpi = {
            "halftone": 300,
            "combination": 500,
            "line": 1000,
        }

        self._rc_params["savefig.dpi"] = dpi[self._content_type]
```

We can also specify some custom units - in particular, we can specify figure widths in 'columns'.
As per their [website](https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-sizing#1-number-of-pixels) (actually publisher rather than journal-specific), 1 column is 90 mm, 1.5 columns is 140 mm, and 2 columns is 190 mm.
To specify this relationship in `pint`, we need to convert the points into a slope and a y-intercept.
Here, the slope is 100 and the y-intercept is -10.
In [the way of defining custom units](https://pint.readthedocs.io/en/stable/advanced/defining.html#programmatically), the y-intercept is referred to as the `offset`.
For Cortex, the 'columns' unit (which can also be referred to as 'column', 'col', or 'cols') is set via:

```python
@pympljstyle.add_journal
class Cortex(pympljstyle.BaseJournal):

    name = "cortex"
    journal_name = "Cortex"
    custom_units = ("1 column", "1.5 columns", "2 columns")

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
```

Once complete, consider contributing your new journal styles to the package via a pull request.


## Development

### Build and release process

First, build the package (after having previously run `pip install -e .[build]`):

```bash
python -m build
```

This will produce files in the `dist/` sub-directory.

Then, test the ability to upload to the test PyPI server:

```bash
python -m twine upload --repository testpypi dist/*
```

If that all looks OK, then upload to PyPI:

```bash
python -m twine twine upload dist/*
```

