import os
import sys

sys.path.insert(0, os.path.abspath(".."))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

napoleon_google_docstring = False
napoleon_numpy_docstring = True
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiohttp": ("https://aiohttp.readthedocs.io/en/stable/", None),
}
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = "PyTenno"
copyright = "2022 Ryan Peckham"
author = "Ryan Peckham"
