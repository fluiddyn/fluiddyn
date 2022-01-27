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
    cmd_run = "time srun --mpi=pmix -K1 --resv-ports"

    def __init__(self):
        super().__init__()
        self.check_name_cluster()

        self.commands_setting_env = [
            "#SBATCH -p x40",
            "OPT=$HOME/opt",            
            "module purge",
            "module load intel-gnu8-runtime/19.1.2.254 impi phdf5 fftw3",     
            "unset I_MPI_PMI_LIBRARY",
            "CC=mpicc",
            "CXX=mpicpc",
            "export FLUIDSIM_PATH=/scratch/$USER",
        ]


