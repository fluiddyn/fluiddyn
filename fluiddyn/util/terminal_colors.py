"""Terminal color codes (:mod:`fluiddyn.util.terminal_colors`)
==============================================================

Defines string variables useful to print in color in a terminal.

"""

from __future__ import print_function

HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

_color_dict = vars()


def print_fail(*args, **kwargs):
    """Print in bold with "FAIL" font color."""
    if len(args) > 0:
        args = list(args)
        args[0] = FAIL + BOLD + args[0]
        args[-1] += ENDC

    print(*args, **kwargs)


def print_warning(*args, **kwargs):
    """Print with "WARNING" font colour."""
    if len(args) > 0:
        args = list(args)
        args[0] = WARNING + args[0]
        args[-1] += ENDC

    print(*args, **kwargs)


def _colorize(*args, **kwargs):
    """Wrap the args with a specified terminal font color."""
    try:
        color = kwargs.pop("color")
        try:
            bold = kwargs.pop("bold")
        except KeyError:
            bold = False

        color = _color_dict[color]

        if len(args) > 0:
            args = list(args)
            if bold:
                color += BOLD
            args[0] = "{}{}".format(color, args[0])
            args[-1] += ENDC

    finally:
        return args, kwargs


def cstring(*args, **kwargs):
    """Return a colored string.

    Parameters
    ----------
    args : iterable of str
    bold : bool
    color : str, {'HEADER', 'OKBLUE', 'OKGREEN', 'WARNING', 'FAIL', 'ENDC',
                  'BOLD', 'UNDERLINE'}
        Terminal color to use.

    """
    args, kwargs = _colorize(*args, **kwargs)
    cstr = " ".join(args)
    return cstr


def cprint(*args, **kwargs):
    """Print with a specified terminal font color.

    Parameters
    ----------
    args : iterable
        To be passed into print_function.
    bold : bool
    color : str, {'HEADER', 'OKBLUE', 'OKGREEN', 'WARNING', 'FAIL', 'ENDC',
                  'BOLD', 'UNDERLINE'}
        Terminal color to use.

    """
    args, kwargs = _colorize(*args, **kwargs)
    print(*args, **kwargs)
