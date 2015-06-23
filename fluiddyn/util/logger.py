"""
Logger (:mod:`fluiddyn.util.logger`)
====================================

.. currentmodule:: fluiddyn.util.logger

Provides:

.. autoclass:: Logger
   :members:
   :private-members:

"""

from __future__ import print_function


class Logger(object):
    """Logger used for log and emails."""
    def __init__(self, email_to=None,
                 email_title='title',
                 email_delay=2*3600):
        self.email_to = email_to
        self.email_title = email_title
        self.email_delay = email_delay
        self._normal_print = print

    def print_log(self, *args, **kargs):
        """Replace the Python 3 print function."""
        self._normal_print('my print:')
        self._normal_print(*args, **kargs)
        with open('my_tmp_file.txt', 'a') as f:
            f.write(str(args)+str(kargs)+'\n')

    def send_mail_if_has_to(self):
        """Send an email if it has to send it..."""
        if True:
            pass


if __name__ == '__main__':

    logger = Logger()

    print = logger.print_log

    print('toto')

    print('no...', 'paf', end='')

    print('Hello...')
