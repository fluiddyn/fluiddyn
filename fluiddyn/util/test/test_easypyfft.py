
import unittest

import numpy as np

from ...io import stdout_redirected
from .. import easypyfft


class TestFFTW1D(unittest.TestCase):
    def test_fft(self):
        op = easypyfft.FFTW1D(4)
        func_fft = np.zeros(op.shapeK, dtype=np.complex128)
        func = op.ifft(func_fft)
        op.fft(func)


class TestFFTW1DReal2Complex(unittest.TestCase):

    def test_fft(self):
        """Should be able to..."""
        nx = 64
        op = easypyfft.FFTW1DReal2Complex(nx)

        func_fft = np.zeros(op.shapeK, dtype=np.complex128)
        func_fft[0] = 1

        self.compute_and_check(func_fft, op)

    def compute_and_check(self, func_fft, op):

        func = op.ifft(func_fft)
        back_fft = op.fft(func)
        back = op.ifft(back_fft)

        self.assertTrue(np.allclose(func_fft, back_fft))
        self.assertTrue(np.allclose(func, back))

        energyX = op.compute_energy_from_spatial(func)
        energyK = op.compute_energy_from_Fourier(func_fft)
        energyKback = op.compute_energy_from_Fourier(back_fft)

        self.assertAlmostEqual(energyX, energyK)
        self.assertAlmostEqual(energyK, energyKback)

    def test_fft_random(self):
        """Should be able to..."""
        nx = 64
        op = easypyfft.FFTW1DReal2Complex(nx)

        func_fft = (np.random.random(op.shapeK)
                    + 1.j*np.random.random(op.shapeK))
        func = op.ifft(func_fft)
        func_fft = op.fft(func)

        self.compute_and_check(func_fft, op)


class TestFFTW2DReal2Complex(unittest.TestCase):
    cls = easypyfft.FFTW2DReal2Complex

    def test_fft(self):
        """Should be able to..."""
        nx = 4
        ny = 2
        op = self.cls(nx, ny)

        func_fft = np.zeros(op.shapeK, dtype=np.complex128)
        func_fft[0, 1] = 1

        self.compute_and_check(func_fft, op)

    def compute_and_check(self, func_fft, op):

        energyK = op.compute_energy_from_Fourier(func_fft)

        func = op.ifft2d(func_fft)
        energyX = op.compute_energy_from_spatial(func)

        back_fft = op.fft2d(func)
        energyKback = op.compute_energy_from_Fourier(back_fft)
        back = op.ifft2d(back_fft)

        self.assertTrue(np.allclose(func_fft, back_fft))
        self.assertTrue(np.allclose(func, back))

        self.assertAlmostEqual(energyX, energyK)
        self.assertAlmostEqual(energyK, energyKback)

    def test_fft_random(self):
        """Should be able to..."""
        nx = 16
        ny = 32
        op = self.cls(nx, ny)

        func_fft = (np.random.random(op.shapeK)
                    + 1.j*np.random.random(op.shapeK))

        with stdout_redirected():
            func = op.ifft2d(func_fft)
        func_fft = op.fft2d(func)

        self.compute_and_check(func_fft, op)


class TestFFTP2D(TestFFTW2DReal2Complex):
    cls = easypyfft.FFTP2D


class TestFFTW3DReal2Complex(unittest.TestCase):

    def test_fft(self):
        """Test easypyfft.FFTW3DReal2Complex"""
        nx = 4
        ny = 2
        nz = 8
        op = easypyfft.FFTW3DReal2Complex(nx, ny, nz)

        func_fft = np.zeros(op.shapeK, dtype=np.complex128)
        func_fft[0, 0, 1] = 1

        self.compute_and_check(func_fft, op)

        op.get_shapeX_loc()
        nX0, nX1, nX2 = op.get_shapeX_seq()
        op.get_shapeK_loc()
        nK0, nK1, nK2 = op.get_shapeK_seq()
        op.get_k_adim()
        op.get_k_adim_loc()
        op.get_dimX_K()
        op.get_seq_indices_first_K()

        o2d = easypyfft.FFTW2DReal2Complex(nX2, nX1)

        arr2d = np.empty(o2d.get_shapeX_loc())
        arr2d_fft = o2d.fft2d(arr2d)
        op.build_invariant_arrayX_from_2d_indices12X(o2d, arr2d)
        op.build_invariant_arrayK_from_2d_indices12X(o2d, arr2d_fft)

    def compute_and_check(self, func_fft, op):

        energyK = op.compute_energy_from_Fourier(func_fft)

        func = op.ifft(func_fft)
        energyX = op.compute_energy_from_spatial(func)

        back_fft = op.fft(func)
        energyKback = op.compute_energy_from_Fourier(back_fft)
        back = op.ifft(back_fft)

        self.assertTrue(np.allclose(func_fft, back_fft))
        self.assertTrue(np.allclose(func, back))

        self.assertAlmostEqual(energyX, energyK)
        self.assertAlmostEqual(energyK, energyKback)

    def test_fft_random(self):
        """Should be able to..."""
        nx = 2
        ny = 4
        nz = 8
        op = easypyfft.FFTW3DReal2Complex(nx, ny, nz)

        func_fft = (np.random.random(op.shapeK)
                    + 1.j*np.random.random(op.shapeK))
        func = op.ifft(func_fft)
        func_fft_back = op.fft(func)

        self.compute_and_check(func_fft_back, op)



if __name__ == '__main__':
    unittest.main()
