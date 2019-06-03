"""
Test SLURM and SNIC clusters
============================

"""
import os
import unittest
from shutil import rmtree

from .. import cines, slurm, snic
from ...io import stdout_redirected

jobid = 123


def my_test_input(message):
    return f"{jobid} {jobid}"


slurm.input = my_test_input


class ClusterSlurmMod(slurm.ClusterSlurm):
    """A modified class which skips checking if SLURM is installed or not."""

    cmd_launch = "echo"

    def check_slurm(self):
        pass

    def check_name_cluster(self, env="HOSTNAME"):
        os.environ[env] = self.name_cluster
        super().check_name_cluster(env)


@unittest.skipUnless(os.name == "posix", "requires POSIX")
class SlurmTestCase(unittest.TestCase):
    """Test ClusterSlurm submit_script method."""

    def setUp(self, cls=ClusterSlurmMod):
        self._work_dir = "test_slurm"
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
                jobid=jobid,
                project="2001-01-01",
                requeue=True,
                nb_switches=2,
                max_waittime="00:10:00",
                ask=False,
                bash=False,
                email="johndoe@example.com",
                interactive=True,
            )

        if os.path.exists(launcher):
            raise ValueError(f"SLURM launching script {launcher} was left behind")


class BeskowMod(ClusterSlurmMod, snic.Beskow):
    pass


class BeskowTestCase(SlurmTestCase):
    def setUp(self):
        super().setUp(BeskowMod)


class TetralithMod(ClusterSlurmMod, snic.Tetralith):
    pass


class TetralithTestCase(SlurmTestCase):
    def setUp(self):
        super().setUp(TetralithMod)


class AbiskoMod(ClusterSlurmMod, snic.Abisko):
    pass


class AbiskoTestCase(SlurmTestCase):
    def setUp(self):
        super().setUp(AbiskoMod)


class OccigenMod(ClusterSlurmMod, cines.Occigen):
    pass


class OccigenTestCase(SlurmTestCase):
    def setUp(self):
        super().setUp(OccigenMod)


if __name__ == "__main__":
    unittest.main()
