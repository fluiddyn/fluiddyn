import os
import sys
import unittest

from fluiddyn.io import stdout_redirected
from fluiddyn.util import mpi

from .. import main

here = os.path.abspath(os.path.dirname(__file__))


class TestsBench(unittest.TestCase):
    def test2d(self):
        with stdout_redirected():
            if mpi.rank > 0:
                return

            path = os.path.join(here, "courant.m")
            args = ["fluidmat2py ", path]
            sys.argv = args
            main()


if __name__ == "__main__":
    unittest.main()
