"""
Test oar clusters
=================

"""

import os
import platform
import subprocess
import unittest
from pathlib import Path
from shutil import rmtree

import pytest

from ..ciment import Froggy
from ..gricad import Dahu, DahuDevel
from ..legi import GPU9, Calcul, Calcul2, Calcul6, Calcul7, Calcul8
from ..oar import ClusterOAR

path_test = "tmp_test"

try:
    subprocess.check_call(["oarsub", "--version"], stdout=subprocess.PIPE)
    oar = True
except OSError:
    oar = False


@unittest.skipUnless(os.name == "posix", "requires POSIX")
class TestCaseOAR(unittest.TestCase):
    Cluster = ClusterOAR

    def setUp(self):
        self.cluster = self.Cluster()
        self.clusternocheck = self.Cluster(check_scheduler=False)

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

        self.clusternocheck.submit_script("tmp_for_test.py", submit=False)


class TestCaseCalcul(TestCaseOAR):
    Cluster = Calcul


class TestCaseCalcul7(TestCaseOAR):
    Cluster = Calcul7


class TestCaseCalcul8(TestCaseOAR):
    Cluster = Calcul8


class TestCaseCalcul2(TestCaseOAR):
    Cluster = Calcul2


class TestCaseCalcul6(TestCaseOAR):
    Cluster = Calcul6


class TestCaseGPU9(TestCaseOAR):
    Cluster = GPU9


class TestFroggy(TestCaseOAR):
    Cluster = Froggy


class TestCaseDahu(TestCaseOAR):
    Cluster = Dahu


class TestCaseDahuDevel(TestCaseOAR):
    Cluster = DahuDevel


@pytest.mark.skipif(platform.system() != "Linux", reason="Only on Linux")
def test_get_commands_setting_env(monkeypatch):

    path_activate = Path("/do/not/exists/bin/activate")

    _exist = Path.exists

    def my_exists(self):

        if self in (Path("/etc/profile"), path_activate):
            return True

        return _exist(self)

    cluster = Calcul()

    monkeypatch.setattr(Path, "exists", my_exists)

    monkeypatch.setenv("PYTHONPATH", "/my/python/path")

    for name in ("VIRTUAL_ENV", "CONDA_DEFAULT_ENV", "CONDA_PREFIX"):
        monkeypatch.delenv(name, raising=False)

    commands = cluster.get_commands_setting_env()

    assert commands == [
        "source /etc/profile",
        "export PYTHONPATH=/my/python/path",
    ]

    monkeypatch.setenv("VIRTUAL_ENV", str(path_activate.parent.parent))

    commands = cluster.get_commands_setting_env()

    assert commands == [
        "source /etc/profile",
        "export PYTHONPATH=/my/python/path",
        f"source {path_activate}",
    ]

    monkeypatch.delenv("VIRTUAL_ENV")
    monkeypatch.delenv("PYTHONPATH")
    monkeypatch.setenv("CONDA_DEFAULT_ENV", "my_env")
    monkeypatch.setenv("CONDA_EXE", "/home/my_uname/miniforge3/bin/conda")

    commands = cluster.get_commands_setting_env()

    assert commands == [
        "source /etc/profile",
        "source /home/my_uname/miniforge3/etc/profile.d/conda.sh",
        "conda activate my_env",
    ]
