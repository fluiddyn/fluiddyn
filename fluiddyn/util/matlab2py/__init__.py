"""Treat Matlab code to help the translation to Python code
===========================================================

This subpackage provides 2 modules to help a developer to translate a Matlab
code into a Python code. It is not a proper Matlab to Python translator. The
code produced is just more similar to Python than the original Matlab code.

.. autosummary::
   :toctree:

   cleanmat
   mat2wrongpy

"""

import argparse
import os


def get_index_closing_parenthesis(line, ind_start):
    if line[ind_start] != "(":
        raise ValueError("line[ind_start] != '('")

    in_parent = 1
    ind = ind_start
    while in_parent > 0:
        ind += 1
        if line[ind] == ")":
            in_parent -= 1
        elif line[ind] == "(":
            in_parent += 1

    return ind


# this can not be put at the top of the file and has to be put after the
# definition of get_index_closing_parenthesis
from . import cleanmat, mat2wrongpy

description = """

Utility to produce a strange code which is no longer Matlab and not yet Python.

"""


def main():
    parser = argparse.ArgumentParser(
        prog="fluidmat2py",
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "path",
        help="str indicating which file or directory has to be used.",
        type=str,
    )

    parser.add_argument(
        "-c", "--clean", help="Only clean the Matlab code.", action="store_true"
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        raise ValueError("Path args.path does not exits.")

    if os.path.isdir(args.path):
        if args.clean:
            cleanmat.treat_matlab_directory(args.path)
        else:
            mat2wrongpy.treat_matlab_directory(args.path)
    else:
        if args.clean:
            code = cleanmat.modif_code(args.path)
        else:
            code = mat2wrongpy.create_py_code(args.path)

        print(code)
