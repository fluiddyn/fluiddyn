======
|logo|
======

|release| |pyversions| |docs| |coverage| |heptapod_ci| |github_actions|

.. |logo| image:: https://foss.heptapod.net/fluiddyn/fluiddyn/raw/branch/default/doc/logo.svg
   :alt: FluidDyn project and fluiddyn package

.. |release| image:: https://img.shields.io/pypi/v/fluiddyn.svg
   :target: https://pypi.python.org/pypi/fluiddyn/
   :alt: Latest version

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/fluiddyn.svg
   :alt: Supported Python versions

.. |docs| image:: https://readthedocs.org/projects/fluiddyn/badge/?version=latest
   :target: http://fluiddyn.readthedocs.org
   :alt: Documentation status

.. |coverage| image:: https://codecov.io/gh/fluiddyn/fluiddyn/branch/branch%2Fdefault/graph/badge.svg
   :target: https://codecov.io/gh/fluiddyn/fluiddyn/branch/branch%2Fdefault
   :alt: Code coverage

.. |heptapod_ci| image:: https://foss.heptapod.net/fluiddyn/fluiddyn/badges/branch/default/pipeline.svg
   :target: https://foss.heptapod.net/fluiddyn/fluiddyn/-/pipelines
   :alt: Heptapod CI

.. |github_actions| image:: https://github.com/fluiddyn/fluidsim/actions/workflows/ci-linux.yml/badge.svg?branch=branch/default
   :target: https://github.com/fluiddyn/fluiddyn/actions/
   :alt: Github Actions

FluidDyn project is an ecosystem of packages for research and teaching in fluid
dynamics. The Python package fluiddyn contains:

* **basic utilities to manage**: File I/O for some esoteric formats,
  publication quality figures, job submission on clusters, MPI
* **powerful classes to handle**: parameters, arrays, series of files
* **simplified interfaces to calculate**: FFT, spherical harmonics

and much more. It is used as a library in `the other specialized packages of
the FluidDyn project <https://foss.heptapod.net/fluiddyn>`_ (in particular in
`fluidfft <http://fluidfft.readthedocs.io>`_, `fluidsim
<http://fluidsim.readthedocs.io>`_, `fluidlab
<http://fluidlab.readthedocs.io>`_ and `fluidimage
<http://fluidimage.readthedocs.io>`_).

**Documentation**: `Read the Docs <https://fluiddyn.readthedocs.io>`_, `Heptapod Pages <https://fluiddyn.pages.heptapod.net/fluiddyn>`_

Installation
------------
The simplest way to install fluiddyn is by using pip::

  pip install fluiddyn

You can also get the source code from
https://foss.heptapod.net/fluiddyn/fluiddyn or from `the Python Package Index
<https://pypi.python.org/pypi/fluiddyn/>`_. The development
mode is often useful if you intend to modify fluiddyn. From the root
directory::

  pip install -e .[dev]


Requirements
------------

+------------------------+-------------------------------------------------------------------------------+
| **Minimum**            | Python (>=3.9), ``numpy matplotlib h5py psutil``                              |
+------------------------+-------------------------------------------------------------------------------+
| **Full functionality** | ``h5py h5netcdf pillow imageio mpi4py scipy pyfftw`` (requires FFTW library), |
|                        | SHTns                                                                         |
+------------------------+-------------------------------------------------------------------------------+
| **Optional**           | OpenCV with Python bindings, ``scikit-image``                                 |
+------------------------+-------------------------------------------------------------------------------+

**Note**: Detailed instructions to install the above dependencies using
Anaconda / Miniconda or in a specific operating system such as Ubuntu, macOS
etc. can be found `here
<https://fluiddyn.readthedocs.io/en/latest/get_good_Python_env.html>`__.

Tests
-----

With an editable installation, you can run the tests with::

  pytest


Metapaper and citation
----------------------

If you use any of the FluidDyn packages to produce scientific articles, please
cite `our metapaper presenting the FluidDyn project and the fluiddyn package
<https://openresearchsoftware.metajnl.com/articles/10.5334/jors.237/>`_:

.. code ::

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

History
-------

The FluidDyn project started in 2015 as the evolution of two packages
previously developed by `Pierre Augier
<http://www.legi.grenoble-inp.fr/people/Pierre.Augier/>`_ (CNRS researcher at
`LEGI <http://www.legi.grenoble-inp.fr>`_, Grenoble): solveq2d (a numerical
code to solve fluid equations in a periodic two-dimensional space with a
pseudo-spectral method, developed at KTH, Stockholm) and fluidlab (a toolkit to
do experiments, developed in the G. K. Batchelor Fluid Dynamics Laboratory at
DAMTP, University of Cambridge).

*Keywords and ambitions*: fluid dynamics research with Python (>= 3.6),
modular, object-oriented, collaborative, tested and documented, free and
open-source software.

License
-------

FluidDyn is distributed under the CeCILL-B_ License, a BSD compatible
french license.

.. _CeCILL-B: http://www.cecill.info/index.en.html
