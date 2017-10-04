"""
Test info module
================

"""
import unittest
from ..info import print_sys_info
from ...io.redirect_stdout import stdout_redirected


class TestInfor(unittest.TestCase):
    """Test fluiddyn.util.info module."""

    def test_print_info(self):
        """Equivalent to testing command `fluidinfo`."""
        with stdout_redirected():
            print_sys_info()
