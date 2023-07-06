"""
Slurm clusters (:mod:`fluiddyn.clusters.slurm`)
===============================================

Provides:

.. autoclass:: ClusterSlurm
   :members:

"""

import os
import subprocess
import sys
from subprocess import PIPE
from warnings import warn

from .local import ClusterLocal


class ClusterSlurm(ClusterLocal):
    """Base class for clusters with SLURM job scheduler."""

    _doc_commands = """
Useful commands
---------------

sbatch
squeue -u $USER
squeue --format="%.12i %.9P %.25j %.8u %.8T %.10M %.6D %R" -u $USER
scancel
scontrol hold
scontrol release
scontrol show <jobid>
scontrol update jobid=<jobid> TimeLimit=1-00:00:00"""
    name_cluster = ""  #: Name of cluster used in :meth:`check_name_cluster`
    nb_cores_per_node = 32  #: Number of cores per node
    default_project = None  #: Default project allocation
    cmd_run = "srun"  #: Command to launch executable
    cmd_run_interactive = None  #: Interactive command to launch exectuable
    cmd_launch = "sbatch"  #: Command to submit job script
    max_walltime = "23:59:59"  #: Maximum walltime allowed per job
    partition = None  #: Partition on the cluster
    dependency = None  #: Dependency option
    mem = None  #: Minimum amount of real memory allocation for the job
    account = None  #: Name of the project for jobs' submission (mandatory on some clusters)
    exclusive = False  #: Reserve nodes when submitting jobs

    def __init__(self):
        self.check_slurm()
        self.commands_setting_env = []
        self.commands_unsetting_env = []

    def check_slurm(self):
        """Check if this script is run on a frontal with slurm installed."""
        try:
            subprocess.check_call(["sbatch", "--version"], stdout=PIPE)
            slurm_installed = True
        except OSError:
            slurm_installed = False

        if not slurm_installed:
            raise ValueError(
                "This script should be run on a cluster with slurm installed."
            )

    def check_name_cluster(self, env="HOSTNAME"):
        """Check if :attr:`name_cluster` matches the environment variable."""

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
        nb_tasks=None,
        nb_tasks_per_node=None,
        nb_cpus_per_task=None,
        walltime="23:59:58",
        project=None,
        nb_mpi_processes=None,
        omp_num_threads=1,
        nb_runs=1,
        path_launching_script=None,
        path_resume=None,
        retain_script=True,
        jobid=None,
        requeue=False,
        nb_switches=None,
        max_waittime=None,
        ask=True,
        bash=True,
        email=None,
        interactive=False,
        signal_num=12,
        signal_time=300,
        flexible_walltime=False,
        partition=None,
        dependency=None,
        mem=None,
        account=None,
        exclusive=exclusive,
        **kwargs,
    ):
        """Submit a command.

        Parameters
        ----------
        command : string
            Command which executes the run
        name_run : string
            Name of the run to be displayed in SLURM queue
        nb_nodes : integer
            Number of nodes
        nb_cores_per_node : integer
            Defaults to a maximum is fixed for a cluster, as set by self.nb_cores_per_node.
            Set as 1 for a serial job. Set as 0 to spread jobs across nodes
            (starts job faster, maybe slower).
        nb_tasks : integer
            Number of tasks. If not specified, computed as `nb_nodes * nb_cores_per_node`.
        nb_tasks_per_node : integer
            Number of tasks per node. If not specified, computed as `nb_cores_per_node`.
        nb_cpus_per_task : integer
            Number of cpus requested per task. Only set if the --cpus-per-task option is specified.
        walltime : string
            Minimum walltime for the job
        project : string
            Sets the allocation to run the job under
        nb_mpi_processes : integer
            Number of MPI processes. Defaults to None (no MPI).
            If ``"auto"``, computed as `nb_cores_per_node * nb_nodes`.
        omp_num_threads : integer
            Number of OpenMP threads
        nb_runs : integer
            Number of times to submit jobs (launch once using ``command`` and
            resume thereafter with ``path_resume`` script / command).
        path_launching_script: string
            Path of the SLURM jobscript
        path_resume : string
            Path of the script to resume a job, which takes one
            argument - the ``path_run`` parsed from the output.
        retain_script : boolean
            Retail or delete script after launching job
        jobid : integer
            Run under already allocated job
        requeue : boolean
            If set True, permit the job to be requeued.
        nb_switches : integer
            Max / Optimum switches
        max_waittime : string
            Max time to wait for optimum
        ask : boolean
            Ask for user input to submit the jobscript or not
        bash : boolean
            Submit jobscript via :func:`fluiddyn.io.query.call_bash` function
        email : string
            In case of failure notify to the specified email address
        interactive : boolean
            Use :attr:`cmd_run_interactive` instead of :attr:`cmd_run` inside the jobscript
        signal_num : int or False
        signal_time : int
            Send the signal ``signal_num`` `signal_time`` seconds before the end of the job.
        flexible_walltime : bool
            If true, submit a job as::

                sbatch --time-min=<walltime> --time=<max_walltime> ...

            where ``walltime`` is a parameter of this method and
            :attr:`max_walltime` is a class attribute. This would allow SLURM
            to provide an optimum walltime in the range requested.

            Note that if ``signal_num`` is provided ``flexible_walltime`` is
            not practical and will be forced to be `False`.
        partition: str
            Request a specific partition for the resource allocation. Default None.
        dependency: str
            Job dependencies are used to defer the start of a job until the
            specified dependencies have been satisfied. They are specified with
            the --dependency option to sbatch
        mem: str
            Minimum amount of real memory allocation for the job
        account: str
            Name of the project to which hours are allocated
        exclusive: boolean
            Reserve nodes when submitting jobs

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

        if jobid is not None:
            launching_command += " --jobid=" + str(jobid)

        if requeue:
            launching_command += " --requeue"

        if flexible_walltime and signal_num:
            warn(
                f"Parameter flexible_walltime={flexible_walltime} is not "
                f"possible when signal_num={signal_num} is set. Forcing "
                "flexible_walltime = False"
            )
            flexible_walltime = False

        if is_resume_script:
            dependencies = input("Enter jobid dependencies :").split()
            launching_command += " --dependency=afternotok:" + ":".join(
                dependencies
            )
        else:
            dependencies = None

        if nb_switches is not None and max_waittime is not None:
            launching_command += (
                " --switches=" + str(nb_switches) + "{@" + max_waittime + "}"
            )

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
            jobid = None
            requeue = False
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
        path_launching_script = kwargs["path_launching_script"]
        command = kwargs["command"]
        name_run = kwargs["name_run"]
        project = kwargs["project"]
        nb_nodes = kwargs["nb_nodes"]
        nb_cores_per_node = kwargs["nb_cores_per_node"]
        nb_tasks = kwargs["nb_tasks"]
        nb_tasks_per_node = kwargs["nb_tasks_per_node"]
        nb_cpus_per_task = kwargs["nb_cpus_per_task"]
        walltime = kwargs["walltime"]
        nb_mpi_processes = kwargs["nb_mpi_processes"]
        omp_num_threads = kwargs["omp_num_threads"]
        dependencies = kwargs["dependencies"]
        email = kwargs["email"]
        interactive = kwargs["interactive"]
        is_resume_script = kwargs["is_resume_script"]
        signal_num = kwargs["signal_num"]
        signal_time = kwargs["signal_time"]
        flexible_walltime = kwargs["flexible_walltime"]
        partition = kwargs["partition"] or self.partition
        dependency = kwargs["dependency"]
        mem = kwargs["mem"]
        account = kwargs["account"]
        exclusive = kwargs["exclusive"] or self.exclusive

        logfile = f"SLURM.{name_run}"
        logfile_stdout = logfile + ".${SLURM_JOBID}.stdout"

        txt = "#!/bin/bash -l\n\n"

        txt += f"#SBATCH -J {name_run}\n\n"
        if project is not None:
            txt += f"#SBATCH -A {project}\n\n"

        if flexible_walltime:
            time = self.max_walltime
        else:
            time = walltime

        txt += f"#SBATCH --time={time}\n"
        txt += f"#SBATCH --time-min={walltime}\n"
        if signal_num:
            txt += f"#SBATCH --signal={signal_num}@{signal_time}\n"

        txt += f"#SBATCH --nodes={nb_nodes}\n"
        if nb_tasks_per_node is not None:
            txt += f"#SBATCH --ntasks-per-node={nb_tasks_per_node}\n"
        else:
            if nb_cores_per_node > 0:
                txt += f"#SBATCH --ntasks-per-node={nb_cores_per_node}\n"

        nb_cores = nb_nodes * nb_cores_per_node
        if nb_tasks is not None:
            txt += f"#SBATCH --ntasks={nb_tasks}\n\n"
        else:
            txt += f"#SBATCH --ntasks={nb_cores}\n\n"

        if nb_cpus_per_task is not None:
            txt += f"#SBATCH --cpus-per-task={nb_cpus_per_task}\n"

        if hasattr(self, "constraint"):
            txt += "#SBATCH --constraint=" + self.constraint + "\n"

        if email is not None:
            txt += "#SBATCH --mail-type=FAIL\n"
            txt += f"#SBATCH --mail-user={email}\n"

        txt += f"#SBATCH -e {logfile}.%J.stderr\n"
        txt += f"#SBATCH -o {logfile}.%J.stdout\n\n"

        if partition is not None:
            txt += f"#SBATCH -p {partition}\n"

        if dependency is not None:
            txt += f"#SBATCH --dependency={dependency}\n"

        if mem is not None:
            txt += f"#SBATCH --mem={mem}\n"

        if account is not None:
            txt += f"#SBATCH --account={account}\n"

        if exclusive == True:
            txt += f"#SBATCH --exclusive\n"

        txt += "\n".join(self.commands_setting_env) + "\n\n"

        txt += 'echo "hostname: "$HOSTNAME\n\n'
        txt += self._log_job(
            nb_cores,
            path_launching_script,
            logfile_stdout,
            command,
            "SLURM_JOB.md",
        )

        if omp_num_threads is not None:
            txt += f"export OMP_NUM_THREADS={omp_num_threads}\n\n"

        if is_resume_script:
            jobid = dependencies[0]
            main_logfile = f"SLURM.{name_run}.{jobid}.stdout"
            txt += "PATH_RUN=$(sed -n '/path_run/{n;p;q}' " + "{})\n".format(
                main_logfile
            )

        if interactive:
            cmd = self.cmd_run_interactive
        else:
            cmd = self.cmd_run

        if nb_mpi_processes is not None and nb_mpi_processes > 1:
            txt += f"{cmd} -n {nb_mpi_processes} "

        if is_resume_script:
            txt += f"{command} $PATH_RUN"
        else:
            txt += command

        if interactive:
            txt += f" > {logfile_stdout} 2>&1"

        txt += "\n" + "\n".join(self.commands_unsetting_env)
        return txt

    def launch_more_dependant_jobs(
        self, job_id, nb_jobs_added, path_launcher=None, job_status="afterok"
    ):
        """Launch dependant jobs using ``sbatch --dependency=...`` command.

        .. seealso:: https://slurm.schedmd.com/sbatch.html

        Parameters
        ----------
        job_id: int
            First running job id to depend on.
        nb_jobs_added: int
            Total number of dependent jobs to be added.
        path_launcher: str
            Path to launcher script
        job_status: str
            Job status of preceding job. Typical values are `afterok, afternotok, afterany`.

        """

        if path_launcher is None:
            process = subprocess.run(
                f"scontrol show job {job_id}".split(),
                text=True,
                stdout=PIPE,
                stderr=PIPE,
            )
            if process.returncode:
                print(process.stdout, process.stderr, sep="\n")
                print("exit because previous command failed")
                sys.exit(process.returncode)
            path_launcher = None
            work_dir = None
            for line in process.stdout.split("\n"):
                line = line.strip()
                if line.startswith("Command="):
                    path_launcher = line[len("Command=") :].strip()
                if line.startswith("WorkDir="):
                    work_dir = line[len("WorkDir=") :].strip()

        assert path_launcher is not None

        if path_launcher.startswith("./"):
            path_launcher = work_dir + path_launcher[1:]

        for i in range(nb_jobs_added):
            print(
                f"submitting job {i+1}/{nb_jobs_added} dependent of job {job_id}",
                end="",
            )
            process = subprocess.run(
                f"sbatch --dependency={job_status}:{job_id} {path_launcher}".split(),
                text=True,
                stdout=PIPE,
                stderr=PIPE,
            )
            if process.returncode:
                print(process.stdout, process.stderr, sep="\n")
                print("\nexit because previous command failed")
                sys.exit(process.returncode)
            job_id = process.stdout.split()[-1].strip()
            print(f" (job_id: {job_id})")

        print(f"Successfully submitted {nb_jobs_added} chained jobs")
