#!/usr/bin/env python3
"""This script provides the main function which serves as entry-point for setup.py."""
import os
import pathlib
import shutil
import sys

import click

# FIX: This way the script is both directly callable and usable via import.
# adding the local version of the package to the beginning of PATH ignores
# other installed package with same name (only important for development)
import sqlalchemy.exc

NT = "\n\t"
if not __package__:
    __package__ = "sync_kobo"  # pylint: disable=redefined-builtin
    pkg_path = pathlib.Path(__file__).absolute().parent.parent
    sys.path = [str(pkg_path)] + sys.path

# RELATIVE IMPORTS FROM OTHER FILES HERE:
# pylint: disable=wrong-import-position

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

from . import CONFIG_PATH, config
from .fzf_select import fzf_select_multi
from .utils import defaults_from_dict, now_str, with_argtypes

try:
    from .db import choose_shelf, print_books_read
except sqlalchemy.exc.OperationalError:
    choose_shelf = print_read = lambda: sys.exit(
        click.echo(f"Could not find kobo database. Check paths in {CONFIG_PATH}") or 1
    )


def check_connected(kobo_dir):
    """Check if kobo_dir exists and notify user otherwise."""
    kobo_dir = (
        kobo_dir if isinstance(kobo_dir, pathlib.Path) else pathlib.Path(kobo_dir)
    )
    if not kobo_dir.exists():
        click.echo(
            f'Kobo reader not found at {config["paths"]["kobo_dir"]}.\n'
            f"Connect reader or change path in {CONFIG_PATH}."
        )
        sys.exit(1)


@defaults_from_dict(config["paths"], as_type=pathlib.Path)
def backup_db(kobo_db_path=None, db_bkp_dir=None):
    """Make a backup of data-base of kobo reader."""
    os.makedirs(db_bkp_dir, exist_ok=True)
    shutil.copy(
        kobo_db_path,
        db_bkp_dir / f"Kobo_Reader_bkp_{now_str(time=True)}.sqlite",
    )
    click.echo(f"Backed up kobo database to {db_bkp_dir}.")


def export_annotations(kobo_annot_dir, annot_export_dir):
    """Export annotations."""
    shutil.copytree(kobo_annot_dir, annot_export_dir, dirs_exist_ok=True)


def get_new_books(kobo_book_dir, book_import_dir):
    """Get books that are in `kobo_import_dir` but not `kobo_book_dir`."""
    kobo_books = kobo_book_dir.glob("*.*")
    kobo_book_names = {k.name for k in kobo_books}
    books = book_import_dir.glob("*.*")
    return [path for path in books if not path.name in kobo_book_names]


@with_argtypes(pathlib.Path)
def import_book(new_book, kobo_book_dir):
    """Choose shelf (on e-reader) of book and copy to device."""
    choose_shelf(new_book)
    shutil.copy(new_book, kobo_book_dir)


def import_selection(new_books, kobo_book_dir):
    """Prompt user with selection and import selected books."""
    if new_books:
        selected = fzf_select_multi(
            new_books, header="Choose books to upload:", on_error=None
        )
        for new_book in selected:
            import_book(new_book, kobo_book_dir)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@defaults_from_dict(config["paths"], as_type=pathlib.Path)
def cli(
    kobo_book_dir=None,
    book_import_dir=None,
    kobo_annot_dir=None,
    annot_export_dir=None,
):
    """Sync books and annotations with Kobo e-reader."""
    check_connected(kobo_book_dir)
    backup_db()
    export_annotations(kobo_annot_dir, annot_export_dir)
    new_books = get_new_books(kobo_book_dir, book_import_dir)
    import_selection(new_books, kobo_book_dir)
    print_books_read()


if __name__ == "__main__":
    cli()
