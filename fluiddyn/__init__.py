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

from .util.util import (
    create_object_from_file,
    time_as_str,
    get_memory_usage,
    ipydebug,
)
from .util import constants
from ._version import __version__

__citation__ = """
@article{fluiddyn,
doi = {10.5334/jors.237},
year = {2019},
publisher = {Ubiquity Press,  Ltd.},
volume = {7},
author = {Pierre Augier and Ashwin Vishnu Mohanan and Cyrille Bonamy},
title = {{FluidDyn}: A Python Open-Source Framework for Research and Teaching in Fluid Dynamics
    by Simulations,  Experiments and Data Processing},
journal = {Journal of Open Research Software}
}
"""


__all__ = [
    "__version__",
    "constants",
    "create_object_from_file",
    "time_as_str",
    "get_memory_usage",
    "ipydebug",
    "__citation__",
]
