"""
Slurm clusters under SNIC (:mod:`fluiddyn.clusters.snic`)
=========================================================

.. currentmodule:: fluiddyn.clusters.snic

Provides:

.. autoclass:: Beskow
   :members:

.. autoclass:: Beskow32
   :members:

.. autoclass:: Beskow36
   :members:

.. autoclass:: Tetralith
   :members:

.. autoclass:: Abisko
   :members:

.. autoclass:: Kebnekaise
   :members:

"""
from __future__ import print_function

from os import getenv
import six
from .slurm import ClusterSlurm


_venv = "$LOCAL_PYTHON" if six.PY2 else "$LOCAL_PYTHON3"


class Beskow(ClusterSlurm):
    name_cluster = "beskow"
    nb_cores_per_node = 32
    cmd_run_interactive = "aprun"
    max_walltime = "23:59:59"

    def __init__(self):
        super(Beskow, self).__init__()
        self.check_name_cluster("SNIC_RESOURCE")
        if six.PY2:
            self.commands_setting_env = [
                "source /etc/profile",
                "module swap PrgEnv-cray PrgEnv-gnu",
                "module load fftw anaconda/py27/2.3" "export CRAY_ROOTFS=DSL",
                "source {}/bin/activate {}".format(_venv, _venv),
                "export ANACONDA_HOME=" + _venv,
                "source activate_python",
            ]

            self.commands_unsetting_env = ["source deactivate_python"]
        else:
            self.commands_setting_env = [
                "source /etc/profile",
                "module load gcc/4.9.1",
                "module swap PrgEnv-cray PrgEnv-intel",
                "module swap intel intel/18.0.0.128",
                "module load cray-fftw/3.3.6.2",
                "export CRAY_ROOTFS=DSL",
                "conda activate {}".format(_venv),
            ]

            self.commands_unsetting_env = ["conda deactivate"]


class Beskow32(Beskow):
    constraint = "Haswell"


class Beskow36(Beskow):
    nb_cores_per_node = 36
    constraint = "Broadwell"


class Tetralith(ClusterSlurm):
    name_cluster = "tetralith"
    nb_cores_per_node = 32
    cmd_run = "mpprun"
    cmd_run_interactive = "mpirun"
    max_walltime = "7-00:00:00"

    def __init__(self):
        super(Tetralith, self).__init__()
        self.check_name_cluster("SNIC_RESOURCE")
        self.commands_setting_env = []

        self.commands_setting_env.extend(
            [
                "ml restore",
                f"source activate {_venv}",
            ]
        )

        self.commands_unsetting_env = ["source deactivate"]


class Abisko(ClusterSlurm):
    name_cluster = "abisko"
    nb_cores_per_node = 24
    cmd_run_interactive = "mpirun"
    max_walltime = "7-00:00:00"

    def __init__(self):
        super(Abisko, self).__init__()
        self.check_name_cluster("SNIC_RESOURCE")

        self.commands_setting_env = [
            "source /etc/profile",
            "module load GCC/6.3.0-2.27 OpenMPI/2.0.2",
            "module load HDF5/1.10.0-patch1",
            "module load FFTW/3.3.6",
            "source {}/bin/activate".format(_venv),
        ]

        self.commands_unsetting_env = []


class Kebnekaise(ClusterSlurm):
    name_cluster = "kebnekaise"
    nb_cores_per_node = 28
    cmd_run_interactive = "mpirun"
    max_walltime = "7-00:00:00"

    def __init__(self):
        super(Kebnekaise, self).__init__()
        self.check_name_cluster("SNIC_RESOURCE")
        self.commands_setting_env = ["source /etc/profile"]

        if six.PY2:
            self.commands_setting_env.extend(
                [
                    "module load foss/2016b",
                    "module rm FFTW/3.3.5",
                    "module load HDF5/1.8.17",
                    "module load Python/2.7.12",
                    "module load PIL/1.1.7-Python-2.7.12",
                    "source {}/bin/activate".format(_venv),
                ]
            )
        else:
            self.commands_setting_env.extend(
                [
                    "module load foss/2017a",
                    # also loads GCC/6.3.0-2.27  OpenMPI/2.0.2
                    # OpenBLAS/0.2.19-LAPACK-3.7.0 FFTW/3.3.6
                    "module rm FFTW/3.3.6",
                    "module load HDF5/1.10.0-patch1",
                    "module load Python/3.6.1",
                    "source {}/bin/activate".format(_venv),
                ]
            )

        self.commands_unsetting_env = []


_host = getenv("SNIC_RESOURCE")
if _host == "beskow":
    ClusterSNIC = Beskow
elif _host == "tetralith":
    ClusterSNIC = Tetralith
elif _host == "abisko":
    ClusterSNIC = Abisko
elif _host == "kebnekaise":
    ClusterSNIC = Kebnekaise


if __name__ == "__main__":
    cluster = ClusterSNIC()
    print("\n".join(cluster.commands_setting_env))
