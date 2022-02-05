"""
Test multitiff module
=====================

"""

import os
import unittest
from shutil import rmtree

import numpy as np
from PIL import Image

from ..multitiff import (
    imsave,
    reorganize_piv2d_doubleframe,
    reorganize_piv2d_singleframe,
    reorganize_piv3dscanning_doubleframe,
    reorganize_single_frame_3Dscannedpiv_data,
)
from ..redirect_stdout import stdout_redirected


class TestMultiTIFF(unittest.TestCase):
    """Test fluiddyn.io.multitiff module."""

    @classmethod
    def setUpClass(cls):
        def im(maxval, dtype, shape=(10, 10)):
            """Generate a test image."""
            return (maxval * np.random.random(shape)).astype(dtype)

        cls._work_dir = "test_fluiddyn_io_multitiff"
        if not os.path.exists(cls._work_dir):
            os.mkdir(cls._work_dir)

        os.chdir(cls._work_dir)
        cls.n_frames = 4
        cls.nb_files = 2

        for ifile in range(cls.nb_files):
            arrays = [im(2**8 - 1, np.int8) for i in range(cls.n_frames)]
            imsave(f"test_multitiff{ifile}.tif", arrays, as_int=True)

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        rmtree(cls._work_dir)

    def test_imsave(self):
        with Image.open("test_multitiff0.tif") as im:
            n_frames = im.n_frames

        if n_frames != self.n_frames:
            raise ValueError(
                "Multiframe TIFF imsave unsuccessful. No. of frames={}".format(
                    n_frames
                )
            )

    def test_single_frame_3Dscannedpiv(self):
        with stdout_redirected():
            reorganize_single_frame_3Dscannedpiv_data(
                "test*.tif", 2, outputdir=".", outputext="png", erase=True
            )

    def test_piv3dscanning_doubleframe(self):
        with stdout_redirected():
            reorganize_piv3dscanning_doubleframe(
                "test*.tif", 2, outputdir=".", outputext="png", erase=False
            )

    def test_piv2d_singleframe(self):
        with stdout_redirected():
            reorganize_piv2d_singleframe(
                "test*.tif", outputdir=".", outputext="png", erase=False
            )

    def test_piv2d_doubleframe(self):
        with stdout_redirected():
            reorganize_piv2d_doubleframe(
                "test*.tif", outputdir=".", outputext="png", erase=False
            )


if __name__ == "__main__":
    unittest.main()
