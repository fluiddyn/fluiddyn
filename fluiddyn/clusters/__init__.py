"""
Clusters
========

.. _clusters:
.. currentmodule:: fluiddyn.clusters

Provides:

.. autosummary::
   :toctree:

   oar
   slurm
   legi
   ciment
   snic

"""

# Warning: subprocess32 should not be used on Windows
import sys
if sys.platform.startswith('win'):
    import subprocess
else:
    try:
        import subprocess32 as subprocess
    except ImportError:
        import subprocess
