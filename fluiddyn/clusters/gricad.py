"""Gricad clusters (:mod:`fluiddyn.clusters.gricad`)
====================================================

Provides:

.. autoclass:: DahuGuix
   :members:

`Gricad <https://gricad.univ-grenoble-alpes.fr>`_ handles the Grenoble University
High Performance Computing (HPC) centre.

"""

from fluiddyn.clusters.oar import ClusterOAR, ClusterOARGuix


class Dahu(ClusterOAR):
    name_cluster = "dahu"
    has_to_add_name_cluster = False
    frontends = ["dahu", "dahu-oar3"]
    use_oar_envsh = False


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


class DahuGuix(Dahu, ClusterOARGuix):

    options_guix_shell = "-E ^OMPI -E ^OAR -E ^OMP -m manifest.scm"

    commands_setting_env = [
        "source /applis/site/guix-start.sh",
        "export OMPI_MCA_plm_rsh_agent=/usr/bin/oarsh",
        "export OMPI_MCA_btl_openib_allow_ib=true",
        "export OMPI_MCA_pml=cm",
        "export OMPI_MCA_mtl=psm2",
    ]


class DahuGuixDevel(DahuGuix, DahuDevel):
    """Dahu devel with Guix"""


class DahuGuix16_6130(DahuGuix, Dahu16_6130):
    """Dahu16_6130 with Guix"""


class DahuGuix32_6130(DahuGuix, Dahu32_6130):
    """Dahu32_6130 with Guix"""


class DahuGuix24_6126(DahuGuix, Dahu24_6126):
    """Dahu24_6126 with Guix"""


class DahuGuix32_5218(DahuGuix, Dahu32_5218):
    """Dahu32_5218 with Guix"""


class DahuGuix16_6244(DahuGuix, Dahu16_6244):
    """Dahu16_6244 with Guix"""
