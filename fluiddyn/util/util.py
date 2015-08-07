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


import numpy as np
import h5py

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

    module_name = fld._verif_names_modules(
        module_name, path, key_file='module_name')

    # fromlist has to be a not-empty so that __import__('A.B',
    # ...)  returns B rather than A.
    # module_exp = __import__(module_exp, fromlist=['not empty str'])

    module = import_module(module_name)  # .decode("utf-8"))
    Class = module.__dict__[class_name]  # .decode("utf-8")]

    return Class(*args, str_path=str_path, **kwargs)


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
