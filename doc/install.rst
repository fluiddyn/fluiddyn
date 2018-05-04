Installation
============

Dependencies
------------

- **Minimum** : Python (2.7, >=3.4), numpy, matplotlib, psutil, future,
  subprocess32 (for Python 2.7 only)

- **Full functionality**: h5py, h5netcdf, pillow, imageio, mpi4py, scipy,
  pyfftw (requires FFTW library)

- **Optional**: OpenCV with Python bindings, scikit-image

It is strongly recommended to install `NumPy
<http://docs.scipy.org/doc/numpy/user/install.html>`_ and `Matplotlib
<http://matplotlib.org/users/installing.html>`_ before installing FluidDyn.

FluidDyn also used some other packages for some particular tasks, as
in particular Scipy and h5py. Since they can be difficult to get for
some small hardware, they are not considered as real dependencies, but
be prepared to get ImportError if you try to do something using these
packages without them.

We present how to install the requirements in this page:

.. toctree::
   :maxdepth: 1

   get_good_Python_env


Basic installation
------------------

FluidDyn can be installed from the Python Package Index by the command::

  pip install fluiddyn

You can also download the source-code and run::

  python setup.py install

Install in development mode
---------------------------

Get the source by cloning the repository (as explained in :ref:`advicedev`)::

  hg clone https://bitbucket.org/fluiddyn/fluiddyn

or by manually downloading the package from `the Bitbucket page
<https://bitbucket.org/fluiddyn/fluiddyn>`__ or from `the PyPI page
<https://pypi.python.org/pypi/fluiddyn>`__.

The development mode is often very convenient. From the root directory
of the project, run::

  cd fluiddyn
  python setup.py develop

After the installation, it is a good practice to run the unit tests by
running ``python -m unittest discover`` from the root directory or
from any of the "test" directories.
