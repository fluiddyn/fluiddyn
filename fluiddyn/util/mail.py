"""Mail (:mod:`fluiddyn.util.mail`)
===================================

Provides:

.. autofunction:: send_email

"""

from __future__ import print_function

import os
import smtplib
import socket

# For guessing MIME type based on file name extension
import mimetypes

from email import encoders
from email.utils import formatdate

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage


def send_email(subject, txt, address_recipients, address_sender=None,
               server='localhost', files=None):
    """Send an email.

    Inspired by an example in
    https://docs.python.org/2/library/email-examples.html

    Parameters
    ----------

    subject : str or unicode

      The subject of the email.

    txt : {str, unicode}

      The text of the email.

    address_recipients : {str, list}

      The recipient(s) of the mail.

    address_sender : {None, str}

      The sender.

    server : {None, str}

      A string defining a SMTP server (for example 'localhost:25')

    files : list

      A list of files that have to be attached.

    Notes
    -----

    You may have to start a SMTP local server.

    """

    if isinstance(address_recipients, str):
        address_recipients = [address_recipients]

    assert isinstance(address_recipients, list)

    if address_sender is None:
        address_sender = address_recipients[0]

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = address_sender
    msg['To'] = ', '.join(address_recipients)
    msg['Date'] = formatdate(localtime=True)

    # main part: the text
    part = MIMEText(txt)
    msg.attach(part)

    if files is None:
        files = []

    # sub parts: the enclosed files
    for path in files:
        # Guess the content type based on the file's extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip'd or compressed files.
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded
            # (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            if maintype == 'text':
                # Note: we should handle calculating the charset
                part = MIMEText(fp.read(), _subtype=subtype)
            elif maintype == 'image':
                part = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == 'audio':
                part = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                part = MIMEBase(maintype, subtype)
                part.set_payload(fp.read())
                # Encode the payload using Base64
                encoders.encode_base64(part)
        # set the filename parameter
        part.add_header('Content-Disposition', 'attachment',
                        filename=os.path.split(path)[1])

        msg.attach(part)
    try:
        server = smtplib.SMTP(host=server)
    except socket.gaierror as e:
        print('socket.gaierror: you may have to setup a local SMTP server.')
        raise e
    server.sendmail(address_sender, address_recipients, msg.as_string())
    server.quit()


if __name__ == '__main__':

    send_email('email test', 'blablabla\n'*3, 'pierre.augier@legi.cnrs.fr')
