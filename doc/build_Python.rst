Build Python from sources
=========================

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


Finalization
............

We set the correct rights and the ownership to root::

  sudo chmod -R a+rX      $path_new_python
  sudo chown -R root:root $path_new_python

