"""
Test hdf5 module
================

"""

import os
import unittest
from shutil import rmtree

import numpy as np

from ..hdf5 import H5File, load_variables_h5, save_variables_h5


class TestHdf5(unittest.TestCase):
    """Test fluiddyn.io.hdf5 module."""

    @classmethod
    def setUpClass(cls):
        cls._work_dir = "test_fluiddyn_io_hdf5"
        if not os.path.exists(cls._work_dir):
            os.mkdir(cls._work_dir)

        os.chdir(cls._work_dir)

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        rmtree(cls._work_dir)

    def test_dict(self):
        path = "test_dict.h5"
        d = {"a": 1, "b": 2}

        with H5File(path, "w") as f:
            f.save_dict("d", d)

        with H5File(path, "r") as f:
            d1 = f.load_dict("d")

        self.assertEqual(d, d1)

    def test_dict_of_ndarrays(self):
        name = "myfile1.h5"
        d = {"times": 0.0, "a": np.ones(10), "b": np.zeros([2, 2])}

        with H5File(name, "w") as f:
            f.save_dict_of_ndarrays(d)

        with H5File(name, "r") as f:
            d1 = f.load()

            for k, v in d.items():
                v1 = d1[k]

                self.assertTrue(np.allclose(v, v1))

        with H5File(name, "a") as f:
            d["times"] = 1.0
            f.save_dict_of_ndarrays(d)

            f.load(times_slice=[0, 2, 0.1])

    def test_functions(self):
        path = "test_functions0.h5"

        a = 1
        b = "str"
        c = np.ones(2)
        d = 10

        save_variables_h5(path, locals(), ("a", "b", "c"))
        variables1 = load_variables_h5(path)

        self.assertEqual(a, variables1["a"])
        self.assertEqual(b, variables1["b"])
        self.assertTrue(np.allclose(c, variables1["c"]))

        path = "test_functions1.h5"
        variables = {"a": a, "b": b, "c": c}
        save_variables_h5(path, variables)
        variables2 = load_variables_h5(path)

        self.assertEqual(a, variables2["a"])
        self.assertEqual(b, variables2["b"])
        self.assertTrue(np.allclose(c, variables2["c"]))


if __name__ == "__main__":
    unittest.main()
