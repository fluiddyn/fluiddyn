import unittest

import numpy as np

from ..signal import FunctionLinInterp, decimate, deriv, smooth


class TestFFTW1DReal2Complex(unittest.TestCase):
    def test_signal(self):
        x = np.linspace(0, 2 * np.pi, 100)
        f = np.sin(x) + 0.02 * (np.random.rand(100) - 0.5)
        smooth(f, window_len=11, window="hanning")
        deriv(f, x, method="diff")
        deriv(f, x, dx=1, method="convolve")
        deriv(f, x, dx=1, method="gaussian_filter")

        sig = np.zeros([4, 4, 4])
        decimate(sig, 2, nwindow=2, axis=0)

        lin_interp = FunctionLinInterp(x, f)
        lin_interp(2)


if __name__ == "__main__":
    unittest.main()
