"""
Slurm clusters (:mod:`fluiddyn.clusters.slurm`)
===============================================

Provides:

.. autoclass:: ClusterSlurm
   :members:

"""

from __future__ import print_function

from builtins import input
from builtins import str
from builtins import range
from builtins import object
import os
import datetime
import stat

from . import subprocess
from ..util.query import run_asking_agreement, call_bash
from ..util.timer import time_gteq


class ClusterSlurm(object):
    name_cluster = ''
    nb_cores_per_node = 32
    default_project = None
    cmd_run = 'srun'
    cmd_run_interactive = None
    cmd_launch = 'sbatch'
    max_walltime = '23:59:59'

    def __init__(self):
        self.check_slurm()
        self.commands_setting_env = []
        self.useful_commands = (
            'sbatch',
            'squeue -u $USER',
            'scancel',
            'scontrol hold',
            'scontrol release')
        self.commands_unsetting_env = []

    def check_slurm(self):
        """Check if this script is run on a frontal with slurm installed."""
        try:
            subprocess.check_call(['sbatch', '--version'],
                                  stdout=subprocess.PIPE)
            slurm_installed = True
        except OSError:
            slurm_installed = False

        if not slurm_installed:
            raise ValueError(
                'This script should be run on a cluster with slurm installed.')

    def check_name_cluster(self, env='HOSTNAME'):
        if self.name_cluster not in os.getenv(env):
            raise ValueError('Cluster name mismatch detected; expected ' + self.name_cluster)

    def submit_script(self, path, path_resume=None, name_run='fluiddyn',
                      path_launching_script=None, retain_script=True,
                      nb_nodes=1, nb_cores_per_node=None, nb_mpi_processes=None,
                      walltime='23:59:58', nb_runs=1,
                      jobid=None, project=None, requeue=False,
                      nb_switches=None, max_waittime=None,
                      ask=True, bash=True, email=None, interactive=False):
        """
        Parameters
        ----------
        path : string
            Path of the simulation script. Usually located at:
            $FLS/scripts/launch
        path_launching_script: string
            Path of the slurm jobscript
        nb_nodes : integer
            Sets number of MPI processes = nb_nodes * nb_cores_per_node
        nb_cores_per_node : integer
            Defaults to a maximum is fixed for a cluster, as set by self.nb_cores_per_node.
            Set as 1 for a serial job. Set as 0 to spread jobs across nodes
            (starts job faster, maybe slower).
        nb_mpi_processes : integer
            Number of MPI processes, set automatically
        walltime : string
            Minimum walltime for the job
        output : string
            Name of file to store standard output
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

        path = os.path.expandvars(path)
        script = path.split()[0]
        if not os.path.exists(script):
            raise ValueError('Script does not exist! path:\n' + script)

        if nb_cores_per_node is None:
            nb_cores_per_node = self.nb_cores_per_node
        elif nb_cores_per_node > self.nb_cores_per_node:
            raise ValueError('Too many cores...')

        if nb_mpi_processes is None:
            if nb_cores_per_node == 0:
                nb_mpi_processes = 1
            else:
                nb_mpi_processes = nb_cores_per_node * nb_nodes

        str_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        if path_launching_script is None:
            path_launching_script = 'launcher_' + str_time + '.sh'

        if os.path.exists(path_launching_script):
            i = 1
            while os.path.exists(path_launching_script + '_' + str(i)):
                i += 1
            path_launching_script += '_' + str(i)

        resume = bool('resumer' in path_launching_script)

        if time_gteq(walltime, self.max_walltime):
            raise ValueError(
                ('Walltime requested {} exceeds permitted maximum walltime '
                 '{}').format(walltime, self.max_walltime))

        if project is None:
            project = self.default_project

        launching_command = self.cmd_launch

        if jobid is not None:
            launching_command += ' --jobid=' + str(jobid)

        if requeue:
            launching_command += ' --requeue'

        if resume:
            dependencies = input('Enter jobid dependencies :').split()
            launching_command += ' --dependency=afternotok:' + ':'.join(dependencies)
        else:
            dependencies = None

        if nb_switches is not None and max_waittime is not None:
            launching_command += ' --switches=' + str(nb_switches) + \
                                 '{@' + max_waittime + '}'

        txt = self._create_txt_launching_script(
            path_launching_script, path, name_run, project, nb_nodes,
            nb_cores_per_node, walltime, nb_mpi_processes, dependencies,
            email, interactive, resume)

        with open(path_launching_script, 'w') as f:
            f.write(txt)

        os.chmod(path_launching_script,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        launching_command += ' ./' + path_launching_script

        print('A launcher for the script {} has been created.'.format(path))
        if ask:
            run_asking_agreement(launching_command)
        else:
            print('The script is submitted with the command:\n',
                  launching_command)
            if bash:
                call_bash(launching_command)
            else:
                subprocess.call(launching_command.split())
        
        if not retain_script:
            os.remove(path_launching_script)

        nb_times_resume = int(nb_runs) - 1
        for n in range(0, nb_times_resume):
            nb_runs = 1
            jobid = None
            requeue = False
            path = path_resume
            path_launching_script = 'resumer_' + str_time + '_' + str(n) + '.sh'
            self.submit_script(
                path, None, name_run, path_launching_script, retain_script,
                nb_nodes, nb_cores_per_node, nb_mpi_processes,
                walltime, nb_runs, jobid, project,
                requeue, nb_switches, max_waittime,
                ask, bash, email, interactive)

    def _create_txt_launching_script(
            self, path_launching_script, path, name_run, project, nb_nodes,
            nb_cores_per_node, walltime, nb_mpi_processes, dependencies,
            email, interactive, resume_script):
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
            srun -n 128 ./myexe
        """

        logfile = 'SLURM.{}'.format(name_run)
        logfile_stdout = logfile + '.${SLURM_JOBID}.stdout'
        logfile_stderr = logfile + '.${SLURM_JOBID}.stderr'

        txt = ('#!/bin/bash -l\n\n')

        txt += '#SBATCH -J {}\n\n'.format(name_run)
        if project is not None:
            txt += '#SBATCH -A {}\n\n'.format(project)

        txt += "#SBATCH --time={}\n".format(self.max_walltime)
        txt += "#SBATCH --time-min={}\n".format(walltime)
        txt += "#SBATCH --nodes={}\n".format(nb_nodes)
        if nb_cores_per_node > 0:
            txt += "#SBATCH --ntasks-per-node={}\n".format(nb_cores_per_node)

        txt += "#SBATCH --ntasks={}\n\n".format(nb_mpi_processes)

        if email is not None:
            txt += '#SBATCH --mail-type=FAIL\n'
            txt += '#SBATCH --mail-user={}\n'.format(email)

        txt += '#SBATCH -e {}.%J.stderr\n'.format(logfile_stderr)
        txt += '#SBATCH -o {}.%J.stdout\n\n'.format(logfile_stdout)

        txt += 'echo "hostname: "$HOSTNAME\n\n'
        txt += (
            r'printf "\n`date` JOBID $SLURM_JOBID {} {}\n{}"' +
            ' >> SLURM_JOB.log\n\n').format(path_launching_script, logfile_stdout, path)

        txt += '\n'.join(self.commands_setting_env) + '\n\n'

        if resume_script:
            jobid = dependencies[0]
            main_logfile = 'SLURM.{}.{}.stdout'.format(name_run, jobid)
            txt += "PATH_RUN=$(sed -n '/path_run/{n;p;q}' " + "{}\n".format(main_logfile)

        if interactive:
            cmd = self.cmd_run_interactive
        else:
            cmd = self.cmd_run

        if nb_mpi_processes > 1:
            txt += '{} -n {} '.format(cmd, nb_mpi_processes)

        if resume_script:
            txt += 'python {} $PATH_RUN'.format(path)
        else:
            txt += 'python {}'.format(path)

        if interactive:
            txt += ' > {} 2>&1'.format(logfile_stdout)

        txt += '\n' + '\n'.join(self.commands_unsetting_env)
        return txt
