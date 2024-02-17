"""dump file utility (:mod:`fluiddyn.io.dump`)
==============================================

"""

import argparse
import os
from glob import glob

import h5py

description = """

Utility to print the hierarchy of hdf5 and netcdf files.

"""

__doc__ += description


def dump(path, print_variables=False):
    print("dump file:", path)
    if path.endswith(".nc"):
        dump_nc_file(path, print_variables=print_variables)
    elif path.endswith(".h5"):
        dump_h5_file(path, print_variables=print_variables)


def dump_nc_file(path, print_variables=False):
    import h5netcdf

    with h5netcdf.File(path, "r") as obj:
        dump_nc_object(obj, level=0, print_variables=print_variables)


def dump_nc_object(obj, level=0, print_variables=False):
    indent1 = "  "
    indent = level * indent1
    indentp1 = indent + indent1

    print(indent + "netcdf object: " + obj.name)

    if len(obj.attrs) != 0:
        print(indentp1 + "attrs:", dict(obj.attrs))

    if len(obj.dimensions) != 0:
        print(indentp1 + "dimensions:", dict(obj.dimensions))

    if len(obj.variables) > 0:
        print(indentp1 + "variables:")
        for value in obj.variables.values():
            print(
                indentp1
                + "- variable {} (dimensions {}, dtype {})".format(
                    value.name, value.dimensions, value.dtype
                )
            )
            if len(value.attrs) != 0:
                print(indent1 + indentp1 + "attrs:", dict(value.attrs))
            if print_variables:
                print(indent1 + indentp1 + repr(value[()]))

    if len(obj.groups) > 0:
        print(indentp1 + "groups:")
        for name_group in obj.groups:
            print(indentp1 + "- " + name_group)

        for group in obj.groups.values():
            print()
            dump_nc_object(
                group, level=level + 1, print_variables=print_variables
            )


def dump_h5_file(path, print_variables=False):
    with h5py.File(path, "r") as obj:
        dump_h5_object(obj, level=0, print_variables=print_variables)


def dump_h5_object(obj, level=0, print_variables=False):
    indent1 = "  "
    indent = level * indent1
    indentp1 = indent + indent1

    print(indent + "hdf5 object: " + obj.name)

    if len(obj.attrs) != 0:
        print(indentp1 + "attrs:", dict(obj.attrs))

    variables = []
    groups = []
    for tmp in obj.values():
        try:
            tmp.keys
        except AttributeError:
            variables.append(tmp)
        else:
            groups.append(tmp)

    if len(variables) > 0:
        print(indentp1 + "variables:")
        for value in variables:
            print(indentp1 + f"- variable {value.name} (dtype {value.dtype})")
            if len(value.attrs) != 0:
                print(indent1 + indentp1 + "attrs:", dict(value.attrs))
            if print_variables:
                print(indent1 + indentp1 + repr(value[()]))

    if len(groups) > 0:
        print(indentp1 + "groups:")
        for group in groups:
            print(indentp1 + "- " + group.name)

        for group in groups:
            print()
            dump_h5_object(
                group, level=level + 1, print_variables=print_variables
            )


def main():
    parser = argparse.ArgumentParser(
        prog="fluiddump",
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "file", help="str indicating which file has to be dump.", type=str
    )

    parser.add_argument(
        "-pv",
        "--print-variables",
        help="also print the content of the variables",
        action="store_true",
    )

    args = parser.parse_args()

    if os.path.isfile(args.file):
        dump(args.file, print_variables=args.print_variables)
    else:
        paths = glob(args.file)
        if len(paths) == 0:
            raise ValueError("No file found from the input string:\n" + args.file)

        for path in paths:
            dump(path, print_variables=args.print_variables)
