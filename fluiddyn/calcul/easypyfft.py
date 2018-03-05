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
from time import time

try:
    import scipy.fftpack as fftp
except ImportError:
    pass

if 'OMP_NUM_THREADS' in os.environ:
    nthreads = int(os.environ['OMP_NUM_THREADS'])
else:
    nthreads = 1

from ..util.mpi import printby0


class BaseFFT(object):
    def run_tests(self):
        arr = np.random.rand(*self.shapeX)
        arr_fft = self.fft(arr)
        arr = self.ifft(arr_fft)
        arr_fft = self.fft(arr)

        nrj = self.compute_energy_from_X(arr)
        nrj_fft = self.compute_energy_from_K(arr_fft)

        assert np.allclose(nrj, nrj_fft)

        arr2_fft = np.zeros(self.shapeK, dtype=np.complex128)
        self.fft_as_arg(arr, arr2_fft)
        nrj2_fft = self.compute_energy_from_K(arr2_fft)
        assert np.allclose(nrj, nrj2_fft)

        arr2 = np.empty(self.shapeX)
        self.ifft_as_arg(arr_fft, arr2)
        nrj2 = self.compute_energy_from_X(arr2)
        assert np.allclose(nrj, nrj2)

    def run_benchs(self, nb_time_execute=10):

        arr = np.zeros(self.shapeX)
        arr_fft = np.zeros(self.shapeK, dtype=np.complex128)

        times = []
        for i in range(nb_time_execute):
            t_start = time()
            self.fft_as_arg(arr, arr_fft)
            times.append(time() - t_start)

        time_fft = np.mean(times)

        times = []
        for i in range(nb_time_execute):
            t_start = time()
            self.ifft_as_arg(arr_fft, arr)
            times.append(time() - t_start)

        time_ifft = np.mean(times)

        name = self.__class__.__name__
        printby0('Internal bench (' + name + ')\n'
                 'time fft ({}):  {:.6f} s\n'.format(name, time_fft) +
                 'time ifft ({}): {:.6f} s'.format(name, time_ifft))

        return time_fft, time_ifft

    def get_short_name(self):
        return self.__class__.__name__.lower()

    def compute_energy_from_X(self, fieldX):
        return np.mean(fieldX**2/2.)

    def get_local_size_X(self):
        return np.prod(self.shapeX)

    def gather_Xspace(self, arr):
        return arr

    def scatter_Xspace(self, arr):
        return arr

    def get_shapeK_seq(self):
        return self.shapeK

    get_shapeK_loc = get_shapeK_seq

    def get_shapeX_seq(self):
        return self.shapeX

    get_shapeX_loc = get_shapeX_seq


class FFTP2D(BaseFFT):
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

        self.fft2d = self.fft
        self.ifft2d = self.ifft

    def fft(self, ff):
        if not (isinstance(ff[0, 0], float)):
            print('Warning: not array of floats')
        big_ff_fft = fftp.fft2(ff)/self.coef_norm
        small_ff_fft = big_ff_fft[:, 0:self.nkx]
        return small_ff_fft

    def ifft(self, small_ff_fft, ARG_IS_COMPLEX=False):
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


class BasePyFFT(BaseFFT):

    def __init__(self, shapeX):
        try:
            import pyfftw
        except ImportError as err:
            raise ImportError(
                'ImportError {0}. Instead fftpack can be used (?)', err)

        shapeK = list(shapeX)
        shapeK[-1] = shapeK[-1]//2 + 1
        shapeK = tuple(shapeK)

        self.shapeX = shapeX
        self.shapeK = shapeK

        self.empty_aligned = pyfftw.empty_aligned
        self.arrayX = pyfftw.empty_aligned(shapeX, 'float64')
        self.arrayK = pyfftw.empty_aligned(shapeK, 'complex128')

        axes = tuple(range(len(shapeX)))

        self.fftplan = pyfftw.FFTW(input_array=self.arrayX,
                                   output_array=self.arrayK,
                                   axes=axes,
                                   direction='FFTW_FORWARD',
                                   threads=nthreads)
        self.ifftplan = pyfftw.FFTW(input_array=self.arrayK,
                                    output_array=self.arrayX,
                                    axes=axes,
                                    direction='FFTW_BACKWARD',
                                    threads=nthreads)

        self.coef_norm = np.prod(shapeX)
        self.inv_coef_norm = 1./self.coef_norm

    def fft(self, fieldX):
        fieldK = self.empty_aligned(self.shapeK, 'complex128')
        self.fftplan(input_array=fieldX, output_array=fieldK,
                     normalise_idft=False)
        return fieldK/self.coef_norm

    def ifft(self, fieldK):
        # This copy is needed because FFTW_DESTROY_INPUT is used.
        # See pyfftw.readthedocs.io/en/latest/source/pyfftw/pyfftw.html
        self.arrayK[:] = fieldK
        field = self.empty_aligned(self.shapeX, 'float64')
        self.ifftplan(input_array=self.arrayK, output_array=field,
                      normalise_idft=False)
        return field

    def fft_as_arg(self, fieldX, fieldK):
        self.fftplan(input_array=fieldX, output_array=fieldK,
                     normalise_idft=False)
        fieldK *= self.inv_coef_norm

    def ifft_as_arg(self, fieldK, fieldX):
        # This copy is needed because FFTW_DESTROY_INPUT is used.
        # See pyfftw.readthedocs.io/en/latest/source/pyfftw/pyfftw.html
        # fieldK = fieldK.copy()
        # self.ifftplan(input_array=fieldK, output_array=fieldX,
        # this seems faster (but it could depend on the size)
        self.arrayK[:] = fieldK
        self.ifftplan(input_array=self.arrayK, output_array=fieldX,
                      normalise_idft=False)

    def ifft_as_arg_destroy(self, fieldK, fieldX):
        self.ifftplan(input_array=fieldK, output_array=fieldX,
                      normalise_idft=False)

    def compute_energy_from_Fourier(self, ff_fft):
        result = self.sum_wavenumbers(abs(ff_fft)**2)/2
        return result

    compute_energy_from_K = compute_energy_from_Fourier
    
    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff)**2)/2

    def project_fft_on_realX(self, ff_fft):
        return self.fft(self.ifft(ff_fft))

    def get_is_transposed(self):
        return False

    def create_arrayX(self, value=None):
        """Return a constant array in real space."""
        shapeX = self.shapeX
        field = self.empty_aligned(shapeX)
        if value is not None:
            field.fill(value)
        return field

    def create_arrayK(self, value=None):
        """Return a constant array in real space."""
        shapeK = self.shapeK
        field = self.empty_aligned(shapeK, dtype=np.complex128)
        if value is not None:
            field.fill(value)
        return field

class FFTW2DReal2Complex(BasePyFFT):
    """ A class to use fftw """
    def __init__(self, nx, ny):
        shapeX = (ny, nx)
        super(FFTW2DReal2Complex, self).__init__(shapeX)
        self.fft2d = self.fft
        self.ifft2d = self.ifft

    def sum_wavenumbers(self, ff_fft):
        if self.shapeX[1] % 2 == 0:
            return (np.sum(ff_fft[:, 0]) +
                    np.sum(ff_fft[:, -1]) +
                    2*np.sum(ff_fft[:, 1:-1]))
        else:
            return (np.sum(ff_fft[:, 0]) +
                    2*np.sum(ff_fft[:, 1:]))

    def get_seq_indices_first_K(self):
        return 0, 0

    def get_seq_indices_first_X(self):
        return 0, 0

    def get_x_adim_loc(self):
        """Get the coordinates of the points stored locally.

        Returns
        -------

        x0loc : np.ndarray

        x1loc : np.ndarray

        The indices correspond to the index of the dimension in real space.
        """
        nyseq, nxseq = self.get_shapeX_seq()

        ix0_start, ix1_start = self.get_seq_indices_first_X()
        nx0loc, nx1loc = self.get_shapeX_loc()

        x0loc = np.array(range(ix0_start, ix0_start+nx0loc))
        x1loc = np.array(range(ix1_start, ix1_start+nx1loc))

        return x0loc, x1loc

    def get_k_adim_loc(self):
        """Get the non-dimensional wavenumbers stored locally.

        Returns
        -------

        k0_adim_loc : np.ndarray

        k1_adim_loc : np.ndarray

        The indices correspond to the index of the dimension in spectral space.
        """
        
        nyseq, nxseq = self.get_shapeX_seq()

        kyseq = np.array(list(range(nyseq//2 + 1)) +
                         list(range(-nyseq//2 + 1, 0)))
        kxseq = np.array(range(nxseq//2 + 1))

        if self.get_is_transposed():
            k0seq, k1seq = kxseq, kyseq
        else:
            k0seq, k1seq = kyseq, kxseq

        ik0_start, ik1_start = self.get_seq_indices_first_K()
        nk0loc, nk1loc = self.get_shapeK_loc()

        k0_adim_loc = k0seq[ik0_start:ik0_start+nk0loc]
        k1_adim_loc = k1seq[ik1_start:ik1_start+nk1loc]

        return k0_adim_loc, k1_adim_loc
    
class FFTW3DReal2Complex(BasePyFFT):
    """ A class to use fftw """
    def __init__(self, nx, ny, nz):
        shapeX = (nz, ny, nx)
        super(FFTW3DReal2Complex, self).__init__(shapeX)
        self.fft3d = self.fft
        self.ifft3d = self.ifft
    
    def sum_wavenumbers(self, ff_fft):
        if self.shapeX[2] % 2 == 0:
            return (np.sum(ff_fft[:, :, 0]) +
                    np.sum(ff_fft[:, :, -1]) +
                    2*np.sum(ff_fft[:, :, 1:-1]))
        else:
            return (np.sum(ff_fft[:, :, 0]) +
                    2*np.sum(ff_fft[:, :, 1:]))

    def get_k_adim(self):
        nK0, nK1, nK2 = self.shapeK
        kz_adim_max = nK0//2
        kz_adim_min = -((nK0-1)//2)
        ky_adim_max = nK1//2
        ky_adim_min = -((nK1-1)//2)
        return (np.r_[0:kz_adim_max+1, kz_adim_min:0],
                np.r_[0:ky_adim_max+1, ky_adim_min:0],
                np.arange(nK2))

    # def get_k_adim_loc(self):
    #     return self.get_k_adim()

    def get_dimX_K(self):
        return 0, 1, 2

    # def get_seq_indices_first_K(self):
    #     return 0, 0

    # def compute_energy_from_spatial(self, ff):
    #     return np.mean(abs(ff)**2)/2

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
    def get_seq_indices_first_K(self):
        """Get the "sequential" indices of the first number in Fourier space."""
        return 0, 0, 0

    def get_k_adim_loc(self):
        """Get the non-dimensional wavenumbers stored locally.

        Returns
        -------

        k0_adim_loc : np.ndarray

        k1_adim_loc : np.ndarray

        k2_adim_loc :  np.ndarray

        The indices correspond to the index of the dimension in spectral space.

        """

        nK0, nK1, nK2 = self.get_shapeK_seq()
        nK0_loc, nK1_loc, nK2_loc = self.get_shapeK_loc()

        d0, d1, d2 = self.get_dimX_K()
        i0_start, i1_start, i2_start = self.get_seq_indices_first_K()

        k0_adim = compute_k_adim_seq_3d(nK0, d0)
        k0_adim_loc = k0_adim[i0_start:i0_start+nK0_loc]

        k1_adim = compute_k_adim_seq_3d(nK1, d1)
        k1_adim_loc = k1_adim[i1_start:i1_start+nK1_loc]

        k2_adim_loc = compute_k_adim_seq_3d(nK2, d2)

        return k0_adim_loc, k1_adim_loc, k2_adim_loc

    
def compute_k_adim_seq_3d(nk, axis):
    """Compute the adimensional wavenumber for an axis. 

    Parameters
    ----------

    nk : int

      Global size in Fourier space for the axis.

    axis : int

      Index of the axis in real space (0 for z, 1 for y and 2 for x).

    """
    if axis == 2:
        return np.arange(nk)
    else:
        k_adim_max = nk//2
        k_adim_min = -((nk-1)//2)
        return np.r_[0:k_adim_max+1, k_adim_min:0]

    
class FFTW1D(BasePyFFT):
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
        self.inv_coef_norm = 1./n

    def fft(self, ff):
        self.arrayX[:] = ff
        self.fftplan()
        return self.arrayK/self.coef_norm

    def ifft(self, ff_fft):
        self.arrayK[:] = ff_fft
        self.ifftplan()
        return self.arrayX.copy()


class FFTW1DReal2Complex(BasePyFFT):
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
        self.inv_coef_norm = 1./n

    def fft(self, ff):
        self.arrayX[:] = ff
        self.fftplan(normalise_idft=False)
        return self.arrayK/self.coef_norm

    def ifft(self, ff_fft):
        self.arrayK[:] = ff_fft
        self.ifftplan(normalise_idft=False)
        return self.arrayX.copy()

    def sum_wavenumbers(self, ff_fft):
        if self.shapeX[0] % 2 == 0:
            return (ff_fft[0] +
                    ff_fft[-1] +
                    2*np.sum(ff_fft[1:-1]))
        else:
            return (ff_fft[0] +
                    2*np.sum(ff_fft[1:]))

    def compute_energy_from_Fourier(self, ff_fft):
        return (abs(ff_fft[0])**2 +
                2*np.sum(abs(ff_fft[1:-1])**2) +
                abs(ff_fft[-1])**2)/2

    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff)**2)/2
