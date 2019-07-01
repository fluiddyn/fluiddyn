"""Input/output streams
=======================

.. _io:

Loading data from files and saving data to files are very common
tasks. However, we can loose a lot of time with silly problems. This subpackage
provides utilities for input/output to different file formats:

.. autosummary::
   :toctree:

   binary
   txt
   mycsv
   hdf5
   digiflow
   dantec
   davis
   rdvision
   ns3d
   multitiff
   in_py
   image
   redirect_stdout
   dump
   tee
   query


To define environment variables, use something like (on POSIX systems, in the
terminal or in your .bashrc)::

  export FLUIDSIM_PATH="/fsnet/project/meige/2015/15DELDUCA/DataSim"

"""

import os
import pathlib

from .redirect_stdout import stdout_redirected

Path = pathlib.Path

HOME_DIR = Path.home()

FLUIDDYN_PATH_EXP = os.environ.get("FLUIDDYN_PATH_EXP")
if FLUIDDYN_PATH_EXP is not None:
    raise DeprecationWarning(
        "FLUIDDYN_PATH_EXP is deprecated: use FLUIDLAB_PATH."
    )

del FLUIDDYN_PATH_EXP

FLUIDLAB_PATH = os.environ.get("FLUIDLAB_PATH")
if FLUIDLAB_PATH is None:
    FLUIDLAB_PATH = str(HOME_DIR / "Exp_data")


FLUIDDYN_PATH_SIM = os.environ.get("FLUIDDYN_PATH_SIM")
if FLUIDDYN_PATH_SIM is not None:
    raise DeprecationWarning(
        "FLUIDDYN_PATH_SIM is deprecated: use FLUIDSIM_PATH."
    )

del FLUIDDYN_PATH_SIM

FLUIDSIM_PATH = os.environ.get("FLUIDSIM_PATH")
if FLUIDSIM_PATH is None:
    FLUIDSIM_PATH = str(HOME_DIR / "Sim_data")


FLUIDDYN_PATH_SCRATCH = os.getenv("FLUIDDYN_PATH_SCRATCH", FLUIDSIM_PATH)

FLUIDDYN_PATH_WARNING = os.environ.get("FLUIDDYN_PATH_WARNING")
if FLUIDDYN_PATH_WARNING is None:
    FLUIDDYN_PATH_WARNING = str(HOME_DIR / ".fluiddyn")


if not os.path.exists(FLUIDDYN_PATH_WARNING):
    os.makedirs(FLUIDDYN_PATH_WARNING)


def _write_warning(*args, **kargs):
    if "end" in kargs:
        end = kargs["end"]
    else:
        end = "\n"
    strings = []
    for i, v in enumerate(args):
        strings.append(str(v))
    with open(os.path.join(FLUIDDYN_PATH_WARNING, "warnings.txt"), "a") as f:
        f.write(" ".join(strings) + end)


__all__ = ["stdout_redirected"]
