"""
Test txt functions
==================

"""

import os
import unittest
from shutil import rmtree

from ..txt import quantities_from_txt_file, save_quantities_in_txt_file

txt_example = """
zekfzlnfk

zklflzefk

1  3. 1

2   5.
3  4.  9
"""

t_example = ([1, 2, 3], [3.0, 5.0, 4.0], [1, 9])


class TestTxt(unittest.TestCase):
    """Test fluiddyn.io.txt module."""

    def setUp(self):
        self._work_dir = "test_fluiddyn_io_txt"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        os.chdir(self._work_dir)

        self.path_in = "path_in"

        with open(self.path_in, "w") as f:
            f.write(txt_example)

    def tearDown(self):
        os.chdir("..")
        rmtree(self._work_dir)

    def test_txt(self):

        t = quantities_from_txt_file(self.path_in)

        for i, l_example in enumerate(t_example):
            for j, a in enumerate(l_example):
                self.assertEqual(a, t[i][j])

        t = ([1, 2, 3],) * 3

        save_quantities_in_txt_file("path_out", t)


if __name__ == "__main__":
    unittest.main()
