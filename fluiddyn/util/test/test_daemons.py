import unittest
from time import sleep

from ..daemons import DaemonProcess, DaemonThread


def func(self):
    assert self._args[0] == "hello"
    assert list(self._kwargs.keys())[0] == "word"
    while self.keepgoing.value:
        print("!", end="")
        sleep(0.01)


class DThread(DaemonThread):
    def run(self):
        func(self)


class DProcess(DaemonProcess):
    def run(self):
        func(self)


class TestDaemonds(unittest.TestCase):
    """Test fluiddyn.util.daemons module."""

    def test_daemons(self):
        dt = DThread(args=("hello",), kwargs={"word": 1})
        dt.start()
        sleep(0.02)
        dt.stop()
        dp = DProcess(args=("hello",), kwargs={"word": 1})
        dp.start()
        sleep(0.02)
        dp.stop()


if __name__ == "__main__":
    unittest.main()
