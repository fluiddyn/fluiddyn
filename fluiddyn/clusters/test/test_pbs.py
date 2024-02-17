"""
Test SLURM and SNIC clusters
============================

"""

import os
import unittest
from shutil import rmtree

from ...io import stdout_redirected
from .. import pbs

jobid = 123


def my_test_input(message):
    return f"{jobid} {jobid}"


pbs.input = my_test_input


class ClusterPBSMod(pbs.ClusterPBS):
    """A modified class which skips checking if PBS is installed or not."""

    cmd_launch = "echo"

    def check_pbs(self):
        pass

    def check_name_cluster(self, env="HOSTNAME"):
        os.environ[env] = self.name_cluster
        super().check_name_cluster(env)


@unittest.skipUnless(os.name == "posix", "requires POSIX")
class PBSTestCase(unittest.TestCase):
    """Test ClusterPBS submit_script method."""

    def setUp(self, cls=ClusterPBSMod):
        self._work_dir = "test_pbs"
        self._script = "script.py"
        self._script_resume = "script_resume.py"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        os.chdir(self._work_dir)
        with open(self._script, "w") as f:
            f.write('print("Hello world")')

        with open(self._script_resume, "w") as f:
            f.write('print("Hello Again")')

        self.cluster = cls()

    def tearDown(self):
        os.chdir("..")
        try:
            rmtree(self._work_dir)
        except OSError:
            # in case something strange happen...
            pass

    def test_submit_defaults(self):
        """Test submit_script method with its default options."""
        with stdout_redirected():
            self.cluster.submit_script(self._script, ask=False)

    def test_submit_non_default(self):
        """Test submit_script method with its non-default options."""
        launcher = "test_launcher.sh"
        self.cluster.max_walltime = "3-00:00:00"
        nb_cores_per_node = self.cluster.nb_cores_per_node // 2

        with stdout_redirected():
            self.cluster.submit_script(
                self._script,
                path_resume=self._script_resume,
                name_run="test",
                path_launching_script=launcher,
                retain_script=False,
                nb_nodes=2,
                nb_cores_per_node=nb_cores_per_node,
                nb_mpi_processes=None,
                walltime="2-23:59:59",
                nb_runs=2,
                project="2001-01-01",
                queue="queuename",
                nb_switches=2,
                max_waittime="00:10:00",
                ask=False,
                bash=False,
                email="johndoe@example.com",
                interactive=True,
            )

        if os.path.exists(launcher):
            raise ValueError(f"PBS launching script {launcher} was left behind")


if __name__ == "__main__":
    unittest.main()
