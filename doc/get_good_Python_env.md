# Get a good scientific Python environment

By a "good Python environment", I mean a recent version of Python with
recent versions of the main packages for sciences installed (SciPy,
NumPy, Matplotlib, IPython, h5py, etc.) and a good editor with fly
checks.

```{admonition} Announcement: require Python 3
:class: warning
As [many other scientific
projects](http://www.python3statement.org/), we now require Python 3 for
all new feature releases. For science, try to use a recent version of
Python (\>= 3.6 in 2019).
```

## The easy way: Mambaforge and conda-forge

A very simple way to get such environment is to use Mambaforge (provided by the
[Miniforge] project), which is a modified version of
[Miniconda](https://docs.conda.io/en/latest/miniconda.html) with the new and
fast cross-platform package manager [mamba] and using by default the community
driven [conda-forge] channel.

```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh" -O Mambaforge_installer.sh
bash Mambaforge_installer.sh -b
$HOME/mambaforge/bin/mamba init bash
```

````{admonition} Command wget not found?
:class: dropdown

You might be more lucky with the equivalent command with `curl`:

```bash
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh -o Mambaforge_installer.sh
```
````

```{warning}
In some systems, the default shell is not bash so you need to modified the last
command to initialize your shell. For example for macOS:
`$HOME/mambaforge/bin/mamba init zsh`.
```

When it's done, try to open a new terminal (click on `ctrl-alt-t`) and check that
the line in the new terminal starts with `(base)`. If yes, you can close the old
terminal (with `ctrl-d`). The indication `(base)` means that you use the base
"environment".

`conda` and `mamba` are 2 commandline tools to manage software installations and
create "environments".

```{admonition} conda and mamba: differences?
:class: dropdown

Conda is an open source package management system and environment management
system that runs on Windows, macOS, Linux and z/OS.

Mamba is a new implementation of conda, which is faster for some operations and
has better logging.
```

```{admonition} Definition: conda environment
:class: dropdown

A environment is a set of programs and libraries with particular versions. An
environment is defined by the software installed on your computer and by
environment variables, in particular the variable `$PATH`, which contains all
the paths where your shell looks for programs (you can read the output of `echo
$PATH`).
```

It is very useful to be able to create different environments for different
tasks. It is usually better to keep the `base` environment only for the `conda`
/ `mamba` software and to use different environments for other tasks. We will
use this strategy here. We will have

- 1 environment for some basic libraries and Fluidsim sequential (called `main`),

- 1 environment with Fluidsim and MPI (called `env_fluidsim`)

- 1 environment with the Spyder editor (automatically created with the tool
  `conda-app`)

- 1 environment with Mercurial (automatically created with the tool `conda-app`)

`conda` takes the programs that it installs from "channels". With Fluiddyn,
we'd like to use the largest open-source community driven channel called
[conda-forge]. With [Miniforge], [conda-forge] is by default the main channel.

We can start by creating the `main` environment with the commands:

```bash
wget https://foss.heptapod.net/fluiddyn/fluiddyn/-/raw/branch/default/doc/main_environment.yml
mamba env create -f main_environment.yml
```

The file `main_environment.yml` contains the following:

```{eval-rst}
.. literalinclude:: main_environment.yml
```

```{tip}
The line `conda activate main` can be added at the end of your `~/.bashrc`.
```

Then, we create another environment for Fluidsim parallel with:

```bash
mamba create -n env-fluidsim -y \
  fluidsim "fluidfft=*=mpi*" "h5py=*=mpi*" openmpi \
  ipython matplotlib ipympl ipykernel spyder-kernels \
  "pyfftw=0.13.0=py310*_0"
```

To install up-to-date versions of useful applications like Mercurial and Spyder, you can run:

```bash
pip install conda-app
conda-app install mercurial
conda-app install spyder
```

```{note}
[conda-app] is a very small utility which installs programs in isolated conda
environments. Very similar to [pipx] but with conda environment.
```

```{note}
In some clusters, it is better to use the native mpi library. To do so, one
needs to install mpi4py from source (i.e. with `pip install mpi4py` and not
with conda).
```

```{note}
To compile Python files with Pythran (which is done when one builds some
fluiddyn packages from source) one can install [clang] (with `mamba install
clangdev`) to compile C++ files produced by Pythran.
```

```{warning}
There are cases for which it is useful to specify the blas version by
adding `blas=*=openblas` to the requirements. This is important if you want to
use the library `fftw_mpi`, which is incompatible with MKL.
```

## Another easy way (slightly more difficult?)

It is now very easy to build the most recent Python versions with
[pyenv](https://github.com/pyenv/pyenv).

With the latest versions of pip and the
[wheels](https://github.com/pypa/wheel), it is now easy and fast to
install scientific packages without conda, using pip.

But without conda, one needs to get the non-python dependencies with the
system package management tool, for example apt for Debian/Ubuntu, as
shown [here](setup_ubuntu1804.md)

[conda-forge]: https://conda-forge.org/
[miniforge]: https://github.com/conda-forge/miniforge
[spyder]: https://www.spyder-ide.org/
[mamba]: https://github.com/mamba-org/mamba
[conda-app]: https://pypi.org/project/conda-app/
[pipx]: https://github.com/pypa/pipx
[clang]: https://clang.llvm.org/