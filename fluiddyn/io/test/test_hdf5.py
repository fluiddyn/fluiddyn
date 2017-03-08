"""
Test hdf5 module
================

"""

import unittest
import os
from shutil import rmtree

import numpy as np

from ..hdf5 import H5File


class TestHdf5(unittest.TestCase):
    """Test fluiddyn.io.hdf5 module."""
    def setUp(self):
        self._work_dir = 'test_fluiddyn_io_hdf5'
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        os.chdir(self._work_dir)

        self.path = 'myfile.h5'

    def tearDown(self):
        os.chdir('..')
        rmtree(self._work_dir)

    def test_dict(self):
        d = {'a': 1, 'b': 2}

        with H5File(self.path, 'w') as f:
            f.save_dict('d', d)

        with H5File(self.path) as f:
            d1 = f.load_dict('d')

        self.assertEqual(d, d1)

    def test_dict_of_ndarrays(self):
        name = 'myfile1.h5'
        d = {'times': 0., 'a': np.ones(10), 'b': np.zeros([2, 2])}

        with H5File(name, 'w') as f:
            f.save_dict_of_ndarrays(d)

        with H5File(name) as f:
            d1 = f.load()

            for k, v in d.items():
                v1 = d1[k]

                self.assertTrue(np.allclose(v, v1))

        with H5File(name, 'a') as f:
            d['times'] = 1.
            f.save_dict_of_ndarrays(d)

            f.load(times_slice=[0, 2, 0.1])


if __name__ == '__main__':
    unittest.main()
