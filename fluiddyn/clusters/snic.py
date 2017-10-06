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
from __future__ import print_function

from .slurm import ClusterSlurm
from os import getenv
import six


_venv = '$LOCAL_PYTHON' if six.PY2 else '$LOCAL_PYTHON3'


class Beskow(ClusterSlurm):
    name_cluster = 'beskow'
    nb_cores_per_node = 32
    cmd_run_interactive = 'aprun'
    max_walltime = '23:59:59'

    def __init__(self):
        super(Beskow, self).__init__()
        self.check_name_cluster('SNIC_RESOURCE')
        if six.PY2:
            modpy = 'anaconda/py27/2.3'
        else:
            modpy = 'anaconda/py36/4.3'

        self.commands_setting_env = [
            'source /etc/profile',
            'module swap PrgEnv-cray PrgEnv-gnu',
            'module load fftw ' + modpy,
            'export CRAY_ROOTFS=DSL',
            'source {}/bin/activate {}'.format(_venv, _venv),
            'export ANACONDA_HOME=' + _venv,
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
        if six.PY2:
            modpy = 'python/2.7.12'
        else:
            modpy = 'python3/3.6.1'
        
        self.commands_setting_env = [
            'module add ' + modpy ,
            'module add gcc/4.9.0 openmpi/1.6.2-build1',
            'module add hdf5/1.8.11-i1214-parallel',
            'source {}/bin/activate'.format(_venv)]

        self.commands_unsetting_env = [
            'deactivate']


class Abisko(ClusterSlurm):
    name_cluster = 'abisko'
    nb_cores_per_node = 24
    cmd_run_interactive = 'mpirun'
    max_walltime = '7-00:00:00'

    def __init__(self):
        super(Abisko, self).__init__()
        self.check_name_cluster('SNIC_RESOURCE')

        self.commands_setting_env = [
            'source /etc/profile',
            'module load GCC/6.3.0-2.27 OpenMPI/2.0.2',
            'module load HDF5/1.10.0-patch1',
            'module load FFTW/3.3.6',
            'module load Python/2.7.12',
            'source {}/bin/activate'.format(_venv)]

        self.commands_unsetting_env = []


class Kebnekaise(ClusterSlurm):
    name_cluster = 'kebnekaise'
    nb_cores_per_node = 28
    cmd_run_interactive = 'mpirun'
    max_walltime = '7-00:00:00'

    def __init__(self):
        super(Kebnekaise, self).__init__()
        self.check_name_cluster('SNIC_RESOURCE')
        self.commands_setting_env = [
            'source /etc/profile']

        if six.PY2:
            self.commands_setting_env.extend([
                'module load GCC/5.4.0-2.26 OpenMPI/1.10.3',
                'module load HDF5/1.8.17',
                'module load Python/2.7.12',
                'module load PIL/1.1.7-Python-2.7.12',
                'source {}/bin/activate'.format(_venv)])
        else:
            self.commands_setting_env.extend([
                'module load GCC/6.3.0-2.27  OpenMPI/2.0.2',
                'module load HDF5/1.10.0-patch1',
                'module load Python/3.6.1',
                'source {}/bin/activate'.format(_venv)])

        self.commands_unsetting_env = []


_host = getenv('SNIC_RESOURCE')
if _host == 'beskow':
    ClusterSNIC = Beskow
elif _host == 'triolith':
    ClusterSNIC = Triolith
elif _host == 'abisko':
    ClusterSNIC = Abisko
elif _host == 'kebnekaise':
    ClusterSNIC = Kebnekaise


if __name__ == '__main__':
    cluster = ClusterSNIC()
    print('\n'.join(cluster.commands_setting_env))
