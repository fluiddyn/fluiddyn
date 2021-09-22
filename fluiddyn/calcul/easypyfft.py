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

import os
from time import time

import numpy as np

from ..util.mpi import nb_proc, printby0

try:
    import scipy.fftpack as fftp
except ImportError:
    pass

if "OMP_NUM_THREADS" in os.environ:
    nthreads = int(os.environ["OMP_NUM_THREADS"])
else:
    nthreads = 1


def fftw_grid_size(nk, bases=[2, 3, 5, 7, 11, 13], debug=False):
    """Find the closest multiple of prime powers greater than or equal to nk
    using Mixed Integer Linear Programming (MILP). Useful while setting the
    grid-size to be compatible with FFTW.

    Parameters
    ----------
    nk : int
        Lower bound for the spectral grid size.

    bases : array-like, optional
        List of bases, typically prime numbers.

    debug : bool, optional
        Print useful messages.

    Returns
    -------
    int

    """
    if {2, 3, 5} == set(bases):
        if debug:
            print("Using scipy.fftpack.next_fast_len")
        return fftp.next_fast_len(nk)

    elif {2, 3, 5, 7, 11, 13} == set(bases):
        try:
            import pyfftw

            return pyfftw.next_fast_len(nk)

        except (ImportError, AttributeError):
            pass
        else:
            if debug:
                print("Using pyfftw.next_fast_len")

    if not {2, 3, 5, 7, 11, 13}.issuperset(bases):
        raise ValueError(
            "FFTW only supports bases which are a subset of "
            "{2, 3, 5, 7, 11, 13}."
        )

    import pulp

    prob = pulp.LpProblem("FFTW Grid-size Problem")

    bases = np.array(bases)
    bases_order1 = bases[bases < 10]
    bases_order2 = bases[bases >= 10]

    exp_max = np.ceil(np.log2(nk))
    exps = pulp.LpVariable.dicts(
        "exponent_o1", bases_order1, 0, exp_max, cat=pulp.LpInteger
    )
    exps.update(
        pulp.LpVariable.dicts(
            "exponent_o2", bases_order2, 0, 1, cat=pulp.LpInteger
        )
    )

    log_nk_new = pulp.LpVariable("log_grid_size", 0)
    log_nk_new = pulp.lpDot(exps.values(), np.log(bases))

    prob += log_nk_new  # Target to be minimized
    # Subject to:
    prob += log_nk_new >= np.log(nk), "T1"
    if {11, 13}.issubset(bases):
        prob += exps[11] + exps[13] <= 1, "T2"

    if debug:
        print("bases =", bases)
        print("exponents =", exps)
        print("log_nk_new =", log_nk_new)
    # prob.writeLP("FFTWGridSizeOptimizationModel.lp")

    prob.solve()

    if debug:
        print("Status:", pulp.LpStatus[prob.status])
        for v in prob.variables():
            print(v.name, "=", v.varValue)

    if pulp.LpStatus[prob.status] == "Infeasible":
        raise ValueError(f"Not enough bases: {bases}")

    exps_solution = [v.varValue for v in prob.variables()]
    nk_new = np.prod(np.power(bases, exps_solution))
    return int(nk_new)


class BaseFFT:
    def run_tests(self):
        arr = np.random.rand(*self.shapeX)
        arr_fft = self.fft(arr)
        arr = self.ifft(arr_fft)
        arr_fft = self.fft(arr)

        nrj = self.compute_energy_from_spatial(arr)
        nrj_fft = self.compute_energy_from_Fourier(arr_fft)

        assert np.allclose(nrj, nrj_fft), (nrj, nrj_fft, nb_proc * nrj_fft - nrj)

        arr2_fft = np.zeros(self.shapeK, dtype=np.complex128)
        self.fft_as_arg(arr, arr2_fft)
        nrj2_fft = self.compute_energy_from_Fourier(arr2_fft)
        assert np.allclose(nrj, nrj2_fft)

        arr2 = np.empty(self.shapeX)
        self.ifft_as_arg(arr_fft, arr2)
        nrj2 = self.compute_energy_from_spatial(arr2)
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
        printby0(
            "Internal bench (" + name + ")\n"
            "time fft ({}):  {:.6f} s\n".format(name, time_fft)
            + f"time ifft ({name}): {time_ifft:.6f} s"
        )

        return time_fft, time_ifft

    def get_short_name(self):
        return self.__class__.__name__.lower()

    def compute_energy_from_X(self, fieldX):
        return np.mean(fieldX ** 2 / 2.0)

    def get_local_size_X(self):
        return np.prod(self.shapeX)

    def get_shapeK_seq(self):
        return self.shapeK

    get_shapeK_loc = get_shapeK_seq

    def get_shapeX_seq(self):
        return self.shapeX

    get_shapeX_loc = get_shapeX_seq


class FFTP2D(BaseFFT):
    """A class to use fftp"""

    def __init__(self, nx, ny):
        if nx % 2 != 0 or ny % 2 != 0:
            raise ValueError("nx and ny should be even")

        self.nx = nx
        self.ny = ny
        self.shapeX = (ny, nx)
        self.nkx = int(float(nx) / 2 + 1)
        self.shapeK = self.shapeK_seq = self.shapeK_loc = (ny, self.nkx)
        self.coef_norm = nx * ny

        self.fft2d = self.fft
        self.ifft2d = self.ifft

    def fft(self, ff):
        if not (isinstance(ff[0, 0], float)):
            print("Warning: not array of floats")
        big_ff_fft = fftp.fft2(ff) / self.coef_norm
        small_ff_fft = big_ff_fft[:, 0 : self.nkx]
        return small_ff_fft

    def ifft(self, small_ff_fft, ARG_IS_COMPLEX=False):
        if not (isinstance(small_ff_fft[0, 0], complex)):
            print("Warning: not array of complexes")
        # print('small_ff_fft\n', small_ff_fft)
        big_ff_fft = np.empty(self.shapeX, dtype=np.complex128)
        big_ff_fft[:, 0 : self.nkx] = small_ff_fft
        for iky in range(self.ny):
            big_ff_fft[iky, self.nkx :] = small_ff_fft[
                -iky, self.nkx - 2 : 0 : -1
            ].conj()

        # print('big_ff_fft final\n', big_ff_fft)
        result_ifft = fftp.ifft2(big_ff_fft * self.coef_norm)
        if np.max(np.imag(result_ifft)) > 10 ** (-8):
            print(
                "ifft2: imaginary part of ifft not equal to zero,",
                np.max(np.imag(result_ifft)),
            )
        return np.real(result_ifft)

    def fft_as_arg(self, field, field_fft):
        field_fft[:] = self.fft(field)

    def ifft_as_arg(self, field_fft, field):
        field[:] = self.ifft(field_fft)

    def compute_energy_from_Fourier(self, ff_fft):
        return (
            np.sum(abs(ff_fft[:, 0]) ** 2 + abs(ff_fft[:, -1]) ** 2)
            + 2 * np.sum(abs(ff_fft[:, 1:-1]) ** 2)
        ) / 2

    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff) ** 2) / 2


class BasePyFFT(BaseFFT):
    def __init__(self, shapeX):
        try:
            import pyfftw
        except ImportError as err:
            raise ImportError(
                "ImportError {0}. Instead fftpack can be used (?)", err
            )

        if isinstance(shapeX, int):
            shapeX = [shapeX]

        shapeK = list(shapeX)
        shapeK[-1] = shapeK[-1] // 2 + 1
        shapeK = tuple(shapeK)

        self.shapeX = shapeX
        self.shapeK = self.shapeK_seq = self.shapeK_loc = shapeK

        self.empty_aligned = pyfftw.empty_aligned
        self.arrayX = pyfftw.empty_aligned(shapeX, np.float64)
        self.arrayK = pyfftw.empty_aligned(shapeK, np.complex128)

        axes = tuple(range(len(shapeX)))

        self.fftplan = pyfftw.FFTW(
            input_array=self.arrayX,
            output_array=self.arrayK,
            axes=axes,
            direction="FFTW_FORWARD",
            threads=nthreads,
        )
        self.ifftplan = pyfftw.FFTW(
            input_array=self.arrayK,
            output_array=self.arrayX,
            axes=axes,
            direction="FFTW_BACKWARD",
            threads=nthreads,
        )

        self.coef_norm = np.prod(shapeX)
        self.inv_coef_norm = 1.0 / self.coef_norm

    def fft(self, fieldX):
        fieldK = self.empty_aligned(self.shapeK, np.complex128)
        self.fftplan(
            input_array=fieldX, output_array=fieldK, normalise_idft=False
        )
        return fieldK / self.coef_norm

    def ifft(self, fieldK):
        fieldX = self.empty_aligned(self.shapeX, np.float64)
        # This copy is needed because FFTW_DESTROY_INPUT is used.
        # See pyfftw.readthedocs.io/en/latest/source/pyfftw/pyfftw.html
        self.arrayK[:] = fieldK
        self.ifftplan(
            input_array=self.arrayK, output_array=fieldX, normalise_idft=False
        )
        return fieldX

    def fft_as_arg(self, fieldX, fieldK):
        self.fftplan(
            input_array=fieldX, output_array=fieldK, normalise_idft=False
        )
        fieldK *= self.inv_coef_norm

    def ifft_as_arg(self, fieldK, fieldX):
        # This copy is needed because FFTW_DESTROY_INPUT is used.
        # See pyfftw.readthedocs.io/en/latest/source/pyfftw/pyfftw.html
        # fieldK = fieldK.copy()
        # self.ifftplan(input_array=fieldK, output_array=fieldX,
        # this seems faster (but it could depend on the size)
        self.arrayK[:] = fieldK
        self.ifftplan(
            input_array=self.arrayK, output_array=fieldX, normalise_idft=False
        )

    def ifft_as_arg_destroy(self, fieldK, fieldX):
        self.ifftplan(
            input_array=fieldK, output_array=fieldX, normalise_idft=False
        )

    def compute_energy_from_Fourier(self, ff_fft):
        result = self.sum_wavenumbers(abs(ff_fft) ** 2) / 2
        return result

    compute_energy_from_K = compute_energy_from_Fourier

    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff) ** 2) / 2

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
    """A class to use fftw"""

    def __init__(self, nx, ny):
        shapeX = (ny, nx)
        super().__init__(shapeX)
        self.fft2d = self.fft
        self.ifft2d = self.ifft

    def sum_wavenumbers(self, ff_fft):
        if self.shapeX[1] % 2 == 0:
            return (
                np.sum(ff_fft[:, 0])
                + np.sum(ff_fft[:, -1])
                + 2 * np.sum(ff_fft[:, 1:-1])
            )

        else:
            return np.sum(ff_fft[:, 0]) + 2 * np.sum(ff_fft[:, 1:])

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

        x0loc = np.array(range(ix0_start, ix0_start + nx0loc))
        x1loc = np.array(range(ix1_start, ix1_start + nx1loc))

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

        kyseq = np.array(
            list(range(nyseq // 2 + 1)) + list(range(-nyseq // 2 + 1, 0))
        )
        kxseq = np.array(range(nxseq // 2 + 1))

        if self.get_is_transposed():
            k0seq, k1seq = kxseq, kyseq
        else:
            k0seq, k1seq = kyseq, kxseq

        ik0_start, ik1_start = self.get_seq_indices_first_K()
        nk0loc, nk1loc = self.get_shapeK_loc()

        k0_adim_loc = k0seq[ik0_start : ik0_start + nk0loc]
        k1_adim_loc = k1seq[ik1_start : ik1_start + nk1loc]

        return k0_adim_loc, k1_adim_loc


class FFTW3DReal2Complex(BasePyFFT):
    """A class to use fftw"""

    def __init__(self, nx, ny, nz):
        shapeX = (nz, ny, nx)
        super().__init__(shapeX)
        self.fft3d = self.fft
        self.ifft3d = self.ifft

    def sum_wavenumbers(self, ff_fft):
        if self.shapeX[2] % 2 == 0:
            return (
                np.sum(ff_fft[:, :, 0])
                + np.sum(ff_fft[:, :, -1])
                + 2 * np.sum(ff_fft[:, :, 1:-1])
            )

        else:
            return np.sum(ff_fft[:, :, 0]) + 2 * np.sum(ff_fft[:, :, 1:])

    def get_k_adim(self):
        nK0, nK1, nK2 = self.shapeK
        kz_adim_max = nK0 // 2
        kz_adim_min = -((nK0 - 1) // 2)
        ky_adim_max = nK1 // 2
        ky_adim_min = -((nK1 - 1) // 2)
        return (
            np.r_[0 : kz_adim_max + 1, kz_adim_min:0],
            np.r_[0 : ky_adim_max + 1, ky_adim_min:0],
            np.arange(nK2),
        )

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
            raise ValueError("Not the same physical shape...")

        # check that the 2d fft is not with distributed memory...
        if o2d.get_shapeX_loc() != o2d.get_shapeX_seq():
            raise ValueError("2d fft is with distributed memory...")

        ind0seq_first, ind1seq_first, _ = self.get_seq_indices_first_K()

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
        ret = np.zeros((nK0,) + o2d.shapeK_seq, dtype=np.complex128)

        ret[0] = arr2d
        return ret

    def get_seq_indices_first_X(self):
        """Get the "sequential" indices of the first number in Real space."""
        return 0, 0, 0

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
        k0_adim_loc = k0_adim[i0_start : i0_start + nK0_loc]

        k1_adim = compute_k_adim_seq_3d(nK1, d1)
        k1_adim_loc = k1_adim[i1_start : i1_start + nK1_loc]

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
        k_adim_max = nk // 2
        k_adim_min = -((nk - 1) // 2)
        return np.r_[0 : k_adim_max + 1, k_adim_min:0]


class FFTW1D(BasePyFFT):
    """A class to use fftw 1D"""

    def __init__(self, n):
        try:
            import pyfftw
        except ImportError as err:
            raise ImportError("ImportError. Instead fftpack?", err)

        if n % 2 != 0:
            raise ValueError("n should be even")

        shapeX = (n,)
        shapeK = (n,)
        self.shapeX = shapeX
        self.shapeK = self.shapeK_seq = self.shapeK_loc = shapeK
        self.arrayX = pyfftw.empty_aligned(shapeX, "complex128")
        self.arrayK = pyfftw.empty_aligned(shapeK, "complex128")
        self.fftplan = pyfftw.FFTW(
            input_array=self.arrayX,
            output_array=self.arrayK,
            axes=(-1,),
            direction="FFTW_FORWARD",
            threads=nthreads,
        )
        self.ifftplan = pyfftw.FFTW(
            input_array=self.arrayK,
            output_array=self.arrayX,
            axes=(-1,),
            direction="FFTW_BACKWARD",
            threads=nthreads,
        )

        self.coef_norm = n
        self.inv_coef_norm = 1.0 / n

    def fft(self, ff):
        self.arrayX[:] = ff
        self.fftplan()
        return self.arrayK / self.coef_norm

    def ifft(self, ff_fft):
        self.arrayK[:] = ff_fft
        self.ifftplan()
        return self.arrayX.copy()


class FFTW1DReal2Complex(BasePyFFT):
    """A class to use fftw 1D"""

    def sum_wavenumbers(self, ff_fft):
        if self.shapeX[0] % 2 == 0:
            return ff_fft[0] + ff_fft[-1] + 2 * np.sum(ff_fft[1:-1])

        else:
            return ff_fft[0] + 2 * np.sum(ff_fft[1:])

    def compute_energy_from_Fourier(self, ff_fft):
        return (
            abs(ff_fft[0]) ** 2
            + 2 * np.sum(abs(ff_fft[1:-1]) ** 2)
            + abs(ff_fft[-1]) ** 2
        ) / 2

    def compute_energy_from_spatial(self, ff):
        return np.mean(abs(ff) ** 2) / 2
