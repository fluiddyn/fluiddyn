Python for FluidDyn
===================

Since FluidDyn aims at being used by new Python users, we have put
together some advice for starting with Python. 


Install a good Python
---------------------

By a "good Python", I mean a recent version of Python with recent
versions of the main packages for sciences installed (SciPy, NumPy,
Matplotlib, IPython, h5py, etc.).


Python 2.7 and Python 3
^^^^^^^^^^^^^^^^^^^^^^^

Python 3 is cleaner but still significantly slower... In 2014, I would
advice to try to write Python 2-3 compatible code (with some ``try``
and ``from __future__`` statements and using for example the package
`future <http://python-future.org/>`_)... and to run the program with
Python 2.7.



Python on Windows
^^^^^^^^^^^^^^^^^

You can use Python - Anaconda http://continuum.io/downloads

For FluidDyn, you really need a good terminal. The standard console of
Windows (cmd) is just surprisingly bad. DO NOT use it since you could
get some silly problems and there are simple alternatives. For
example, you could use `Console2 with bash
<https://www.google.com/search?q=console2+git+bash>`_ instead.





Recent Python version on not so recent Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some still widely used Linux work with Python 2.6 but you can always
install a more up-to-date Python 2.7.

It is a good idea to use a virtual environment. With `virtualenv
<https://virtualenv.pypa.io>`_ it is very easy. I do something like
this::

  MYPY=$HOME/path/mypy
  mkdir -p $MYPY
  virtualenv --system-site-packages $MYPY

Then I have a non-executable script ``load_mypy.sh`` in the directory
~/bin with something like this::

  export VIRTUAL_ENV_DISABLE_PROMPT=0
  MYPY=$HOME/path/mypy
  source $MYPY/bin/activate

This script should be use by `source ~/bin/load_mypy.sh` so you can
have a line with `alias load_mypython='source ~/bin/load_mypy.sh'` in the
file ~/.bash_aliases.

Remark: it could also be convenient to use the ``module load ...``
procedure...


Build Python from sources
^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, it can be useful to recompile a recent Python from
scratch.

Create the directory where the new Python will be. We then change the
owner to the user since like that we will be able to work without sudo
(we will put the correct rights and owner manually at the end)::

  version=2.7.9
  path_new_python=/opt/python/$version
  sudo mkdir -p $path_new_python
  sudo chown -R pierre $path_new_python

Install some dependencies for Python. On Debian or Ubuntu::

  sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

Download and extract the source::

  cd ~/Downloads/
  wget http://python.org/ftp/python/$version/Python-$version.tgz
  tar -xvf Python-$version.tgz
  cd Python-$version

Build and install::

  ./configure --enable-shared --prefix=$path_new_python \
              LDFLAGS=-Wl,-rpath=$path_new_python/lib
  make 
  make install

Change the used python version::

  PATH=$path_new_python/bin:$PATH
  LD_LIBRARY_PATH=$path_new_python/lib/python2.7/lib-dynload:$LD_LIBRARY_PATH

If we tell nothing about where we want to install the packages for
this Python, they should be put in the right place, i.e. in something like
`/opt/python/2.7.9/lib/python2.7/site-packages`.

Manually install pip (and setuptools)::

  wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
  python get-pip.py



Now, we can use pip for most packages. For the pure pythons packages,
it should work without any problems. For example for sympy and
virtualenv::

  pip install sympy
  pip install virtualenv

But it works also for packages with C extensions::

  pip install numpy
  pip install cython
  pip install matplotlib
  pip install mpi4py
  pip install pyfftw
  pip install lxml
  pip install flake8
  pip install pylint
  pip install sphinx
  pip install rope
  pip install psutil
  pip install subprocess32
  pip install mercurial

Even for packages using mpi (with the libraries compiles with the
correct flags)::

  export CC=mpicc
  pip install h5py
  pip install netcdf4

There are some packages that are slightly more complicated to build.

Scipy
.....

For Scipy, some dependencies have to be installed first::

  sudo apt-get libblas-dev liblapack-dev

Then :code:`pip install scipy` should work.

QUESTION: compiler options for performance?

PySide
......

PySide are Python bindings for the Qt cross-platform application and UI framework (http://pyside.readthedocs.org/en/latest/building/linux.html)::

  pip install wheel
  wget https://pypi.python.org/packages/source/P/PySide/PySide-1.2.2.tar.gz --no-check-certificate
  tar -xvzf PySide-1.2.2.tar.gz
  cd PySide-1.2.2
  python setup.py bdist_wheel --qmake=/usr/bin/qmake-qt4
  pip install dist/PySide-1.2.2*.whl
  python pyside_postinstall.py -install

Then we can install Spyder (Matlab users are happier)::

  pip install spyder

Basemap 
.......

Plot data on map projections with matplotlib. It seems that we have to
download the .tar from sourceforge
(http://matplotlib.org/basemap/users/installing.html). It's pretty big
(~48 Mo)::

  cd $dir_source
  wget http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz --no-check-certificate
  tar xzf basemap-1.0.7.tar.gz
  cd basemap-1.0.7
  python setup.py install
  cd $dir_source


Finalisation
............

We set the correct rights and the ownership to root::

  sudo chmod -R a+rX      $path_new_python
  sudo chown -R root:root $path_new_python




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

Advice
------

- It is always useful to have a look at `the official Python
  documentation <https://www.python.org/doc/>`_.

- If you already know Python, it could be useful to check out some
  `best practices <http://docs.python-guide.org/en/latest/>`_.

- A famous very good book:
  http://www.diveintopython.net/ (and now http://www.diveintopython3.net/).

- If you begin with Python and even if you have some experience with
  this language, `understanding Python variables
  <http://foobarnbaz.com/2012/07/08/understanding-python-variables/>`_
  is important and can avoid some bugs.


- For Matlab users who begin with Python, I would advice to add in your
  ``.bashrc`` the line::

    alias ipython='ipython --pylab'

  With the option ``--pylab``, Ipython imports the module
  ``matplolib.pylab`` with the command ``from matplotlib.pylab import
  *`` and runs ``matplotlib.pylab.ion()`` [1]_ (this can take a few
  seconds), so the iterative Python console will behave much more like
  in Matlab than the standard ipython console without ``pylab``
  imported.


- Use the code checker pylint. Examples of commands (from the FluidDyn
  root directory)::

    pylint fluiddyn
    pylint -E fluiddyn.lab.probes
    pylint --help-msg=no-member

- Use an editor running fly checks (for example Emacs with `Flycheck
  <http://flycheck.readthedocs.org/en/latest/index.html>`_).






---------------------------------------------

.. [1] In your scripts, it is better to use ``import matplotlib.pyplot as plt``.
