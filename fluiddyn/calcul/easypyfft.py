"""Fast Fourier transforms (:mod:`fluiddyn.calcul.easypyfft`)
=============================================================

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

from __future__ import division, print_function

from builtins import range
from builtins import object
import os
import numpy as np
from copy import copy
try:
    import scipy.fftpack as fftp
except ImportError:
    pass

if 'OMP_NUM_THREADS' in os.environ:
    nthreads = int(os.environ['OMP_NUM_THREADS'])
else:
    nthreads = 1


class FFTP2D(object):
    """ A class to use fftp """
    def __init__(self, nx, ny):
        if nx % 2 != 0 or ny % 2 != 0:
            raise ValueError('nx and ny should be even')
        self.nx = nx
        self.ny = ny
        self.shapeX = (ny, nx)
        self.nkx = int(float(nx)/2+1)
        self.shapeK = (ny, self.nkx)
        self.coef_norm = nx*ny

        self.fft2d = self.fftp2d
        self.ifft2d = self.ifftp2d

    def fftp2d(self, ff):
        if not (isinstance(ff[0, 0], float)):
            print('Warning: not array of floats')
        big_ff_fft = fftp.fft2(ff)/self.coef_norm
        small_ff_fft = big_ff_fft[:, 0:self.nkx]
        return small_ff_fft

    def ifftp2d(self, small_ff_fft, ARG_IS_COMPLEX=False):
        if not (isinstance(small_ff_fft[0, 0], complex)):
            print('Warning: not array of complexes')
        # print('small_ff_fft\n', small_ff_fft)
        big_ff_fft = np.empty(self.shapeX, dtype=np.complex128)
        big_ff_fft[:, 0:self.nkx] = small_ff_fft
        for iky in range(self.ny):
            big_ff_fft[iky, self.nkx:] = \
                small_ff_fft[-iky, self.nkx-2:0:-1].conj()

        # print('big_ff_fft final\n', big_ff_fft)
        result_ifft = fftp.ifft2(big_ff_fft*self.coef_norm)
        if np.max(np.imag(result_ifft)) > 10**(-8):
            print('ifft2: imaginary part of ifft not equal to zero,',
                  np.max(np.imag(result_ifft)))
        return np.real(result_ifft)

    def compute_energy_from_Fourier(self, ff_fft):
        return (np.sum(abs(ff_fft[:, 0])**2 + abs(ff_fft[:, -1])**2) +
                2*np.sum(abs(ff_fft[:, 1:-1])**2))/2

    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff)**2)/2


class FFTW2DReal2Complex(object):
    """ A class to use fftw """
    def __init__(self, nx, ny):
        try:
            import pyfftw
        except ImportError as err:
            raise ImportError(
                'ImportError {0}. Instead fftpack can be used (?)', err)
        if nx % 2 != 0 or ny % 2 != 0:
            raise ValueError('nx and ny should be even')
        shapeX = (ny, nx)
        shapeK = (ny, nx//2 + 1)

        self.shapeX = shapeX
        self.shapeK = shapeK

        self.arrayX = pyfftw.empty_aligned(shapeX, 'float64')
        self.arrayK = pyfftw.empty_aligned(shapeK, 'complex128')

        self.fftplan = pyfftw.FFTW(input_array=self.arrayX,
                                   output_array=self.arrayK,
                                   axes=(0, 1),
                                   direction='FFTW_FORWARD',
                                   threads=nthreads)
        self.ifftplan = pyfftw.FFTW(input_array=self.arrayK,
                                    output_array=self.arrayX,
                                    axes=(0, 1),
                                    direction='FFTW_BACKWARD',
                                    threads=nthreads)

        self.coef_norm = nx*ny

        self.get_shapeK_seq = self.get_shapeK_loc = lambda: shapeK
        self.get_shapeX_seq = self.get_shapeX_loc = lambda: shapeX

    def fft2d(self, ff):
        self.arrayX[:] = ff
        self.fftplan(normalise_idft=False)
        return self.arrayK/self.coef_norm

    def ifft2d(self, ff_fft):
        self.arrayK[:] = ff_fft
        self.ifftplan(normalise_idft=False)
        return self.arrayX.copy()

    def compute_energy_from_Fourier(self, ff_fft):
        return (np.sum(abs(ff_fft[:, 0])**2 + abs(ff_fft[:, -1])**2) +
                2*np.sum(abs(ff_fft[:, 1:-1])**2))/2

    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff)**2)/2

    def project_fft_on_realX(self, ff_fft):
        return self.fft2d(self.ifft2d(ff_fft))


class FFTW3DReal2Complex(object):
    """ A class to use fftw """
    def __init__(self, nx, ny, nz):
        try:
            import pyfftw
        except ImportError as err:
            raise ImportError(
                "ImportError {0}. Instead fftpack can be used (?)", err)
        if nx % 2 != 0 or ny % 2 != 0 or nz % 2 != 0:
            raise ValueError('nx, ny and nz should be even')
        shapeX = (nz, ny, nx)
        shapeK = (nz, ny, nx//2 + 1)

        self.shapeX = shapeX
        self.shapeK = shapeK

        self.arrayX = pyfftw.empty_aligned(shapeX, 'float64')
        self.arrayK = pyfftw.empty_aligned(shapeK, 'complex128')

        self.fftplan = pyfftw.FFTW(input_array=self.arrayX,
                                   output_array=self.arrayK,
                                   axes=(0, 1, 2),
                                   direction='FFTW_FORWARD',
                                   threads=nthreads)
        self.ifftplan = pyfftw.FFTW(input_array=self.arrayK,
                                    output_array=self.arrayX,
                                    axes=(0, 1, 2),
                                    direction='FFTW_BACKWARD',
                                    threads=nthreads)

        self.coef_norm = nx*ny*nz

    def fft(self, ff):
        self.arrayX[:] = ff
        self.fftplan(normalise_idft=False)
        return self.arrayK/self.coef_norm

    def ifft(self, ff_fft):
        self.arrayK[:] = ff_fft
        self.ifftplan(normalise_idft=False)
        return self.arrayX.copy()

    def sum_wavenumbers(self, ff_fft):
        return (np.sum(ff_fft[:, :, 0] + ff_fft[:, :, -1]) +
                2*np.sum(ff_fft[:, :, 1:-1]))/2

    def compute_energy_from_Fourier(self, ff_fft):
        return self.sum_wavenumbers(abs(ff_fft)**2)

    def get_shapeX_loc(self):
        return self.shapeX

    def get_shapeX_seq(self):
        return self.shapeX

    def get_shapeK_loc(self):
        return self.shapeK

    def get_shapeK_seq(self):
        return self.shapeK

    def get_k_adim(self):
        nK0, nK1, nK2 = self.shapeK
        kz_adim_max = nK0//2
        ky_adim_max = nK1//2
        return (np.r_[0:kz_adim_max+1, -kz_adim_max+1:0],
                np.r_[0:ky_adim_max+1, -ky_adim_max+1:0],
                np.arange(nK2))

    def get_k_adim_loc(self):
        return self.get_k_adim()

    def get_dimX_K(self):
        return 0, 1, 2

    def get_seq_indices_first_K(self):
        return 0, 0

    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff)**2)/2

    def project_fft_on_realX(self, ff_fft):
        return self.fft2d(self.ifft2d(ff_fft))

    def build_invariant_arrayX_from_2d_indices12X(self, o2d, arr2d):

        nX0, nX1, nX2 = self.get_shapeX_seq()
        nX0loc, nX1loc, nX2loc = self.get_shapeX_loc()

        if (nX1, nX2) != o2d.get_shapeX_seq():
            raise ValueError('Not the same physical shape...')

        # check that the 2d fft is not with distributed memory...
        if o2d.get_shapeX_loc() != o2d.get_shapeX_seq():
            raise ValueError('2d fft is with distributed memory...')

        ind0seq_first, ind1seq_first = self.get_seq_indices_first_K()

        if (nX1loc, nX2loc) == o2d.get_shapeX_loc():
            arr3d_loc_2dslice = arr2d
        else:
            raise NotImplementedError

        arr3d = np.empty([nX0loc, nX1loc, nX2loc])
        for i0 in range(nX0loc):
            arr3d[i0] = arr3d_loc_2dslice

        return arr3d

    def build_invariant_arrayK_from_2d_indices12X(self, o2d, arr2d):

        nK0, nK1, nK2 = self.get_shapeK_seq()
        ret = np.zeros((nK0,) + tuple(o2d.get_shapeK_seq()),
                       dtype=np.complex128)

        ret[0] = arr2d
        return ret


class FFTW1D(object):
    """ A class to use fftw 1D """
    def __init__(self, n):
        try:
            import pyfftw
        except ImportError as err:
            raise ImportError("ImportError. Instead fftpack?", err)

        if n % 2 != 0:
            raise ValueError('n should be even')
        shapeX = (n,)
        shapeK = (n,)
        self.shapeX = shapeX
        self.shapeK = shapeK
        self.arrayX = pyfftw.empty_aligned(shapeX, 'complex128')
        self.arrayK = pyfftw.empty_aligned(shapeK, 'complex128')
        self.fftplan = pyfftw.FFTW(input_array=self.arrayX,
                                   output_array=self.arrayK,
                                   axes=(-1,),
                                   direction='FFTW_FORWARD', threads=nthreads)
        self.ifftplan = pyfftw.FFTW(input_array=self.arrayK,
                                    output_array=self.arrayX,
                                    axes=(-1,),
                                    direction='FFTW_BACKWARD',
                                    threads=nthreads)

        self.coef_norm = n

    def fft(self, ff):
        self.arrayX[:] = ff
        self.fftplan()
        return self.arrayK/self.coef_norm

    def ifft(self, ff_fft):
        self.arrayK[:] = ff_fft
        self.ifftplan()
        return self.arrayX.copy()


class FFTW1DReal2Complex(object):
    """ A class to use fftw 1D """
    def __init__(self, arg, axis=-1):
        try:
            import pyfftw
        except ImportError as err:
            raise ImportError("ImportError. Instead fftpack?", err)

        if isinstance(arg, int):
            n = arg
            shapeX = (n,)
            shapeK = (n//2+1,)
        else:
            n = arg[axis]
            shapeX = arg
            shapeK = list(copy(arg))
            shapeK[axis] = n//2+1
            shapeK = tuple(shapeK)

        if n % 2 != 0:
            raise ValueError('n should be even')

        self.shapeX = shapeX
        self.shapeK = shapeK
        self.arrayX = pyfftw.empty_aligned(shapeX, 'float64')
        self.arrayK = pyfftw.empty_aligned(shapeK, 'complex128')
        self.fftplan = pyfftw.FFTW(input_array=self.arrayX,
                                   output_array=self.arrayK,
                                   axes=(axis,),
                                   direction='FFTW_FORWARD', threads=nthreads)
        self.ifftplan = pyfftw.FFTW(input_array=self.arrayK,
                                    output_array=self.arrayX,
                                    axes=(axis,),
                                    direction='FFTW_BACKWARD',
                                    threads=nthreads)

        self.coef_norm = n

    def fft(self, ff):
        self.arrayX[:] = ff
        self.fftplan(normalise_idft=False)
        return self.arrayK/self.coef_norm

    def ifft(self, ff_fft):
        self.arrayK[:] = ff_fft
        self.ifftplan(normalise_idft=False)
        return self.arrayX.copy()

    def compute_energy_from_Fourier(self, ff_fft):
        return (abs(ff_fft[0])**2 +
                2*np.sum(abs(ff_fft[1:-1])**2) +
                abs(ff_fft[-1])**2)/2

    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff)**2)/2
