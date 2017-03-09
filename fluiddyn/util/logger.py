"""
Logger sending emails (:mod:`fluiddyn.util.logger`)
===================================================

Provides:

.. autoclass:: Logger
   :members:
   :private-members:

"""

from __future__ import print_function

from builtins import str
from builtins import object
import os
import sys
import time
import traceback

from fluiddyn.util import time_as_str
from fluiddyn.util.mail import send_email


class Logger(object):
    """Logger that can send emails."""
    def __init__(self, path='log.txt',
                 email_to=None, email_from=None,
                 email_title='title',
                 email_delay=2*3600,
                 email_server='localhost'):

        if email_delay is None:
            email_delay = 2*3600

        self.path = path
        self.email_to = email_to
        self.has_to_send_email = email_to is not None

        self.email_from = email_from
        self.email_title = email_title
        self.email_delay = email_delay
        self.email_server = email_server
        self._normal_print = print
        self.time_last_email = time.time() - self.email_delay

        base, ext = os.path.splitext(self.path)
        self.path_logerr = base + '_stderr' + ext

        old_excepthook = sys.excepthook

        def my_excepthook(ex_cls, ex, tb):
            name_exception = ex_cls.__name__
            str_time = time_as_str()

            with open(self.path, 'a') as f:
                f.write(
                    'Python error ({}) at {}\n'.format(
                        name_exception, str_time))

            with open(self.path_logerr, 'a') as f:
                f.write('-' * 40 +
                        '\nError at {}\n'.format(str_time) +
                        '-' * 40 + '\n' +
                        ''.join(traceback.format_exception(ex_cls, ex, tb)) +
                        '\n')

            if self.has_to_send_email and ex_cls != KeyboardInterrupt:
                self.send_email(name_exception=name_exception)

            old_excepthook(ex_cls, ex, tb)

        sys.excepthook = my_excepthook

    def print_log(self, *args, **kargs):
        """Replaces the Python 3 print function."""
        self._normal_print(*args, **kargs)
        self.write(*args, **kargs)

    def write(self, *args, **kargs):
        end = kargs.setdefault('end', '\n')
        with open(self.path, 'a') as f:
            f.write(' '.join([str(arg) for arg in args]) + end)

    def send_email_if_has_to(self, figures=None):
        """Sends an email if no email was sent recently."""
        if self.has_to_send_email:
            if time.time() - self.time_last_email >= self.email_delay:
                self.send_email(figures=figures)
                self.time_last_email = time.time()

    def send_email(self, name_exception=None, figures=None):
        """Sends the content of the storage file as an email"""
        with open(self.path, 'r') as f:
            txt = f.read()

        if name_exception is None:
            subject = self.email_title
        else:
            subject = name_exception + ', ' + self.email_title

            if os.path.exists(self.path_logerr):
                with open(self.path_logerr, 'r') as f:
                    txt += f.read()

        if figures is None:
            files = None
        else:
            path_tmp = '/tmp/fluiddyn_' + time_as_str()
            os.makedirs(path_tmp)
            files = []
            for i, fig in enumerate(figures):
                fname = 'fig_{}.png'.format(i)
                path = os.path.join(path_tmp, fname)
                fig.savefig(path)
                files.append(path)

        send_email(
            subject, txt,
            address_recipients=self.email_to,
            address_sender=self.email_from,
            server=self.email_server,
            files=files)

        print('Email sent at ' + time_as_str())

    # def __del__(self):
    #     sys.excepthook = self._excepthook


if __name__ == '__main__':
    logger = Logger('storage_file', '@ens-lyon.org',
                    '@legi.cnrs.fr',
                    email_title='itworks', email_delay=9)
    print = logger.print_log
    print('fluiddyn, blablabla')

    logger.send_email_if_has_to()
    logger.send_email_if_has_to()
    time.sleep(10)
    logger.send_email_if_has_to()
    logger.send_email_if_has_to()
