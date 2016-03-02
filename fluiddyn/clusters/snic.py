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

from fluiddyn.clusters.slurm import ClusterSlurm


class Beskow(ClusterSlurm):
    name_cluster = 'beskow'
    nb_cores_per_node = 32
    default_project ='2015-16-46'
    cmd_run = 'aprun'
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
    default_project ='2015-16-46'
    cmd_run = 'mpprun'
    max_walltime = '7-00:00:00'

    def __init__(self):
        super(Triolith, self).__init__()
        self.check_name_cluster('SNIC_RESOURCE')


class Abisko(ClusterSlurm):
    name_cluster = 'abisko'
    nb_cores_per_node = 48
    default_project ='SNIC2015-16-46'  
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
