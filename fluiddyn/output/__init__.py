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
    import fluiddyn
    from fluiddyn.output.figs import show
    from fluiddyn.output.rcparams import set_rcparams
    from fluiddyn.output.util import gradient_colors

    fluiddyn.show = show
except ImportError:
    pass

__all__ = ["show", "set_rcparams", "gradient_colors"]
