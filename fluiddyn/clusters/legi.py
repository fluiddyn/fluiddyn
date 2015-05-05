"""
LEGI clusters (:mod:`fluiddyn.clusters.legi`)
===========================================

.. currentmodule:: fluiddyn.clusters.legi

Provides:

.. autoclass:: Calcul8
   :members:

"""

from fluiddyn.clusters.oar import ClusterOAR


class Calcul3(ClusterOAR):
    name_cluster = 'calcul3'
    nb_cores_per_node = 12
    frontends = ['calcul8sv109', 'legilnx44']


class Calcul9(ClusterOAR):
    name_cluster = 'calcul9'
    nb_cores_per_node = 8
    frontends = ['calcul8sv109', 'legilnx44']


class Calcul7(ClusterOAR):
    name_cluster = 'calcul7'
    nb_cores_per_node = 32
    frontends = ['nrj1sv223']
