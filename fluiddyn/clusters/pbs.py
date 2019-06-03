"""
PBS clusters (:mod:`fluiddyn.clusters.pbs`)
===========================================

Provides:

.. autoclass:: ClusterPBS
   :members:

"""

import os

from . import subprocess
from .local import ClusterLocal


class ClusterPBS(ClusterLocal):
    """Base class for clusters with PBS job scheduler."""

    _doc_commands = """
Useful commands
---------------

qsub
qstat -u $USER
qdel
qhold
qrls"""
    name_cluster = ""
    nb_cores_per_node = 32
    default_project = None
    cmd_run = "mpirun"
    cmd_launch = "qsub"
    max_walltime = "23:59:59"

    def __init__(self):
        self.check_pbs()
        self.commands_setting_env = ["cd $PBS_O_WORKDIR"]
        self.commands_unsetting_env = []

    def check_pbs(self):
        """Check if this script is run on a frontal with pbs installed."""
        try:
            subprocess.check_call(["qsub", "--version"], stdout=subprocess.PIPE)
        except OSError:
            raise ValueError(
                "This script should be run on a cluster with PBS installed."
            )

    def check_name_cluster(self, env="HOSTNAME"):
        """Check if self.name_cluster matches the environment variable."""

        if self.name_cluster not in os.getenv(env):
            raise ValueError(
                "Cluster name mismatch detected; expected " + self.name_cluster
            )

    def submit_command(
        self,
        command,
        name_run="fluiddyn",
        nb_nodes=1,
        nb_cores_per_node=None,
        walltime=None,
        project=None,
        queue=None,
        nb_mpi_processes=None,
        omp_num_threads=1,
        nb_runs=1,
        path_launching_script=None,
        path_resume=None,
        retain_script=True,
        ask=True,
        bash=True,
        email=None,
        interactive=False,
        **kwargs,
    ):
        """Submit a command.

        Parameters
        ----------
        command : string
            Command which executes the run
        name_run : string
            Name of the run to be displayed in PBS queue
        nb_nodes : integer
            Sets number of MPI processes = nb_nodes * nb_cores_per_node
        nb_cores_per_node : integer
            Defaults to a maximum is fixed for a cluster, as set by self.nb_cores_per_node.
            Set as 1 for a serial job. Set as 0 to spread jobs across nodes
            (starts job faster, maybe slower).
        walltime : string
            Minimum walltime for the job
        project : string
            Sets the allocation to run the job under
        queue: string
            Sets the cluster queue to run the job on
        nb_mpi_processes : integer
            Number of MPI processes. Defaults to a `nb_cores_per_node * nb_nodes`.
        omp_num_threads : integer
            Number of OpenMP threads
        nb_runs : integer
            Number of times to submit jobs (launch once using `command` and
            resume thereafter with `path_resume` script / command).
        path_launching_script: string
            Path of the PBS jobscript
        path_resume : string
            Path of the script to resume a job, which takes one
            argument - the `path_run` parsed from the output.
        retain_script : boolean
            Retail or delete script after launching job
        ask : boolean
            Ask for user input to submit the jobscript or not
        bash : boolean
            Submit jobscript via `call_bash` function
        email : string
            In case of failure notify to the specified email address
        interactive : boolean
            Use `cmd_run_interactive` instead of `cmd_run` inside the jobscript
        """
        nb_cores_per_node, nb_mpi_processes = self._parse_cores_procs(
            nb_nodes, nb_cores_per_node, nb_mpi_processes
        )

        path_launching_script = self._make_path_launching_script()

        self._check_walltime(walltime)

        is_resume_script = bool("resumer" in path_launching_script)
        if project is None:
            project = self.default_project

        launching_command = self.cmd_launch

        if is_resume_script:
            dependencies = input("Enter jobid dependencies :").split()
            launching_command += " -W depend=afternotok:" + ":".join(dependencies)
        else:
            dependencies = None

        create_txt_kwargs = locals()
        del create_txt_kwargs["self"]
        txt = self._create_txt_launching_script(**create_txt_kwargs)
        self._write_txt_launching_script(txt, path_launching_script)
        launching_command += " ./" + path_launching_script
        self._launch(launching_command, command, bash, ask)

        if not retain_script:
            os.remove(path_launching_script)

        nb_times_resume = int(nb_runs) - 1
        for n in range(0, nb_times_resume):
            nb_runs = 1
            path = path_resume
            path_launching_script = self._make_path_launching_script("resumer")
            submit_script_kwargs = locals()
            del submit_script_kwargs["self"]
            del submit_script_kwargs["command"]
            self.submit_script(**submit_script_kwargs)

    def _create_txt_launching_script(self, **kwargs):
        """
        Examples
        --------

            #!/bin/bash -l
            # The -l above is required to get the full environment with modules

            # The name of the script is myjob
            #PBS -N myjob

            # Set the allocation to be charged for this job
            # not required if you have set a default allocation
            #PBS -A 201X-X-XX

            # Set the queue to launch this job on
            #PBS -q queuename

            # Only 1 hour wall-clock time will be given to this job
            #PBS -l walltime=1:00:00

            # Number of nodes and processes per node
            #PBS -l nodes=1:ppn=32

            #PBS -e $PBS.myjob.$PBS_JOBID.stderr
            #PBS -o $PBS.myjob.$PBS_JOBID.stdout

            # Run the executable named myexe
            mpirun -n 128 ./myexe
        """
        path_launching_script = kwargs["path_launching_script"]
        command = kwargs["command"]
        name_run = kwargs["name_run"]
        project = kwargs["project"]
        queue = kwargs["queue"]
        nb_nodes = kwargs["nb_nodes"]
        nb_cores_per_node = kwargs["nb_cores_per_node"]
        walltime = kwargs["walltime"]
        nb_mpi_processes = kwargs["nb_mpi_processes"]
        omp_num_threads = kwargs["omp_num_threads"]
        dependencies = kwargs["dependencies"]
        email = kwargs["email"]
        is_resume_script = kwargs["is_resume_script"]

        logfile = f"PBS.{name_run}"
        logfile_stdout = logfile + ".${PBS_JOBID}.stdout"

        txt = "#!/bin/bash -l\n\n"

        txt += f"#PBS -N {name_run}\n\n"
        if project is not None:
            txt += f"#PBS -A {project}\n\n"

        if queue is not None:
            txt += f"#PBS -q {queue}\n\n"

        if walltime is not None:
            txt += f"#PBS -l walltime={walltime}\n"

        txt += f"#PBS -l nodes={nb_nodes}:ppn={nb_cores_per_node}\n"

        if email is not None:
            txt += "#PBS -m a\n"
            txt += f"#PBS -M {email}\n"

        txt += f"#PBS -e {logfile}.%J.stderr\n"
        txt += f"#PBS -o {logfile}.%J.stdout\n\n"

        txt += 'echo "hostname: "$HOSTNAME\n\n'
        txt += self._log_job(
            nb_mpi_processes,
            path_launching_script,
            logfile_stdout,
            command,
            "PBS_JOB.md",
        )

        txt += "\n".join(self.commands_setting_env) + "\n\n"

        if omp_num_threads is not None:
            txt += f"export OMP_NUM_THREADS={omp_num_threads}\n\n"

        if is_resume_script:
            jobid = dependencies[0]
            main_logfile = f"PBS.{name_run}.{jobid}.stdout"
            txt += "PATH_RUN=$(sed -n '/path_run/{n;p;q}' " + "{}\n".format(
                main_logfile
            )

        cmd = self.cmd_run

        if nb_mpi_processes > 1:
            txt += f"{cmd} -n {nb_mpi_processes} "

        if is_resume_script:
            txt += f"{command} $PATH_RUN"
        else:
            txt += command

        txt += "\n" + "\n".join(self.commands_unsetting_env)
        return txt
