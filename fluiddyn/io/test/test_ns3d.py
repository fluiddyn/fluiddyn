"""
Test ns3d module
====================

"""

import os
import unittest
from glob import glob
from shutil import copy, rmtree

from ..ns3d import NS3DFieldFile, NS3DForcingInfoFile
from ..redirect_stdout import stdout_redirected

input_dir = os.path.join(os.path.dirname(__file__), "ns3d_files")
input_files = glob(os.path.join(input_dir, "*"))

try:
    import pyfftw

    fftw_import_error = False
except ImportError:
    fftw_import_error = True


@unittest.skipIf(fftw_import_error, "pyfftw ImportError")
class TestNS3D(unittest.TestCase):
    """Test fluiddyn.io.ns3d module."""

    def setUp(self):
        self._work_dir = "test_fluiddyn_io_ns3d"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        for path in input_files:
            copy(path, self._work_dir)

        os.chdir(self._work_dir)

        self.path_forcing_info_big = (
            "forcing_2D_info.in_L=30x30_nh=48_expLO_"
            "b=1.8_Ti=7.0_nbgene=4_d=4_T=28"
        )
        self.path_forcing_info_little = (
            self.path_forcing_info_big + "_little-endian"
        )
        self.path_field = "PV.t=0000.000"

    def tearDown(self):
        os.chdir("..")
        rmtree(self._work_dir)

    def test_forcing_info(self):
        f_b = NS3DForcingInfoFile(self.path_forcing_info_big)
        f_l = NS3DForcingInfoFile(self.path_forcing_info_little)

        self.assertEqual(f_l.byteorder, "little")
        self.assertEqual(f_b.byteorder, "big")

        with stdout_redirected():
            f_l.save_with_byteorder_changed()

    def test_field(self):
        f = NS3DFieldFile(self.path_field)
        f.read_xy()
        f.read_field()
        with stdout_redirected():
            f.save_with_byteorder_changed()
            f.save_with_resol_changed(2, 2, 2)


if __name__ == "__main__":
    unittest.main()
