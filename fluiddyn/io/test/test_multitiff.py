"""
Test multitiff module
=====================

"""

import unittest
import os
from glob import glob
from shutil import rmtree, copy

import numpy as np
from PIL import Image

from ..multitiff import (
    imsave,
    reorganize_single_frame_3Dscannedpiv_data,
    reorganize_double_frame_3Dscannedpiv_data,
    reorganize_single_frame_2Dpiv_data,
    reorganize_double_frame_2Dpiv_data)


class TestMultiTIFF(unittest.TestCase):
    """Test fluiddyn.io.multitiff module."""
    def setUp(self):
        def im(maxval, dtype, shape=(10, 10)):
            """Generate a test image."""
            return (maxval * np.random.random(shape)).astype(dtype)

        self._work_dir = 'test_fluiddyn_io_multitiff'
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        # we have to be able to produce a small multiframe tiff file.

        os.chdir(self._work_dir)
        self.n_frames = 5
        self.path = 'test.tif'
        arrays = [im(2 ** 8 - 1, np.int8) for i in range(self.n_frames)]
        imsave(self.path, *arrays, as_int=True)

    def tearDown(self):
        os.chdir('..')
        rmtree(self._work_dir)

    def test_imsave(self):
        im = Image.open(self.path)
        im.load()
        n_frames = im.n_frames
        im.close()
        if n_frames != self.n_frames:
            raise ValueError(
                'Multiframe TIFF imsave unsuccessful. No. of frames={}'.format(
                    n_frames))


if __name__ == '__main__':
    unittest.main()
