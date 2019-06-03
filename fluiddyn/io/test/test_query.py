"""
Test query module
=================

"""

import builtins
import subprocess
import unittest
from contextlib import contextmanager

from .. import query
from ...io.redirect_stdout import stdout_redirected


def do_nothing(*args, **kwargs):
    pass


@contextmanager
def mock_input(mock):
    # mocking write works only in Python 3
    # original_write = sys.stdout.write
    original_input = builtins.input
    # sys.stdout.write = do_nothing
    builtins.input = lambda: mock
    yield

    # sys.stdout.write = original_write
    builtins.input = original_input


@contextmanager
def mock_call():
    original_call = subprocess.call
    subprocess.call = do_nothing
    yield

    subprocess.call = original_call


class TestQuery(unittest.TestCase):
    """Test fluiddyn.io.query module."""

    def test_query(self):
        with mock_input("1.2"):
            self.assertEqual(1.2, query.query_number(""))

        with mock_input("test"):
            with stdout_redirected():
                query.query("?", "t")

        with mock_input("yes"):
            with mock_call():
                with stdout_redirected():
                    query.run_asking_agreement("ls")


if __name__ == "__main__":
    unittest.main()
