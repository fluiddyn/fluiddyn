"""
LEGI clusters (:mod:`fluiddyn.clusters.legi`)
===========================================

.. currentmodule:: fluiddyn.clusters.legi

Provides:

.. autoclass:: Calcul8
   :members:

"""

from fluiddyn.clusters.oar import ClusterOAR


class Calcul8(ClusterOAR):
    name_cluster = 'calcul3'
    nb_cores_per_node = 12
