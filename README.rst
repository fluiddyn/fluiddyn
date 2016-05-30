========
FluidDyn
========

|release| |docs|

.. |release| image:: https://img.shields.io/pypi/v/fluiddyn.svg
   :target: https://pypi.python.org/pypi/fluiddyn/
   :alt: Latest version

.. |docs| image:: https://readthedocs.org/projects/fluiddyn/badge/?version=latest
   :target: http://fluiddyn.readthedocs.org
   :alt: Documentation status

FluidDyn is a framework for studying fluid dynamics. Most of the
features are actually implemented in other packages (fluidsim,
fluidlab, fluidimage).

It is the evolution of two other projects previously developed by
`Pierre Augier
<http://www.legi.grenoble-inp.fr/people/Pierre.Augier/>`_ (CNRS
researcher at `LEGI <http://www.legi.grenoble-inp.fr>`_, Grenoble):
Solveq2d (a numerical code to solve fluid equations in a periodic
two-dimensional space with a pseudo-spectral method, developed at KTH,
Stockholm) and FluidLab (a toolkit to do experiments, developed in
the G. K. Batchelor Fluid Dynamics Laboratory at DAMTP, University of
Cambridge).

*Key words and ambitions*: fluid dynamics research with Python (2.7 or
>= 3.3); modular, object-oriented, collaborative, tested and
documented, free and open-source software.

License
-------

FluidDyn is distributed under the CeCILL-B_ License, a BSD compatible
french license.

.. _CeCILL-B: http://www.cecill.info/index.en.html

Installation
------------

You can get the source code from `Bitbucket
<https://bitbucket.org/fluiddyn/fluiddyn>`__ or from `the Python
Package Index <https://pypi.python.org/pypi/fluiddyn/>`__.

The development mode is often useful. From the root directory::

  python setup.py develop

Tests
-----

From the root directory::

  make tests

Or, from the root directory or from any of the "test" directories::

  python -m unittest discover
