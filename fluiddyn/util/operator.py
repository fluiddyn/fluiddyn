"""
Simple operations on signals (:mod:`fluiddyn.util.operator`)
============================================================

"""

from __future__ import division, print_function

import numpy as np
from scipy import ndimage


#Data:
x = np.linspace(0,2*np.pi,100)
f = np.sin(x) + .02*(np.random.rand(100)-.5)

#First derivatives:
dx = x[1] - x[0] # use np.diff(x) if x is not uniform
df = np.diff(f) / dx
cf = np.convolve(f, [1,-1]) / dx
gf = ndimage.gaussian_filter1d(f, sigma=1, order=1, mode='wrap') / dx

#Second derivatives:
dxdx = dx**2
ddf = np.diff(f, 2) / dxdx
ccf = np.convolve(f, [1, -2, 1]) / dxdx
ggf = ndimage.gaussian_filter1d(f, sigma=1, order=2, mode='wrap') / dxdx




def deriv(f, x=None, dx=None, method='diff'):

    if dx is None:
        dx = np.diff(x)


    if method == 'diff':
        x = (x[:-1]+x[1:])/2
        return x, np.diff(f) / dx
    elif method == 'convolve':
        
        return np.convolve(f, [1,-1]) / dx
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
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
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
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    if window_len%2 == 0:
        raise ValueError('window_len should be odd.')


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError(
"Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s = np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w = np.ones(window_len,'d')
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(), s, mode='valid')
    return y[(window_len/2-1):-(window_len/2+1)]

