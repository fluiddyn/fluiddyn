"""
Clocking timer (:mod:`fluiddyn.util.timer`)
===========================================

.. currentmodule:: fluiddyn.util.timer

Provides:

.. autoclass:: Timer
   :members:
   :private-members:

"""

from __future__ import division, print_function

from builtins import range
from builtins import object
import time


def parse_timestamp(str):
    """Converts a timestamp to a time.struct_time object."""

    try:
        time_struct = time.strptime(str, "%d-%H:%M:%S")
    except ValueError:
        time_struct = time.strptime(str, "%H:%M:%S")

    return time_struct


def time_gteq(timestr1, timestr2):
    """Compares two timestamps strings and returns a greater than or equals comparison."""

    time1 = parse_timestamp(timestr1) 
    time2 = parse_timestamp(timestr2)
    return (time1 >= time2)


class Timer(object):
    """Timer ticking with a particular period.

    Attributes
    ----------

    time_between_ticks : float
       Period between the ticks.

"""
    def __init__(self, time_between_ticks):
        self.time_between_ticks = time_between_ticks
        self.tstart = time.time()
        self.last_period = -1

    def wait_tick(self):
        """Block till the next tick."""
        tnow = time.time()
        tsleep = (self.time_between_ticks -
                  (tnow - self.tstart) % self.time_between_ticks)
        this_period = int((tnow - self.tstart)/self.time_between_ticks)
        if this_period == self.last_period:
            self.last_period = this_period+1
            tsleep += self.time_between_ticks
        else:
            self.last_period = this_period

        time.sleep(tsleep)
        return time.time() - self.tstart

    def restart(self):
        self.tstart = time.time()

    def get_time_till_start(self):
        return time.time() - self.tstart


class TimerIrregular(Timer):
    """Timer ticking for a numpy array of time.

    This time array can be irregular.
    """
    def __init__(self, timing):
        self.timing = [ti - min(timing) for ti in timing[1:]]
        self.tstart = time.time()

    def wait_tick(self):
        """Block till the next tick."""
        tnow = time.time() - self.tstart
        if self.timing:
            while self.timing and self.timing[0] - tnow < 0:
                self.timing = self.timing[1:]
        if self.timing:
            tsleep = self.timing[0] - tnow
            self.timing = self.timing[1:]
            time.sleep(tsleep)
        return time.time() - self.tstart


if __name__ == '__main__':

    tstart = time.time()

    timer = Timer(2)
    for it in range(10):
        # print(it, end=' ')

        # time.sleep(float(it)/5)

        # print('before timer.wait_tick()', time.time()-timer.tstart)
        timer.wait_tick()
        # print('after  timer.wait_tick()', time.time()-timer.tstart)

    tend = time.time()

    print(tend-tstart)
