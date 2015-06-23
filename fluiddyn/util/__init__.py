"""
Utilities (:mod:`fluiddyn.util`)
================================

.. currentmodule:: fluiddyn.util

.. autosummary::
   :toctree:

   util
   paramcontainer
   constants
   query
   timer
   deamons
   operator
   logger

"""

from fluiddyn.util.util import (
    Params, load_exp, decimate,
    FunctionLinInterp, gradient_colors, time_as_str
)
