.. _advicedev:

Advice for FluidDyn developers
==============================

- Discussions on the development of the FluidDyn packages take place in the
  `FluidDyn developer chat room
  <https://riot.im/app/#/room/#fluiddyn-dev:matrix.org>`_.

- Use a good Python editor with at least flake8 enabled.

- Use the Python code formatter `black <https://github.com/ambv/black>`_ with the
  command ``make black``.

- Run the unittests before committing.

Hosted on Heptapod by Octobus and Clever Cloud!
-----------------------------------------------

For FluidDyn, we use the revision control software Mercurial and our
main repositories are hosted here: https://foss.heptapod.net/fluiddyn.

`Heptapod <https://heptapod.net/>`_ is a friendly fork of GitLab Community
Edition supporting Mercurial. https://foss.heptapod.net is a public instance
for Free and Open-Source Software (more information `here
<https://foss.heptapod.net/heptapod/foss.heptapod.net>`_).

Thanks to `Octobus <https://octobus.net/>`_ and `Clever Cloud
<https://www.clever-cloud.com>`_ for providing this service!

.. raw:: html

   <h1 align="center">
     <a href="https://foss.heptapod.net/heptapod/foss.heptapod.net">
       <img width="500" alt="Octobus + Clever Cloud"
            src="https://foss.heptapod.net/heptapod/slides/2020-FOSDEM/raw/branch/default/octobus+clever.png"
            >
     </a>
   </h1>

If you are new with Mercurial and Heptapod, you can read this short tutorial:

.. toctree::
   :maxdepth: 1

   mercurial_heptapod

fluiddevops: a tool to handle the FluidDyn repositories
-------------------------------------------------------

We present a tool to handle the different FluidDyn repositories.

.. toctree::
   :maxdepth: 1

   workflow_dev
