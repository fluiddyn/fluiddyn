"""
Test timer module
=================

"""

import unittest

from ..timer import Timer, TimerIrregular, time_gteq


class TestTimer(unittest.TestCase):
    """Test fluiddyn.util.timer module."""

    def test_timer(self):
        time_gteq('16:20:10', '17:20:10')

        timer = Timer(0.01)
        timer.wait_tick()

        timer = TimerIrregular([0, 0.01])
        timer.wait_tick()

if __name__ == '__main__':
    unittest.main()
