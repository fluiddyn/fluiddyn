"""Utilities for readthedocs.org
================================


"""


import os
import sys

try:
    from unittest.mock import Mock
except ImportError:
    # Python 2
    from mock import Mock


on_rtd = os.environ.get('READTHEDOCS')


def mock_modules(modules):

    class MyMock(Mock):
        @classmethod
        def __getattr__(cls, name):
            return Mock()

    sys.modules.update((mod_name, MyMock()) for mod_name in modules)
