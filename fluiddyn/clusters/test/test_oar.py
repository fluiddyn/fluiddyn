'''
Test oar clusters
=================

'''
import unittest
import os
from shutil import rmtree

from ...io import stdout_redirected

from ..oar import ClusterOAR
from ..legi import Calcul, Calcul3, Calcul9, Calcul7, Calcul8
from ..ciment import Froggy

path_test = 'tmp_test'


class ClusterNoCheck(ClusterOAR):
    """A modified class which skips checking if oar is installed or not."""
    def check_oar(self):
        pass


class CalculNoCheck(ClusterNoCheck, Calcul):
    pass


class Calcul3NoCheck(ClusterNoCheck, Calcul3):
    pass


class Calcul9NoCheck(ClusterNoCheck, Calcul9):
    pass


class Calcul7NoCheck(ClusterNoCheck, Calcul7):
    pass


class Calcul8NoCheck(ClusterNoCheck, Calcul8):
    pass


class FroggyNoCheck(ClusterNoCheck, Froggy):
    pass


class TestCaseOAR(unittest.TestCase):
    Cluster = ClusterOAR
    ClusterNoCheck = ClusterNoCheck

    def setUp(self):
        self.cluster = self.Cluster()
        self.clusternocheck = self.ClusterNoCheck()

        self._work_dir = 'tmp_test_oar'
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)
        os.chdir(self._work_dir)

    def tearDown(self):
        os.chdir('..')
        rmtree(self._work_dir)

    def test_submit_check(self):
        with self.assertRaises(OSError):
            self.cluster.submit_script('blabla', submit=False)

    def test_submit_nocheck(self):
        with self.assertRaises(ValueError):
            self.clusternocheck.submit_script(
                'script_that_does_not_exist.py', submit=False)

        with open('tmp_for_test.py', 'w') as f:
            f.write('print("hello")')

        with stdout_redirected():
            self.clusternocheck.submit_script(
                'tmp_for_test.py', submit=False)


class TestCaseCalcul(TestCaseOAR):
    Cluster = Calcul
    ClusterNoCheck = CalculNoCheck


class TestCaseCalcul3(TestCaseOAR):
    Cluster = Calcul3
    ClusterNoCheck = Calcul3NoCheck


class TestCaseCalcul9(TestCaseOAR):
    Cluster = Calcul9
    ClusterNoCheck = Calcul3NoCheck


class TestCaseCalcul7(TestCaseOAR):
    Cluster = Calcul7
    ClusterNoCheck = Calcul3NoCheck


class TestCaseCalcul8(TestCaseOAR):
    Cluster = Calcul8
    ClusterNoCheck = Calcul3NoCheck


class TestCaseFroggy(TestCaseOAR):
    Cluster = Froggy
    ClusterNoCheck = FroggyNoCheck


if __name__ == '__main__':
    unittest.main()
