import numpy as np
from .fft import BaseFFTW, nthreads


class BaseRealTransform(BaseFFTW):
    _dtypeK = np.float64

    @staticmethod
    def _type_forward(fft_type):
        """Forward DCT type."""
        return int(fft_type)

    @staticmethod
    def _type_inverse(fft_type):
        """Inverse DCT type.

        - Type I and IV are inverses of itself
        - Type II and III are inverses of each other

        """
        inv = (1, 3, 2, 4)
        return inv[int(fft_type) - 1]


class BasePyDCT(BaseRealTransform):
    """Base class interface for pyfftw's DCT.

    Parameters
    ----------
    shapeX: array_like
        Shape of input array.

    types: int or array_like of ints
        Type of the DCT. See :method:`_type_forward`

    axes: int or array_like of ints
        Axes over which DCT should be applied

    """

    @staticmethod
    def _type_forward(fft_type):
        """Formal kinds_ of DCT expressed as shown here_ `and here`_.

        .. _kinds: http://www.fftw.org/fftw3_doc/Real_002dto_002dReal-Transform-Kinds.html
        .. _here: http://www.fftw.org/fftw3_doc/1d-Real_002deven-DFTs-_0028DCTs_0029.html
        .. _and here: http://www.fftw.org/fftw3_doc/Real-even_002fodd-DFTs-_0028cosine_002fsine-transforms_0029.html#Real-even_002fodd-DFTs-_0028cosine_002fsine-transforms_0029
        """
        fft_type = BaseRealTransform._type_inverse(fft_type)
        return f"FFTW_REDFT{fft_type - 1:02b}"  # in binary

    @staticmethod
    def _type_inverse(fft_type):
        ifft_type = BaseRealTransform._type_forward(fft_type)
        return f"FFTW_REDFT{ifft_type - 1:02b}"  # in binary

    def __init__(self, shapeX, types=2, axes=None):
        try:
            import pyfftw
        except ImportError as err:
            raise ImportError(f"{err}. Instead scipy.fft may be used?")

        if isinstance(shapeX, int):
            shapeX = tuple(shapeX)

        shapeK = shapeX

        self.shapeX = shapeX
        self.shapeK = self.shapeK_seq = self.shapeK_loc = shapeK

        self.empty_aligned = pyfftw.empty_aligned
        self.arrayX = pyfftw.empty_aligned(shapeX, np.float64)
        self.arrayK = pyfftw.empty_aligned(shapeK, np.float64)

        if axes is None:
            axes = tuple(range(len(shapeX)))

        self.axes = axes

        if isinstance(types, int):
            fft_types = (self._type_forward(types),)
            ifft_types = (self._type_inverse(types),)
        else:
            fft_types = tuple(self._type_forward(t) for t in types)
            ifft_types = tuple(self._type_inverse(t) for t in types)

        if len(axes) != len(fft_types):
            raise ValueError(
                "Parameter ``axes`` should have the same length as "
                "parameter ``types``."
            )

        self.fftplan = pyfftw.FFTW(
            input_array=self.arrayX,
            output_array=self.arrayK,
            axes=axes,
            direction=fft_types,
            threads=nthreads,
        )
        self.ifftplan = pyfftw.FFTW(
            input_array=self.arrayK,
            output_array=self.arrayX,
            axes=axes,
            direction=ifft_types,
            threads=nthreads,
        )

        def _norm(N, fft_type):
            """See normalization note_.

            .. _note: http://www.fftw.org/fftw3_doc/1d-Real_002deven-DFTs-_0028DCTs_0029.html
            """
            return 2 * (N - 1) if fft_type == "FFTW_REDFT00" else 2 * N

        fft_shapes = np.array(shapeX).take(axes)
        self.coef_norm = np.prod(
            [_norm(N, ft) for N, ft in zip(fft_shapes, fft_types)]
        )
        self.inv_coef_norm = 1.0 / self.coef_norm

    def compute_energy_from_Fourier(self, ff_fft):
        """
        .. todo:: Validate!

        """
        result = self.sum_wavenumbers(ff_fft ** 2) / 2
        return result

    compute_energy_from_K = compute_energy_from_Fourier

    def compute_energy_from_spatial(self, ff):
        """
        .. todo:: Validate! Why is a coefficient 3.5 needed?

        """
        return np.mean(ff ** 2 / 3.5)


class FFTW1DReal2RealCosine(BasePyDCT):
    """A class to use FFTW DCT in 1D"""

    def __init__(self, n, type=2, axis=0):
        shapeX = (n,)
        self.type = type
        super().__init__(shapeX, (type,), (axis,))

    def sum_wavenumbers(self, ff_fft):
        """Sum an array which is a function of wavenumbers. See formulae_.

        .. todo:: Validate!

        .. _formulae: http://www.fftw.org/fftw3_doc/1d-Real_002deven-DFTs-_0028DCTs_0029.html
        """
        #  if self.type == 1:
        #      sign = 1 if self.shapeK[0] % 2 == 0 else -1
        #      return 2 * (ff_fft[0] + sign * ff_fft[-1]) + np.sum(ff_fft[1:-1])
        #  elif self.type in (2, 4):
        #      return np.sum(ff_fft)
        #  elif self.type == 3:
        #      return 2 * ff_fft[0] + np.sum(ff_fft[1:])
        return np.sum(ff_fft)
