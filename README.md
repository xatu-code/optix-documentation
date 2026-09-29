# optix-documentation

Online documentation for the OptiX (`opticx`) optical-response package, built with Sphinx and hosted on Read the Docs.

## Building locally

```
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html`.

## Layout

- `docs/index.rst`: landing page and table of contents
- `docs/installation.rst`, `quickstart.rst`, `input_file.rst`, `workflows.rst`: user guide
- `docs/outputs/`: one page per output file type
- `docs/theory/`: conventions, linear response, shift current
- `docs/troubleshooting.rst`: error messages and fixes
- `docs/images/`: figures (the GeS examples come from a 40×40 run of the example inputs)
