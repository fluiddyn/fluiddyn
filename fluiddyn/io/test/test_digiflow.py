"""
Test digiflow module
====================

"""

import os
import unittest
from shutil import rmtree

from ..digiflow import DigiflowImage, DigiflowMovie

# import numpy as np


class TestDigiflow(unittest.TestCase):
    """Test fluiddyn.io.digiflow module."""

    def setUp(self):
        self._work_dir = "test_fluiddyn_io_digiflow"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        os.chdir(self._work_dir)

        self.path_dfi = "myfile.dfi"
        self.path_dfm = "myfile.dfm"

    def tearDown(self):
        os.chdir("..")
        rmtree(self._work_dir)


if __name__ == "__main__":
    unittest.main()
