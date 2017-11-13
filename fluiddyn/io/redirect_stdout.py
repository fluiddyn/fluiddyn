"""Redirect stdoutput (:mod:`fluiddyn.io.redirect_stdout`)
==========================================================


"""

import os
import sys
from contextlib import contextmanager
if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO


def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd


@contextmanager
def stdout_redirected(doit=True, to=os.devnull, stdout=None):
    """Redirect stdout to os.devnull

    Parameters
    ----------
    doit : bool

        Toggle redirection.

    to : StringIO instance or file object or str

        Buffer or file or file path to redirect to.

    stdout : file object

        File from which output is redirected.

    """
    if not doit:
        yield
        return

    if stdout is None:
        stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    # NOTE: `copied` is inheritable on Windows when duplicating a standard
    # stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        if isinstance(to, StringIO):
            sys.stdout = to
            try:
                yield to
            finally:
                to.flush()
                sys.stdout = stdout
        else:
            try:
                os.dup2(fileno(to), stdout_fd)  # $ exec >&to
            except ValueError:  # filename
                with open(to, 'wb') as to_file:
                    os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to

            try:
                yield stdout  # allow code to be run with the redirected stdout
            finally:
                # restore stdout to its previous value
                # NOTE: dup2 makes stdout_fd inheritable unconditionally
                stdout.flush()
                os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied
