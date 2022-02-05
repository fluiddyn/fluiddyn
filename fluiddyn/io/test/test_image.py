"""
Test image saving and reading
=============================

"""

import os
import unittest
from itertools import chain

import numpy as np

from ..image import imread, imread_h5, imsave, imsave_h5, use_opencv


def err_msg(_format, _type, path):
    """Assertion error message."""
    return "while testing format={}, data type={} saved as {}.".format(
        _format, _type, path
    )


class TestImage(unittest.TestCase):
    """Test fluiddyn.io.image module."""

    @classmethod
    def setUpClass(cls):
        def im(maxval, dtype, shape=(10, 10)):
            """Generate a test image."""
            return (maxval * np.random.random(shape)).astype(dtype)

        cls.paths = {
            None: "test_image_none.png",
            "PNG": "test_image.png",
            #  TIFF image saving with Pillow gives error
            # 'TIFF': 'test_image.tif',
        }

        cls.paths_h5 = {"gray8": "test_gray.h5", "color8": "test_color.h5"}

        cls.images = {
            "gray8": im(2**8 - 1, np.uint8),
            "gray16": im(2**16 - 1, np.int32),
            "gray8f": im(2**8 - 1, np.float16),
            "gray16f": im(2**16 - 1, np.float32),
            "color8": im(2**8 - 1, np.uint8, (10, 10, 3)),
        }

    @classmethod
    def tearDownClass(cls):
        for path in chain(cls.paths.values(), cls.paths_h5.values()):
            if os.path.exists(path):
                os.remove(path)
            if os.path.exists(path + ".h5"):
                os.remove(path + ".h5")

    def test_save_load_image(self):
        """Test save to and load from image file."""
        for _format, path in self.paths.items():
            for _type, image in self.images.items():
                if _type == "color8":
                    continue  # Cannot handle 3D images now

                err = (
                    err_msg(_format, _type, path)
                    + f" Function imread from OpenCV={use_opencv}"
                )
                as_int = bool(_type.endswith("f"))
                try:
                    imsave(path, image, _format, as_int)
                    image2 = imread(path)
                except Exception as e:
                    raise Exception(err) from e

                if as_int:
                    np.testing.assert_array_almost_equal(image, image2, 0, err)
                else:
                    np.testing.assert_array_equal(image, image2, err)

    def test_save_load_hdf5(self):
        """Test save to and load from hdf5 file."""
        _format = "HDF5"
        for _type, path in self.paths_h5.items():
            image = self.images[_type]
            imsave_h5(path, image, splitext=False)
            imsave_h5(path, image)
            image2 = imread_h5(path)
            np.testing.assert_array_equal(
                image, image2, err_msg(_format, _type, path)
            )


if __name__ == "__main__":
    unittest.main()
