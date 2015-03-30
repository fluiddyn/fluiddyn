"""
Utilities (:mod:`fluiddyn.util`)
================================

.. currentmodule:: fluiddyn.util

.. autosummary::
   :toctree:

   util
   containerxml
   constants
   query
   timer
   deamons
   operator

"""

from fluiddyn.util.util import (
    Params, load_exp, decimate,
    FunctionLinInterp, gradient_colors, time_as_str
)
