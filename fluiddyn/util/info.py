"""Console script to print and save system information. (:mod:`fluiddevops.info`)
=================================================================================

"""
from __future__ import print_function
from importlib import import_module as _import
import os
import shlex
import inspect
from collections import OrderedDict
import platform
import argparse

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
         'scipy', 'skimage']
    )
    return _get_info(pkgs)


def get_info_software():
    """Create a dictionary for compiler and OS information."""
    uname = platform.uname()
    info_sw = dict(zip(
        ['system', 'hostname', 'kernel'], uname))
    try:
        info_sw['distro'] = ' '.join(linux_distribution())
    except:
        pass

    cc = os.getenv('CC')
    if cc is None:
        cc = 'gcc'

    info_sw['CC'] = safe_check_output(cc + ' --version')
    info_sw['MPI'] = safe_check_output('mpirun --version')
    return info_sw


def get_info_numpy(only_print=False, verbose=False):
    """Print or create a dictionary for numpy and linalg library information."""
    if only_print:
        if verbose:
            np_sys_info.show_all()
        else:
            np.show_config()
    else:
        libs = ['lapack', 'lapack_opt', 'blas', 'blas_opt', 'fftw_opt',
                'atlas', 'openblas', 'mkl']

        return dict((k, np_sys_info.get_info(k)) for k in libs)


def filter_modify_dict(d, filter_keys, mod_keys):
    """Create a new dictionary by filtering and modifying the keys."""
    filter_d = dict((k, v) for k, v in d.items() if k in filter_keys)
    for old_key, new_key in zip(filter_keys, mod_keys):
        if old_key != new_key:
            try:
                filter_d[new_key] = filter_d.pop(old_key)
            except KeyError:
                pass

    return filter_d


def update_dict(d1, d2):
    """Update dictionary with missing keys and related values."""
    d1.update(dict((k, v) for k, v in d2.items() if k not in d1))
    return d1


def get_info_hardware():
    """Create a dictionary for CPU information."""
    def _cpu_freq():
        """psutil can return `None` sometimes, esp. in Travis."""
        hz = psutil.cpu_freq()
        if hz is None:
            return 0., 0., 0.
        else:
            return hz.current, hz.min, hz.max

    try:
        from numpy.distutils.cpuinfo import cpu

        # Keys are specific to Linux distributions only
        info_hw = filter_modify_dict(
            cpu.info[0],
            ['uname_m', 'cpu cores', 'bogomips', 'cache size',
             'model name', 'siblings', 'address sizes'],
            ['arch', 'nb_cores', 'bogomips', 'cache_size',
             'cpu_name', 'nb_procs', 'address_sizes']
        )
        info_hw['cpu_MHz_actual'] = []
        for d in cpu.info:
            info_hw['cpu_MHz_actual'].append(d['cpu MHz'])
    except KeyError as e:
        print('KeyError with', e)
        info_hw = dict()

    hz_current, hz_min, hz_max = _cpu_freq()
    info_hw_alt = {
        'arch': platform.machine(),
        'cpu_name': platform.processor(),
        'nb_procs': psutil.cpu_count(),
        'cpu_MHz_current': '{:.3f}'.format(hz_current),
        'cpu_MHz_min': '{:.3f}'.format(hz_min),
        'cpu_MHz_max': '{:.3f}'.format(hz_max)
    }
    info_hw = update_dict(info_hw, info_hw_alt)
    return info_hw


def reset_col_width(nb_cols):
    """Detect total width of the current terminal."""
    global _COL_WIDTH
    try:
        tot_width = int(subprocess.check_output(['tput', 'cols']))
        _COL_WIDTH = tot_width // nb_cols
    except:
        pass


# Table formatting functions

def _print_item(item):
    print(item.ljust(_COL_WIDTH), end='')


def _print_heading(heading):
    if isinstance(heading, str):
        heading = [heading]

    heading = [h.replace('_', ' ').title() for h in heading]

    underline = ['=' * len(h) for h in heading]

    for item in heading:
        _print_item(item)

    print()
    for item in underline:
        _print_item(item)

    print()


def _print_dict(d, title=None):
    if title is not None:
        _print_heading('\n' + title)

    for k, v in d.items():
        print(' - {}: {}'.format(k.ljust(_COL_WIDTH), v))


def print_sys_info(verbose=False):
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
    _print_heading('\nNumPy')
    get_info_numpy(True, verbose)


def save_sys_info(path_dir='.', filename='sys_info.xml'):
    """Save all system information as a xml file."""

    sys_info = ParamContainer('sys_info')
    info_sw = get_info_software()
    info_hw = get_info_hardware()
    info_py = get_info_python()
    info_np = get_info_numpy()
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

    path = os.path.join(path_dir, filename)
    sys_info._save_as_xml(path, find_new_name=True)


def main():
    parser = argparse.ArgumentParser(
        prog='fluidinfo',
        description='print and save system information')
    parser.set_defaults(func=print_sys_info)
    parser.add_argument(
        '-s', '--save', help='saves system information to an xml file',
        action='store_true')
    parser.add_argument(
        '-o', '--output-dir', help='save to directory', default=None)
    parser.add_argument(
        '-v', '--verbose', help='verbose print output',
        action='store_true')

    args = parser.parse_args()
    if args.save:
        save_sys_info()
    elif args.output_dir is not None:
        save_sys_info(args.output_dir)
    else:
        print_sys_info(args.verbose)


if __name__ == '__main__':
    main()
