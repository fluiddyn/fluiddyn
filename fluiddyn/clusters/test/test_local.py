"""
Test local cluster
==================

"""
import os
import unittest
from shutil import rmtree

from .. import local
from .test_slurm_snic import SlurmTestCase, stdout_redirected


class LocalTestCase(SlurmTestCase):
    def setUp(self):
        super().setUp(local.ClusterLocal)

    def test_submit_non_default(self):
        """Test submit_script method with its non-default options."""
        self.cluster.max_walltime = "3-00:00:00"
        nb_cores_per_node = self.cluster.nb_cores_per_node // 2

        with stdout_redirected():
            self.cluster.submit_script(
                self._script,
                name_run="test",
                nb_nodes=2,
                nb_cores_per_node=nb_cores_per_node,
                walltime="2-23:59:58",
                nb_mpi_processes=1,
                retain_script=False,
                omp_num_threads=2,
                ask=False,
                bash=False,
                interactive=True,
            )


if __name__ == "__main__":
    unittest.main()
