"""
Slurm clusters under SNIC (:mod:`fluiddyn.clusters.snic`)
=========================================================

.. currentmodule:: fluiddyn.clusters.snic

Provides:

.. autoclass:: Beskow
   :members:

.. autoclass:: Triolith
   :members:

.. autoclass:: Abisko
   :members:

"""

from .slurm import ClusterSlurm
from os import getenv


class Beskow(ClusterSlurm):
    name_cluster = 'beskow'
    nb_cores_per_node = 32
    cmd_run_interactive = 'aprun'
    max_walltime = '23:59:59'

    def __init__(self):
        super(Beskow, self).__init__()
        self.check_name_cluster('SNIC_RESOURCE')

        self.commands_setting_env = [
            'source /etc/profile',
            'module swap PrgEnv-cray PrgEnv-gnu',
            'module load fftw anaconda/py27/2.3',
            'export CRAY_ROOTFS=DSL',
            'source $LOCAL_ANACONDA/bin/activate $LOCAL_ANACONDA',
            'export ANACONDA_HOME=$LOCAL_ANACONDA',
            'source activate_python']

        self.commands_unsetting_env = [
            'source deactivate_python']


class Triolith(ClusterSlurm):
    name_cluster = 'triolith'
    nb_cores_per_node = 16
    cmd_run_interactive = 'mpirun'
    max_walltime = '7-00:00:00'

    def __init__(self):
        super(Triolith, self).__init__()
        self.check_name_cluster('SNIC_RESOURCE')

        self.commands_setting_env = [
            'module add python/2.7.12',
            'module add gcc/4.9.0 openmpi/1.6.2-build1',
            'module add hdf5/1.8.11-i1214-parallel',
            'source $LOCAL_PYTHON/bin/activate']

        self.commands_unsetting_env = [
            'deactivate']


class Abisko(ClusterSlurm):
    name_cluster = 'abisko'
    nb_cores_per_node = 48
    max_walltime = '7-00:00:00'

    def __init__(self):
        super(Abisko, self).__init__()
        self.check_name_cluster('SNIC_RESOURCE')

        self.commands_setting_env = [
            'source /etc/profile',
            'module load openmpi/gcc/1.8.8',
            'module load fftw/gcc/3.3.4 hdf5/gcc-ompi/1.8.11',
            'source $LOCAL_PYTHON/bin/activate']

        self.commands_unsetting_env = []


_host = getenv('SNIC_RESOURCE')
if _host == 'beskow':
    ClusterSNIC = Beskow
elif _host == 'triolith':
    ClusterSNIC = Triolith
elif _host == 'abisko':
    ClusterSNIC = Abisko
