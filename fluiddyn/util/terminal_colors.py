"""Terminal color codes (:mod:`fluiddyn.util.terminal_colors`)
==============================================================

Defines string variables useful to print in color in a terminal.

"""

from __future__ import print_function

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


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
        color = kwargs.pop('color')
        color = _color_dict[color]
    except KeyError:
        return args, kwargs

    if len(args) > 0:
        args = list(args)
        args[0] = '{}{}'.format(WARNING, args[0])
        args[-1] = '{}{}'.format(args[-1], ENDC)

    return args, kwargs


def cstring(*args, **kwargs):
    """Return a colored string.

    Parameters
    ----------
    args : iterable of str
    color : str, {'HEADER', 'OKBLUE', 'OKGREEN', 'WARNING', 'FAIL', 'ENDC',
                  'BOLD', 'UNDERLINE'}
        Terminal color to use.

    """
    args, kwargs = _colorize(*args, **kwargs)
    cstr = ' '.join(args)
    return cstr


def cprint(*args, **kwargs):
    """Print with a specified terminal font color.

    Parameters
    ----------
    args : iterable
        To be passed into print_function.

    color : str, {'HEADER', 'OKBLUE', 'OKGREEN', 'WARNING', 'FAIL', 'ENDC',
                  'BOLD', 'UNDERLINE'}
        Terminal color to use.

    """
    args, kwargs = _colorize(*args, **kwargs)
    print(*args, **kwargs)
