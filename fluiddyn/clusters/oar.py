"""
OAR clusters (:mod:`fluiddyn.clusters.oar`)
===========================================

.. currentmodule:: fluiddyn.clusters.oar

Provides:

.. autoclass:: ClusterOAR
   :members:

"""

from __future__ import print_function

import os
import datetime
import stat
import subprocess

from fluiddyn.util.query import run_asking_agreement


class ClusterOAR(object):
    name_cluster = ''
    nb_cores_per_node = 12

    def __init__(self):

        # check if this script is run on a frontal with oar installed
        oar_installed = not subprocess.check_call(['oarsub', '--version'],
                                                  stdout=subprocess.PIPE)
        if not oar_installed:
            raise ValueError(
                'This script should be run on a cluster with oar installed.')

        self.commands_setting_env = [
            'source /etc/profile',
            'module load python/2.7.8',
            'source /home/users/$USER/useful'
            '/save/opt/mypysqueeze/bin/activate']

        self.useful_commands = (
            'oarsub -S script.sh',
            'oarstat -u',
            'oardel $JOB_ID'
            'oarsub -C $JOB_ID')

    def submit_script(self, path, name_run='fluiddyn',
                      nb_nodes=1,
                      nb_cores_per_node=1,
                      walltime='24:00:00',
                      nb_mpi_processes=None,
                      omp_num_threads=None,
                      idempotent=False):

        if not os.path.exists(path):
            raise ValueError('script does not exists! path:\n' + path)

        if nb_mpi_processes is None:
            nb_mpi_processes = nb_cores_per_node

            if nb_cores_per_node > self.nb_cores_per_node:
                raise ValueError('Too many cores...')

        str_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path_launching_script = 'oar_launcher_' + str_time
        if os.path.exists(path_launching_script):
            raise ValueError('path_launching_script already exists...')

        txt = self._create_txt_launching_script(
            path, name_run,
            nb_nodes, nb_cores_per_node, walltime,
            nb_mpi_processes=nb_mpi_processes)

        with open(path_launching_script, 'w') as f:
            f.write(txt)

        os.chmod(path_launching_script,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

        launching_command = 'oarsub --checkpoint 600'

        if idempotent:
            launching_command += ' -t idempotent'

        launching_command += ' -S ./' + path_launching_script

        print('A launcher for the script {} has been created.'.format(path))
        run_asking_agreement(launching_command)

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
            "#OAR -l {{cluster='{}'}}/node=1/core={},walltime={}\n\n").format(
                name_run, self.name_cluster, nb_cores_per_node, walltime)

        txt += 'echo "hostname: "$HOSTNAME\n\n'

        txt += '\n'.join(self.commands_setting_env) + '\n\n'

        if nb_mpi_processes > 1:
            txt += 'exec mpirun -np {} '.format(nb_mpi_processes)

        txt += 'python {}\n'.format(path)

        return txt