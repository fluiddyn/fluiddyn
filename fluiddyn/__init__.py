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

from fluiddyn.util.util import create_object_from_file
from fluiddyn.util import constants
from fluiddyn._version import __version__


# temporary, for compatibility with an old fluidlab...
def _verif_names_modules(name_mod, path_h5_file, key_file):

    if isinstance(name_mod, str):
        name_mod = name_mod.encode('utf-8')

    exp_TC_old = 'fluidlab.experiments.taylorcouette_'
    exp_TC_new = 'fluidlab.exp.taylorcouette.'

    new_names_modules = {
        exp_TC_old + 'linearprofil': exp_TC_new + 'linearprofile',
        exp_TC_old + 'quadprofil': exp_TC_new + 'quadprofile',
        exp_TC_old + '2layers': exp_TC_new + 'twolayers',
        'fluidlab.tanks': 'fluidlab.tanks'
    }

    if name_mod in new_names_modules.keys():
        name_mod = new_names_modules[name_mod]
        import h5py
        with h5py.File(path_h5_file, 'r+') as f:
            f.attrs[key_file] = name_mod

    return name_mod
