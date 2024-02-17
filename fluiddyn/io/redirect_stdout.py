"""Redirect stdout (:mod:`fluiddyn.io.redirect_stdout`)
==========================================================


"""

import contextlib
import io
import os
import pathlib
from typing import TextIO, Union

__all__ = ["stdout_redirected"]


@contextlib.contextmanager
def stdout_redirected(
    doit: bool = True,
    to: Union[str, pathlib.Path, TextIO, io.StringIO] = os.devnull,
):
    """Redirect stdout to os.devnull or a buffer

    Parameters
    ----------
    doit : bool

        Toggle redirection.

    to : StringIO instance or file object or str

        Buffer or file or file path to redirect to.

    """
    if not doit:
        yield  # Control to the with block
        return  # Do nothing and exit contextmanager

    with contextlib.ExitStack() as stack:
        if isinstance(to, (str, pathlib.Path)):
            to_file = stack.enter_context(open(to, "w+"))
        elif isinstance(to, (io.TextIOBase, io.StringIO)):
            to_file = to

        stack.enter_context(contextlib.redirect_stdout(to_file))
        yield  # Control to the with block
        # Exit the contextmanagers and finally, exit the stack
