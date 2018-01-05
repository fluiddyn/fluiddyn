.. FluidDyn documentation master file, created by
   sphinx-quickstart on Sun Mar  2 12:15:31 2014.

FluidDyn documentation
======================

The FluidDyn project aims at promoting the use of open-source Python software
in research in fluid dynamics.  The project provides some Python packages
specialized for different tasks, in particular

- `fluidlab <http://fluidlab.readthedocs.org>`_ for laboratory experiments,

- `fluidimage <http://fluidimage.readthedocs.io>`_ for processing of images of
  fluid,

- `fluidfft <http://fluidfft.readthedocs.org>`_ for 2D and 3D Fast Fourier
  Transforms,

- `fluidsim <http://fluidsim.readthedocs.org>`_ for numerical simulations.

This documentation presents the FluidDyn project and the package of
the same name, which is the base package on which the other packages
depend on. For the specific documentations of these specialized
packages, follow the links above.

The FluidDyn project
--------------------

.. toctree::
   :maxdepth: 1

   intro-motivations
   advice_on_Python

User Guide of the fluiddyn package
----------------------------------

.. toctree::
   :maxdepth: 1

   install
   ipynb/overview
   tutorials


Modules Reference
-----------------

In order to discover FluidDyn, the best is to see how it is structured. Here is
a list of the first-level packages.  If you are looking for a particular
feature, you can also use the "Quick search" tool in this page.

.. autosummary::
   :toctree: generated/

   fluiddyn.io
   fluiddyn.util
   fluiddyn.clusters
   fluiddyn.output
   fluiddyn.calcul

Fluiddyn also provides a small package for documentation:

.. autosummary::
   :toctree: generated/

   fluiddoc

More
----

.. toctree::
   :maxdepth: 1

   FluidDyn forge in Bitbucket <https://bitbucket.org/fluiddyn/fluiddyn>
   FluidDyn in PyPI  <https://pypi.python.org/pypi/fluiddyn/>
   to_do
   changes
   authors


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

