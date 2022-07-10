import sys

import os


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

napoleon_google_docstring = False
napoleon_numpy_docstring = True
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiohttp": ("https://aiohttp.readthedocs.io/en/stable/", None),
}
source_suffix = ".rst"
master_doc = "index"

autodoc_member_order = "bysource"
autodoc_typehints = "none"

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "style_external_links": True,
    "display_version": True,
    "github_url": "https://github.com/ShadowMagic896/pytenno",
}
html_sidebars = {
    "**": ["about.html", "navigation.html", "relations.html", "searchbox.html"],
}

project = "PyTenno"
copyright = "2022 Ryan Peckham"
author = "Ryan Peckham"
