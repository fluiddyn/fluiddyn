.. FluidDyn documentation master file, created by
   sphinx-quickstart on Sun Mar  2 12:15:31 2014.

FluidDyn documentation
======================

.. raw:: html

    <h1 align="center">
      <img width="400" alt="FluidDyn logo"
      src="https://foss.heptapod.net/fluiddyn/fluiddyn/raw/branch/default/doc/logo.png">
    </h1>

The FluidDyn project aims at promoting the use of open-source Python software
in research in fluid dynamics.  The project provides some Python packages
specialized for different tasks, in particular

- `transonic <http://transonic.readthedocs.org>`_, to make your Python code fly
  at transonic speeds!

- `fluidfft <http://fluidfft.readthedocs.org>`_ for 2D and 3D Fast Fourier
  Transforms,

- `fluidsim <http://fluidsim.readthedocs.org>`_ for numerical simulations,

- `fluidlab <http://fluidlab.readthedocs.org>`_ for laboratory experiments,

- `fluidimage <http://fluidimage.readthedocs.io>`_ for processing of images of
  fluid,

- `fluidsht <http://fluidsht.readthedocs.org>`_ for Spherical Harmonic
  Transforms.

This documentation presents the FluidDyn project and the package of the same
name, which is the base package on which the other packages depend on. For the
specific documentations of these specialized packages, follow the links above.

.. toctree::
   :maxdepth: 1
   :caption: The FluidDyn project

   intro-motivations
   advice_on_Python

Metapaper and citation
^^^^^^^^^^^^^^^^^^^^^^

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

.. toctree::
   :maxdepth: 2
   :caption: User Guide of the fluiddyn package

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

.. toctree::
   :maxdepth: 1
   :caption: More

   changes
   advice_developers
   to_do
   authors

Links
-----

- `Forge of the FluidDyn project on Heptapod <https://foss.heptapod.net/fluiddyn>`_
- `Forge of the fluiddyn package on Heptapod
  <https://foss.heptapod.net/fluiddyn/fluiddyn>`_
- `FluidDyn in PyPI <https://pypi.org/project/fluiddyn/>`_
- `FluidDyn project blog <https://fluiddyn.bitbucket.io/>`_
- FluidDyn user chat room in
  `riot <https://riot.im/app/#/room/#fluiddyn-users:matrix.org>`_ or
  `slack <https://fluiddyn.slack.com>`_
- `FluidDyn mailing list <https://www.freelists.org/list/fluiddyn>`_
- `FluidDyn on Twitter <https://twitter.com/pyfluiddyn>`_
- `FluidDyn on Youtube
  <https://www.youtube.com/channel/UCPhRtVq1v4HtcecEdEOcXBw>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
