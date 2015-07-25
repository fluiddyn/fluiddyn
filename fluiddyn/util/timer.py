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

import time


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


if __name__ == '__main__':

    tstart = time.time()

    timer = Timer(2)
    for it in xrange(10):
        # print(it, end=' ')

        # time.sleep(float(it)/5)

        # print('before timer.wait_tick()', time.time()-timer.tstart)
        timer.wait_tick()
        # print('after  timer.wait_tick()', time.time()-timer.tstart)

    tend = time.time()

    print(tend-tstart)
