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
   multitiff
   redirect_stdout

"""

from builtins import str
import os
from .redirect_stdout import stdout_redirected


FLUIDDYN_PATH_EXP = os.environ.get('FLUIDDYN_PATH_EXP')
if FLUIDDYN_PATH_EXP is not None:
    raise DeprecationWarning(
        'FLUIDDYN_PATH_EXP is depreciated: use FLUIDLAB_PATH.')
del FLUIDDYN_PATH_EXP

FLUIDLAB_PATH = os.environ.get('FLUIDLAB_PATH')
if FLUIDLAB_PATH is None:
    FLUIDLAB_PATH = os.path.expanduser('~/Exp_data')


FLUIDDYN_PATH_SIM = os.environ.get('FLUIDDYN_PATH_SIM')
if FLUIDDYN_PATH_SIM is not None:
    raise DeprecationWarning(
        'FLUIDDYN_PATH_SIM is depreciated: use FLUIDSIM_PATH.')
del FLUIDDYN_PATH_SIM

FLUIDSIM_PATH = os.environ.get('FLUIDSIM_PATH')
if FLUIDSIM_PATH is None:
    FLUIDSIM_PATH = os.path.expanduser('~/Sim_data')


FLUIDDYN_PATH_SCRATCH = os.environ.get('FLUIDDYN_PATH_SCRATCH')

FLUIDDYN_PATH_WARNING = os.environ.get('FLUIDDYN_PATH_WARNING')
if FLUIDDYN_PATH_WARNING is None:
    FLUIDDYN_PATH_WARNING = os.path.expanduser('~/.fluiddyn')


if not os.path.exists(FLUIDDYN_PATH_WARNING):
    os.makedirs(FLUIDDYN_PATH_WARNING)


def _write_warning(*args, **kargs):
    if 'end' in kargs:
        end = kargs['end']
    else:
        end = '\n'
    strings = []
    for i, v in enumerate(args):
        strings.append(str(v))
    with open(os.path.join(FLUIDDYN_PATH_WARNING, 'warnings.txt'), 'a') as f:
        f.write(' '.join(strings)+end)


__all__ = ['stdout_redirected']
