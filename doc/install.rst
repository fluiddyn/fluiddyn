Installation
============


Get a good Python
-----------------

FluidDyn works with Python 2.7 and 3.2 or newer. It would not be
difficult to support Python 2.6 but I think that for this purpose, one
should use a recent version of Python and of the main libraries
(mainly Matplotlib, NumPy, SciPy).  See this page:

.. toctree::
   :maxdepth: 1

   python_for_fluiddyn


Get the source code
-------------------

FluidDyn has been designed to be used by scientists-developers. There
is a high probability that you will have to modify the code or even
write a new class in the package.  So I would advice to work "as a
developer", i.e. to get the source code and to use revision control
and the development mode of the Python installer.

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


Install in development mode
---------------------------


The development mode is very convenient. From the root directory of
the project, run::

  sudo python setup.py develop

Of course you can also install FluidDyn in the standard ways,
downloading the package and doing ``python setup.py install`` or just
using pip by running ``pip install fluiddyn``.


To build the C and Cython extensions::

  python setup.py build_ext --inplace


Run the tests
-------------

You can run some unit tests by running ``python -m unittest discover``
from the root directory or from any of the "test"
directories.


