"""Zen supercomputer

https://www.mesonet.fr/documentation/user-documentation/code_form/zen/

"""

from fluiddyn.clusters.slurm import ClusterSlurm


class Zen(ClusterSlurm):
    """Zen is a cluster using Slurm"""

    name_cluster = "zen"
    nb_cores_per_node = 128
