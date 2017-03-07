"""
Test hdf5 module
================

"""

import unittest
# import os
# from shutil import rmtree

import numpy as np

from .. import util


class TestUtil(unittest.TestCase):
    """Test fluiddyn.util.util module."""

    def test_(self):

        util.import_class('fluiddyn.output.figs', 'Figures')

        util.time_as_str(decimal=0)

        # util.create_object_from_file()
        util.run_from_ipython()

        util.print_memory_usage('test')

        util.print_size_in_Mo(np.arange(4))

        with util.print_options():
            pass

        util.config_logging()

if __name__ == '__main__':
    unittest.main()
