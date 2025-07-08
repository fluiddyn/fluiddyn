"""Gricad clusters (:mod:`fluiddyn.clusters.gricad`)
====================================================

Provides:

.. autoclass:: Dahu
   :members:

`Gricad <https://gricad.univ-grenoble-alpes.fr>`_ handles the Grenoble University
High Performance Computing (HPC) centre.

"""

from fluiddyn.clusters.oar import ClusterOAR, ClusterOARGuix


class Dahu(ClusterOAR):
    name_cluster = "dahu"
    has_to_add_name_cluster = False
    frontends = ["dahu", "dahu-oar3"]
    use_oar_envsh = "/bettik/legi/oar-envsh"
    commands_setting_mpi = [
        "export OMPI_MCA_btl_openib_allow_ib=true",
        "export OMPI_MCA_pml=cm",
        "export OMPI_MCA_mtl=psm2",
    ]


class DahuDevel(Dahu):
    devel = True
    frontends = ["dahu-oar3"]


class Dahu16_6130(Dahu):
    nb_cores_per_node = 16
    resource_conditions = "cpumodel='Gold 6130' and n_cores=16"


class Dahu32_6130(Dahu):
    nb_cores_per_node = 32
    resource_conditions = "cpumodel='Gold 6130' and n_cores=32"


class Dahu24_6126(Dahu):
    nb_cores_per_node = 24
    resource_conditions = "cpumodel='Gold 6126' and n_cores=24"


class Dahu32_5218(Dahu):
    nb_cores_per_node = 32
    resource_conditions = "cpumodel='Gold 5218' and n_cores=32"


class Dahu16_6244(Dahu):
    nb_cores_per_node = 16
    resource_conditions = "cpumodel='Gold 6244' and n_cores=16"
