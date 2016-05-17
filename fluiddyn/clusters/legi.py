"""
LEGI clusters (:mod:`fluiddyn.clusters.legi`)
=============================================

.. currentmodule:: fluiddyn.clusters.legi

Provides:

.. autoclass:: Calcul
   :members:

.. autoclass:: Calcul3
   :members:

.. autoclass:: Calcul9
   :members:

.. autoclass:: Calcul7
   :members:

"""

from fluiddyn.clusters.oar import ClusterOAR


class Calcul3(ClusterOAR):
    name_cluster = 'calcul3'
    has_to_add_name_cluster = True
    nb_cores_per_node = 12
    frontends = ['calcul8sv109', 'legilnx44']


class Calcul9(ClusterOAR):
    name_cluster = 'calcul9'
    has_to_add_name_cluster = True
    nb_cores_per_node = 8
    frontends = ['calcul8sv109', 'legilnx44']


class Calcul(ClusterOAR):
    name_cluster = 'calcul7-8'
    has_to_add_name_cluster = False
    nb_cores_per_node = 20
    frontends = ['nrj1sv223', 'nrj1sv224']

    def __init__(self):

        super(Calcul, self).__init__()

        self.commands_setting_env = [
            'source /etc/profile',
            'module load python/2.7.9',
            'source /home/users/$USER/opt/mypy2.7/bin/activate']


class Calcul7(Calcul):
    name_cluster = 'calcul7'
    has_to_add_name_cluster = True
    nb_cores_per_node = 16


class Calcul8(Calcul):
    name_cluster = 'calcul8'
    has_to_add_name_cluster = True
