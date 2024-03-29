"""
Test oar clusters
=================

"""

import os
import subprocess
import unittest
from shutil import rmtree

from ...io import stdout_redirected
from ..ciment import Froggy
from ..legi import GPU9, Calcul, Calcul2, Calcul6, Calcul7, Calcul8
from ..oar import ClusterOAR

path_test = "tmp_test"

try:
    subprocess.check_call(["oarsub", "--version"], stdout=subprocess.PIPE)
    oar = True
except OSError:
    oar = False


class ClusterNoCheck(ClusterOAR):
    """A modified class which skips checking if oar is installed or not."""

    def check_oar(self):
        pass


class CalculNoCheck(ClusterNoCheck, Calcul):
    pass


class Calcul2NoCheck(ClusterNoCheck, Calcul2):
    pass


class Calcul6NoCheck(ClusterNoCheck, Calcul6):
    pass


class Calcul7NoCheck(ClusterNoCheck, Calcul7):
    pass


class Calcul8NoCheck(ClusterNoCheck, Calcul8):
    pass


class GPU9NoCheck(ClusterNoCheck, GPU9):
    pass


class FroggyNoCheck(ClusterNoCheck, Froggy):
    pass


@unittest.skipUnless(os.name == "posix", "requires POSIX")
class TestCaseOAR(unittest.TestCase):
    Cluster = ClusterOAR
    ClusterNoCheck = ClusterNoCheck

    def setUp(self):
        self.cluster = self.Cluster()
        self.clusternocheck = self.ClusterNoCheck()

        self._work_dir = "tmp_test_oar"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)
        os.chdir(self._work_dir)

        with open("blabla.py", "w") as f:
            f.write('print("hello")')

    def tearDown(self):
        os.chdir("..")
        rmtree(self._work_dir)

    @unittest.skipIf(oar, "oar is present...")
    def test_submit_check(self):
        with self.assertRaises(OSError):
            self.cluster.submit_script("blabla.py", submit=False)

    def test_submit_nocheck(self):
        with self.assertRaises(ValueError):
            self.clusternocheck.submit_script(
                "script_that_does_not_exist.py", submit=False
            )

        with open("tmp_for_test.py", "w") as f:
            f.write('print("hello")')

        with stdout_redirected():
            self.clusternocheck.submit_script("tmp_for_test.py", submit=False)


class TestCaseCalcul(TestCaseOAR):
    Cluster = Calcul
    ClusterNoCheck = CalculNoCheck


class TestCaseCalcul7(TestCaseOAR):
    Cluster = Calcul7
    ClusterNoCheck = Calcul7NoCheck


class TestCaseCalcul8(TestCaseOAR):
    Cluster = Calcul8
    ClusterNoCheck = Calcul8NoCheck


class TestCaseCalcul2(TestCaseOAR):
    Cluster = Calcul2
    ClusterNoCheck = Calcul2NoCheck


class TestCaseCalcul6(TestCaseOAR):
    Cluster = Calcul6
    ClusterNoCheck = Calcul6NoCheck


class TestCaseGPU9(TestCaseOAR):
    Cluster = GPU9
    ClusterNoCheck = GPU9NoCheck


class TestCaseFroggy(TestCaseOAR):
    Cluster = Froggy
    ClusterNoCheck = FroggyNoCheck


if __name__ == "__main__":
    unittest.main()
