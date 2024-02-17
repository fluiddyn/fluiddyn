"""Console script to print and save system information. (:mod:`fluiddyn.util.info`)
===================================================================================
Displays all important information related to software and hardware. It also
includes detailed information such as currently installed FluidDyn packages,
other third-party packages, C compiler, MPI and NumPy configuration.

Examples
--------
>>> fluidinfo  # print package, Python, software and hardware info
>>> fluidinfo -v  # also print Numpy info
>>> fluidinfo -s  # save all information into sys_info.xml
>>> fluidinfo -o /tmp  # save all information into /tmp/sys_info.xml

.. todo::
    Use a YAML package to print.

"""

import argparse
import inspect
import os
import platform
import shlex
import shutil
import subprocess
import warnings
from collections import OrderedDict
from configparser import ConfigParser
from importlib import import_module as _import
from pathlib import Path

import distro
import numpy as np
import psutil


# linux_distribution is deprecated and no longer exists in Python 3.8
def linux_distribution():
    return (distro.name(), distro.version(), distro.codename())


with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=ImportWarning)
    from .paramcontainer import ParamContainer
    from .terminal_colors import cprint

_COL_WIDTH = 32
_COL_MAX = 80


def safe_check_output(cmd, first_row_only=True):
    """Error-tolerant version of subprocess check output"""
    if os.name == "posix":
        cmd = f'/bin/sh -c "{cmd}; exit 0"'
    else:
        cmd = f'bash -c "{cmd}; exit 0"'

    try:
        output = subprocess.check_output(
            shlex.split(cmd), stderr=subprocess.STDOUT
        ).decode("utf-8")
    except subprocess.CalledProcessError as error:
        output = error.output

    if first_row_only and output != "":
        return output.splitlines()[0]

    else:
        return output


def _get_hg_repo(path_dir):
    """Parse `hg paths` command to find remote path."""
    if path_dir == "":
        return ""

    hgrc = Path(path_dir) / ".hg" / "hgrc"
    if hgrc.exists():
        config = ConfigParser()
        config.read(str(hgrc))
        if "paths" in config:
            return config["paths"].get("default", "hgrc: no default path?")
        else:
            return "hgrc: no [paths] section?"
    else:
        return "not a hg repo"


def make_dict_about(pkg):
    """Make dictionary with all collected information about one package."""
    about_pkg = OrderedDict(
        [
            ("installed", None),
            ("version", ""),
            ("local_path", ""),
            ("remote_path", ""),
        ]
    )
    try:
        pkg = _import(pkg)
    except ImportError:
        about_pkg["installed"] = False
        return about_pkg

    else:
        about_pkg["installed"] = True
        about_pkg["version"] = pkg.__version__
        init_file = inspect.getfile(pkg)
        if "site-packages" in init_file or "dist-packages" in init_file:
            about_pkg["local_path"] = os.path.dirname(init_file)
            about_pkg["remote_path"] = ""
        else:
            about_pkg["local_path"] = os.path.dirname(os.path.dirname(init_file))
            about_pkg["remote_path"] = _get_hg_repo(about_pkg["local_path"])
        return about_pkg


def get_info_python():
    """Python information."""
    info_py = OrderedDict.fromkeys(["version", "implementation", "compiler"])
    for k in info_py:
        func = getattr(platform, "python_" + k)
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
        [
            "fluiddyn",
            "fluidsim",
            "fluidlab",
            "fluidimage",
            "fluidfft",
            "fluidsht",
            "fluidcoriolis",
            "fluiddevops",
            "transonic",
        ]
    )
    return _get_info(pkgs)


def get_info_third_party():
    """Create a dictionary of dictionaries for all third party packages."""
    pkgs = OrderedDict.fromkeys(
        [
            "numpy",
            "cython",
            "mpi4py",
            "pythran",
            "pyfftw",
            "matplotlib",
            "scipy",
            "skimage",
            "h5py",
        ]
    )
    return _get_info(pkgs)


def get_info_software():
    """Create a dictionary for compiler and OS information."""
    uname = platform.uname()
    info_sw = OrderedDict(zip(["system", "hostname", "kernel"], uname))
    try:
        info_sw["distro"] = " ".join(linux_distribution())
    except Exception:
        pass

    cc = os.getenv("CC", "gcc")

    info_sw["CC"] = safe_check_output(cc + " --version")
    info_sw["MPI"] = safe_check_output("mpirun --version")
    return info_sw


def get_info_numpy():
    """Create a dictionary for numpy and linalg library information."""
    try:
        return np.show_config("dicts")
    except TypeError:
        return {}


def print_info_numpy(verbosity=None):
    """Print information about Numpy"""
    info_numpy = get_info_numpy()
    if info_numpy:
        _print_dict(info_numpy)
        return

    # Numpy <1.25
    np.show_config()


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

    info = OrderedDict(
        (
            ("HDF5_version", h5py.version.hdf5_version),
            ("MPI_enabled", config.mpi),
            ("virtual_dataset_available", vds),
            ("single_writer_multiple_reader_available", swmr),
        )
    )
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
        """psutil can return `None` sometimes, esp. in CI."""
        func = "psutil.cpu_freq: "
        try:
            hz = psutil.cpu_freq()
        except IOError:
            return (func + "IOError",) * 3  # See psutil issue #1071

        except AttributeError:
            return (func + "AttributeError",) * 3  # See psutil issue #1006

        except NotImplementedError:
            return (
                func + "NotImplementedError",
            ) * 3  # on occigen (cluster cines)

        if hz is None:
            return (func + "None",) * 3  # See psutil issue #981

        else:
            ret = []
            for h in hz:
                try:
                    h = f"{h:.3f}"
                except TypeError:
                    pass
                ret.append(h)
            return ret

    from .numpy_distutils_cpuinfo import cpu

    try:
        # Keys are specific to Linux distributions only
        info_hw = filter_modify_dict(
            cpu.info[0],
            [
                "uname_m",
                "address sizes",
                "bogomips",
                "cache size",
                "model name",
                "cpu cores",
                "siblings",
            ],
            [
                "arch",
                "address_sizes",
                "bogomips",
                "cache_size",
                "cpu_name",
                "nb_cores",
                "nb_siblings",
            ],
        )
        info_hw["cpu_MHz_actual"] = []
        for d in cpu.info:
            info_hw["cpu_MHz_actual"].append(float(d["cpu MHz"]))
    except KeyError as error:
        print("KeyError with", error)
        info_hw = OrderedDict()

    hz_current, hz_min, hz_max = _cpu_freq()
    info_hw_alt = OrderedDict(
        (
            ("arch", platform.machine()),
            ("cpu_name", platform.processor()),
            ("nb_procs", psutil.cpu_count()),
            ("cpu_MHz_current", hz_current),
            ("cpu_MHz_min", hz_min),
            ("cpu_MHz_max", hz_max),
        )
    )
    info_hw = update_dict(info_hw, info_hw_alt)
    return info_hw


def reset_col_width(widths):
    """Detect total width of the current terminal."""
    global _COL_MAX, _COL_WIDTH
    nb_cols = len(widths)
    _COL_MAX = shutil.get_terminal_size().columns
    _COL_WIDTH = _COL_MAX // nb_cols

    widths_array = np.array(widths)
    widths_sum = widths_array.sum()
    if widths_sum > _COL_MAX:
        too_long = np.greater(widths_array, _COL_WIDTH)
        nb_too_long = np.count_nonzero(too_long)
        widths_too_long = widths_array[too_long].sum()

        _COL_WIDTH = (_COL_MAX - (widths_sum - widths_too_long)) // nb_too_long
        widths = [_COL_WIDTH if w > _COL_WIDTH else w for w in widths]

    return widths


# Table formatting functions


def _print_item(item, color=None, bold=False, width=None):
    if width is None:
        width = _COL_WIDTH

    cprint(item.ljust(width), end="", color=color, bold=bold)


def _print_heading(heading, underline_with="=", case="title", widths=None):
    if isinstance(heading, str):
        heading = [heading]

    if widths is None:
        widths = [None] * len(heading)

    if case == "title":
        heading = [h.replace("_", " ").title() for h in heading]
    elif case == "upper":
        heading = [h.replace("_", " ").upper() for h in heading]

    underline = [underline_with * len(h) for h in heading]

    for item, w in zip(heading, widths):
        _print_item(item, color="RED", bold=True, width=w)

    print()
    for item, w in zip(underline, widths):
        _print_item(item, color="RED", width=w)

    print()


def _print_dict(
    d,
    heading=None,
    underline_with="=",
    case="title",
    subheading=None,
    indent_level=0,
):
    if heading is not None:
        _print_heading("\n" + heading, underline_with, case)

    indent = " " * indent_level * 2
    WIDTH = _COL_WIDTH - indent_level * 2

    if subheading is not None:
        cprint(f"{indent}{subheading}:", color="BLUE")

    for k, v in d.items():
        if isinstance(v, dict):
            _print_dict(v, subheading=k, indent_level=indent_level + 1)
        else:
            print("{}  - {}: {}".format(indent, k.ljust(WIDTH), v))


def get_col_widths(d, widths=None):
    if widths is None:
        widths = [len(key) + 1 for key in d]

    for i, string in enumerate(d.values()):
        widths[i] = max(widths[i], len(repr(string)) + 1)

    return widths


def print_sys_info(verbosity=None):
    """Print package information as a formatted table."""
    global _COL_MAX
    pkgs = get_info_fluiddyn()
    pkgs_third_party = get_info_third_party()

    widths = None
    width_pkg_name = 0
    for _pkgs in (pkgs, pkgs_third_party):
        for pkg_name, pkg_details in _pkgs.items():
            width_pkg_name = max(width_pkg_name, len(pkg_name) + 1)
            widths = get_col_widths(pkg_details, widths)

    widths.insert(0, width_pkg_name)

    pkgs_keys = list(pkgs)
    heading = ["Package"]
    heading.extend(pkgs[pkgs_keys[0]])
    widths = reset_col_width(widths)

    _print_heading(heading, widths=widths)

    def print_pkg(about_pkg):
        for v, w in zip(about_pkg.values(), widths[1:]):
            v = str(v)
            if len(v) > w:
                v = v[:10] + "..." + v[10 + 4 - w :]
            _print_item(str(v), width=w)

        print()

    for pkg_name, about_pkg in pkgs.items():
        print(pkg_name.ljust(widths[0]), end="")
        print_pkg(about_pkg)

    for pkg_name, about_pkg in pkgs_third_party.items():
        print(pkg_name.ljust(widths[0]), end="")
        print_pkg(about_pkg)

    info_sw = get_info_software()
    _print_dict(info_sw, "Software")
    info_hw = get_info_hardware()
    _print_dict(info_hw, "Hardware")
    info_py = get_info_python()
    _print_dict(info_py, "Python")
    if verbosity is not None:
        _print_heading("\nNumPy", case=None)
        print_info_numpy()
        info_h5py = get_info_h5py()
        _print_dict(info_h5py, "h5py", case=None)

    print()


def save_sys_info(path_dir=".", filename="sys_info.xml"):
    """Save all system information as a xml file."""

    sys_info = ParamContainer("sys_info")
    info_sw = get_info_software()
    info_hw = get_info_hardware()
    info_py = get_info_python()
    info_np = get_info_numpy()
    info_h5py = get_info_h5py()
    pkgs = get_info_fluiddyn()
    pkgs_third_party = get_info_third_party()

    sys_info._set_child("software", info_sw)
    sys_info._set_child("hardware", info_hw)
    sys_info._set_child("python", info_py)
    for pkg in pkgs:
        sys_info.python._set_child(pkg, pkgs[pkg])

    for pkg in pkgs_third_party:
        sys_info.python._set_child(pkg, pkgs_third_party[pkg])

    for k, v in info_np.items():
        sys_info.python.numpy._set_child(k, v)

    sys_info.python.h5py._set_child("config", info_h5py)
    path = os.path.join(path_dir, filename)
    sys_info._save_as_xml(path, find_new_name=True)


def _get_parser():
    desc = "\n".join(__doc__.splitlines()[2:])
    parser = argparse.ArgumentParser(
        prog="fluidinfo",
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(func=print_sys_info)
    parser.add_argument(
        "-s",
        "--save",
        help="saves system information to an xml file " "(sys_info.xml)",
        action="store_true",
    )
    parser.add_argument(
        "-o", "--output-dir", help="save to directory", default=None
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        help="increase output verbosity (max: -vvv)",
        action="count",
    )
    parser.add_argument(
        "-W", "--warnings", help="show warnings", action="store_true"
    )
    return parser


def main(args=None):
    """Parse arguments and execute ``fluidinfo``."""
    if args is None:
        parser = _get_parser()
        args = parser.parse_args()

    if not args.warnings:
        warnings.filterwarnings("ignore", category=UserWarning)

    if args.save:
        save_sys_info()
    elif args.output_dir is not None:
        save_sys_info(args.output_dir)
    else:
        print_sys_info(args.verbosity)

    if not args.warnings:
        warnings.resetwarnings()


if __name__ == "__main__":
    main()
