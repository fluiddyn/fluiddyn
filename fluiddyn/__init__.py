"""
FluidDyn
========

Provides 

  1. An object-oriented and modular set of solvers.
  2. Tools useful for carrying out experiments in fluid dynamics.

The docstring examples assume that `fluiddyn` has been imported as `fld`::

  >>> import fluiddyn as fld

Use the built-in ``help`` function to view a function's docstring::

  >>> help(fld.figs.Figures)
  ... # doctest: +SKIP

Available subpackages
---------------------
lab
    Utilities for carrying out experiments in fluid dynamics.
simul
    Code for simulations of sets of equations modelling fluids (mostly
    in geophysical context).

"""

from fluiddyn import lab
from fluiddyn import simul

from fluiddyn.util.util import load_exp, create_object_from_file

import fluiddyn.util.constants as constants

from fluiddyn._version import __version__

# temporary to avoid the error where matplotlib is not installed
try:
    from fluiddyn.output.figs import show
except ImportError:
    pass

from fluiddyn.util.debug_with_ipython import ipydebug


# temporary, for compatibility with fluidlab...
def _verif_names_modules(name_mod, path_h5_file, key_file):

    if isinstance(name_mod, str):
        name_mod = name_mod.encode('utf-8')

    exp_TC_old = 'fluidlab.experiments.taylorcouette_'
    exp_TC_new = 'fluiddyn.lab.exp.taylorcouette.'

    new_names_modules = {
        exp_TC_old+'linearprofil': exp_TC_new+'linearprofile',
        exp_TC_old+'quadprofil': exp_TC_new+'quadprofile',
        exp_TC_old+'2layers': exp_TC_new+'twolayers',
        'fluidlab.tanks': 'fluiddyn.lab.tanks'
    }

    if name_mod in new_names_modules.keys():
        name_mod = new_names_modules[name_mod]
        import h5py
        with h5py.File(path_h5_file, 'r+') as f:
            f.attrs[key_file] = name_mod

    if name_mod.startswith('fluidlab'):
        raise ValueError('Use of module ' + name_mod)

    return name_mod
