======
|logo|
======

|release| |pyversions| |docs| |coverage| |travis| |appveyor|

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

.. |coverage| image:: https://codecov.io/bb/fluiddyn/fluiddyn/branch/default/graph/badge.svg
   :target: https://codecov.io/bb/fluiddyn/fluiddyn/branch/default/
   :alt: Code coverage

.. |travis| image:: https://travis-ci.org/fluiddyn/fluiddyn.svg?branch=master
   :target: https://travis-ci.org/fluiddyn/fluiddyn
   :alt: Travis CI status

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/rxafwwpmxymki2u1/branch/default?svg=true
   :target: https://ci.appveyor.com/project/fluiddyn/fluiddyn
   :alt: AppVeyor status

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/fluiddyn/fluiddyn/master?urlpath=lab/tree/doc/ipynb
   :alt: Binder notebook

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

**Documentation**: https://fluiddyn.readthedocs.io

Getting started
---------------
To try fluiddyn without installation: |binder|

Installation
------------
The simplest way to install fluiddyn is by using pip::

  pip install fluiddyn [--user]

Add ``--user`` flag if you are installing without setting up a virtual
environment.

You can also get the source code from
https://foss.heptapod.net/fluiddyn/fluiddyn or from `the Python Package Index
<https://pypi.python.org/pypi/fluiddyn/>`_. It is recommended to `install numpy
<http://scipy.org/install.html>`_ before installing fluiddyn. The development
mode is often useful if you intend to modify fluiddyn. From the root
directory::

  python setup.py develop


Requirements
------------

+------------------------+-------------------------------------------------------------------------------+
| **Minimum**            | Python (>=3.6), ``numpy matplotlib h5py psutil``                              |
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

From the root directory::

  make tests

Or, from the root directory or any of the "test" directories::

  python -m unittest discover

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
