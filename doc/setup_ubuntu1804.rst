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

- To build CPython, we first have to modify a file (see
  http://cpython-devguide.readthedocs.io/setup/#build-dependencies). Then::

    sudo apt-get update
    sudo apt-get build-dep python3.6

- Install pyenv (see https://github.com/pyenv/pyenv)::

    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

  Then, for Bash::

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc'
    exec "$SHELL"

  And for Fish, see https://github.com/fisherman/pyenv

- Build nice Python versions and use Python 3.6 or 3.7::

    pyenv install 3.6.6
    pyenv install 3.7.0
    pyenv install pypy3.5-6.0.0
    pyenv global 3.7.0  # or 3.6.6

  Then install several packages (as wheels) using pip::

    pip install --upgrade pip
    pip install pipenv
    pip install pytest coverage
    pip install ipython jupyterlab
    pip install numpy scipy matplotlib pandas ipympl
    pip install h5py h5netcdf
    pip install imageio pims
    pip install cython mako colorlog pythran
    pip install mpi4py
    pip install future
    pip install pyfftw
    pip install pylint flake8 mypy black yapf
    pip install trio
    pip install sphinx numpydoc sphinx-rtd-theme
    pip install pyqt5
    pip install spyder
    pip install pyqtgraph

    pip install opencv-python

    pip install scikit-image scikit-learn

  Note that `pip install numpy` installs a numpy wheel containing openblas.

- More Jupyter::

    sudo apt install nodejs npm

    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    jupyter labextension install jupyter-matplotlib

    sudo apt install chromium-browser
    jupyter-lab --generate-config
    echo 'c.NotebookApp.browser = "/usr/bin/chromium-browser"' >> ~/.jupyter/jupyter_notebook_config.py

- Install https://code.visualstudio.com

- Setup ``~/.pythranrc``::

    wget https://bitbucket.org/fluiddyn/fluiddyn/raw/default/doc/simple.pythranrc -O ~/.pythranrc

- Fix Gnome::

    sudo apt-get install chrome-gnome-shell gnome-tweak-tool

  * Install

    - https://extensions.gnome.org/extension/484/workspace-grid/

    - https://extensions.gnome.org/extension/15/alternatetab/

  * Using ``gnome-tweaks``, set static workspaces

  * Dock: hidden and smaller (in Settings)

- Install Latex::

    sudo apt install dvipng texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra

- Install GMT 6 and gmt-python::

    sudo apt install gmt-gshhg libgdal-dev libpcre2-dev libnetcdf-dev ghostscript

    git clone https://github.com/GenericMappingTools/gmt
    cd gmt/
    cp cmake/ConfigUserTemplate.cmake cmake/ConfigUser.cmake
    mkdir build
    cd build/

    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
    make -j4
    sudo make -j4 install

    pip install https://github.com/GenericMappingTools/gmt-python/archive/master.zip

    # for bash
    echo -e '\nexport LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/' >> ~/.bashrc

    # for fish
    echo -e '\nset -gx LD_LIBRARY_PATH $LD_LIBRARY_PATH /usr/local/lib/' >> ~/.config/fish/config.fish
