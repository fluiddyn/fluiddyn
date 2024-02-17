"""
LEGI clusters (:mod:`fluiddyn.clusters.legi`)
=============================================

Provides:

.. autoclass:: Calcul
   :members:

.. autoclass:: Calcul7
   :members:

.. autoclass:: Calcul8
   :members:

.. autoclass:: Calcul2
   :members:

"""

import time
from subprocess import check_output

from fluiddyn.clusters.oar import ClusterOAR


class Calcul3(ClusterOAR):
    name_cluster = "calcul3"
    has_to_add_name_cluster = True
    nb_cores_per_node = 12
    frontends = ["calcul8sv109", "legilnx44"]


class Calcul9(ClusterOAR):
    name_cluster = "calcul9"
    has_to_add_name_cluster = True
    nb_cores_per_node = 8
    frontends = ["calcul8sv109", "legilnx44"]


class Calcul(ClusterOAR):
    name_cluster = "calcul7-8"
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
