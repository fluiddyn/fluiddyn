"""Ciment clusters (:mod:`fluiddyn.clusters.ciment`)
====================================================

Provides:

.. autoclass:: Froggy
   :members:

`CIMENT <https://ciment.ujf-grenoble.fr>`_ is the Grenoble University
High Performance Computing (HPC) centre.

"""
from sys import version_info as version

from fluiddyn.clusters.oar import ClusterOAR


class Froggy(ClusterOAR):
    name_cluster = 'froggy'
    has_to_add_name_cluster = False
    nb_cores_per_node = 16
    frontends = ['']

    def __init__(self):

        super(Froggy, self).__init__()

        self.commands_setting_env = [
            'source /applis/site/env.bash',
            'export MODULEPATH='
            '/home/PROJECTS/pr-stratturb/modulefiles:$MODULEPATH',
            'module load python/{}.{}.{}'.format(
                version.major, version.minor, version.micro),
            'source /home/$USER/opt/mypy{}.{}/bin/activate'.format(
                version.major, version.minor)]
