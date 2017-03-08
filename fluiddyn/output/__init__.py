"""
Scientific output toolkit
=========================

.. _output:
.. currentmodule:: fluiddyn.output

.. autosummary::
   :toctree:

   figs
   rcparams
   util
   colorchart

"""

# temporary to avoid the error where matplotlib is not installed
try:
    from fluiddyn.output.figs import show
    import fluiddyn
    fluiddyn.show = show
except ImportError:
    pass
