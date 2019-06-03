"""
Test dump utility
=================

"""

import os
import sys
import unittest
from shutil import rmtree

import h5netcdf
import h5py
import numpy as np

from ..dump import main
from ..redirect_stdout import stdout_redirected


class TestDump(unittest.TestCase):
    """Test fluiddyn.io.dump module."""

    _work_dir = "test_fluiddyn_io_dump"

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(cls._work_dir):
            os.mkdir(cls._work_dir)

        os.chdir(cls._work_dir)

        # create nc file
        with h5netcdf.File("mydata.nc", "w") as f:
            nx = 5
            f.dimensions = {"x": nx}
            v = f.create_variable("hello", ("x",), float)
            v[:] = np.ones(nx)
            v = f.create_variable("/group0/data", ("y",), data=np.arange(10))
            v.attrs["foo"] = "bar"

        # create hdf5 file
        with h5py.File("mydata.h5", "w") as f:
            f.attrs["a"] = "a"
            f.create_dataset("a", [0, 1])
            g = f.create_group("mygroup")
            g.attrs["a"] = "a"

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        rmtree(cls._work_dir)

    def test_nc(self):
        sys.argv = ["fluiddump", "mydata.nc"]
        with stdout_redirected():
            main()

    def test_h5(self):
        sys.argv = ["fluiddump", "mydata.h5"]
        with stdout_redirected():
            main()


if __name__ == "__main__":
    unittest.main()
