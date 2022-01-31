"""
Slurm clusters under LICALLO (:mod:`fluiddyn.clusters.licallo`)
===============================================================

Provides:

.. autoclass:: Licallo
   :members:

"""

from fluiddyn.clusters.slurm import ClusterSlurm


class Licallo(ClusterSlurm):
    nb_cores_per_node = 40
    max_walltime = "23:59:59"
    cmd_run = "time srun --mpi=pmi2 -K1 --resv-ports"
    partition = "x40"

    def __init__(self):
        super().__init__()
        self.check_name_cluster()

        self.commands_setting_env = [
            "OPT=$HOME/opt",
            "module purge",
            "module load intel-gnu8-runtime/19.1.2.254 impi phdf5 fftw3",
            "export FLUIDSIM_PATH=/scratch/$USER",
        ]
