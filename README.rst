========
FluidDyn
========

|release| |docs| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/fluiddyn.svg
   :target: https://pypi.python.org/pypi/fluiddyn/
   :alt: Latest version

.. |docs| image:: https://readthedocs.org/projects/fluiddyn/badge/?version=latest
   :target: http://fluiddyn.readthedocs.org
   :alt: Documentation status

.. |coverage| image:: https://codecov.io/bb/fluiddyn/fluiddyn/branch/default/graph/badge.svg
   :target: https://codecov.io/bb/fluiddyn/fluiddyn/branch/default/
   :alt: Code coverage

FluidDyn is a framework for research and teaching in fluid dynamics. The Python
package fluiddyn contains basic utilities (file io, figures, clusters, mpi,
etc.).  Most of the features of the FluidDyn project are actually implemented
in `other packages <https://bitbucket.org/fluiddyn>`_ (in particular in
`fluidlab <http://fluidlab.readthedocs.io>`_, `fluidimage
<http://fluidimage.readthedocs.io>`_ and `fluidsim
<http://fluidsim.readthedocs.io>`_).

*Key words and ambitions*: fluid dynamics research with Python (2.7 or >= 3.4);
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
installing fluiddyn. The simplest way to install fluiddyn is by using pip::

  pip install fluiddyn

You can get the source code from `Bitbucket
<https://bitbucket.org/fluiddyn/fluiddyn>`_ or from `the Python Package Index
<https://pypi.python.org/pypi/fluiddyn/>`_.

The development mode is often useful. From the root directory, run::

  python setup.py develop

Tests
-----

From the root directory::

  make tests

Or, from the root directory or any of the "test" directories::

  python -m unittest discover

History
-------

FluidDyn is the evolution of two other codes previously developed by `Pierre
Augier <http://www.legi.grenoble-inp.fr/people/Pierre.Augier/>`_ (CNRS
researcher at `LEGI <http://www.legi.grenoble-inp.fr>`_, Grenoble): Solveq2d (a
numerical code to solve fluid equations in a periodic two-dimensional space
with a pseudo-spectral method, developed at KTH, Stockholm) and FluidLab (a
toolkit to do experiments, developed in the G. K. Batchelor Fluid Dynamics
Laboratory at DAMTP, University of Cambridge).
