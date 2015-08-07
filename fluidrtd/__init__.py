"""Utilities for readthedocs.org
================================


"""


import os
import sys

try:
    from unittest.mock import MagicMock
except ImportError:
    # Python 2
    from mock import Mock as MagicMock


on_rtd = os.environ.get('READTHEDOCS')


def mock_modules(modules):

    class Mock(MagicMock):
        @classmethod
        def __getattr__(cls, name):
            return Mock()

    sys.modules.update((mod_name, Mock()) for mod_name in modules)
