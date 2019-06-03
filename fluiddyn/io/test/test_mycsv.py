"""
Test mycsv module
====================

"""

import os
import unittest
from shutil import rmtree

from ..mycsv import CSVFile


class TestDantex(unittest.TestCase):
    """Test fluiddyn.io.mycsv module."""

    def setUp(self):
        self._work_dir = "test_fluiddyn_io_mycsv"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        os.chdir(self._work_dir)

        with open("myfile.csv", "w") as f:
            f.write("a,b,c\n1,2,3\n")

    def tearDown(self):
        os.chdir("..")
        rmtree(self._work_dir)

    def test_csv(self):
        with CSVFile("myfile.csv") as f:
            f.get_fieldnames()
            f.load_as_dict(["a", "b"])


if __name__ == "__main__":
    unittest.main()
