<h1 align="center">sync-kobo</h1>

## 🚧 Setup

* install fzf
```
pip install pip install git+https://github.com/david-fischer/sync-kobo.git
```

## 🔧 Usage

Connect Kobo-Reader and call the script via:
```
sync-kobo
```

<!-- jinja-block help
Help text:

```
> sync_kobo -h

{{ execute_command("./sync_kobo/cli.py -h") }}

```
jinja-block help-->
<!-- jinja-out help start-->
Help text:

```
> sync_kobo -h

Usage: cli.py [OPTIONS]

  Sync books and annotations with Kobo e-reader.

Options:
  --version    Show the version and exit.
  --configure  Open config-file in default text-editor.
  -h, --help   Show this message and exit.

```
<!-- jinja-out help end-->


## 📦 Dependencies

<!-- jinja-block deps
{{ "\n".join(dep_strings) }}
jinja-block deps-->
<!-- jinja-out deps start-->
 * [appdirs](http://github.com/ActiveState/appdirs) - A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".
 * [click](https://palletsprojects.com/p/click/) - Composable command line interface toolkit
 * [pyfzf](https://github.com/nk412/pyfzf) - Python wrapper for junegunn's fuzzyfinder (fzf)
 * [SQLAlchemy](http://www.sqlalchemy.org) - Database Abstraction Library
 * [toml](https://github.com/uiri/toml) - Python Library for Tom's Obvious, Minimal Language
 * [titlecase](https://github.com/ppannuto/python-titlecase) - Python Port of John Gruber's titlecase.pl
 * [tabulate](https://github.com/astanin/python-tabulate) - Pretty-print tabular data
 * [toolz](https://github.com/pytoolz/toolz/) - List processing tools and functional utilities
 * [ansicolors](http://github.com/jonathaneunice/colors/) - ANSI colors for Python
 * [beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/bs4/) - Screen-scraping library
<!-- jinja-out deps end-->
