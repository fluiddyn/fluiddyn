"""
Daemons (:mod:`fluiddyn.util.daemons`)
======================================

"""

from multiprocessing import Process, Value
from threading import Thread

from fluiddyn.util import Params


class BaseDaemon:
    """Base Daemon class

    You may override the `run` method in a subclass and use
    `self.keepgoing.value`, `self._args` and `self._kwargs`.

    """

    def __init__(self, target=None, args=None, kwargs=None):
        self.daemon = True

    def stop(self):
        self.keepgoing.value = 0


class DaemonThread(BaseDaemon, Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        Thread.__init__(self, target=target, args=args, kwargs=kwargs)
        super().__init__()
        # for compatibility with Process
        self.keepgoing = Params()
        self.keepgoing.value = True


class DaemonProcess(BaseDaemon, Process):
    def __init__(self, target=None, args=None, kwargs=None):
        Process.__init__(self, target=target, args=args, kwargs=kwargs)
        super().__init__()
        self.keepgoing = Value("i", 1)
