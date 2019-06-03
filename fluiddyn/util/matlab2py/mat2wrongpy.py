"""Matlab -> wrong Python translator
====================================

Many more simple transformations can be implemented, for example:

+----------------+---------------------+
|   ``disp(``    |    ``print(``       |
+----------------+---------------------+
| ``zeros(...)`` | ``np.zeros((...))`` |
+----------------+---------------------+

"""


import os

from . import cleanmat
from .cleanmat import modif_code

block_definers = ("if", "while", "for", "elseif")

ident = 4 * " "


def is_comment_line(line):
    return line.strip().startswith("#")


def modif_blocks(code_lines):
    lines_new = []
    for line in code_lines:

        if not any(line.strip().startswith(s) for s in block_definers + ("end",)):
            lines_new.append(line)
            continue

        if not line.strip().startswith("end"):
            lines_new.append(line + ":")

    return lines_new


def modif_comments(code_lines):
    lines_new = []

    for line in code_lines:
        if not cleanmat.is_comment_line(line):
            lines_new.append(line)
            continue

        lines_new.append(line.replace("%", "#", 1))

    return lines_new


def modif_remove_semicolon(code_lines):
    lines_new = []

    for line in code_lines:
        if is_comment_line(line):
            lines_new.append(line)
            continue

        if line.endswith(";"):
            line = line[:-1]

        lines_new.append(line)

    return lines_new


def modif_remove_3dots(code_lines):
    lines_new = []

    for line in code_lines:
        if is_comment_line(line):
            lines_new.append(line)
            continue

        if line.endswith("..."):
            line = line[:-3] + "\\"

        lines_new.append(line)

    return lines_new


def create_py_code(path_file):

    code = modif_code(path_file)

    code_lines = code.split("\n")

    modif_functions = [
        modif_blocks,
        modif_comments,
        modif_remove_semicolon,
        modif_remove_3dots,
    ]

    for func in modif_functions:
        code_lines = func(code_lines)

    new_code = "\n".join(code_lines)
    return new_code


def treat_matlab_directory(path_dir):

    path_cleaner = path_dir + "_py"

    if not os.path.exists(path_cleaner):
        os.mkdir(path_cleaner)

    for root, subdirs, nfiles in os.walk(path_dir):
        relative_path = root[len(path_dir) :]

        new_dir = path_cleaner + relative_path

        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        matlab_nfiles = [nfile for nfile in nfiles if nfile.endswith(".m")]

        for nfile in matlab_nfiles:
            nfilepy = nfile[:-2] + ".py"

            path_file = os.path.join(root, nfile)
            path_file_new = os.path.join(new_dir, nfilepy)

            print((path_file, path_file_new))

            new_code = create_py_code(path_file)

            with open(path_file_new, "w") as f:
                f.write(new_code)


if __name__ == "__main__":

    path_dir = "diablo_mat"

    treat_matlab_directory(path_dir)

# code = modif_code(path_dir + '/diablo.m')
# print(code)

# code_lines = [
#     "    TIME=TIME+DELTA_T;",
#     "    if (mod(TIME_STEP,10)==0 & toto == 2)"]
# print('\n'.join(modif_spaces_around_operators(code_lines)))
