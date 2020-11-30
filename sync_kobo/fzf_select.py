"""Selection functions via fzf (pyfzf)."""
import plumbum
from pyfzf.pyfzf import FzfPrompt

from sync_kobo.utils import kwargs_to_flags

fzf = FzfPrompt()


def fzf_select(choices, header=None, **kwargs):
    """Select single entry using fzf."""
    if header:
        kwargs["header-lines"] = 1 + header.count("\n")
    kwargs.setdefault("cycle", True)
    events = {}
    for key in list(kwargs.keys()):
        if key.startswith("on_"):
            events[key] = kwargs.pop(key)
    event_selectors = {
        key: f"<{key[3:].upper()}>" for key in events if key != "on_error"
    }
    fzf_lines = [header] if header else [] + choices + list(event_selectors.values())
    try:
        selection = fzf.prompt(fzf_lines, kwargs_to_flags(**kwargs))
    except plumbum.commands.processes.ProcessExecutionError as error:
        if "on_error" in events:
            if events["on_error"]:
                events["on_error"]()
            return []
        raise error
    for k, v in event_selectors.items():
        if selection == v:
            events[k]()
    return selection


def fzf_select_multi(choices, header=None, **kwargs):
    """Select multiple entries using fzf."""
    kwargs.setdefault("multi", True)
    if header:
        kwargs["header-lines"] = 1 + header.count("\n")
    events = {}
    for key in list(kwargs.keys()):
        if key.startswith("on_"):
            events[key] = kwargs.pop(key)
    # event_selectors = {key: f"<{key[3:].upper()}>" for key in events}
    fzf_lines = [header] if header else [] + choices
    try:
        selection = fzf.prompt(fzf_lines, kwargs_to_flags(**kwargs))
    except plumbum.commands.processes.ProcessExecutionError as error:
        if "on_error" in events:
            if events["on_error"]:
                events["on_error"]()
            return []
        raise error
    return selection
