# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'OptiX'
copyright = '2025, Atomelix'
author = 'Atomelix'

release = '0.3'
version = '0.3'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',
]

mathjax3_config = {
    "tex": {
        "inlineMath": [["\\(", "\\)"], ["$", "$"]],
        "macros": {
            "bm": "\\boldsymbol",
        },
    }
}

templates_path = ['_templates']
exclude_patterns = ['_build']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

def setup(app):
    app.add_css_file('custom.css')
