Installation
============

Dependencies
------------

- **Minimum** : Python (>=3.6), numpy, matplotlib, h5py, h5netcdf, psutil

- **Full functionality**: pillow, imageio, mpi4py, scipy, pyfftw (requires FFTW
  library)

- **Optional**: OpenCV with Python bindings, scikit-image

It is recommended to install `NumPy
<http://docs.scipy.org/doc/numpy/user/install.html>`_ and `Matplotlib
<http://matplotlib.org/users/installing.html>`_ before installing FluidDyn.

FluidDyn also used some other packages for some particular tasks, as in
particular Scipy. Since it can be difficult to install them for some small
hardware, they are not considered as real dependencies. However, be prepared to
get some ImportError :-)

We present how to install the requirements in this page:

.. toctree::
   :maxdepth: 1

   get_good_Python_env


Basic installation
------------------

FluidDyn can be installed from the Python Package Index by the command::

  pip install fluiddyn

Or, to also install all optional dependencies::

  pip install fluiddyn[full]


Install in development mode
---------------------------

Get the source by cloning the repository (as explained in :ref:`advicedev`)::

  hg clone https://foss.heptapod.net/fluiddyn/fluiddyn

or by manually downloading the package from `the Heptapod page
<https://foss.heptapod.net/fluiddyn/fluiddyn>`__ or from `the PyPI page
<https://pypi.python.org/pypi/fluiddyn>`__.

The development mode is often very convenient. From the root directory
of the project, run::

  cd fluiddyn
  pip install -e .

After the installation, it is a good practice to run the unit tests by running
``pytest`` from the root directory or from any of the "test" directories.
To install the test dependencies::

  pip install -e .[test]
