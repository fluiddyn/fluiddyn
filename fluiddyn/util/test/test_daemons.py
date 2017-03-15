
import unittest

from ..daemons import DaemonThread, DaemonProcess


def func():
    pass


class TestDaemonds(unittest.TestCase):
    """Test fluiddyn.util.daemons module."""

    def test_daemons(self):
        dt = DaemonThread(func)
        dt.run()
        dt.stop()
        dp = DaemonProcess(func)
        dp.run()
        dp.stop()

if __name__ == '__main__':
    unittest.main()
