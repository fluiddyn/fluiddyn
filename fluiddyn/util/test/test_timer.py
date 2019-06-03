"""
Test timer module
=================

"""

import unittest

from ..timer import Timer, TimerIrregular, TimeStr, time_gteq


class TestTimer(unittest.TestCase):
    """Test fluiddyn.util.timer module."""

    def test_timer(self):
        time_gteq("16:20:10", "17:20:10")

        timer = Timer(0.01)
        timer.wait_tick()

        timer = TimerIrregular([0, 0.01])
        timer.wait_tick()

    def test_timestr(self):
        assert TimeStr("1:20") == TimeStr("00:01:20")
        assert TimeStr("1:20") == "1-00:01:20"
        assert TimeStr("1:20") != "00:01:00"
        assert TimeStr("1:20") <= "00:01:20"
        assert TimeStr("1:20") < "2-00:01:20"
        assert TimeStr("1:20") >= "00:01:00"
        assert TimeStr("1:20") > "20"


if __name__ == "__main__":
    unittest.main()
