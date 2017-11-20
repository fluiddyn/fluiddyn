"""Console script to print and save system information. (:mod:`fluiddyn.util.info`)
===================================================================================
Displays all important information related to software and hardware. It also
includes detailed information such as currently installed FluidDyn packages,
other third-party packages, C compiler, MPI and NumPy configuration.

Examples
--------
>>> fluidinfo  # print package, Python, software and hardware info
>>> fluidinfo -v  # also print basic Numpy info
>>> fluidinfo -vv  # also print detailed Numpy info
>>> fluidinfo -s  # save all information into sys_info.xml
>>> fluidinfo -o /tmp  # save all information into /tmp/sys_info.xml


"""
from __future__ import print_function
from importlib import import_module as _import
import os
import shlex
import inspect
from collections import OrderedDict
import platform
import argparse
import warnings

try:
    from platform import linux_distribution
    # Pending deprecation (Python 3.7)
except ImportError:
    print('Install distro package to use this module.')
    from distro import linux_distribution

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

import psutil
import numpy as np
import numpy.distutils.system_info as np_sys_info

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=ImportWarning)
    from fluiddyn.io.redirect_stdout import stdout_redirected
    from fluiddyn.util.paramcontainer import ParamContainer


_COL_WIDTH = 32


def safe_check_output(cmd, first_row_only=True):
    """Error-tolerant version of subprocess check output"""
    cmd = '/bin/sh -c "{}; exit 0"'.format(cmd)
    output = subprocess.check_output(
        shlex.split(cmd), stderr=subprocess.STDOUT).decode('utf-8')

    if first_row_only and output != '':
        return output.splitlines()[0]
    else:
        return output


def _get_hg_repo(path_dir):
    """Parse `hg paths` command to find remote path."""
    if path_dir == '':
        return ''

    pwd = os.getcwd()
    os.chdir(path_dir)
    output = safe_check_output('hg paths')
    os.chdir(pwd)

    if output == '':
        return 'not an hg repo'
    elif output.startswith('default'):
        return output.split(' ')[2]
    else:
        return output


def make_dict_about(pkg):
    """Make dictionary with all collected information about one package."""
    about_pkg = OrderedDict([
        ('installed', None),
        ('version', ''),
        ('local_path', ''),
        ('remote_path', ''),
    ])
    try:
        pkg = _import(pkg)
    except ImportError:
        about_pkg['installed'] = False
        return about_pkg
    else:
        about_pkg['installed'] = True
        about_pkg['version'] = pkg.__version__
        init_file = inspect.getfile(pkg)
        if 'site-packages' in init_file or 'dist-packages' in init_file:
            about_pkg['local_path'] = os.path.dirname(init_file)
            about_pkg['remote_path'] = ''
        else:
            about_pkg['local_path'] = os.path.dirname(os.path.dirname(init_file))
            about_pkg['remote_path'] = _get_hg_repo(about_pkg['local_path'])
        return about_pkg


def get_info_python():
    """Python information."""
    info_py = OrderedDict.fromkeys(
        ['version', 'implementation', 'compiler']
    )
    for k in info_py:
        func = getattr(platform, 'python_' + k)
        info_py[k] = func()

    return info_py


def _get_info(pkgs):
    """Create a dictionary of dictionaries for all packages."""
    for pkg in pkgs:
        dict_pkg = make_dict_about(pkg)
        pkgs[pkg] = dict_pkg

    return pkgs


def get_info_fluiddyn():
    """Create a dictionary of dictionaries for all FluidDyn packages."""
    pkgs = OrderedDict.fromkeys(
        ['fluiddyn', 'fluidsim', 'fluidlab', 'fluidimage', 'fluidfft',
         'fluidcoriolis', 'fluiddevops']
    )
    return _get_info(pkgs)


def get_info_third_party():
    """Create a dictionary of dictionaries for all third party packages."""
    pkgs = OrderedDict.fromkeys(
        ['numpy', 'cython', 'mpi4py', 'pythran', 'pyfftw', 'matplotlib',
         'scipy', 'skimage', 'h5py']
    )
    return _get_info(pkgs)


def get_info_software():
    """Create a dictionary for compiler and OS information."""
    uname = platform.uname()
    info_sw = OrderedDict(zip(
        ['system', 'hostname', 'kernel'], uname))
    try:
        info_sw['distro'] = ' '.join(linux_distribution())
    except Exception:
        pass

    cc = os.getenv('CC', 'gcc')

    info_sw['CC'] = safe_check_output(cc + ' --version')
    info_sw['MPI'] = safe_check_output('mpirun --version')
    return info_sw


def get_info_numpy(only_print=False, verbosity=None):
    """Print or create a dictionary for numpy and linalg library information."""
    libs = ['lapack_opt', 'blas_opt', 'fftw', 'mkl']

    def rm_configtest():
        if os.path.exists('_configtest.o.d'):
            os.remove('_configtest.o.d')

    def np_sys_info_dict():
        with stdout_redirected():
            d = OrderedDict((k, np_sys_info.get_info(k)) for k in libs)

        rm_configtest()
        return d

    if only_print:
        if verbosity == 1:
            for k, v in np_sys_info_dict().items():
                _print_dict(v, k, '-', 'upper')
        elif verbosity == 2:
            np.show_config()
        else:
            np_sys_info.show_all(argv=[])
            rm_configtest()
    else:
        return np_sys_info_dict()


def get_info_h5py():
    """Create a dictionary detailing h5py installation."""
    try:
        import h5py
    except ImportError:
        return {}

    config = h5py.get_config()
    hdf5_version = h5py.version.hdf5_version_tuple
    try:
        vds = hdf5_version > config.vds_min_hdf5_version
    except AttributeError:
        vds = False

    try:
        swmr = hdf5_version > config.swmr_min_hdf5_version
    except AttributeError:
        swmr = False

    info = OrderedDict((
        ('HDF5_version', h5py.version.hdf5_version),
        ('MPI_enabled', config.mpi),
        ('virtual_dataset_available', vds),
        ('single_writer_multiple_reader_available', swmr)
    ))
    return info


def filter_modify_dict(d, filter_keys, mod_keys):
    """Create a new dictionary by filtering and modifying the keys."""
    filter_d = OrderedDict((k, v) for k, v in d.items() if k in filter_keys)
    for old_key, new_key in zip(filter_keys, mod_keys):
        if old_key != new_key:
            try:
                filter_d[new_key] = filter_d.pop(old_key)
            except KeyError:
                pass

    return filter_d


def update_dict(d1, d2):
    """Update dictionary with missing keys and related values."""
    d1.update(((k, v) for k, v in d2.items() if k not in d1))
    return d1


def get_info_hardware():
    """Create a dictionary for CPU information."""
    def _cpu_freq():
        """psutil can return `None` sometimes, esp. in Travis."""
        func = 'psutil.cpu_freq: '
        try:
            hz = psutil.cpu_freq()
        except IOError:
            return (func + 'IOError',) * 3  # See psutil issue #1071
        except AttributeError:
            return (func + 'AttributeError',) * 3  # See psutil issue #1006
        except NotImplementedError:
            return (func + 'NotImplementedError',) * 3 # on occigen (cluster cines)


        if hz is None:
            return (func + 'None',) * 3  # See psutil issue #981
        else:
            return ('{:.3f}'.format(h) for h in hz)

    try:
        from numpy.distutils.cpuinfo import cpu

        # Keys are specific to Linux distributions only
        info_hw = filter_modify_dict(
            cpu.info[0],
            ['uname_m', 'address sizes', 'bogomips', 'cache size', 'model name',
             'cpu cores', 'siblings'],
            ['arch', 'address_sizes', 'bogomips', 'cache_size', 'cpu_name',
             'nb_cores', 'nb_siblings']
        )
        info_hw['cpu_MHz_actual'] = []
        for d in cpu.info:
            info_hw['cpu_MHz_actual'].append(float(d['cpu MHz']))
    except KeyError as e:
        print('KeyError with', e)
        info_hw = OrderedDict()

    hz_current, hz_min, hz_max = _cpu_freq()
    info_hw_alt = OrderedDict((
        ('arch', platform.machine()),
        ('cpu_name', platform.processor()),
        ('nb_procs', psutil.cpu_count()),
        ('cpu_MHz_current', hz_current),
        ('cpu_MHz_min', hz_min),
        ('cpu_MHz_max', hz_max)
    ))
    info_hw = update_dict(info_hw, info_hw_alt)
    return info_hw


def reset_col_width(nb_cols):
    """Detect total width of the current terminal."""
    global _COL_WIDTH
    try:
        tot_width = int(subprocess.check_output(['tput', 'cols']))
        _COL_WIDTH = tot_width // nb_cols
    except Exception:
        pass


# Table formatting functions

def _print_item(item):
    print(item.ljust(_COL_WIDTH), end='')


def _print_heading(heading, underline_with='=', case='title'):
    if isinstance(heading, str):
        heading = [heading]

    if case == 'title':
        heading = [h.replace('_', ' ').title() for h in heading]
    elif case == 'upper':
        heading = [h.replace('_', ' ').upper() for h in heading]

    underline = [underline_with * len(h) for h in heading]

    for item in heading:
        _print_item(item)

    print()
    for item in underline:
        _print_item(item)

    print()


def _print_dict(d, title=None, underline_with='=', case='title'):
    if title is not None:
        _print_heading('\n' + title, underline_with, case)

    for k, v in d.items():
        print(' - {}: {}'.format(k.ljust(_COL_WIDTH), v))


def print_sys_info(verbosity=None):
    """Print package information as a formatted table."""

    pkgs = get_info_fluiddyn()
    pkgs_keys = list(pkgs)

    heading = ['Package']
    heading.extend(pkgs[pkgs_keys[0]])
    reset_col_width(len(heading))

    _print_heading(heading)

    def print_pkg(about_pkg):
        for v in about_pkg.values():
            v = str(v)
            if len(v) > _COL_WIDTH:
                v = v[:10] + '...' + v[10 + 4 - _COL_WIDTH:]
            _print_item(str(v))

        print()

    for pkg_name, about_pkg in pkgs.items():
        print(pkg_name.ljust(_COL_WIDTH), end='')
        print_pkg(about_pkg)

    pkgs_third_party = get_info_third_party()
    for pkg_name, about_pkg in pkgs_third_party.items():
        print(pkg_name.ljust(_COL_WIDTH), end='')
        print_pkg(about_pkg)

    info_sw = get_info_software()
    _print_dict(info_sw, 'Software')
    info_hw = get_info_hardware()
    _print_dict(info_hw, 'Hardware')
    info_py = get_info_python()
    _print_dict(info_py, 'Python')
    if verbosity is not None:
        _print_heading('\nNumPy', case=None)
        get_info_numpy(True, verbosity)
        info_h5py = get_info_h5py()
        _print_dict(info_h5py, 'h5py', case=None)

    print()


def save_sys_info(path_dir='.', filename='sys_info.xml'):
    """Save all system information as a xml file."""

    sys_info = ParamContainer('sys_info')
    info_sw = get_info_software()
    info_hw = get_info_hardware()
    info_py = get_info_python()
    info_np = get_info_numpy()
    info_h5py = get_info_h5py()
    pkgs = get_info_fluiddyn()
    pkgs_third_party = get_info_third_party()

    sys_info._set_child('software', info_sw)
    sys_info._set_child('hardware', info_hw)
    sys_info._set_child('python', info_py)
    for pkg in pkgs:
        sys_info.python._set_child(pkg, pkgs[pkg])

    for pkg in pkgs_third_party:
        sys_info.python._set_child(pkg, pkgs_third_party[pkg])

    for lib in info_np:
        sys_info.python.numpy._set_child(lib, info_np[lib])

    sys_info.python.h5py._set_child('config', info_h5py)
    path = os.path.join(path_dir, filename)
    sys_info._save_as_xml(path, find_new_name=True)


def main():
    desc = '\n'.join(__doc__.splitlines()[2:])
    parser = argparse.ArgumentParser(
        prog='fluidinfo',
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func=print_sys_info)
    parser.add_argument(
        '-s', '--save', help='saves system information to an xml file '
        '(sys_info.xml)',
        action='store_true')
    parser.add_argument(
        '-o', '--output-dir', help='save to directory', default=None)
    parser.add_argument(
        '-v', '--verbosity', help='increase output verbosity (max: -vvv)',
        action='count')
    parser.add_argument(
        '-W', '--warnings', help='show warnings', action='store_true')

    args = parser.parse_args()
    if not args.warnings:
        warnings.filterwarnings('ignore', category=UserWarning)

    if args.save:
        save_sys_info()
    elif args.output_dir is not None:
        save_sys_info(args.output_dir)
    else:
        print_sys_info(args.verbosity)

    if not args.warnings:
        warnings.resetwarnings()


if __name__ == '__main__':
    main()
