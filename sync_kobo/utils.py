"""Utils functions."""
import inspect
import pathlib
from datetime import datetime
from functools import wraps

import click
import titlecase
from bs4 import BeautifulSoup


def iter_prompt(old_dict):
    """Yield dict with user-input as values."""
    for (key, val) in old_dict.items():
        prompt_text = titlecase.titlecase(key.replace("_", " "))
        yield {key: click.prompt(prompt_text, default=val, show_default=bool(val))}


def dict_prompt(**old_dict):
    """Yield dict with user-input as values."""
    new_dict = {}
    for (key, val) in old_dict.items():
        prompt_text = titlecase.titlecase(key.replace("_", " "))
        new_dict[key] = click.prompt(prompt_text, default=val, show_default=bool(val))
    return new_dict


def now_str(time=False):
    """Return string to be used as time-stamp."""
    now = datetime.now()
    return now.strftime(f"%Y-%m-%d{('_%H:%M:%S' if time else '')}")


def enforce_argtypes(*arg_types, **kwarg_types):
    """Enforce arg-types for function."""

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(
                *[a if isinstance(a, t) else t(a) for a, t in zip(args, arg_types)],
                **{
                    k: v
                    if k not in kwarg_types or isinstance(v, kwarg_types[k])
                    else kwarg_types[k](v)
                    for k, v in kwargs.items()
                },
            )

        return wrapper

    return inner


def defaults_from_dict(arg_dict, as_type=None):
    """Replace ``None`` as default value of kwargs by the ones found in ``arg_dict``."""

    def inner(func):
        default_kwargs = {
            k: v.default for k, v in inspect.signature(func).parameters.items()
        }
        new_defaults = {
            k: v or (arg_dict[k] if not as_type else as_type(arg_dict[k]))
            for k, v in default_kwargs.items()
        }

        @wraps(func)
        def wrapper(*args, **kwargs):
            for k, v in new_defaults.items():
                kwargs.setdefault(k, v)
            return func(
                *args,
                **kwargs,
            )

        return wrapper

    return inner


def kwargs_to_flags(**kwargs):
    """Convert `kwargs` to flags to pass on to CLI."""
    flag_strings = []
    for (key, val) in kwargs.items():
        if isinstance(val, bool):
            if val:
                flag_strings.append(f"--{key}")
        else:
            flag_strings.append(f"--{key}={val}")
    return " ".join(flag_strings)


def get_annotations(path):
    """Parse kobos .annot-file and return list of (annotations,comments)."""
    with open(path) as file:
        soup = BeautifulSoup(file, "lxml")
    annotations = soup.select("annotation")
    annotations = [
        (
            tag.target.text.strip(),
            tag.content.select("text")[0].text if tag.content else "",
        )
        for tag in annotations
    ]
    return annotations


@enforce_argtypes(pathlib.Path)
def save_annotations(annot_dir):
    """Extract annotations from .annot files in a dir and save as .txt files."""
    for path in annot_dir.glob("*.annot"):
        with open(path.with_suffix(".txt"), "w") as file:
            notes = [note[0] for note in get_annotations(path)]
            file.write("\n".join(notes))


if __name__ == "__main__":
    save_annotations("/home/david/Nextcloud/Book-Annotations")
    # print(get_annotations(path))
