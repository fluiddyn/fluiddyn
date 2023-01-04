# How to

## How to upload to PyPI — the Python Package Index

First, run the tests with `pytest`

Install build dependencies:

```sh
pip install twine build -U
```

With a correct $HOME/.pypirc, run:

```sh
rm -rf dist
# both sdist and wheel:
python -m build
# or only sdist:
python -m build -s
twine upload dist/*
```
