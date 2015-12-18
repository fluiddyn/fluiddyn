"""
Slurm clusters (:mod:`fluiddyn.clusters.slurm`)
===========================================

.. currentmodule:: fluiddyn.clusters.slurm

Provides:

.. autoclass:: ClusterSlurm
   :members:

"""

from __future__ import print_function

import os
import datetime
import stat
# Warning: subprocess32 should not be used on Windows
import sys
if sys.platform.startswith('win'):
    import subprocess
else:
    import subprocess32 as subprocess

from fluiddyn.util.query import run_asking_agreement


class ClusterSlurm(object):
    name_cluster = ''
    nb_cores_per_node = 32

    def __init__(self):

        # check if this script is run on a frontal with slurm installed
        try:
            subprocess.check_call(['sbatch', '--version'],
                                  stdout=subprocess.PIPE)
            slurm_installed = True
        except OSError:
            slurm_installed = False

        if not slurm_installed:
            raise ValueError(
                'This script should be run on a cluster with slurm installed.')

        self.commands_setting_env = [
            'source /etc/profile',
            'module swap PrgEnv-cray PrgEnv-gnu',
            'module load fftw anaconda/py27/2.3',
            'export CRAY_ROOTFS=DSL',
            'source $LOCAL_ANACONDA/bin/activate $LOCAL_ANACONDA',
            'export ANACONDA_HOME=$LOCAL_ANACONDA',
            'source activate_python']

        self.useful_commands = (
            'sbatch -J script.sh',
            'squeue -u',
            'scancel $SLURM_JOB_ID',
            'scontrol hold $SLURM_JOB_ID',
            'scontrol release $SLURM_JOB_ID')

        self.commands_unsetting_env = [
            'source deactivate_python']

    def submit_script(
            self, path, name_run='fluiddyn',
            nb_nodes=1, nb_cores_per_node=None,
            walltime='24:00:00', nb_mpi_processes=None,
            output='output_file.o',
            jobid=None, project='2014-11-24', requeue=False,
            nb_switches=None, max_waittime=None):
        """
        Parameters
        ----------
        path : string
            Path of the simulation script. Usually located at:
            $FLD/scripts/launch
        nb_nodes : integer
            Sets number of MPI processes = nb_nodes * nb_cores_per_node
        nb_cores_per_node : integer
            Defaults to a maximum is fixed for a cluster, as set by self.nb_cores_per_node.
            Set as 1 for a serial job
        walltime : string
            Maximum walltime for the job is fixed for a cluster, the default value
        nb_mpi_processes : integer
            Number of MPI processes, set automatically
        jobid : integer
            Run under already allocated job
        project : string
            Sets the allocation to run the job under
        requeue : boolean
            If set True, permit the job to be requeued.
        nb_switches : integer
            Max / Optimum switches
        max_waittime : string
            Max time to wait for optimum
        """

        if not os.path.exists(path):
            raise ValueError('script does not exists! path:\n' + path)

        if nb_cores_per_node is None:
            nb_cores_per_node = self.nb_cores_per_node
        elif nb_cores_per_node > self.nb_cores_per_node:
            raise ValueError('Too many cores...')

        if nb_mpi_processes is None:
            nb_mpi_processes = nb_cores_per_node * nb_nodes

        str_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path_launching_script = 'slurm_launcher_' + str_time
        if os.path.exists(path_launching_script):
            raise ValueError('path_launching_script already exists...')

        txt = self._create_txt_launching_script(
            path, name_run, project,
            nb_nodes, nb_cores_per_node, walltime,
            nb_mpi_processes, output)

        with open(path_launching_script, 'w') as f:
            f.write(txt)

        os.chmod(path_launching_script,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

        launching_command = 'sbatch'

        if jobid is not None:
            launching_command += ' --jobid=' + str(jobid)

        if requeue:
            launching_command += ' --requeue'

        if nb_switches is not None and max_waittime is not None:
            launching_command += ' --switches=' + str(nb_switches) + \
                                 '{@' + max_waittime + '}'

        launching_command += ' ./' + path_launching_script

        print('A launcher for the script {} has been created.'.format(path))
        run_asking_agreement(launching_command)

    def _create_txt_launching_script(
            self, path, name_run, project,
            nb_nodes, nb_cores_per_node, walltime,
            nb_mpi_processes, output):
        """
        Example
        -------
            #!/bin/bash -l
            # The -l above is required to get the full environment with modules

            # Set the allocation to be charged for this job
            # not required if you have set a default allocation
            #SBATCH -A 201X-X-XX

            # The name of the script is myjob
            #SBATCH -J myjob

            # Only 1 hour wall-clock time will be given to this job
            #SBATCH -t 1:00:00

            # Number of nodes
            #SBATCH -N 4
            # Number of MPI processes per node (the following is actually the default)
            #SBATCH --ntasks-per-node=32
            # Number of MPI processes.
            #SBATCH -n 128

            #SBATCH -e error_file.e
            #SBATCH -o output_file.o

            # Run the executable named myexe
            # and write the output into my_output_file
            aprun -n 128 ./myexe > my_output_file 2>&1
        """

        txt = ('#!/bin/bash -l\n\n')

        txt += '#SBATCH -J {}\n\n'.format(name_run)
        txt += '#SBATCH -A {}\n\n'.format(project)

        txt += "#SBATCH -t {}\n".format(walltime)
        txt += "#SBATCH -N {}\n".format(nb_nodes)
        txt += "#SBATCH --ntasks-per-node={}\n".format(nb_cores_per_node)
        txt += "#SBATCH -n {}\n\n".format(nb_mpi_processes)

        txt += '#SBATCH -e error_file.e\n'
        txt += '#SBATCH -o output_file.o\n\n'

        txt += 'echo "hostname: "$HOSTNAME\n\n'

        txt += '\n'.join(self.commands_setting_env) + '\n\n'

        if nb_mpi_processes > 1:
            txt += 'aprun -n {} '.format(nb_mpi_processes)

        txt += 'python {} > {} 2>&1\n\n'.format(path, output)

        txt += '\n'.join(self.commands_unsetting_env) + '\n\n'
        return txt
