Get a good scientific Python environment
========================================

By a "good Python environment", I mean a recent version of Python with
recent versions of the main packages for sciences installed (SciPy,
NumPy, Matplotlib, IPython, h5py, etc.) and a good editor with fly checks.

.. warning:: 

   **Announcement: Moving to require Python 3**. As `many other
   scientific projects <http://www.python3statement.org/>`_, we are planning to
   soon require Python 3 for all new feature releases. For science, try to use
   a recent version of Python (>= 3.5 in 2018).

The easy way: Python distributions (for example Anaconda)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A very simple way to get such environment is to use one of the major
science-oriented Python distributions, for example the good `Python - Anaconda
<http://anaconda.io/downloads>`_ (for slightly more advanced users, `Miniconda
<https://conda.io/miniconda.html>`_ is surely better).

To get started with Miniconda::

  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3-latest-Linux-x86_64.sh
  
It can be good to use the channel conda-forge. This can be done using a file
`~/.condarc` with::

  channels:
    - conda-forge
    - defaults

Then load the conda environment (maybe start a new terminal) and you can run
typical conda and pip install commands, for example::

  conda install scipy matplotlib pandas h5py ipython jupyterlab imageio cython psutil
  conda install spyder
  pip install mpi4py pythran colorlog    

The intermediate way and the hard way: from source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another (harder) way is to build the packages from source (using the system
Python interpreter) or (even harder) to build everything from source (the
Python interpreter and then the packages) as explained here:

.. toctree::
   :maxdepth: 0

   build_Python

Python on Windows
^^^^^^^^^^^^^^^^^

On windows, I use `Python - Anaconda <http://anaconda.io/downloads>`_.

For FluidDyn, you really need a good terminal. The standard console of
Windows (cmd) is just surprisingly bad. DO NOT use it since you could
get some silly problems and there are simple alternatives. For
example, you could use

- `Console2 with bash from git
  <https://www.google.com/search?q=console2+git+bash>`_ instead.

- http://conemu.github.io/ with bash from git.

For flycheck, I install http://aspell.net/win32/


Recent Python versions on old GNU/Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some old Linux work with Python 2.6 but you can always install a more
up-to-date Python version. If you can not install a package with python 3 (and
conda or virtualenv), build Python from source.
