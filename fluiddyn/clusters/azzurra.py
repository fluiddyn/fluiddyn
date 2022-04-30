"""
Slurm clusters under AZZURRA (:mod:`fluiddyn.clusters.azzurra`)
===============================================================

Provides:

.. autoclass:: Azzurra
   :members:

"""

from fluiddyn.clusters.slurm import ClusterSlurm


class Azzurra(ClusterSlurm):
    nb_cores_per_node = 40
    max_walltime = "23:59:59"
    cmd_run = "time mpirun"
    partition = "cpucourt"
    account = "turbulence"
    exclusive = True

    def __init__(self):
        super().__init__()
        self.check_name_cluster()

        self.commands_setting_env = [
            "conda deactivate",
            "OPT=$HOME/opt",
            "module purge",
            "module load gnu8 openmpi hdf5/1.12.1-ompi412 fftw/3.3.8",
            "export LD_LIBRARY_PATH=$HOME/opt/p3dfft/2.7.5/lib:$HOME/opt/pfft/lib:$LD_LIBRARY_PATH",
            "export FLUIDSIM_PATH=/workspace/$USER",
        ]
