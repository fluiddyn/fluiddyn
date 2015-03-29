"""
Deamons (:mod:`fluiddyn.util.deamons`)
======================================

"""

from __future__ import division, print_function

from threading import Thread
from multiprocessing import Process, Value

from fluiddyn.util import Params

class Daemon(object):
    def __init__(self):
        self.daemon = True
    def stop(self):
        self.keepgoing.value = 0

class DaemonThread(Thread, Daemon):
    def __init__(self):
        super(DaemonThread, self).__init__()
        Daemon.__init__(self)
        # for compatibility with Process
        self.keepgoing = Params()
        self.keepgoing.value = True

class DaemonProcess(Process, Daemon):
    def __init__(self):
        super(DaemonProcess, self).__init__()
        Daemon.__init__(self)
        self.keepgoing = Value('i', 1)
        # Then, acces to the value through self.keepgoing.value












# if __name__ == '__main__':
#     pass
