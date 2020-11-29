"""__init__ file."""

from appdirs import AppDirs

PROJECT_NAME = "sync-kobo"
AUTHOR = "David Fischer"

dirs = AppDirs(appname=PROJECT_NAME, appauthor=AUTHOR)


CONFIG_DIR = dirs.user_config_dir
APP_DIR = dirs.user_data_dir
