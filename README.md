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
The height of the figure can be (optionally) specified using the same set of units, with the additional option of using a 'width' (or 'w') unit to allow for the height to be a multiple of the width (e.g., '0.5 widths').
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



