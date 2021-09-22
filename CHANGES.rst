Changes
=======

All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

.. Type of changes
.. ---------------
.. Added      Added for new features.
.. Changed    Changed for changes in existing functionality.
.. Deprecated Deprecated for soon-to-be removed features.
.. Removed    Removed for now removed features.
.. Fixed      Fixed for any bug fixes.
.. Security   Security in case of vulnerabilities.

Unreleased_
-----------

.. towncrier release notes start

.. _Unreleased: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.4...branch%2Fdefault

0.3.4_ (2021-09-22)
-------------------

- General maintenance
- Various improvements for clusters SLURM and OAR
- New module :mod:`fluiddyn.util.opencv`: fix incompatibility between `cv2` and
  Qt wheels

0.3.3_ (2020-10-01)
-------------------

- `execute_notebooks` fluiddoc/ipynb_maker.py

0.3.2_ (2020-03-31)
-------------------

- Improve API for ``ParamContainer``
- New API for ``terminal_colors``
- Update clusters LEGI

0.3.1_ (2019-02-14)
-------------------

- Compatibility sphinx >= 1.8
- Improve cluster Slurm

0.3.0_ (2019-01-27)
-------------------

- Python>=3.6 only
- Native implementation for ``stdout_redirected``
- JSON rendering for ParamContainer objects in Jupyter
- Use pathlib when possible
- Minor fixes and cleanup for EasySHT class
- Update SNIC cluster classes
- Compatibility layer for ``cached_property``
- Function ``imsave_h5`` has a ``splitext`` option, allowing the function to
  preserve the original file extension

0.2.5 (2018-09-12)
------------------

- Improve serieofarrays for fluidimage
- bugfixes...

0.2.4
-----

- Bugfixes and compatibility Python 3.7.
- Context manager to set environ vars.
- More colorlog.

0.2.3
-----

- ``fluiddoc.mathmacro``.
- More fft (get_seq_indices_first_X, fftw_grid_size).
- Better test coverage and less bugs.
- ``fluidcluster-help``.
- Better ``fluidinfo``.

0.2.2
-----

- Add setofvariables (previously in fluidsim).
- Faster and better easypyfft.

0.2.1
-----

- Better Spherical Harmonic operators
- New util function is_run_from_jupyter

0.2.0
-----

- Changes of the API

0.1.6
-----

- Can now execute the notebooks during the doc building
  (fluiddoc/ipynb_maker.py)

0.1.5
-----

- Travis
- Bug fix (Python 3)
- PyQt5

0.1.3
-----

- Improve paramcontainer (print doc, GUI with Qt)

0.1.2
-----

- Better paramcontainer (ordered children + `_print_docs` method).
- Better cluster oar (python 2/3).

0.1.1
-----

- More unittests (coverage = 76%).
- read/write functions h5py and in_py.

0.1.0
-----

- Clean-up code.
- More unittests (coverage = 60%).
- Compatible Python 2.7 and Python >= 3.4.
- fluiddyn.util.easypyfft.

0.0.13
------

- Configure logging.

- Clusters slurm.

- Multitiff.

- Better paramcontainer and serieofarrays.

0.0.12
------

- Better email sending, with enclosed files.

0.0.11
------

- User configuration files.

- Add color charts to choose the colors in figures.

0.0.10
------

- Logger for error logging.

- Utility to use comma separated values (csv) files.

- Tiny package for readthedocs.

0.0.9_
------

- New parameter container (API slightly changed).

0.0.8_
------

- The fluiddyn package now only contains base files for the FluidDyn
  project. Other packages (fluidsim, fluidlab, ...) provide other
  files.

.. _0.3.4: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.3...0.3.4
.. _0.3.3: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.2...0.3.3
.. _0.3.2: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.1...0.3.2
.. _0.3.1: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.0...0.3.1
.. _0.3.0: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.2.5...0.3.0
.. _0.0.9: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.0.8a1...0.0.9a1
.. _0.0.8: https://foss.heptapod.net/fluiddyn/fluiddyn/-/tags/0.0.8a1
