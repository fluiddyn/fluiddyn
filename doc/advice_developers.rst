.. _advicedev:

Advice for FluidDyn developers
==============================

- Discussions on the development of the FluidDyn packages take place in the
  `FluidDyn developer chat room
  <https://riot.im/app/#/room/#fluiddyn-dev:matrix.org>`_.

- Use a text editor with flake8 enabled (see for example `our emacs setup
  <https://foss.heptapod.net/fluiddyn/fluid_emacs.d>`_).

- Use the Python code formatter `black <https://github.com/ambv/black>`_ with the
  command ``make black``.

- Run the unittests before committing.

Mercurial
---------

Fluiddyn has been designed to be used by scientists-developers. Thus, you may
have to modify the code of the FluidDyn packages.  So I would advice to work
"as a developer", i.e. to get the source code and to use revision control and
the development mode of the Python installer.

For FluidDyn, we use the revision control software Mercurial and the main
repository is hosted here: https://foss.heptapod.net/fluiddyn/fluiddyn. We
advice to fork this repository (click on "Fork") and to clone your newly
created repository to get the code on your computer (click on "Clone" and run
the command that will be given). If you are new with Mercurial and Heptapod,
you can also read this short tutorial:

.. toctree::
   :maxdepth: 1

   mercurial_heptapod

fluiddevops: a tool to handle the FluidDyn repositories
-------------------------------------------------------

We present a tool to handle the different FluidDyn repositories.

.. toctree::
   :maxdepth: 1

   workflow_dev
