How to setup a fresh install of Ubuntu 18.04 for Python and fluiddyn
====================================================================

- Install some useful compilers, libraries and utilities::

   sudo apt-get install \
     clang-6.0 gfortran cmake \
     libpng-dev libfftw3-dev libfftw3-mpi-dev \
     libhdf5-dev libopenmpi-dev \
     qt5-default \
     curl ack pandoc \
     fish

- Setup https://fishshell.com/

- Install Mercurial with pip, we still need python 2.7!

  .. code::

     sudo apt install python2.7 python-pip
     python2 -m pip install mercurial hg-git --user

- Install Git::

    sudo apt-get install git

- Install and setup emacs::

    sudo apt-get install emacs

  and then follow https://bitbucket.org/fluiddyn/fluid_emacs.d

- Install miniconda::

    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash ./Miniconda3-latest-Linux-x86_64.sh

- To build Cpython, we first have to modify a file (see
  http://cpython-devguide.readthedocs.io/setup/#build-dependencies). Then::

    sudo apt-get update
    sudo apt-get build-dep python3.6

- Install pyenv (see https://github.com/pyenv/pyenv)::

    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash'
    exec "$SHELL"

- Build nice Python versions and use Python 3.7::

    pyenv install 3.7.0
    pyenv install pypy3.5-6.0.0
    pyenv global 3.7.0

  Then install several packages (as wheels) using pip::

    pip install ipython jupyterlab
    pip install numpy scipy matplotlib
    pip install h5py h5netcdf
    pip install cython mako colorlog pythran
    pip install future
    pip install mpi4py
    pip install pyfftw
    pip install pylint flake8 mypy black yapf
    pip install trio
    pip install sphinx numpydoc
    pip install pyqt5
    pip install spyder
    pip install pipenv

- Install https://code.visualstudio.com
