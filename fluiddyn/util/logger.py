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

import os
import sys
import time
import smtplib
from email.mime.text import MIMEText
import traceback

from fluiddyn.util import time_as_str


class Logger(object):
    """Logger used for log and emails."""
    def __init__(self, path='log.txt',
                 email_to=None, email_from=None,
                 email_title='title',
                 email_delay=2*3600,
                 email_server='localhost'):

        if email_delay is None:
            email_delay = 2*3600

        self.path = path
        self.email_from = email_from or email_to
        self.email_to = email_to
        self.email_title = email_title
        self.email_delay = email_delay
        self.email_server = email_server
        self._normal_print = print
        self.time_last_email = time.time() - self.email_delay

        base, ext = os.path.splitext(self.path)
        self.path_logerr = base + '_stderr' + ext

        if self.email_to is None:
            send_email = False
        else:
            send_email = self.send_email

        old_excepthook = sys.excepthook

        def my_excepthook(ex_cls, ex, tb):
            str_ex = ex_cls.__name__
            str_time = time_as_str()

            with open(self.path, 'a') as f:
                f.write(
                    'Python error ({}) at {}\n'.format(str_ex, str_time))

            with open(self.path_logerr, 'a') as f:
                f.write('-' * 40 +
                        '\nError at {}\n'.format(str_time) +
                        '-' * 40 + '\n' +
                        ''.join(traceback.format_exception(ex_cls, ex, tb)) +
                        '\n')

            if send_email and ex_cls != KeyboardInterrupt:
                self.send_email(exception=str_ex)

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

    def send_email_if_has_to(self):
        """Sends an email if no email was sent recently."""
        if self.email_to is not None:
            if time.time() - self.time_last_email >= self.email_delay:
                self.send_email()
                self.time_last_email = time.time()

    def send_email(self, exception=False):
        """Sends the content of the storage file as an email"""
        with open(self.path, 'rb') as f:
            txt = f.read()

        if not exception:
            subject = self.email_title
        else:
            subject = exception + ', ' + self.email_title

            if os.path.exists(self.path_logerr):
                with open(self.path_logerr, 'rb') as f:
                    txt += f.read()

        msg = MIMEText(txt)
        msg['Subject'] = subject
        msg['From'] = self.email_from
        msg['To'] = self.email_to

        s = smtplib.SMTP(self.email_server)
        s.sendmail(self.email_from, [self.email_to], msg.as_string())
        s.quit()
        print('Email sent at ' + time_as_str())

    # def __del__(self):
    #     sys.excepthook = self._excepthook


if __name__ == '__main__':
    logger = Logger('storage_file', 'aymeric.rodriguez@minesdedouai.fr',
                    'aymeric.rodriguez@legi.cnrs.fr', 'itworks', 9)
    print = logger.print_log
    print('toto')
    print('no...', 'paf', end='')
    print('Hellooo...')

    logger.send_email_if_has_to()
    logger.send_email_if_has_to()
    time.sleep(10)
    logger.send_email_if_has_to()
    logger.send_email_if_has_to()
