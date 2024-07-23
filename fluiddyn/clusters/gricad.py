"""Gricad clusters (:mod:`fluiddyn.clusters.gricad`)
====================================================

Provides:

.. autoclass:: DahuGuix
   :members:

`Gricad <https://gricad.univ-grenoble-alpes.fr>`_ handles the Grenoble University
High Performance Computing (HPC) centre.

"""

from fluiddyn.clusters.oar import ClusterOARGuix


class DahuGuix(ClusterOARGuix):

    name_cluster = "dahu"
    has_to_add_name_cluster = False
    frontends = ["dahu", "dahu-oar3"]
    use_oar_envsh = False
    options_guix_shell = "-E ^OMPI -E ^OAR -E ^OMP -m manifest.scm"

    commands_setting_env = [
        "source /applis/site/guix-start.sh",
        "export OMPI_MCA_plm_rsh_agent=/usr/bin/oarsh",
        "export OMPI_MCA_btl_openib_allow_ib=true",
        "export OMPI_MCA_pml=cm",
        "export OMPI_MCA_mtl=psm2",
    ]


class DahuGuixDevel(DahuGuix):
    devel = True
    frontends = ["dahu-oar3"]


class DahuGuix16_6130(DahuGuix):
    nb_cores_per_node = 16
    resource_conditions = "cpumodel='Gold 6130' and n_cores=16"


class DahuGuix32_6130(DahuGuix):
    nb_cores_per_node = 32
    resource_conditions = "cpumodel='Gold 6130' and n_cores=32"


class DahuGuix24_6126(DahuGuix):
    nb_cores_per_node = 24
    resource_conditions = "cpumodel='Gold 6126' and n_cores=24"


class DahuGuix32_5218(DahuGuix):
    nb_cores_per_node = 32
    resource_conditions = "cpumodel='Gold 5218' and n_cores=32"


class DahuGuix16_6244(DahuGuix):
    nb_cores_per_node = 16
    resource_conditions = "cpumodel='Gold 6244' and n_cores=16"
