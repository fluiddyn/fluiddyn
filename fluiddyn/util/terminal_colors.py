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


def print_fail(*args, **kwargs):
    """Print in bold with "FAIL" font"""
    if len(args) > 0:
        args = list(args)
        args[0] = FAIL + BOLD + args[0]
        args[-1] += ENDC

    print(*args, **kwargs)


def print_warning(*args, **kwargs):
    """Print with "WARNING" font"""
    if len(args) > 0:
        args = list(args)
        args[0] = WARNING + args[0]
        args[-1] += ENDC

    print(*args, **kwargs)
