"""
Toolkit for various tasks (:mod:`fluiddyn.util.util`)
=====================================================


.. autofunction:: create_object_from_file


"""

from __future__ import division, print_function

import os
import glob
import inspect
import shutil
import datetime
import psutil
from importlib import import_module

import contextlib

import h5py
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


from fluiddyn import io
from fluiddyn.util import mpi
import fluiddyn as fld


def import_class(module_name, class_name):
    module = import_module(module_name)
    try:
        return module.__dict__[class_name]
    except KeyError:
        raise KeyError(
            'The given class_name "' + class_name + '" is wrong. '
            'module_name: ' + module_name)


def time_as_str():
    """Return a string coding the time."""
    dt = datetime.datetime.now()
    return dt.strftime('%Y-%m-%d_%H-%M-%S')


def copy_me_in(dest='~'):
    """Copy the file from where this function is called."""
    stack = inspect.stack()
    path_caller = stack[1][1]
    name_file = os.path.basename(path_caller)
    name_file_dest = name_file+'_'+time_as_str()
    shutil.copyfile(path_caller, os.path.join(dest, name_file_dest))
    return path_caller


def load_exp(str_path=None, *args, **kwargs):
    """Load an experiment from the disk."""
    if str_path is None:
        str_path = os.getcwd()

    path = None
    if os.path.isabs(str_path):
        path = str_path

    depth_path_max = 5
    idepth = -1
    while path is None and idepth < depth_path_max:
        idepth += 1
        paths = glob.glob(io.FLUIDDYN_PATH_EXP+'/' +
                          idepth*'*/' + '*' + str_path + '*')
        if len(paths) > 0:
            path = paths[0]

    if path is None:
        raise ValueError(
            """Haven't been able to find a path corresponding to str_path.
You can try to increase the value of the constant depth_path_max
(FLUIDDYN_PATH_EXP: {}
str_path: {}).""".format(io.FLUIDDYN_PATH_EXP, str_path))

    path_h5_file = path+'/params.h5'

    # temporary... for compatibility
    with h5py.File(path_h5_file, 'r+') as f:
        keys = f.attrs.keys()
        if 'name_class_exp' in keys and 'class_name' not in keys:
            f.attrs['class_name'] = f.attrs['name_class_exp']
        if 'module_exp' in keys and 'module_name' not in keys:
            f.attrs['module_name'] = f.attrs['module_exp']

    with h5py.File(path_h5_file, 'r') as f:
        class_name = f.attrs['class_name']
        module_exp = f.attrs['module_name']

    if isinstance(class_name, np.ndarray):
        class_name = class_name[0]
        module_exp = module_exp[0]

    module_exp = fld._verif_names_modules(
        module_exp, path_h5_file, key_file='module_exp')

    # fromlist has to be a not-empty so that __import__('A.B',
    # ...)  returns B rather than A.
    # module_exp = __import__(module_exp, fromlist=['not empty str'])

    module_exp = import_module(module_exp)  # .decode("utf-8"))
    Exp = module_exp.__dict__[class_name]  # .decode("utf-8")]

    return Exp(*args, str_path=path, **kwargs)


def create_object_from_file(str_path, *args, **kwargs):
    """Create an object from a file."""
    path = None
    if os.path.isabs(str_path):
        path = str_path

    paths = glob.glob('*'+str_path+'*')

    for p in paths:
        if p.endswith('h5'):
            path = p
            break

    if path is None:
        raise ValueError(
            "Haven't been able to find a path corresponding to str_path."
            "(str_path: {}).".format(str_path))

    # temporary... for compatibility
    with h5py.File(path, 'r+') as f:
        keys = f.attrs.keys()
        if 'class' in keys and 'class_name' not in keys:
            f.attrs['class_name'] = f.attrs['class']
        if 'module_tank' in keys and 'module_name' not in keys:
            f.attrs['module_name'] = f.attrs['module_tank']
        else:
            if path.endswith('tank.h5') and 'module_name' not in keys:
                f.attrs['module_name'] = 'fluiddyn.lab.tanks'

    with h5py.File(path, 'r') as f:
        class_name = f.attrs['class_name']
        module_name = f.attrs['module_name']

    if isinstance(class_name, np.ndarray):
        class_name = class_name[0]
        module_name = module_name[0]

    # temporary... for compatibility
    if class_name.startswith('<class '):
        class_name = class_name[8:-2].split('.')[-1]
        with h5py.File(path, 'r+') as f:
            f.attrs['class_name'] = class_name

    module_name = fluiddyn._verif_names_modules(
        module_name, path, key_file='module_name')

    # fromlist has to be a not-empty so that __import__('A.B',
    # ...)  returns B rather than A.
    # module_exp = __import__(module_exp, fromlist=['not empty str'])

    module = import_module(module_name)  # .decode("utf-8"))
    Class = module.__dict__[class_name]  # .decode("utf-8")]

    return Class(*args, str_path=str_path, **kwargs)


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


def gradient_colors(nb_colors, color_start=None,
                    color_end=None):
    """Produce a color gradient."""
    if color_start is None:
        color_start = [1, 0, 0]
    if color_end is None:
        color_end = [0, 0, 1]
    # start at black, finish at white
    gradient = [color_start]
    # If only one color, return black
    if nb_colors == 1:
        return gradient
    # Calcuate a color at each evenly spaced value
    # of t = i / n from i in 0 to 1
    for t in range(1, nb_colors):
        gradient.append(
            [color_start[j]
             + (float(t)/(nb_colors-1))*(color_end[j]-color_start[j])
             for j in range(3)
             ])
    return gradient


def run_from_ipython():
    """Check wether the code is run from Ipython."""
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


class Params(object):
    """Minimalist object to store some parameters."""
    def __repr__(self):
        return dict.__repr__(self.__dict__)


def get_memory_usage():
    """Return the memory usage in Mo."""
    process = psutil.Process(os.getpid())
    mem = process.get_memory_info()[0] / float(2 ** 20)
    return mem


def print_memory_usage(string):
    """Print the memory usage."""
    mem = get_memory_usage()
    if mpi.nb_proc > 1:
        mem = mpi.comm.allreduce(mem, op=mpi.MPI.SUM)
    if mpi.rank == 0:
        print((string+':').ljust(30), mem, 'Mo')


def print_size_in_Mo(arr, string=None):
    """Print the size of an array."""
    if string is None:
        string = 'Size of ndarray (equiv. seq.)'
    else:
        string = 'Size of '+string+' (equiv. seq.)'

    mem = float(arr.nbytes)*1e-6
    if mpi.nb_proc > 1:
        mem = mpi.comm.allreduce(mem, op=mpi.MPI.SUM)
    if mpi.rank == 0:
        print(string.ljust(30), ':', mem, 'Mo')


@contextlib.contextmanager
def print_options(*args, **kwargs):
    """Set print option

    example:
    >>> with print_options(precision=3, suppress=True):
    >>>     print something
    """
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    yield
    np.set_printoptions(**original)


if __name__ == '__main__':

    sig = np.zeros([4, 4, 4])

    sigd = decimate(sig, 2, nwindow=2, axis=0)
