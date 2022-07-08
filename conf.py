source_suffix = ".rst"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinx.ext.todo", "sphinx.ext.coverage", "sphinx.ext.viewcode"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "aiohttp": ("https://aiohttp.readthedocs.io/en/stable/", None),
}

project = "PyTenno"
copyright = "2022, Ryan Peckham"
author = "Ryan Peckham"

pygments_style = "sphinx"
html_theme = "pyramid"