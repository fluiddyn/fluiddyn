# ![FluidDyn project and fluiddyn package](https://foss.heptapod.net/fluiddyn/fluiddyn/raw/branch/default/doc/logo.svg)

[![Latest version](https://img.shields.io/pypi/v/fluiddyn.svg)](https://pypi.python.org/pypi/fluiddyn/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/fluiddyn.svg)
[![Documentation status](https://readthedocs.org/projects/fluiddyn/badge/?version=latest)](http://fluiddyn.readthedocs.org)
[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Code coverage](https://codecov.io/gh/fluiddyn/fluiddyn/branch/branch%2Fdefault/graph/badge.svg)](https://codecov.io/gh/fluiddyn/fluiddyn/branch/branch%2Fdefault)
[![Heptapod CI](https://foss.heptapod.net/fluiddyn/fluiddyn/badges/branch/default/pipeline.svg)](https://foss.heptapod.net/fluiddyn/fluiddyn/-/pipelines)
[![Github Actions](https://github.com/fluiddyn/fluidsim/actions/workflows/ci-linux.yml/badge.svg?branch=branch/default)](https://github.com/fluiddyn/fluiddyn/actions/)

FluidDyn project is an ecosystem of packages for research and teaching
in fluid dynamics. The Python package fluiddyn contains:

-   **basic utilities to manage**: File I/O for some esoteric formats,
    publication quality figures, job submission on clusters, MPI
-   **powerful classes to handle**: parameters, arrays, series of files
-   **simplified interfaces to calculate**: FFT, spherical harmonics

and much more. It is used as a library in [the other specialized
packages of the FluidDyn project](https://foss.heptapod.net/fluiddyn)
(in particular in [fluidfft](http://fluidfft.readthedocs.io),
[fluidsim](http://fluidsim.readthedocs.io),
[fluidlab](http://fluidlab.readthedocs.io) and
[fluidimage](http://fluidimage.readthedocs.io)).

**Documentation**: [Read the Docs](https://fluiddyn.readthedocs.io),
[Heptapod Pages](https://fluiddyn.pages.heptapod.net/fluiddyn)

## Installation

The simplest way to install fluiddyn is by using pip:

```sh
pip install fluiddyn
```

## Requirements

  ----------------- ------------------------------------------------------
  **Minimum**       Python (\>=3.11), `numpy matplotlib h5py psutil`

  **Full            `h5py h5netcdf pillow imageio mpi4py scipy pyfftw`
  functionality**   (requires FFTW library), SHTns

  **Optional**      OpenCV with Python bindings, `scikit-image`
  ----------------- ------------------------------------------------------

**Note**: Detailed instructions to install the above dependencies using
Anaconda / Miniconda or in a specific operating system such as Ubuntu,
macOS etc. can be found
[here](https://fluiddyn.readthedocs.io/en/latest/get_good_Python_env.html).

## Tests

With an editable installation, you can run the tests with:

```sh
pytest
```

## Metapaper and citation

If you use any of the FluidDyn packages to produce scientific articles,
please cite [our metapaper presenting the FluidDyn project and the
fluiddyn
package](https://openresearchsoftware.metajnl.com/articles/10.5334/jors.237/):

```bibtex
@article{fluiddyn,
doi = {10.5334/jors.237},
year = {2019},
publisher = {Ubiquity Press,  Ltd.},
volume = {7},
author = {Pierre Augier and Ashwin Vishnu Mohanan and Cyrille Bonamy},
title = {{FluidDyn}: A Python Open-Source Framework for Research and Teaching in Fluid Dynamics
    by Simulations,  Experiments and Data Processing},
journal = {Journal of Open Research Software}
}
```

## History

The FluidDyn project started in 2015 as the evolution of two packages
previously developed by [Pierre
Augier](http://www.legi.grenoble-inp.fr/people/Pierre.Augier/) (CNRS
researcher at [LEGI](http://www.legi.grenoble-inp.fr), Grenoble):
solveq2d (a numerical code to solve fluid equations in a periodic
two-dimensional space with a pseudo-spectral method, developed at KTH,
Stockholm) and fluidlab (a toolkit to do experiments, developed in the
G. K. Batchelor Fluid Dynamics Laboratory at DAMTP, University of
Cambridge).

*Keywords and ambitions*: fluid dynamics research with Python (\>= 3.6),
modular, object-oriented, collaborative, tested and documented, free and
open-source software.

## License

FluidDyn is distributed under the
[CeCILL-B](http://www.cecill.info/index.en.html) License, a BSD
compatible french license.
