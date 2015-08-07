"""
Simple operations on signals (:mod:`fluiddyn.util.signal`)
==========================================================

"""

from __future__ import division, print_function

import numpy as np
from scipy import ndimage
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


import fluiddyn as fld


def decimate(sig, q, nwindow=None, axis=-1):
    """Decimate a signal."""
    if nwindow is None:
        nwindow = q

    shape_decimated = list(sig.shape)
    len_axis = shape_decimated[axis]
    shape_decimated[axis] = int(len_axis/q)

    sigdec = np.empty(shape_decimated, dtype=sig.dtype)

    for inds, value in np.ndenumerate(sigdec):
        # print(inds)

        sl = list(inds)

        ind_axis = q*inds[axis]
        indmin_axis = max(ind_axis-nwindow, 0)
        indmax_axis = min(ind_axis+nwindow, len_axis-1)

        sl[axis] = slice(indmin_axis, indmax_axis)

        sl = tuple(sl)

        # print(sl)
        # print(sig[sl])

        sigdec[inds] = sig[sl].mean()

    return sigdec


class FunctionLinInterp(object):
    """Function defined by a linear interpolation."""
    def __init__(self, x, f):
        if (not isinstance(x, (list, tuple, np.ndarray)) or
                not isinstance(f, (list, tuple, np.ndarray))):
            raise ValueError('x and f should be sequence.')

        self.x = np.array(x, np.float64)
        self.f = np.array(f, np.float64)

        # test for same length
        if len(x) != len(f):
            raise ValueError('len(x) != len(f)')

        # test for x increasing
        if any([x2 - x1 < 0 for x1, x2 in zip(self.x, self.x[1:])]):
            raise ValueError("x must be in ascending order!")

        self.func = interp1d(x, f)

    def __call__(self, x):
        return self.func(x)

    def plot(self):

        fig = plt.figure()

        size_axe = [0.13, 0.16, 0.84, 0.76]
        ax = fig.add_axes(size_axe)

        ax.set_xlabel(r'$x$')
        ax.set_ylabel(r'$y$')
        ax.plot(self.x, self.f, 'k-.')

        fld.show()


def deriv(f, x=None, dx=None, method='diff'):

    if dx is None:
        dx = np.diff(x)

    if method == 'diff':
        x = (x[:-1]+x[1:])/2
        return x, np.diff(f) / dx
    elif method == 'convolve':

        return np.convolve(f, [1, -1]) / dx
    elif method == 'gaussian_filter':
        return ndimage.gaussian_filter1d(f, sigma=1, order=1, mode='wrap')/dx
    else:
        raise ValueError('unknown method...')


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with
    the signal.  The signal is prepared by introducing reflected
    copies of the signal (with the window size) in both ends so that
    transient parts are minimized in the begining and end part of the
    output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be
        an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming',
        'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman,
    numpy.convolve, scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array
    instead of a string

    NOTE: length(output) != length(input), to correct this: return
    y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        ret = np.empty(x.shape)
        for i0 in xrange(x.shape[0]):
            ret[i0] = smooth(x[i0], window_len=window_len, window=window)
        return ret

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if window_len % 2 == 0:
        raise ValueError('window_len should be odd.')

    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError(
"Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len-1:0:-1], x, x[-1:-window_len:-1]]
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(), s, mode='valid')
    return y[(window_len/2-1):-(window_len/2+1)]


if __name__ == '__main__':

    # Data:
    x = np.linspace(0, 2*np.pi, 100)
    f = np.sin(x) + .02*(np.random.rand(100)-.5)

    # First derivatives:
    dx = x[1] - x[0]  # use np.diff(x) if x is not uniform
    df = np.diff(f) / dx
    cf = np.convolve(f, [1, -1]) / dx
    gf = ndimage.gaussian_filter1d(f, sigma=1, order=1, mode='wrap') / dx

    # Second derivatives:
    dxdx = dx**2
    ddf = np.diff(f, 2) / dxdx
    ccf = np.convolve(f, [1, -2, 1]) / dxdx
    ggf = ndimage.gaussian_filter1d(f, sigma=1, order=2, mode='wrap') / dxdx

    sig = np.zeros([4, 4, 4])

    sigd = decimate(sig, 2, nwindow=2, axis=0)
