"""
Slurm clusters under CINES (:mod:`fluiddyn.clusters.cines`)
===========================================================

Provides:

.. autoclass:: Occigen
   :members:

"""

from fluiddyn.clusters.slurm import ClusterSlurm


class Occigen(ClusterSlurm):
    name_cluster = 'occigen'
    nb_cores_per_node = 24
    max_walltime = '23:59:59'
    cmd_run = 'srun --mpi=pmi2 -K1 --resv-ports'

    def __init__(self):
        super(Occigen, self).__init__()
        self.check_name_cluster()

        self.commands_setting_env = [
            'OPT=/scratch/cnt0022/egi2153/SHARED/opt',
            'module purge',
            'module load libffi python/2.7.11 qt mkl',
            'unset PYTHONPATH',
            'module load gcc/4.9.2',
            'module load intel',
            'module load bullxmpi/1.2.8.4',
            'source $HOME/opt/mypy/bin/activate',
            'export FFTW3_LIB_DIR=$OPT/fftw-3.3.5/lib/',
            'export FFTW3_INC_DIR=$OPT/fftw-3.3.5/include/',
            'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$FFTW3_LIB_DIR:$OPT/pfft/1.0.6/lib:$OPT/p3dfft/2.7.5/lib',
            'export LANG=C',
            'export LC_LANG=C',
            'export OMP_NUM_THREADS=1']
