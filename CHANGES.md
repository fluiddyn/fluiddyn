# Release notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

% Type of changes:

% Added      Added for new features.
% Changed    Changed for changes in existing functionality.
% Deprecated Deprecated for soon-to-be removed features.
% Removed    Removed for now removed features.
% Fixed      Fixed for any bug fixes.
% Security   Security in case of vulnerabilities.

See also the
[unreleased changes](https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.6.5...branch%2Fdefault).

## [0.6.5] (2024-08-17)

- Cluster Gricad (OAR with Guix).
- Compatibility Numpy 2.0.

## [0.6.4] (2024-05-03)

- Use `matplotlib.backends.qt_compat` instead of `qtpy`.

## [0.6.3] (2024-04-22)

- New functions {func}`fluiddyn.clusters.Cluster.get_commands_setting_env` and
  {func}`fluiddyn.clusters.Cluster.get_commands_activating_lauching_python`.

## [0.6.2] (2024-04-16)

- Fix a bug in {class}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles` when an index
  is coded over two letters.

## [0.6.1] (2024-04-02)

- Update LEGI clusters

## [0.6.0] (2024-03-04)

Improvements and refactoring {mod}`fluiddyn.util.serieofarrays` with much better testing.

### Added

- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.get_slicing_tuples`
- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.get_slicing_tuples_all_files`
- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.set_slicing_tuples`
- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.set_slicing_tuples_from_str`
- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.get_separator_base_index`
- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.get_index_separators`
- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.get_tuple_array_name_from_index`
- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.get_str_for_name_from_idim_idx`
- {func}`fluiddyn.util.serieofarrays.SerieOfArraysFromFiles.compute_str_indices_from_indices`

### Changed

- The argument `ind_start` of {class}`fluiddyn.util.serieofarrays.SeriesOfArrays` is now
  `"first"` by default.

- {class}`fluiddyn.util.serieofarrays.SeriesOfArrays` can now be created with
  `SeriesOfArrays(path, "pairs")` and with `SeriesOfArrays(path, "all1by1")`.

### Deprecated

- `get_index_slices` and all methods containing in their name `index_slices`. Use the
  corresponding method with `slicing_tuples`.

## [0.5.4] (2024-02-17)

- Fix `util/serieofarrays.py` for multiprocessing on Windows
- Less verbose check about Qt

## [0.5.3] (2024-01-17)

- Compatibility with Python 3.12 and requires Python >=3.9

## [0.5.2] (2023-03-07)

- New argument `doc` for {func}`fluiddyn.util.paramcontainer.ParamContainer._set_child`.

## [0.5.1] (2022-09-27)

- Fluiddyn
  [code of conduct](https://fluiddyn.readthedocs.io/en/latest/code-of-conduct.html)
- New cluster {mod}`fluiddyn.clusters.azzurra`
- More options in {mod}`fluiddyn.clusters.oar` and {mod}`fluiddyn.clusters.slurm`
- New functions {func}`fluiddyn.clusters.oar.get_job_id` and
  {func}`fluiddyn.clusters.oar.get_job_info`
- New function {func}`fluiddyn.util.has_to_be_made`.

## [0.5.0] (2022-02-04)

- Add 2 SLURM clusters ({class}`fluiddyn.clusters.idris.JeanZay` and
  {class}`fluiddyn.clusters.licallo.Licallo`).

## [0.4.1] (2022-01-05)

- Fix to avoid a bug in pyfftw 0.13.0

## [0.4.0] (2021-11-05)

- clusters: fix inconsistency between different clusters
  ([#62](https://foss.heptapod.net/fluiddyn/fluiddyn/-/merge_requests/62))
- paramcontainer: avoid an `eval` call + fix bug `_parent` + better get_item/set_item

## [0.3.4] (2021-09-22)

- General maintenance
- Various improvements for clusters SLURM and OAR
- New module {mod}`fluiddyn.util.opencv`: fix incompatibility between `cv2` and Qt wheels

## [0.3.3] (2020-10-01)

- `execute_notebooks` fluiddoc/ipynb_maker.py

## [0.3.2] (2020-03-31)

- Improve API for `ParamContainer`
- New API for `terminal_colors`
- Update clusters LEGI

## [0.3.1] (2019-02-14)

- Compatibility sphinx >= 1.8
- Improve cluster Slurm

## [0.3.0] (2019-01-27)

- Python>=3.6 only
- Native implementation for `stdout_redirected`
- JSON rendering for ParamContainer objects in Jupyter
- Use pathlib when possible
- Minor fixes and cleanup for EasySHT class
- Update SNIC cluster classes
- Compatibility layer for `cached_property`
- Function `imsave_h5` has a `splitext` option, allowing the function to preserve the
  original file extension

## 0.2.5 (2018-09-12)

- Improve serieofarrays for fluidimage
- bugfixes...

## 0.2.4

- Bugfixes and compatibility Python 3.7.
- Context manager to set environ vars.
- More colorlog.

## 0.2.3

- `fluiddoc.mathmacro`.
- More fft (get_seq_indices_first_X, fftw_grid_size).
- Better test coverage and less bugs.
- `fluidcluster-help`.
- Better `fluidinfo`.

## 0.2.2

- Add setofvariables (previously in fluidsim).
- Faster and better easypyfft.

## 0.2.1

- Better Spherical Harmonic operators
- New util function is_run_from_jupyter

## 0.2.0

- Changes of the API

## 0.1.6

- Can now execute the notebooks during the doc building (fluiddoc/ipynb_maker.py)

## 0.1.5

- Travis
- Bug fix (Python 3)
- PyQt5

## 0.1.3

- Improve paramcontainer (print doc, GUI with Qt)

## 0.1.2

- Better paramcontainer (ordered children + `_print_docs` method).
- Better cluster oar (python 2/3).

## 0.1.1

- More unittests (coverage = 76%).
- read/write functions h5py and in_py.

## 0.1.0

- Clean-up code.
- More unittests (coverage = 60%).
- Compatible Python 2.7 and Python >= 3.4.
- fluiddyn.util.easypyfft.

## 0.0.13

- Configure logging.
- Clusters slurm.
- Multitiff.
- Better paramcontainer and serieofarrays.

## 0.0.12

- Better email sending, with enclosed files.

## 0.0.11

- User configuration files.
- Add color charts to choose the colors in figures.

## 0.0.10

- Logger for error logging.
- Utility to use comma separated values (csv) files.
- Tiny package for readthedocs.

## [0.0.9]

- New parameter container (API slightly changed).

## [0.0.8]

- The fluiddyn package now only contains base files for the FluidDyn project. Other
  packages (fluidsim, fluidlab, ...) provide other files.

[0.0.8]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/tags/0.0.8a1
[0.0.9]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.0.8a1...0.0.9a1
[0.3.0]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.2.5...0.3.0
[0.3.1]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.0...0.3.1
[0.3.2]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.1...0.3.2
[0.3.3]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.2...0.3.3
[0.3.4]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.3...0.3.4
[0.4.0]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.3.4...0.4.0
[0.4.1]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.4.0...0.4.1
[0.5.0]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.4.1...0.5.0
[0.5.1]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.5.0...0.5.1
[0.5.2]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.5.1...0.5.2
[0.5.3]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.5.2...0.5.3
[0.5.4]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.5.3...0.5.4
[0.6.0]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.5.4...0.6.0
[0.6.1]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.6.0...0.6.1
[0.6.2]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.6.1...0.6.2
[0.6.3]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.6.2...0.6.3
[0.6.4]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.6.3...0.6.4
[0.6.5]: https://foss.heptapod.net/fluiddyn/fluiddyn/-/compare/0.6.4...0.6.5
