=====================================
FluidDyn project and fluiddyn package
=====================================

|release| |docs| |coverage| |travis| |appveyor|

.. |release| image:: https://img.shields.io/pypi/v/fluiddyn.svg
   :target: https://pypi.python.org/pypi/fluiddyn/
   :alt: Latest version

.. |docs| image:: https://readthedocs.org/projects/fluiddyn/badge/?version=latest
   :target: http://fluiddyn.readthedocs.org
   :alt: Documentation status

.. |coverage| image:: https://codecov.io/bb/fluiddyn/fluiddyn/branch/default/graph/badge.svg
   :target: https://codecov.io/bb/fluiddyn/fluiddyn/branch/default/
   :alt: Code coverage

.. |travis| image:: https://travis-ci.org/fluiddyn/fluiddyn.svg?branch=master
   :target: https://travis-ci.org/fluiddyn/fluiddyn
   :alt: Travis CI status

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/8tipjogdw679ucsh?svg=true
   :target: https://ci.appveyor.com/project/fluiddyn/fluiddyn
   :alt: AppVeyor status

FluidDyn is a framework for research and teaching in fluid dynamics. The Python
package fluiddyn contains basic utilities (file io, figures, clusters, mpi,
etc.). It is used as a library in `the other specialized packages of the
FluidDyn project <https://bitbucket.org/fluiddyn>`_ (in particular in `fluidfft
<http://fluidfft.readthedocs.io>`_, `fluidsim
<http://fluidsim.readthedocs.io>`_, `fluidlab
<http://fluidlab.readthedocs.io>`_ and `fluidimage
<http://fluidimage.readthedocs.io>`_).

*Keywords and ambitions*: fluid dynamics research with Python (2.7 or >= 3.4),
modular, object-oriented, collaborative, tested and documented, free and
open-source software.

License
-------

FluidDyn is distributed under the CeCILL-B_ License, a BSD compatible
french license.

.. _CeCILL-B: http://www.cecill.info/index.en.html

Installation
------------

It is recommended to `install numpy <http://scipy.org/install.html>`_ before
installing fluiddyn. Then, the simplest way to install fluiddyn is by using
pip::

  pip install fluiddyn

You can get the source code from `Bitbucket
<https://bitbucket.org/fluiddyn/fluiddyn>`_ or from `the Python Package Index
<https://pypi.python.org/pypi/fluiddyn/>`_.

The development mode is often useful. From the root directory, run::

  python setup.py develop


Requirements
------------

**Minimum** : Python (2.7, >=3.4), numpy, matplotlib, psutil, future, subprocess32 (for Python 2.7 only)

**Full functionality**: h5py, h5netcdf, pillow, imageio, mpi4py, scipy, pyfftw (requires FFTW library)

**Optional**: OpenCV with Python bindings, scikit-image

Tests
-----

From the root directory::

  make tests

Or, from the root directory or any of the "test" directories::

  python -m unittest discover

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
