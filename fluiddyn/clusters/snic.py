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

from os import getenv

from .slurm import ClusterSlurm

_venv = getenv("VIRTUAL_ENV", getenv("CONDA_PREFIX", getenv("LOCAL_PYTHON")))


class SNIC(ClusterSlurm):
    def __init__(self):
        if _venv is None:
            from warnings import warn

            warn(
                "Cannot detect a virtualenv / conda env. You should set an environment "
                "variable LOCAL_PYTHON instead for fluiddyn.clusters.snic to work."
            )
        super().__init__()


class Beskow(SNIC):
    name_cluster = "beskow"
    nb_cores_per_node = 32
    cmd_run_interactive = "aprun"
    max_walltime = "23:59:59"

    def __init__(self):
        super().__init__()
        self.check_name_cluster("SNIC_RESOURCE")
        self.commands_setting_env = [
            "source /etc/profile",
            "module load gcc/4.9.1",
            "module swap PrgEnv-cray PrgEnv-intel",
            "module swap intel intel/18.0.0.128",
            "module load cray-fftw/3.3.6.2",
            "export CRAY_ROOTFS=DSL",
            f"conda activate {_venv}",
        ]

        self.commands_unsetting_env = ["conda deactivate"]


class Beskow32(Beskow):
    constraint = "Haswell"


class Beskow36(Beskow):
    nb_cores_per_node = 36
    constraint = "Broadwell"


class Tetralith(SNIC):
    name_cluster = "tetralith"
    nb_cores_per_node = 32
    cmd_run = "mpprun"
    cmd_run_interactive = "mpirun"
    max_walltime = "7-00:00:00"

    def __init__(self):
        super().__init__()
        self.check_name_cluster("SNIC_RESOURCE")
        self.commands_setting_env = []

        # NOTE: Typically load the following modules and save them
        # Python/3.6.3-anaconda-5.0.1-nsc1 intel/2018a
        # buildtool-easybuild/3.5.3-nsc17d8ce4 buildenv-intel/2018a-eb
        # FFTW/3.3.6-nsc1
        self.commands_setting_env.extend(
            [
                "ml restore",
                f"source activate {_venv}",
                'export LD_LIBRARY_PATH="$LD_LIBRARY_PATH":"$LIBRARY_PATH"',
            ]
        )

        self.commands_unsetting_env = ["source deactivate"]


class Abisko(SNIC):
    name_cluster = "abisko"
    nb_cores_per_node = 24
    cmd_run_interactive = "mpirun"
    max_walltime = "7-00:00:00"

    def __init__(self):
        super().__init__()
        self.check_name_cluster("SNIC_RESOURCE")

        self.commands_setting_env = [
            "source /etc/profile",
            "module load GCC/6.3.0-2.27 OpenMPI/2.0.2",
            "module load HDF5/1.10.0-patch1",
            "module load FFTW/3.3.6",
            f"source {_venv}/bin/activate",
        ]

        self.commands_unsetting_env = []


class Kebnekaise(SNIC):
    name_cluster = "kebnekaise"
    nb_cores_per_node = 28
    cmd_run_interactive = "mpirun"
    max_walltime = "7-00:00:00"

    def __init__(self):
        super().__init__()
        self.check_name_cluster("SNIC_RESOURCE")
        self.commands_setting_env = ["source /etc/profile"]

        self.commands_setting_env.extend(
            [
                "module load foss/2017a",
                # also loads GCC/6.3.0-2.27  OpenMPI/2.0.2
                # OpenBLAS/0.2.19-LAPACK-3.7.0 FFTW/3.3.6
                "module rm FFTW/3.3.6",
                "module load HDF5/1.10.0-patch1",
                "module load Python/3.6.1",
                f"source {_venv}/bin/activate",
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
