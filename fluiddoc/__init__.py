"""Utilities to build documentations with sphinx
================================================

The documentations of the packages of the Fluiddyn project are built and hosted
by Readthedocs (by the way, thank you to the readthedocs people!).

.. data:: on_rtd

   Boolean telling whether the code is being run on readthedocs server.

.. autofunction:: mock_modules

.. autosummary::
   :toctree:

   ipynb_maker
   fluidnbstripout
   fluiddocset
   mathmacro

"""

import os
import sys

try:
    from unittest.mock import Mock
except ImportError:
    # Python 2
    from mock import Mock


on_rtd = os.environ.get("READTHEDOCS")


class _MyMock(Mock):
    @classmethod
    def __getattr__(cls, name):
        return Mock()


def mock_modules(modules):
    """Mock modules (for example for building a documentation)

    Examples
    --------

    .. code-block:: python

       mock_modules((
           'h5py', 'h5netcdf', 'pyfftw', 'theano',
           'reikna.cluda', 'reikna.fft', 'reikna.transformations'))


    """

    sys.modules.update((mod_name, _MyMock()) for mod_name in modules)


__all__ = ["on_rtd", "mock_modules"]
