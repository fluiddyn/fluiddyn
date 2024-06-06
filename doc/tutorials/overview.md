---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
from fluiddoc import mock_modules

mock_modules(('nbstripout', 'scipy', 'scipy.fftpack', 'scipy.interpolate',
              'skimage', 'skimage.io'))
```

# Main features of the fluiddyn package

We here give an overview of the main features of the package. Fluiddyn contains pure
python code useful when developing and using fluiddyn packages. It is like the Ali Baba's
cave of the fluiddyn project. Here, we just show typical import commands and point
towards pages in the documentation.

Just importing the main package can be useful:

```{code-cell} ipython3
import fluiddyn as fld
```

```{code-cell} ipython3
fld.constants.g
```

```{code-cell} ipython3
fld.time_as_str()
```

```{code-cell} ipython3
fld.get_memory_usage()
```

```{code-cell} ipython3
fld.ipydebug
```

```{raw-cell}
is a function to debug code with ipython (simpler than with pdb or ipdb):
```

## Subpackage `fluiddyn.output`

```{raw-cell}
The subpackage :mod:`fluiddyn.output` ("scientific outputs" like figures and movies) uses (and imports) matplotlib.
```

```{code-cell} ipython3
from fluiddyn.output import show, set_rcparams, gradient_colors
```

## Subpackage `fluiddyn.io`

```{raw-cell}
The subpackage :mod:`fluiddyn.io` ("input/output") contains modules to save and load data in many formats:
```

```{code-cell} ipython3
from fluiddyn.io import (
    binary, txt, mycsv, hdf5, digiflow, dantec, davis, multitiff, in_py, image)
```

```{code-cell} ipython3
from fluiddyn.io.query import query_yes_no, query, query_number
from fluiddyn.io.tee import MultiFile
```

There is also a function to disable the standard output which we use a lot in unittests.

```{code-cell} ipython3
from fluiddyn.io import stdout_redirected
```

### fluiddump

This package also contains the code of a very simple utility to dump hdf5 and netcdf
files (without dependency in the netcdf library and in the program `h5dump`)

```{code-cell} ipython3
from fluiddyn.io.dump import dump_h5_file, dump_nc_file
```

```{code-cell} ipython3
! fluiddump -h
```

## Subpackage `fluiddyn.util`

```{raw-cell}
The subpackage :mod:`fluiddyn.util` contains functions and modules to do very different things:
```

```{code-cell} ipython3
from fluiddyn.util import (
    time_as_str, get_memory_usage, print_memory_usage,
    import_class, is_run_from_ipython)

# very simple use of mpi (no dependency on mpi4py if the process is run without mpi)
from fluiddyn.util import mpi

# storing parameters
from fluiddyn.util.paramcontainer import ParamContainer
from fluiddyn.util.paramcontainer_gui import QtParamContainer

# handling series of arrays in files
from fluiddyn.util.serieofarrays import SerieOfArraysFromFiles, SeriesOfArrays

# "tickers"
from fluiddyn.util.timer import Timer, TimerIrregular

# daemon
from fluiddyn.util.daemons import DaemonThread, DaemonProcess

# emails
from fluiddyn.util import mail

# matlab to py (command line utility fluidmat2py)
from fluiddyn.util.matlab2py import cleanmat, mat2wrongpy
```

### Logging

```{code-cell} ipython3
from fluiddyn.util.logger import Logger
from fluiddyn.util import terminal_colors
from fluiddyn.util import config_logging

from fluiddyn.util.terminal_colors import cprint
cprint("RED", color="RED")
cprint.cyan("cyan")
cprint.light_blue("bold light blue", bold=True)
```

### fluidinfo: gather information on your Python environment

```{code-cell} ipython3
from fluiddyn.util import info
```

```{code-cell} ipython3
!fluidinfo -h
```

## Subpackage `fluiddyn.calcul`

```{raw-cell}
The subpackage :mod:`fluiddyn.calcul` provides helpers for simple numerical computing.
```

```{code-cell} ipython3
from fluiddyn.calcul import easypyfft
```

```{code-cell} ipython3
from fluiddyn.calcul import sphericalharmo
```

```{code-cell} ipython3
from fluiddyn.calcul import signal
```

```{code-cell} ipython3
from fluiddyn.calcul.setofvariables import SetOfVariables
```

## Subpackage `fluiddyn.clusters`

```{raw-cell}
The subpackage :mod:`fluiddyn.clusters` provides classes helping to use computer clusters.
```

```{code-cell} ipython3
from fluiddyn.clusters.legi import Calcul8 as Cluster
Cluster.print_doc_commands()
```

```{code-cell} ipython3
from fluiddyn.clusters.cines import Occigen as Cluster
Cluster.print_doc_commands()
```

## Package `fluiddoc`: helping to build nice web documentations

```{code-cell} ipython3
import fluiddoc
print(fluiddoc.on_rtd)
```

```{code-cell} ipython3
fluiddoc.mock_modules
```

```{code-cell} ipython3
from fluiddoc.ipynb_maker import ipynb_to_rst
```
