Get a good scientific Python environment
========================================

By a "good Python environment", I mean a recent version of Python with
recent versions of the main packages for sciences installed (SciPy,
NumPy, Matplotlib, IPython, h5py, etc.) and a good editor with fly checks.

Remark: FluidDyn works with Python 2.7. It would not be difficult to
support Python 2.6 but I think that for science, it is important and
not difficult to use a recent version of Python and of the main
libraries.

- A very simple way to get such environment is to use one of the major
  science-oriented Python distributions, for example the good
  `Python - Anaconda <http://continuum.io/downloads>`_.

- Another way is to build the packages (or even the Python interpreter)
  for source as explained here: 

  .. toctree::
     :maxdepth: 0

     build_Python


Python on Windows
^^^^^^^^^^^^^^^^^

On windows, I use Python - Anaconda http://continuum.io/downloads

For FluidDyn, you really need a good terminal. The standard console of
Windows (cmd) is just surprisingly bad. DO NOT use it since you could
get some silly problems and there are simple alternatives. For
example, you could use

- `Console2 with bash from git
  <https://www.google.com/search?q=console2+git+bash>`_ instead.

- http://conemu.github.io/ with bash from git.

For flycheck, I install http://aspell.net/win32/


Recent Python version on not so recent Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some still widely used Linux work with Python 2.6 but you can always
install a more up-to-date Python 2.7. If you can not install a package
with python 2.7 and virtualenv, build Python from source.


Python 2 on Arch Linux
^^^^^^^^^^^^^^^^^^^^^^

Arch Linux uses Python 3 for the applications and the command python
is associated with the Python 3 interpreter.

If you have Python 2 installed, you could use a virtual environment like this::

  PYTHON2=`which python2`
  MYPY=$HOME/opt/mypy2
  mkdir $MYPY
  virtualenv --python=$PYTHON2 --system-site-packages $MYPY

Then put a non-executable script ``load_python2.sh`` in the directory
~/bin with something like this::

  export VIRTUAL_ENV_DISABLE_PROMPT=0
  MYPY=$HOME/opt/mypy2
  source $MYPY/bin/activate

This script should be use by *source ~/bin/load_python2.sh* so you can
have a line with *alias load_python2='source ~/bin/load_python2.sh'*
in the file *~/.bash_aliases*. Then, each time you want to use Python
2 in a terminal, just run the command *load_python2* and the command
*python* will be associated with Python 2 as in most Linux
distributions. Moreover, the command *ipython* and *sphinx-build*
should also use this Python version. To install packages for this
environment, activate the environment and use *pip*.

You can test if the virtual environment has been correctly activated
by running *which python* and *python -V*.

