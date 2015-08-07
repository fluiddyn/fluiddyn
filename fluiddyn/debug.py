"""Debug utility
================

Provides:

.. autofunction:: ipydebug

"""

from IPython.terminal.embed import InteractiveShellEmbed
import inspect


def ipydebug():
    """Launch an Ipython shell"""

    ipshell = InteractiveShellEmbed()

    frame = inspect.currentframe().f_back
    msg = 'Stopped at {0.f_code.co_filename} at line {0.f_lineno}'.format(
        frame)

    # Go back one level!  This is needed because the call to
    # ipshell is inside this function.
    ipshell(msg, stack_depth=2)
