"""
Test rdvision module
====================

"""

import os
import unittest
from glob import glob
from shutil import copy, rmtree

from ..rdvision import SetOfFiles, read_seq, read_sqb, read_xml

input_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "rdvision_files")
)
input_files = glob(os.path.join(input_dir, "*"))


class TestDantex(unittest.TestCase):
    """Test fluiddyn.io.rdvision module."""

    @classmethod
    def setUpClass(cls):
        work_dir = cls._work_dir = "test_fluiddyn_io_rdvision"
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)

        for path in input_files:
            copy(path, work_dir)

        cls.base_name = os.path.splitext(input_files[0])[0]

        os.chdir(work_dir)

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        rmtree(cls._work_dir)

    def test(self):
        read_xml(self.base_name)
        read_sqb(self.base_name)
        SetOfFiles(self.base_name)


if __name__ == "__main__":
    unittest.main()
