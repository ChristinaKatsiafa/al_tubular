# Configuration file for the Sphinx documentation builder.
# import sys
import os

os.path.abspath("../al_tubular/")


# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "al_tubular_testdocs"
project_copyright = "2025, author"
author = "author"
release = "v1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme"
]


templates_path = ["_templates"]
exclude_patterns = []

autodoc_default_flags = ["members", "inherited-members", "show-inheritance"]
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "show-inheritance": True,
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
