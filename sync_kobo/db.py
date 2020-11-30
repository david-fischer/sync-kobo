"""Interaction with data-base on kobo-reader."""
from datetime import datetime

import click
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from . import config
from .fzf_select import fzf_select

engine = create_engine(f'sqlite:///{config["paths"]["kobo_db_path"]}')
meta = MetaData()
meta.reflect(bind=engine)
Base = automap_base(metadata=meta)
Base.prepare()
Session = sessionmaker(bind=engine)
session = Session()
Content = Base.classes.content
Shelf = Base.classes.Shelf
ShelfContent = Base.classes.ShelfContent


def choose_shelf(file):
    """Choose shelf to add book to."""
    shelves = [q[0] for q in session.query(Shelf.Name)]
    selection = fzf_select(
        shelves,
        header=f"Select shelve for {file}",
        on_none=lambda: False,
        on_new=lambda: new_shelf(click.prompt("Enter name for new shelf:")),
    )
    add_to_shelf(file, selection)


def add_to_shelf(book, shelf):
    """Add entry to data-base so that ``book`` appears in ``shelf``."""
    shelf_content = ShelfContent(
        ShelfName=shelf,
        ContentId=f"file:///mnt/onboard/contents/{book.name}",
        DateModified=datetime.today(),
        _IsDeleted=False,
        _IsSynced=False,
    )
    session.add(shelf_content)
    session.commit()
    click.echo(f"Added {book} to shelf {shelf}.")


def new_shelf(name):
    """Add new shelf to data-base."""
    shelf = Shelf(
        Name=name,
        Id=name,
        InternalName=name,
        CreationDate=datetime.today(),
        LastModified=datetime.today(),
        _IsDeleted=False,
        _IsVisible=True,
        _IsSynced=False,
    )
    session.add(shelf)
    session.commit()


def print_books_read():
    """Print books that are marked as read on kobo."""
    books_read = session.query(Content.Title).filter(Content.ReadStatus == 2)
    if books_read.first():
        click.echo("Nice done! You read the following books:")
    for book in books_read:
        print(f"\t{book[0]}")
