"""
LEGI clusters (:mod:`fluiddyn.clusters.legi`)
=============================================

.. currentmodule:: fluiddyn.clusters.legi

Provides:

.. autoclass:: Calcul
   :members:

.. autoclass:: Calcul3
   :members:

.. autoclass:: Calcul9
   :members:

.. autoclass:: Calcul7
   :members:

"""
from __future__ import print_function
from subprocess import check_output
import time

from fluiddyn.clusters.oar import ClusterOAR


class Calcul3(ClusterOAR):
    name_cluster = 'calcul3'
    has_to_add_name_cluster = True
    nb_cores_per_node = 12
    frontends = ['calcul8sv109', 'legilnx44']


class Calcul9(ClusterOAR):
    name_cluster = 'calcul9'
    has_to_add_name_cluster = True
    nb_cores_per_node = 8
    frontends = ['calcul8sv109', 'legilnx44']


class Calcul(ClusterOAR):
    name_cluster = 'calcul7-8'
    has_to_add_name_cluster = False
    nb_cores_per_node = 20
    frontends = ['nrj1sv223', 'nrj1sv224']
    job_count = 0

    def __init__(self):

        super(Calcul, self).__init__()

        self.commands_setting_env = [
            'source /etc/profile',
            'module load python/2.7.9',
            'source /home/users/$USER/opt/mypy2.7/bin/activate']

    def stall(self, name_run='fluiddyn', stall_after=1, t_sleep=30):
        """Stall job submission to wait for similar jobs to complete.

        Parameters
        ----------
        name_run: str
            Description of the job. Should be the same as in submit_script.
        stall_after: int
            Continue launching jobs, and stall when `job_count` is divisible
            by `stall_after`.
        t_sleep: int
            Time to sleep in seconds.

        """
        tstart = time.time()
        self.job_count += 1
        while (name_run in check_output(['oarstat', '-u']) and
               self.job_count % stall_after == 0):
            tnow = time.time()
            print('\rWaiting for', name_run, 'to finish...',
                  tnow - tstart, 'seconds', end=' ')
            time.sleep(t_sleep)

class Calcul7(Calcul):
    name_cluster = 'calcul7'
    has_to_add_name_cluster = True
    nb_cores_per_node = 16


class Calcul8(Calcul):
    name_cluster = 'calcul8'
    has_to_add_name_cluster = True
