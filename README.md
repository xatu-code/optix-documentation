# optix-documentation

Online documentation for the OptiX (`opticx`) optical-response package, built with Sphinx and hosted on Read the Docs.

## Building locally

Use a virtual environment: the docs need the `furo` theme and the `sphinx-design` and `sphinx-copybutton`
extensions, which are usually not present in a system Python, and many distributions refuse `pip install` into one ("externally managed environment").

```
python3 -m venv .venv
.venv/bin/pip install -r docs/requirements.txt
.venv/bin/sphinx-build -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html`.

If you build with a system `sphinx-build` that has no theme installed, it fails with
`ThemeError: no theme named 'furo' found` (or an `Extension error` for `sphinx_design`). That is the environment,
not the documentation — install the requirements as above. Read the Docs is unaffected: `.readthedocs.yaml`
installs `docs/requirements.txt` itself.

## Layout

- `docs/index.rst`: landing page and table of contents
- `docs/installation.rst`, `quickstart.rst`, `input_file.rst`, `workflows.rst`: user guide
- `docs/outputs/`: one page per output file type
- `docs/theory/`: conventions, linear response, shift current, the covariant shift current, general second
  order, and the DC limit
- `docs/validation.rst`, `limitations.rst`, `changes.rst`: test suite, known limitations, changelog
- `docs/_static/custom.css`, `docs/_templates/base.html`: theme styling (shared with the Xatu documentation)
- `docs/troubleshooting.rst`: error messages and fixes
- `docs/images/`: figures (the GeS examples come from a 40×40 run of the example inputs)
