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
    nb_cores_per_node = 16
    frontends = ['nrj1sv223']

    def __init__(self):

        super(Calcul7, self).__init__()

        self.commands_setting_env = [
            'source /etc/profile',
            'module load python/2.7.9',
            'source /home/users/$USER/useful'
            '/save/opt/mypy2.7.9_jessie/bin/activate']

    def _create_txt_launching_script(
            self, path, name_run,
            nb_nodes, nb_cores_per_node,
            walltime,
            nb_mpi_processes=None):

        if nb_mpi_processes is None:
            nb_mpi_processes = nb_cores_per_node

        txt = ('#!/bin/bash\n\n')

        txt += (
            '#OAR -n {}\n'
            "#OAR -l /nodes=1/core={},walltime={}\n\n").format(
                name_run, nb_cores_per_node, walltime)

        txt += 'echo "hostname: "$HOSTNAME\n\n'

        txt += '\n'.join(self.commands_setting_env) + '\n\n'

        if nb_mpi_processes > 1:
            txt += 'exec mpirun -np {} '.format(nb_mpi_processes)

        txt += 'python {}\n'.format(path)

        return txt
