Installation
============


Get a good scientific Python environment
----------------------------------------

FluidDyn works with Python 2.7. It would not be difficult to support
Python 2.6 but I think that for science, it is important and not
difficult to use a recent version of Python and of the main libraries
(mainly NumPy, Matplotlib, SciPy).  See this page:

.. toctree::
   :maxdepth: 1

   python_for_fluiddyn

**Remark:** we also discussed in this page how to use `virtualenv`,
which is very very convenient.

**Dependencies:** it is recommended to install NumPy and Matplotlib
before installing FluidDyn.


Basic install
-------------

FluidDyn can be installed from the Python Package Index by the command::

  pip install fluiddyn --pre

The ``--pre`` option of pip allows the installation of a pre-release version.


Install in development mode
---------------------------

FluidDyn is still in alpha version ("testing for
developers"!). Moreover, it has been designed to be used by
scientists-developers. Thus, there is a high probability that you will
have to modify the code or even write a new class in the package.  So
I would advice to work "as a developer", i.e. to get the source code
and to use revision control and the development mode of the Python
installer.

For FluidDyn, I use the revision control software Mercurial and the
main repository is hosted `here
<https://bitbucket.org/fluiddyn/fluiddyn>`_ in Bitbucket. I would
advice to fork this repository (click on "Fork") and to clone your
newly created repository to get the code on your computer (click on
"Clone" and run the command that will be given). If you are new with
Mercurial and Bitbucket, you can also read this short tutorial:

.. toctree::
   :maxdepth: 1

   mercurial_bitbucket

If you really don't want to use Mercurial, you can also just manually
download the package from `the Bitbucket page
<https://bitbucket.org/fluiddyn/fluiddyn>`__ or from `the PyPI page
<https://pypi.python.org/pypi/fluiddyn>`__.

The development mode is often very convenient. From the root directory
of the project, run::

  python setup.py develop

Of course you can also install FluidDyn in the standard ways,
downloading the sources and doing ``python setup.py install``.

After the installation, it is a good practice to run the unit tests by
running ``python -m unittest discover`` from the root directory or
from any of the "test" directories.
