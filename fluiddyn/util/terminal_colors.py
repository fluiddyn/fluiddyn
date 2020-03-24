"""Terminal color codes (:mod:`fluiddyn.util.terminal_colors`)
==============================================================

Defines string variables useful to print in color in a terminal.

Provides:

.. autoclass:: CPrint
   :members:
   :undoc-members:

"""

import sys

FAIL = "\033[91m"
# OKGREEN and OKBLUE kept for background compatibility
OKGREEN = LIGHTGREEN = "\033[92m"
WARNING = "\033[93m"
OKBLUE = LIGHTBLUE = "\033[94m"
HEADER = "\033[95m"
LIGHTCYAN = "\033[96m"
WHITE = "\033[97m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
LIGHTGRAY = "\033[37m"

ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

_color_dict = vars()


def print_fail(*args, **kwargs):
    """Print in bold with "FAIL" font color."""
    args, kwargs = _colorize(color="FAIL", bold=True, *args, **kwargs)
    print(*args, **kwargs)


def print_warning(*args, **kwargs):
    """Print with "WARNING" font colour."""
    args, kwargs = _colorize(color="WARNING", *args, **kwargs)
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
            args[-1] = "{}{}".format(args[-1], ENDC)

    finally:
        return args, kwargs


def cstring(*args, **kwargs):
    """Return a colored string.

    Parameters
    ----------
    args : iterable of str
    bold : bool
    color : str, {'HEADER', 'LIGHTBLUE', 'LIGHTGREEN', 'WARNING', 'FAIL',
                  'ENDC', 'BOLD', 'UNDERLINE' 'BLACK', 'RED', 'GREEN',
                  'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE'}
        Terminal color to use.

    """
    args, kwargs = _colorize(*args, **kwargs)
    cstr = " ".join(args)
    return cstr


class CPrint:
    """Print colored text

    >>> cprint = CPrint()
    >>> cprint("vorticity", color="RED")
    >>> cprint.red("divergence")

    """

    def __call__(
        self,
        *args,
        color=None,
        bold=False,
        sep=" ",
        end="\n",
        file=sys.stdout,
        flush=False,
    ):
        """Print with a specified terminal font color.

        Parameters
        ----------
        args : iterable
            To be passed into print_function.
        bold : bool
        color : str, {'HEADER', 'LIGHTBLUE', 'LIGHTGREEN', 'WARNING', 'FAIL',
                    'ENDC', 'BOLD', 'UNDERLINE' 'BLACK', 'RED', 'GREEN',
                    'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE'}

            Terminal color to use.

        """

        args, kwargs = _colorize(
            *args,
            color=color,
            bold=bold,
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )
        print(*args, **kwargs)

    def header(self, *args, **kwargs):
        kwargs["color"] = "HEADER"
        self.__call__(*args, **kwargs)

    def light_blue(self, *args, **kwargs):
        kwargs["color"] = "LIGHTBLUE"
        self.__call__(*args, **kwargs)

    def light_green(self, *args, **kwargs):
        kwargs["color"] = "LIGHTGREEN"
        self.__call__(*args, **kwargs)

    def light_gray(self, *args, **kwargs):
        kwargs["color"] = "LIGHTGRAY"
        self.__call__(*args, **kwargs)

    def warning(self, *args, **kwargs):
        kwargs["color"] = "WARNING"
        self.__call__(*args, **kwargs)

    def fail(self, *args, **kwargs):
        kwargs["color"] = "FAIL"
        self.__call__(*args, **kwargs)

    def black(self, *args, **kwargs):
        kwargs["color"] = "BLACK"
        self.__call__(*args, **kwargs)

    def red(self, *args, **kwargs):
        kwargs["color"] = "RED"
        self.__call__(*args, **kwargs)

    def green(self, *args, **kwargs):
        kwargs["color"] = "GREEN"
        self.__call__(*args, **kwargs)

    def yellow(self, *args, **kwargs):
        kwargs["color"] = "YELLOW"
        self.__call__(*args, **kwargs)

    def blue(self, *args, **kwargs):
        kwargs["color"] = "BLUE"
        self.__call__(*args, **kwargs)

    def magenta(self, *args, **kwargs):
        kwargs["color"] = "MAGENTA"
        self.__call__(*args, **kwargs)

    def cyan(self, *args, **kwargs):
        kwargs["color"] = "CYAN"
        self.__call__(*args, **kwargs)

    def white(self, *args, **kwargs):
        kwargs["color"] = "WHITE"
        self.__call__(*args, **kwargs)


cprint = CPrint()
