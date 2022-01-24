"""
Slurm clusters under IDRIS (:mod:`fluiddyn.clusters.idris`)
===========================================================

Provides:

.. autoclass:: JeanZay
   :members:

"""

from fluiddyn.clusters.slurm import ClusterSlurm


class JeanZay(ClusterSlurm):
    nb_cores_per_node = 40
    max_walltime = "23:59:59"
    cmd_run = "srun"

    def __init__(self):
        super().__init__()
        self.check_name_cluster()

        self.commands_setting_env = [
            "OPT=$WORK/opt",
            "module purge",
            "module load python/3.8.8 gcc/8.3.1 openmpi/4.1.1 hdf5/1.12.0-mpi",
            "module load fftw/3.3.8-mpi pfft/1.0.8-alpha-mpi p3dfft/2.7.9-mpi",
            "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$WORK/.local/p3dfft/2.7.6/lib",
            "export LANG=C",
            "export LC_LANG=C",
        ]
