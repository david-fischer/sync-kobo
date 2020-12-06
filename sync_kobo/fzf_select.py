"""Use pyfzf to select dictionary."""
from copy import deepcopy
from functools import partial

import pyfzf
import tabulate
import toolz
from colors import color
from plumbum.commands.processes import ProcessExecutionError as FZFError

from .utils import kwargs_to_flags

fzf = pyfzf.FzfPrompt()
BOM = "\uFEFF"

PREVIEW_STRINGS = {
    "colorized code output": '" SOME_CMD | pygmentize -l py3 -O style=monokai"',
}


def cut_values(item, max_width):
    """Cut length of strings of columns."""
    key, val = item
    max_width = max_width if isinstance(max_width, int) else max_width[key]
    if isinstance(val, str) and len(val) > max_width:
        val = val[: max_width - 1] + "…"
    return key, val


def colorize_lines(table_lines, dicts, color_map):
    """Colorize lines."""
    if color_map is None:
        return table_lines
    table_lines = deepcopy(table_lines)
    for i, d in enumerate(dicts):
        line_color = color_map(d)
        if line_color:
            table_lines[i] = color(table_lines[i], line_color)
    return table_lines


def get_unique_lines(multiline_string):
    """Use a non-breaking zero-width space :const:`BOM` to make each line unique."""
    return [f"{row}{BOM * i}" for i, row in enumerate(multiline_string.splitlines())]


def get_table_lines(dicts, max_width: int or dict = 50, keys=None):
    """Return list of lines formatted as table."""
    display_dicts = [{key: d.get(key) for key in (keys or d)} for d in dicts]
    cut_at_max_width = partial(cut_values, max_width=max_width)
    display_dicts = [toolz.itemmap(cut_at_max_width, d) for d in display_dicts]
    table_string = tabulate.tabulate(display_dicts, headers="keys", tablefmt="github")
    table_lines = get_unique_lines(table_string)
    return table_lines


def fzf_select(choices, return_index=False, header=None, on_error=None, **kwargs):
    """Wrapper-function for fzf.

    * All fzf command line options are available as kwargs.
    * Can handle events specified as `on_event=func_without_args`.
    Adds <EVENT> to choices and executes function if it was selected.
    If the function returns something that evaluates to True,
    this is appended to the returned selection.
    """
    if header:
        kwargs["header-lines"] = 1 + header.count("\n")
    kwargs.setdefault("cycle", True)
    events, selectors = get_events_and_selectors(kwargs)
    fzf_lines = ([header] if header else []) + list(selectors.values()) + choices
    try:
        selection = fzf.prompt(fzf_lines, kwargs_to_flags(**kwargs))
    except FZFError as error:
        if on_error:
            return on_error()
        raise error
    event_results = handle_events(selection, events, selectors)
    return (
        selection
        if not return_index
        else [choices.index(selected) for selected in selection]
    ) + event_results


def handle_events(selection, events, selectors):
    """Execute functions corresponding to the selector contained in selection."""
    results = []
    for k, v in selectors.items():
        if v in selection:
            results.append(events[k]())
            selection.remove(v)
    return [res for res in results if res]


def get_events_and_selectors(kwargs):
    """Extract events and corresponding selectors from kwargs."""
    events = {
        key: kwargs.pop(key) for key in list(kwargs.keys()) if key.startswith("on_")
    }
    selectors = {key: f"<{key[3:].upper()}>" for key in events}
    return events, selectors


def fzf_select_single(
    choices, return_index=False, header=None, on_error=None, **kwargs
):
    """Select single entry using fzf."""
    kwargs["multi"] = False
    selection = fzf_select(
        choices, return_index=return_index, header=header, on_error=on_error, **kwargs
    )
    return selection[0] if selection else None


def fzf_select_dicts(
    dicts,
    max_width=20,
    color_map=None,
    keys=None,
    on_error=None,
    **kwargs,
):
    """Display dictionaries as lines of table and use fzf to select entries.

    **kwargs are passed as flags to fzf. Possible keys include e.g.:
        * multi=True/False
        * preview="cat {}"
    """
    if color_map:
        kwargs.setdefault("ansi", True)
    cols, separator, *data = get_table_lines(dicts, max_width, keys)
    kwargs["header"] = "\n".join(
        (kwargs.get("header", ""), separator, cols, separator)
    ).strip()
    fzf_lines = colorize_lines(data, dicts, color_map)
    selection = fzf_select(
        fzf_lines,
        return_index=False,
        on_error=on_error,
        **kwargs,
    )
    return [
        dicts[data.index(selected)] if selected in data else selected
        for selected in selection
    ]


if __name__ == "__main__":
    a = fzf_select_dicts(
        [{"a": 1, "b": i, "c": "abc" * i} for i in range(10)],
        color_map=lambda d: "red" if d["b"] % 2 else "blue",
        header="Some\nmultiline\nheader:",
        on_error=lambda: print("OOOOps."),
        on_new=lambda: "MAKE NEW OBJECT!",
        on_edit=lambda: print("EDIT OBJECT!"),
    )
    print(a)
