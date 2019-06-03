import os
import sys
import unittest
from runpy import run_path
from shutil import rmtree

import numpy as np

from ..in_py import save_in_py


class TestInPy(unittest.TestCase):
    """Test fluiddyn.io.in_py module."""

    @classmethod
    def setUpClass(cls):
        cls._work_dir = "test_fluiddyn_io_in_py"
        if not os.path.exists(cls._work_dir):
            os.mkdir(cls._work_dir)

        os.chdir(cls._work_dir)

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        rmtree(cls._work_dir)

    def test(self):
        a = 1
        b = np.ones(2)
        c = np.ones([2, 2])
        d = 2
        save_in_py("file_globals.py", locals(), ("a", "b", "c"))

        # for python 3.7
        sys.path.insert(0, "")

        import file_globals as fg

        self.assertEqual(a, fg.a)
        self.assertTrue(np.allclose(b, fg.b))
        self.assertTrue(np.allclose(c, fg.c))

        d = {"a": a, "b": b, "c": d}
        save_in_py("file_dict.py", d)

        fd = run_path("file_dict.py")
        self.assertEqual(d["a"], fd["a"])
        self.assertTrue(np.allclose(d["b"], fd["b"]))
        self.assertTrue(np.allclose(d["c"], fd["c"]))


if __name__ == "__main__":
    unittest.main()
