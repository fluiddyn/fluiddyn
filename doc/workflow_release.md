# Release checklist for maintainers

:::{note}
For demonstration's sake, we assume that the next version is `$VERSION`
and the package name is `$PACKAGE`.
:::

- Ensure tests pass locally and on CI:

  ```
  pytest
  ```

- Update version in `$PACKAGE/_version.py`

- Compile changelog from [news fragments] and verify the output, for example:

  ```
  towncrier build --version $VERSION --draft
  ```

- Apply the changelog to `CHANGES.rst` and edit the links as required:

  ```
  towncrier build --version $VERSION
  ```

- Compile documentation:

  ```
  cd docs/
  make html
  ```

- Commit changes and tag a release:

  ```
  hg commit
  hg tag $VERSION
  ```

- Prepare source distribution package and wheel:

  ```
  make clean
  python setup.py sdist bdist_wheel
  ```

- Verify the package with twine:

  ```
  twine check dist/*
  ```

- Upload to [TestPyPI] and verify:

  ```
  twine upload --repository testpypi dist/*
  cd /tmp
  python -m venv testpypi
  source testpypi/bin/activate
  pip install \
      --index-url https://test.pypi.org/simple \
      --extra-index-url https://pypi.org/simple \
      $PACKAGE
  ```

- Upload to [PyPI]:

  ```
  twine upload dist/*
  ```

[news fragments]: newsfragments/README.md
[pypi]: https://pypi.org/
[testpypi]: https://packaging.python.org/guides/using-testpypi/
