"""
Test image saving and reading
=============================

"""
from __future__ import print_function
from future.utils import raise_from

import unittest
import os
from itertools import chain
import numpy as np
from ..image import imread, imsave, imread_h5, imsave_h5, use_opencv


def err_msg(_format, _type, path):
    """Assertion error message. """
    return 'while testing format={}, data type={} saved as {}.'.format(
        _format, _type, path)


class TestImage(unittest.TestCase):
    """Test fluiddyn.io.image module."""

    def setUp(self):
        def im(maxval, dtype, shape=(10, 10)):
            """Generate a test image."""
            return (maxval * np.random.random(shape)).astype(dtype)

        self.paths = {
            None: 'test_image_none.png',
            'PNG': 'test_image.png',
            #  TIFF image saving with Pillow gives error
            # 'TIFF': 'test_image.tif',
        }

        self.paths_h5 = {
            'gray8': 'test_gray.h5',
            'color8': 'test_color.h5'
        }

        self.images = {
            'gray8': im(2 ** 8 - 1, np.uint8),
            'gray16': im(2 ** 16 - 1, np.int32),
            'gray8f': im(2 ** 8 - 1, np.float16),
            'gray16f': im(2 ** 16 - 1, np.float32),
            'color8': im(2 ** 8 - 1, np.uint8, (10, 10, 3)),
        }

    def tearDown(self):
        for path in chain(self.paths.values(), self.paths_h5.values()):
            if os.path.exists(path):
                os.remove(path)

    def test_save_load_image(self):
        """Test save to and load from image file."""
        for _format, path in self.paths.items():
            for _type, image in self.images.items():
                if _type == 'color8':
                    continue  # Cannot handle 3D images now

                err = (err_msg(_format, _type, path) +
                       ' Function imread from OpenCV={}'.format(use_opencv))
                as_int = bool(_type.endswith('f'))
                try:
                    imsave(path, image, _format, as_int)
                    image2 = imread(path, flatten=True)
                except Exception as e:
                    raise_from(Exception(err), e)

                if as_int:
                    np.testing.assert_array_almost_equal(image, image2, 0, err)
                else:
                    np.testing.assert_array_equal(image, image2, err)

    def test_save_load_hdf5(self):
        """Test save to and load from hdf5 file."""
        _format = 'HDF5'
        for _type, path in self.paths_h5.items():
            image = self.images[_type]
            imsave_h5(path, image)
            image2 = imread_h5(path)
            np.testing.assert_array_equal(image, image2, err_msg(
                _format, _type, path))


if __name__ == '__main__':
    unittest.main()
