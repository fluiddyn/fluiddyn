"""
Slurm clusters under TGCC Joliot Curie (:mod:`fluiddyn.clusters.tgcc`)
======================================================================

Provides:

.. autoclass:: SKL
   :members:

"""

from fluiddyn.clusters.slurm import ClusterSlurm


class SKL(ClusterSlurm):
    name_cluster = "skl"
    nb_cores_per_node = 24
    max_walltime = "23:59:59"
    cmd_run = "srun --mpi=pmi2 -K1 --resv-ports"

    def __init__(self):
        super().__init__()
        # self.check_name_cluster()

        self.commands_setting_env = [
            "OPT=$HOME/opt",
            "module purge",
            "module load gcc/6.2.0",
            "module load intel/17.2",
            "module load openmpi/intel/2.0.2",
            "module load qt",
            "module load hdf5-seq",
            "module load python/3.6.3",
            "unset PYTHONPATH",
            "source $HOME/mypy/bin/activate",
            (
                "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"
                "$OPT/pfft/lib:$OPT/p3dfft/2.7.5/lib:$OPT/fftw/3.3.7/lib"
            ),
            "export LANG=C",
            "export LC_LANG=C",
        ]
