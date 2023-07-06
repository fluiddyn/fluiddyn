"""
Test hdf5 module
================

"""

import os
import unittest
from shutil import rmtree

import h5py
import numpy as np

from ...io.redirect_stdout import stdout_redirected
from .. import util
from ..terminal_colors import cprint, cstring, print_fail, print_warning
from ..userconfig import load_user_conf_files


def expectedFailureIf(condition):
    if condition:
        return unittest.expectedFailure
    else:
        return lambda func: func


class MyObject:
    def __init__(self, str_path=None, *args, **kwargs):
        pass

    def save(self, path):
        with h5py.File(path, "w") as f:
            f.attrs["class_name"] = "MyObject"
            f.attrs["module_name"] = "fluiddyn.util.test.test_util"


class TestUtil(unittest.TestCase):
    """Test fluiddyn.util.util module."""

    @classmethod
    def setUpClass(cls):
        cls._work_dir = "test_fluiddyn_util_util"
        if not os.path.exists(cls._work_dir):
            os.mkdir(cls._work_dir)

        os.chdir(cls._work_dir)

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        rmtree(cls._work_dir)

    def test_util(self):
        util.import_class("fluiddyn.output.figs", "Figures")

        util.time_as_str(decimal=1)

        util.is_run_from_ipython()
        util.is_run_from_jupyter()
        with stdout_redirected():
            util.print_memory_usage("test")
            util.print_size_in_Mo(np.arange(4))
            util.print_size_in_Mo(np.arange(4), string="test")
            print_fail("")
            print_warning("")
            cprint("bar", color="RED")
            cprint.header("header")
            cprint.light_blue("light_blue")
            cprint.light_green("light_green")
            cprint.light_gray("light_gray")
            cprint.warning("warning")
            cprint.fail("fail")
            cprint.black("black")
            cprint.red("bar", bold=True)
            cprint.green("green")
            cprint.yellow("yellow")
            cprint.blue("blue")
            cprint.magenta("magenta")
            cprint.cyan("cyan")
            cprint.white("white")
            cstring("foo", color="GREEN")

        with util.print_options():
            pass

        util.config_logging()
        load_user_conf_files()

    def test_copy_me(self):
        # Relative path before chdir are supplied with Python 2
        util.copy_me_in(os.curdir)

    def test_mod_date(self):
        # Relative path before chdir are supplied with Python 2
        util.modification_date(os.path.dirname(__file__))

    def test_create_object(self):
        o = MyObject()
        o.save("myobject.h5")
        util.create_object_from_file("object")


if __name__ == "__main__":
    unittest.main()
