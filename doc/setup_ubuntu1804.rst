How to setup a fresh install of Ubuntu 18.04 for Python for sciences
====================================================================

This is just an example (2018-07-10), but it is useful for me (Pierre Augier) to
have this page, so it may be useful to others.

- Install some useful compilers, libraries and utilities::

   sudo apt-get install \
     clang-6.0 gfortran cmake \
     libpng-dev libfftw3-dev libfftw3-mpi-dev \
     libhdf5-dev libopenmpi-dev \
     qt5-default \
     curl ack meld pandoc \
     fish

- Install Mercurial with pip, we still need python 2.7!

  See http://fluiddyn.readthedocs.io/en/latest/mercurial_bitbucket.html

  .. code::

     sudo apt install python2.7 python-pip
     python2 -m pip install mercurial hg-git --user
     hg config --edit

- Install Git::

    sudo apt install git

- Install and setup emacs::

    sudo apt install emacs

  and then follow https://bitbucket.org/fluiddyn/fluid_emacs.d

- Setup Bash (``.bashrc`` and ``.bash_aliases``)

- Setup https://fishshell.com/ (if you want Fish!)::

    chsh -s $(which fish)
    echo 'set -gx PATH $PATH $HOME/.cask/bin $HOME/.local/bin/' >> ~/.config/fish/config.fish

- Install miniconda::

    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash ./Miniconda3-latest-Linux-x86_64.sh

- To build Cpython, we first have to modify a file (see
  http://cpython-devguide.readthedocs.io/setup/#build-dependencies). Then::

    sudo apt-get update
    sudo apt-get build-dep python3.6

- Install pyenv (see https://github.com/pyenv/pyenv)::

    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

  Then, for Bash::

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash'
    exec "$SHELL"

  And for Fish, see https://github.com/fisherman/pyenv

- Build nice Python versions and use Python 3.7::

    pyenv install 3.7.0
    pyenv install pypy3.5-6.0.0
    pyenv global 3.7.0

  Then install several packages (as wheels) using pip::

    pip install ipython jupyterlab
    pip install numpy scipy matplotlib pandas
    pip install h5py h5netcdf
    pip install imageio
    pip install cython mako colorlog pythran
    pip install mpi4py
    pip install future
    pip install pyfftw
    pip install pylint flake8 mypy black yapf
    pip install trio
    pip install sphinx numpydoc sphinx-rtd-theme
    pip install pyqt5
    pip install spyder
    pip install pipenv

  Note that `pip install numpy` installs a numpy wheel containing openblas.

- Install https://code.visualstudio.com

- Setup ``~/.pythranrc``::

    wget https://bitbucket.org/fluiddyn/fluiddyn/raw/default/doc/simple.pythranrc -O ~/.pythranrc

- Fix Gnome::

    sudo apt-get install chrome-gnome-shell gnome-tweak-tool

  * Install https://extensions.gnome.org/extension/484/workspace-grid/

  * Using ``gnome-tweaks``, set static workspaces

  * Dock: hidden and smaller (in Settings)
