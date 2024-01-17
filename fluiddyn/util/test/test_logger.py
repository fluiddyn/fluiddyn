import os
import smtplib
import sys
import unittest

import matplotlib.pyplot as plt

from ..logger import Logger


class UnitTestException(Exception):
    pass


def mySMTP(*args, **kwargs):
    raise UnitTestException


# monkey patch
smtplib.SMTP = mySMTP


class TestFFTW1DReal2Complex(unittest.TestCase):
    def tearDown(self):
        os.remove("storage_file.txt")

    def test_logger(self):
        logger = Logger(
            "storage_file.txt",
            "test@test.org",
            "test@test.com",
            email_title="test",
            email_delay=0.02,
        )
        logger.print_log("")

        with self.assertRaises(UnitTestException):
            raise UnitTestException

        if "win" in sys.platform:
            return

        with self.assertRaises(UnitTestException):
            logger.send_email_if_has_to(name_exception="", figures=[plt.figure()])


if __name__ == "__main__":
    unittest.main()
