"""Test fluidinfo
=================

"""

import os
import unittest
import warnings

from ..info import _get_parser, main, print_sys_info


class TestInfo(unittest.TestCase):
    """Test fluiddyn.util.info module."""

    @classmethod
    def tearDownClass(cls):
        filename = "sys_info.xml"
        if os.path.exists(filename):
            os.remove(filename)

    def test_save_info(self):
        """Equivalent to testing command `fluidinfo -s`."""
        parser = _get_parser()
        args = parser.parse_args(["-s"])
        main(args)

    def test_print_info(self):
        """Equivalent to testing command `fluidinfo -v`."""
        # Warnings arise from third-party packages
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
        print_sys_info(verbosity=1)

        warnings.resetwarnings()
