"""
Test txt functions
==================

"""

import os
import unittest
from shutil import rmtree

import numpy as np

from ..binary import BinFile


class TestBinary(unittest.TestCase):
    """Test fluiddyn.io.binary module."""

    def setUp(self):
        self._work_dir = "test_fluiddyn_io_binary"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        os.chdir(self._work_dir)

    def tearDown(self):
        os.chdir("..")
        rmtree(self._work_dir)

    def test_dict(self):
        name = "myfile"
        s = "poum"
        l = [1, 3]
        a = np.array([1.0, 1.5])

        with BinFile(name, "w") as f:
            f.write_as(s, buffersize=1)
            f.write_as(l, "I", buffersize=1)
            f.write_as(a, "float64", buffersize=1)

        with BinFile(name) as f:
            s1 = f.readt(4, "s")
            l1 = f.readt(2, "I")
            a1 = f.readt(2, "float64")

        self.assertEqual(s.encode(), s1)
        self.assertEqual([int(n) for n in l], list(l1))
        self.assertTrue(np.allclose(a, np.array(a1)))


if __name__ == "__main__":
    unittest.main()
