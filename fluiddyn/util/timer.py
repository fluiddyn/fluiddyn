"""
Clocking timer (:mod:`fluiddyn.util.timer`)
===========================================

.. currentmodule:: fluiddyn.util.timer

Provides:

.. autoclass:: Timer
   :members:
   :private-members:

.. autoclass:: TimerIrregular
   :members:
   :private-members:

"""

from __future__ import division, print_function

from builtins import range
from builtins import object
import time
from datetime import timedelta


def parse_timestamp(timestr):
    """Converts a timestamp to a time.struct_time object."""

    try:
        time_struct = time.strptime(timestr, "%d-%H:%M:%S")
    except ValueError:
        time_struct = time.strptime(timestr, "%H:%M:%S")

    return time_struct


def timestamp_to_seconds(timestr):
    """Converts a timestamp to total seconds."""
    ts = parse_timestamp(timestr)
    # Handle both formats:
    days = ts.tm_yday if '-' in timestr else (ts.tm_yday - 1)
    td = timedelta(
        hours=ts.tm_hour, minutes=ts.tm_min, seconds=ts.tm_sec,
        days=days)

    return int(td.total_seconds())


def time_gteq(timestr1, timestr2):
    """Compares two timestamps strings."""

    time1 = parse_timestamp(timestr1)
    time2 = parse_timestamp(timestr2)
    return (time1 >= time2)


class Timer(object):
    """Timer ticking with a particular period.

    Parameters
    ----------

    time_between_ticks : float
       Period between the ticks (in s).

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
        this_period = int((tnow - self.tstart) / self.time_between_ticks)
        if this_period == self.last_period:
            self.last_period = this_period + 1
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

    Parameters
    ----------

    times_ticks: (sorted) sequence
      A sequence of times (in second), which can be irregular.

    """
    def __init__(self, times_ticks):
        t0 = times_ticks[0]
        self.times_ticks = [ti - t0 for ti in times_ticks[1:]]
        self.tstart = time.time()

    def wait_tick(self):
        """Block till the next tick."""
        tnow = time.time() - self.tstart
        if self.times_ticks:
            while self.times_ticks and self.times_ticks[0] - tnow < 0:
                self.times_ticks = self.times_ticks[1:]
        if self.times_ticks:
            tsleep = self.times_ticks[0] - tnow
            self.times_ticks = self.times_ticks[1:]
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

    print(tend - tstart)
