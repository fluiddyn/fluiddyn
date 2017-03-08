"""
Test multitiff module
=====================

"""

import unittest
import os
from glob import glob
from shutil import rmtree, copy

# import numpy as np

from ..multitiff import (
    reorganize_single_frame_3Dscannedpiv_data,
    reorganize_double_frame_3Dscannedpiv_data,
    reorganize_single_frame_2Dpiv_data,
    reorganize_double_frame_2Dpiv_data)


class TestNS3D(unittest.TestCase):
    """Test fluiddyn.io.multitiff module."""
    def setUp(self):
        self._work_dir = 'test_fluiddyn_io_multitiff'
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        # we have to be able to produce a small multiframe tiff file.

        os.chdir(self._work_dir)

    def tearDown(self):
        os.chdir('..')
        rmtree(self._work_dir)

    def test_(self):
        pass

if __name__ == '__main__':
    unittest.main()
