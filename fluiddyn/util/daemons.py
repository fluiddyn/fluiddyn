"""
Daemons (:mod:`fluiddyn.util.daemons`)
======================================

"""

from __future__ import division, print_function

from builtins import object
from threading import Thread
from multiprocessing import Process, Value

from fluiddyn.util import Params


class BaseDaemon(object):
    def __init__(self, target=None, args=None, kwargs=None):
        self.daemon = True

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        self._target = target
        self._args = args
        self._kwargs = kwargs

    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run()
        method invokes the callable object passed to the object's
        constructor as the target argument, if any, with sequential
        and keyword arguments taken from the args and kwargs
        arguments, respectively.

        """
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def stop(self):
        self.keepgoing.value = 0


class DaemonThread(BaseDaemon, Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        Thread.__init__(self)
        super(DaemonThread, self).__init__(target, args, kwargs)
        # for compatibility with Process
        self.keepgoing = Params()
        self.keepgoing.value = True


class DaemonProcess(BaseDaemon, Process):
    def __init__(self, target=None, args=None, kwargs=None):
        Process.__init__(self)
        super(DaemonProcess, self).__init__(target, args, kwargs)
        self.keepgoing = Value('i', 1)
        # Then, acces to the value through self.keepgoing.value












# if __name__ == '__main__':
#     pass
