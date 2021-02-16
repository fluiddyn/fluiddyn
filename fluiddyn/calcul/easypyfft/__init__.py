"""Fast Fourier transforms (:mod:`fluiddyn.calcul.easypyfft`)
=============================================================

.. autofunction:: fftw_grid_size

Provides classes for performing fft in 1, 2, and 3 dimensions:

.. autoclass:: FFTP2D
   :members:

.. autoclass:: FFTW2DReal2Complex
   :members:

.. autoclass:: FFTW3DReal2Complex
   :members:

.. autoclass:: FFTW1D
   :members:

.. autoclass:: FFTW1DReal2Complex
   :members:

"""
from .fft import (
    fftw_grid_size,
    FFTP2D,
    FFTW2DReal2Complex,
    FFTW3DReal2Complex,
    FFTW1D,
    FFTW1DReal2Complex,
)
from .dct import (
    FFTW1DReal2RealCosine,
)
