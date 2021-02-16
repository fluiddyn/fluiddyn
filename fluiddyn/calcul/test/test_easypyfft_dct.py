import unittest
import numpy as np
from .. import easypyfft


class TestFFTW1DReal2RealCosine(unittest.TestCase):
    def test_fft(self):
        """Should be able to..."""
        nx = 24
        op = easypyfft.FFTW1DReal2RealCosine(nx)

        func_fft = np.zeros(op.shapeK, dtype=np.float64)
        func_fft[0:4] = 1

        self.compute_and_check(func_fft, op)

    def compute_and_check(self, func_fft, op):

        func = op.ifft(func_fft)
        back_fft = op.fft(func)
        back = op.ifft(back_fft)

        np.testing.assert_allclose(func_fft, back_fft, atol=1e-15)
        np.testing.assert_allclose(func, back, atol=1e-15)

        energyX = op.compute_energy_from_spatial(func)
        energyK = op.compute_energy_from_Fourier(func_fft)
        energyKback = op.compute_energy_from_Fourier(back_fft)

        self.assertAlmostEqual(energyX, energyK)
        self.assertAlmostEqual(energyK, energyKback)

    def test_fft_random(self):
        """Should be able to..."""
        nx = 64
        op = easypyfft.FFTW1DReal2Complex(nx)

        func_fft = np.random.random(op.shapeK)
        func = op.ifft(func_fft)
        func_fft = op.fft(func)

        self.compute_and_check(func_fft, op)
