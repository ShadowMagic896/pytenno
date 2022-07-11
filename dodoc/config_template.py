import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "PyTenno"
author = "Ryan Peckham"
copyright = f"2022, {author}"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]
html_theme = "sphinx_rtd_theme"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiohttp": ("https://aiohttp.readthedocs.io/en/stable/", None),
}
source_suffix = ".rst"
master_doc = "index"
