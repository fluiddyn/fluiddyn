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

import time
import smtplib
from email.mime.text import MIMEText

class Logger(object):
    """Logger used for log and emails."""
    def __init__(self, storage_file_name='storage_file', email_from=None, email_to=None,
                 email_title='title',
                 email_delay=2*3600):
        self.storage_file_name = storage_file_name
        self.email_from = email_from
        self.email_to = email_to
        self.email_title = email_title
        self.email_delay = email_delay
        self._normal_print = print
        self.time_last_email = time.clock() - self.email_delay

    def print_log(self, *args, **kargs):
        """Replaces the Python 3 print function."""
        self._normal_print(*args, **kargs)

        end = kargs.setdefault('end', '\n')
        with open(self.storage_file_name, 'a') as f:
            f.write(' '.join([str(arg) for arg in args]) + end)

    def send_mail_if_has_to(self):
        """Sends an email if no email was sent recently."""
        if time.time() - self.time_last_email >= self.email_delay:
            self.send_mail()
            self.time_last_email = time.time()

    def send_mail(self):
        """Sends the content of the storage file as an email"""
        with open(self.storage_file_name, 'rb') as fp:
            msg = MIMEText(fp.read())
        msg['Subject'] = self.email_title
        msg['From'] = self.email_from
        msg['To'] = self.email_to

        s = smtplib.SMTP('localhost')
        s.sendmail(self.email_from, [self.email_to], msg.as_string())
        s.quit()


if __name__ == '__main__':
    logger = Logger('storage_file', 'aymeric.rodriguez@legi.cnrs.fr',
                    'aymeric.rodriguez@minesdedouai.fr', 'itworks', 9)
    print = logger.print_log
    print('toto')
    print('no...', 'paf', end='')
    print('Hellooo...')

    logger.send_mail_if_has_to()
    logger.send_mail_if_has_to()
    time.sleep(10)
    logger.send_mail_if_has_to()
    logger.send_mail_if_has_to()
