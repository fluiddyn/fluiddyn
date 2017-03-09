"""
Test rdvision module
====================

"""

import unittest
import os
from shutil import rmtree

from .. import rdvision


class TestDantex(unittest.TestCase):
    """Test fluiddyn.io.rdvision module."""
    def setUp(self):
        self._work_dir = 'test_fluiddyn_io_rdvision'
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        os.chdir(self._work_dir)

    def tearDown(self):
        os.chdir('..')
        rmtree(self._work_dir)


if __name__ == '__main__':
    unittest.main()
