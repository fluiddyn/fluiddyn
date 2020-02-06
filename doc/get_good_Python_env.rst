Get a good scientific Python environment
========================================

By a "good Python environment", I mean a recent version of Python with recent
versions of the main packages for sciences installed (SciPy, NumPy, Matplotlib,
IPython, h5py, etc.) and a good editor with fly checks.

.. warning::

   **Announcement: require Python 3**. As `many other scientific projects
   <http://www.python3statement.org/>`_, we now require Python 3 for all new
   feature releases. For science, try to use a recent version of Python (>= 3.6
   in 2019).

The easy way: Python distributions (for example Anaconda)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A very simple way to get such environment is to use one of the major
science-oriented Python distributions, for example the good `Python - Anaconda
<http://anaconda.io/downloads>`_ (for slightly more advanced users, `Miniconda
<https://conda.io/miniconda.html>`_ is surely better).

To get started with Miniconda (commands for Linux)::

  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3-latest-Linux-x86_64.sh

Then load the conda environment (maybe start a new terminal). It can be good to
add the channel conda-forge::

  conda config --add channels conda-forge

You are then ready to run typical conda and pip install commands, for example::

  conda install numpy matplotlib h5py blas=*=openblas
  conda install scipy pandas ipython jupyterlab imageio cython psutil

  # if you use Spyder (good idea if you do not use a good Python editor)
  conda install spyder

  # to use clang to compile C++ files produced by Pythran
  conda install clangdev

  # it can be better to install mpi4py from source rather than with conda to
  # use the native mpi library
  pip install mpi4py

  # Same for pyfftw
  pip install pyfftw

  # and for Pythran...
  pip install pythran colorlog

  # pip is also the good tool to install pure python packages, for example:
  pip install h5netcdf yapf future mako

.. warning::

   Note the ``blas=*=openblas`` requirement in the first line. This is important
   if you want to use the library fftw_mpi, with is incompatible with MKL.

Another easy way (slightly more difficult?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is now very easy to build the most recent Python versions with `pyenv
<https://github.com/pyenv/pyenv>`_.

With the latest versions of pip and the `wheels
<https://github.com/pypa/wheel>`_, it is now easy and fast to install
scientific packages without conda, using pip.

But without conda, one needs to get the non-python dependencies with the system
package management tool, for example apt for Debian/Ubuntu, as shown here:

.. toctree::
   :maxdepth: 1

   setup_ubuntu1804


Python on Windows
^^^^^^^^^^^^^^^^^

On windows, I use `Python - Anaconda <http://anaconda.io/downloads>`_.

For FluidDyn, you really need a good terminal. The standard console of Windows
7 (cmd) is just surprisingly bad. DO NOT use it since you could get some silly
problems and there are simple alternatives. For example, you could use

- `Console2 with bash from git
  <https://www.google.com/search?q=console2+git+bash>`_ instead.

- http://conemu.github.io/ with bash from git.

For flycheck, I install http://aspell.net/win32/

And on macOS
^^^^^^^^^^^^

.. warning::

  As of July 2018, there is a bad bug with clang++ with a pure conda install:
  clang++ does not find the standard C++ library (see `this fluidsim_ocean
  issue
  <https://foss.heptapod.net/fluiddyn/fluidsim_ocean/issues/1>`_)...
  One needs to use `homebrew <https://brew.sh/>`_ to install::

    brew install open-mpi
    brew install fftw --with-mpi
    brew install --with-clang llvm
    brew install mercurial

Then, two alternatives. First with the "homebrew" Python and pip::

  brew install python

  python3 -m pip install virtualenv
  virtualenv -p python3 fluid-env
  source fluid-env/bin/activate

  pip install scipy matplotlib cython h5py ipython imageio pandas

  pip install mpi4py
  pip install pyfftw
  pip install pythran colorlog
  pip install h5netcdf mako pulp

Other alternative, using ``conda`` and pip::

  conda config --add channels conda-forge
  conda env create fluid-env blas=*=openblas scipy matplotlib cython h5py ipython imageio pandas
  conda activate fluid-env

  pip install mpi4py
  pip install pyfftw
  pip install pythran colorlog
  pip install h5netcdf mako pulp


The intermediate way and the hard way: from source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another (harder) way is to build the packages from source (using the system
Python interpreter) or (even harder) to build everything from source (the
Python interpreter and then the packages) as explained here:

.. toctree::
   :titlesonly:

   build_Python
