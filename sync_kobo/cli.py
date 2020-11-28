#!/usr/bin/env python3
"""This script provides the main function which serves as entry-point for setup.py."""
import pathlib
import sys

import click

# FIX: This way the script is both directly callable and usable via import.
# adding the local version of the package to the beginning of PATH ignores
# other installed package with same name (only important for development)
if not __package__:
    __package__ = "sync_kobo"  # pylint: disable=redefined-builtin
    pkg_path = pathlib.Path(__file__).absolute().parent.parent
    sys.path = [str(pkg_path)] + sys.path

# RELATIVE IMPORTS FROM OTHER FILES HERE:
# pylint: disable=wrong-import-order

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
def cli():
    """Print placeholder text."""
    click.echo("Called main function.")


if __name__ == "__main__":
    cli()
