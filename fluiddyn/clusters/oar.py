"""
OAR clusters (:mod:`fluiddyn.clusters.oar`)
===========================================

Provides:

.. autoclass:: ClusterOAR
   :members:

"""

from __future__ import print_function

from builtins import str

import os
import datetime
import stat
from sys import version_info as version

from . import subprocess, Cluster
from ..io.query import run_asking_agreement, call_bash


class ClusterOAR(Cluster):
    name_cluster = ""
    nb_cores_per_node = 12
    has_to_add_name_cluster = False

    _doc_commands = (
        """
Useful commands
---------------
oarsub -S script.sh
oarstat -u
oardel $JOB_ID
oarsub -C $JOB_ID"""
    )

    def __init__(self):
        self.commands_setting_env = [
            "source /etc/profile",
            "module load python/{}.{}.{}".format(
                version.major, version.minor, version.micro
            ),
            "source /home/users/$USER/opt/mypy{}.{}/bin/activate".format(
                version.major, version.minor
            ),
        ]

    def check_oar(self):
        """check if this script is run on a frontal with oar installed"""
        try:
            subprocess.check_call(["oarsub", "--version"], stdout=subprocess.PIPE)
        except OSError:
            raise OSError("oar does not seem to be installed.")

    def submit_script(
        self,
        path,
        name_run="fluiddyn",
        nb_nodes=1,
        nb_cores_per_node=1,
        walltime="24:00:00",
        project=None,
        nb_mpi_processes=None,
        omp_num_threads=None,
        idempotent=False,
        delay_signal_walltime=300,
        network_address=None,
        ask=True,
        submit=True,
    ):

        path = os.path.expanduser(path)
        if not os.path.exists(path.split(" ")[0]):
            raise ValueError("The script does not exists! path:\n" + path)

        if not path.startswith("python "):
            command = "python " + path

        self.submit_command(
            command,
            name_run=name_run,
            nb_nodes=nb_nodes,
            nb_cores_per_node=nb_cores_per_node,
            walltime=walltime,
            project=project,
            nb_mpi_processes=nb_mpi_processes,
            omp_num_threads=omp_num_threads,
            idempotent=idempotent,
            delay_signal_walltime=delay_signal_walltime,
            network_address=network_address,
            ask=ask,
            submit=submit,
        )

    def submit_command(
        self,
        command,
        name_run="fluiddyn",
        nb_nodes=1,
        nb_cores_per_node=1,
        walltime="24:00:00",
        project=None,
        nb_mpi_processes=None,
        omp_num_threads=None,
        idempotent=False,
        delay_signal_walltime=300,
        network_address=None,
        ask=True,
        submit=True,
    ):

        self.check_oar()

        if nb_cores_per_node is None and nb_mpi_processes is not None:
            nb_cores_per_node = nb_mpi_processes

        if nb_cores_per_node > self.nb_cores_per_node:
            raise ValueError("Too many cores...")

        str_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path_launching_script = "oar_launcher_" + str_time
        if os.path.exists(path_launching_script):
            i = 1
            while os.path.exists(path_launching_script + "_" + str(i)):
                i += 1
            path_launching_script += "_" + str(i)

        txt = self._create_txt_launching_script(
            command,
            name_run,
            nb_nodes,
            nb_cores_per_node,
            walltime,
            nb_mpi_processes=nb_mpi_processes,
            omp_num_threads=omp_num_threads,
            network_address=network_address,
        )

        with open(path_launching_script, "w") as f:
            f.write(txt)

        os.chmod(
            path_launching_script, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
        )

        launching_command = "oarsub"

        if project is not None:
            launching_command += " --project " + project

        if delay_signal_walltime is not None:
            launching_command += " --checkpoint " + str(delay_signal_walltime)

        if idempotent:
            launching_command += " -t idempotent"

        launching_command += " -S ./" + path_launching_script

        print('A launcher for the command "{}" has been created.'.format(command))
        if submit:
            if ask:
                run_asking_agreement(launching_command)
            else:
                print(
                    "The script is submitted with the command:\n",
                    launching_command,
                )
                call_bash(launching_command)

    def _create_txt_launching_script(
        self,
        command,
        name_run,
        nb_nodes,
        nb_cores_per_node,
        walltime,
        nb_mpi_processes=None,
        omp_num_threads=None,
        network_address=None,
    ):

        txt = ("#!/bin/bash\n\n" "#OAR -n {}\n".format(name_run))

        txt += "#OAR -l "

        if self.has_to_add_name_cluster and network_address is None:
            txt += "{cluster='" + self.name_cluster + "'}"
        elif network_address is not None:
            txt += "{network_address='" + network_address + "'}"

        txt += "/nodes={}/core={},walltime={}\n\n".format(
            nb_nodes, nb_cores_per_node, walltime
        )

        txt += 'echo "hostname: "$HOSTNAME\n\n'

        txt += "\n".join(self.commands_setting_env) + "\n\n"

        if omp_num_threads is not None:
            txt += "export OMP_NUM_THREADS={}\n\n".format(omp_num_threads)

        if nb_mpi_processes is not None and nb_nodes > 1:
            txt += (
                "# Shell with environment variables forwarded\n"
                "export OMPI_MCA_plm_rsh_agent=oar-envsh\n\n"
            )

        txt += "exec "

        if nb_mpi_processes is not None:
            txt += "mpirun -np {} ".format(nb_mpi_processes)

            if nb_nodes > 1:
                txt += "-machinefile ${OAR_NODEFILE} "

        txt += command + "\n"

        return txt
