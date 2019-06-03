"""
Test mpi module
===============

"""

import io
import os
import unittest
from shutil import rmtree

import numpy as np

from ...io.redirect_stdout import stdout_redirected
from ..mpi import _mpi_type, nb_proc, printby0, rank


class TestMPI(unittest.TestCase):
    """Test fluiddyn.util.mpi module."""

    @classmethod
    def barrier(cls):
        if _mpi_type is not None:
            from ..mpi import comm

            comm.barrier()

    @classmethod
    def setUpClass(cls):
        cls._work_dir = "test_fluiddyn_util_mpi"
        if rank == 0:
            if not os.path.exists(cls._work_dir):
                os.mkdir(cls._work_dir)

        cls.barrier()
        os.chdir(cls._work_dir)

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        cls.barrier()
        if rank == 0:
            rmtree(cls._work_dir)

    def test_print(self):
        """Test fluiddyn.util.mpi.printby0 to write to a buffer."""

        msg_write = "test by rank ="
        output = io.StringIO()
        with stdout_redirected(to=output):
            printby0(msg_write, rank, end="")

        output.flush()
        self.barrier()
        msg_read = output.getvalue()
        output.close()

        msg_expected = msg_write + " 0" if rank == 0 else ""
        self.assertEqual(msg_read, msg_expected)

    @unittest.skipIf(nb_proc == 1, "Meant for testing if mpi4py works.")
    def test_scatter_gather(self):
        """Test MPI Scatter and Gather functions for numpy objects."""

        from ..mpi import comm, MPI

        N_loc = 4
        N = N_loc * nb_proc
        if comm.rank == 0:
            arr = np.arange(N, dtype=np.float64)
        else:
            arr = np.empty(N, dtype=np.float64)

        arr_loc = np.empty(N_loc, dtype=np.float64)
        comm.Scatter([arr, MPI.DOUBLE], [arr_loc, MPI.DOUBLE])

        arr_loc *= 2
        if comm.rank == 0:
            arr2 = np.empty(N, dtype=np.float64)
        else:
            arr2 = None

        comm.Gather([arr_loc, MPI.DOUBLE], [arr2, MPI.DOUBLE])

        if rank == 0:
            np.testing.assert_array_equal(arr * 2, arr2)


if __name__ == "__main__":
    unittest.main()
