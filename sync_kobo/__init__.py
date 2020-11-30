"""__init__ file."""
import configparser
import os
import pathlib
from importlib.metadata import metadata

from appdirs import AppDirs

from .utils import dict_prompt, iter_prompt

META = dict(metadata(__name__))
__author__ = META["Author"]
__version__ = META["Version"]

dirs = AppDirs(appname=__name__, appauthor=__author__, version=__version__)


CONFIG_DIR = pathlib.Path(dirs.user_config_dir)
CONFIG_PATH = CONFIG_DIR / "config.ini"
APP_DIR = pathlib.Path(dirs.user_data_dir)
HOME = pathlib.Path.home()
USER = HOME.stem

config = configparser.ConfigParser()
if CONFIG_PATH.exists():
    config.read(CONFIG_PATH)
else:
    kobo_base = pathlib.Path("/media", USER, "KOBOeReader")
    config.add_section("paths")
    user_paths = dict_prompt(
        kobo_dir=kobo_base,
        kobo_book_dir=kobo_base / "contents",
        kobo_db_path=kobo_base / ".kobo" / "KoboReader.sqlite",
        kobo_annot_dir=kobo_base / "Digital Editions" / "Annotations" / "contents",
        db_bkp_dir=HOME / "bkps" / "Kobo",
        book_import_dir=HOME / "Nextcloud" / "Books",
        annot_export_dir=HOME / "Nextcloud" / "Book-Annotations",
    )
    config["paths"].update(**{k: str(v) for k, v in user_paths.items()})
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as file:
        config.write(file)
