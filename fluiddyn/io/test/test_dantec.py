"""
Test dantec module
====================

"""

import os
import unittest
from shutil import rmtree

from .. import dantec


class TestDantex(unittest.TestCase):
    """Test fluiddyn.io.dantec module."""

    def setUp(self):
        self._work_dir = "test_fluiddyn_io_dantec"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        os.chdir(self._work_dir)

    def tearDown(self):
        os.chdir("..")
        rmtree(self._work_dir)


if __name__ == "__main__":
    unittest.main()
