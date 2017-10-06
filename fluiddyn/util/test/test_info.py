"""
Test info module
================

"""
import unittest
from ..info import print_sys_info
from ...io.redirect_stdout import stdout_redirected
import warnings


class TestInfo(unittest.TestCase):
    """Test fluiddyn.util.info module."""

    def test_print_info(self):
        """Equivalent to testing command `fluidinfo -vvv`."""
        # Warnings arise from third-party packages
        warnings.filterwarnings('ignore', category=UserWarning)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        warnings.filterwarnings('ignore', category=PendingDeprecationWarning)
        warnings.filterwarnings('ignore', category=ResourceWarning)
        with stdout_redirected():
            print_sys_info(verbosity=1)

        warnings.resetwarnings()
