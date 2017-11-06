"""
FluidDyn
========

Provides 

  1. An object-oriented and modular set of solvers.
  2. Tools useful for carrying out experiments in fluid dynamics.

The docstring examples assume that `fluiddyn` has been imported as `fld`::

  >>> import fluiddyn as fld

Use the question mark in ipython to view a function's docstring::

  >>> fld.create_object_from_file?
  ... # doctest: +SKIP

"""

from fluiddyn.util.util import create_object_from_file
from fluiddyn.util import constants
from fluiddyn._version import __version__

__all__ = ['create_object_from_file', 'constants', '__version__']
