"""
Local workstations as clusters (:mod:`fluiddyn.clusters.local`)
===============================================================

Provides:

.. autoclass:: ClusterLocal
   :members:

"""

import datetime
import os
import stat
from shlex import split
from socket import gethostname

import psutil

from ..io.query import call_bash, run_asking_agreement
from ..util.timer import TimeStr, timestamp_to_seconds
from . import Cluster, subprocess


def is_python_script(path):
    """Check whether path points to a file ending with .py extension."""
    return os.path.splitext(path)[1] == ".py"


class ClusterLocal(Cluster):
    """Works as a compatibility layer to execute submit scripts on local
    workstations as clusters with no job schedulers.

    Instead uses POSIX commands:

     - ``nohup`` and ``mpirun`` to launch jobs.
     - ``timeout`` to set walltime..

    """

    _doc_commands = "\n".join(
        [
            "Useful commands",
            "---------------",
            "pgrep -af python",
            "killall python",
            "nohup python -u launcher.py >launcher.stdout 2>launcher.stderr &",
            "top",
        ]
    )
    name_cluster = gethostname()
    nb_cores_per_node = psutil.cpu_count()
    cmd_run = "mpirun"
    cmd_launch = "nohup"
    max_walltime = "30-00:00:00"

    def __init__(self):
        self.commands_setting_env = []
        self.commands_unsetting_env = []
        virtualenv = os.getenv("VIRTUAL_ENV")
        if virtualenv is not None:
            self.commands_setting_env.append(
                "source " + virtualenv + "/bin/activate"
            )
            self.commands_unsetting_env.append("deactivate")

    def submit_script(self, path, *args, **kwargs):
        """Submit a script. See `submit_command` for all possible arguments"""
        path = os.path.expandvars(path)
        script = path.split()[0]
        if not os.path.exists(script):
            raise ValueError("Script does not exist! path:\n" + script)

        if is_python_script(script) and not path.startswith("python "):
            path = "python " + path

        self.submit_command(path, *args, **kwargs)

    def submit_command(
        self,
        command,
        name_run="fluiddyn",
        nb_nodes=1,
        nb_cores_per_node=None,
        walltime="23:59:58",
        nb_mpi_processes=None,
        retain_script=True,
        omp_num_threads=1,
        ask=True,
        bash=True,
        interactive=False,
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
        walltime : string
            Minimum walltime for the job
        nb_mpi_processes : None, integer or ``"auto"``
            Number of MPI processes. Defaults to None (no MPI).
            If ``"auto"``, computed as `nb_cores_per_node * nb_nodes`.
        omp_num_threads : integer
            Number of OpenMP threads
        ask : boolean
            Ask for user input to submit the jobscript or not
        bash : boolean
            Submit jobscript via `call_bash` function
        interactive : boolean
            When True do not use cmd_launch to execute.

        """
        nb_cores_per_node, nb_mpi_processes = self._parse_cores_procs(
            nb_nodes, nb_cores_per_node, nb_mpi_processes
        )

        path_launching_script = self._make_path_launching_script()
        self._check_walltime(walltime)

        create_txt_kwargs = locals()
        del create_txt_kwargs["self"]
        txt = self._create_txt_launching_script(**create_txt_kwargs)
        self._write_txt_launching_script(txt, path_launching_script)

        launching_command = " ./" + path_launching_script
        self._launch(launching_command, command, bash, ask)

        if not retain_script:
            os.remove(path_launching_script)

    def _make_path_launching_script(
        self, prefix="launcher", path_launching_script=None
    ):
        """Make a uniques path and name of the launching script from the current
        time.

        """
        if path_launching_script is None:
            str_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path_launching_script = prefix + "_" + str_time + ".sh"

        if os.path.exists(path_launching_script):
            i = 1
            while os.path.exists(path_launching_script + "_" + str(i)):
                i += 1
            path_launching_script += "_" + str(i)

        return path_launching_script

    def _check_walltime(self, walltime):
        """Check if walltime exceeds maximum walltime."""
        if walltime is None:
            return

        elif TimeStr(walltime) > self.max_walltime:
            raise ValueError(
                (
                    "Walltime requested {} exceeds permitted maximum walltime "
                    "{}"
                ).format(walltime, self.max_walltime)
            )

    def _launch(self, launching_command, command="", bash=True, ask=True):
        """Ask and launch the command using a subprocess call."""
        print(f"A launcher for the command {command} has been created.")

        if ask:
            run_asking_agreement(launching_command)
        else:
            print(
                "The script is submitted with the command:\n", launching_command
            )
            if bash:
                call_bash(launching_command)
            else:
                subprocess.call(split(launching_command))

    def _create_txt_launching_script(self, **kwargs):
        """Create the text for a script which launches the command."""
        path_launching_script = kwargs["path_launching_script"]
        command = kwargs["command"]
        name_run = kwargs["name_run"]
        nb_mpi_processes = kwargs["nb_mpi_processes"]
        walltime = kwargs["walltime"]
        omp_num_threads = kwargs["omp_num_threads"]
        interactive = kwargs["interactive"]

        logfile = f"LOCAL.{name_run}"
        logfile_stdout = logfile + ".$$.stdout"
        logfile_stderr = logfile + ".$$.stderr"

        txt = "#!/bin/bash -l\n\n"

        txt += 'echo "hostname: "$HOSTNAME\n\n'
        txt += self._log_job(
            nb_mpi_processes,
            path_launching_script,
            logfile_stdout,
            command,
            "LOCAL_JOB.md",
        )
        txt += "\n".join(self.commands_setting_env) + "\n\n"

        if omp_num_threads is not None:
            txt += f"export OMP_NUM_THREADS={omp_num_threads}\n\n"

        cmd = command
        if nb_mpi_processes is not None and nb_mpi_processes > 1:
            cmd = f"{self.cmd_run} -n {nb_mpi_processes} {cmd}"

        walltime_seconds = timestamp_to_seconds(walltime)
        cmd = f"timeout -s TERM {walltime_seconds}s {cmd}"

        if interactive:
            txt += cmd
        else:
            txt += "{} {} >{} 2>{} &".format(
                self.cmd_launch, cmd, logfile_stdout, logfile_stderr
            )

        txt += "\n" + "\n".join(self.commands_unsetting_env)
        return txt

    def _log_job(
        self,
        nb_cores,
        path_launching_script,
        logfile_stdout,
        command,
        logfile_job,
    ):
        """Generate a shell command to log the job into a markdown file."""
        return (
            "\n" + rf'printf "\n# np={nb_cores} `date` PID $$ '
            rf'{path_launching_script} {logfile_stdout}\n{command}" >> {logfile_job}'
            + "\n"
        )

    def _write_txt_launching_script(self, txt, path_launching_script):
        """Write the text into an executable script which launches the command."""
        with open(path_launching_script, "w") as f:
            f.write(txt)

        os.chmod(
            path_launching_script, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
        )
