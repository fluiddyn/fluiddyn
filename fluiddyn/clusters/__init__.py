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
   local
   legi
   ciment
   cines
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

class Cluster(object):
    _doc_commands = ''

    @classmethod
    def print_doc_commands(cls):
        print(cls._doc_commands)

