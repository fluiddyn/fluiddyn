"""
LEGI clusters
=============

Provides:

.. autoclass:: Calcul
   :members:

.. autoclass:: Calcul7
   :members:

.. autoclass:: Calcul8
   :members:

.. autoclass:: Calcul2
   :members:

.. autoclass:: Calcul6
   :members:

"""

from fluiddyn.clusters.oar import ClusterOAR


class GPU9(ClusterOAR):
    name_cluster = "gpu9"
    has_to_add_name_cluster = True
    nb_cores_per_node = 28
    frontends = ["nrj1sv223", "nrj1sv224", "meige4sv14"]


class Calcul(ClusterOAR):
    name_cluster = "calcul7-8-2-6"
    has_to_add_name_cluster = False
    nb_cores_per_node = 20
    frontends = ["nrj1sv223", "nrj1sv224", "meige4sv14"]


class Calcul7(Calcul):
    name_cluster = "calcul7"
    has_to_add_name_cluster = True
    nb_cores_per_node = 16


class Calcul8(Calcul):
    name_cluster = "calcul8"
    has_to_add_name_cluster = True


class Calcul2(Calcul):
    name_cluster = "calcul2"
    has_to_add_name_cluster = True


class Calcul6(Calcul):
    name_cluster = "calcul6"
    has_to_add_name_cluster = True
    nb_cores_per_node = 32
