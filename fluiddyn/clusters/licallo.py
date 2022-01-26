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
    cmd_run = "srun"

    def __init__(self):
        super().__init__()
        self.check_name_cluster()

        self.commands_setting_env = [
            "OPT=$HOME/opt",
            "module purge",
            "module load intel-gnu8-runtime/19.1.2.254 impi phdf5 fftw3 intelpython3", # To test
            "unset I_MPI_PMI_LIBRARY", # To test
            "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.local/p3dfft/2.7.6/lib", # To test
            "export LANG=C",
            "export LC_LANG=C",
        ]
