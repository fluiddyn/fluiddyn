"""
Scientific output toolkit
=========================

.. _output:
.. currentmodule:: fluiddyn.output

.. autosummary::
   :toctree:

   figs
   movies
   latextables

"""

# temporary to avoid the error where matplotlib is not installed
try:
    from fluiddyn.output.figs import show
except ImportError:
    pass

