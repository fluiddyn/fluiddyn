# Installation

The first step to install the fluiddyn packages is to get Python (>=3.9). We discuss
different methods in this page:

```{toctree}
---
maxdepth: 1
---
get_good_Python_env
```

## From the Python Package Index

FluidDyn can be installed from the Python Package Index by the command:

```sh
pip install fluiddyn
```

This installs Fluiddyn and its hard dependencies (numpy, matplotlib, h5py, h5netcdf,
psutil, simpleeval).

FluidDyn also used some other packages for some particular tasks, as in particular Scipy.
Since it can be difficult to install them for some small hardware, they are not
considered as hard dependencies.

Fluiddyn has few sets of optional dependencies (`fft`, `mpi`, `sht`, `full`), which can
be installed with commands like

```sh
pip install fluiddyn[full]
```

## From the repository

```sh
pip install fluiddyn@hg+https://foss.heptapod.net/fluiddyn/fluiddyn
```

## From the conda-forge index

```sh
conda install fluiddyn
# or
mamba install fluiddyn
```
