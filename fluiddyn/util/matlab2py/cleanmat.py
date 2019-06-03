"""Clean Matlab code
====================

"""


import os

from . import get_index_closing_parenthesis

block_definers = ("if", "while", "for")

ident = 4 * " "


def is_comment_line(line):
    return line.strip().startswith("%")


def modif_identation(code_lines):

    ident_level = 0
    lines_new = []

    for line in code_lines:
        line = line.strip()
        if line == "":
            lines_new.append(line)
            continue

        ident_direction_for_next = 0
        ident_this_line = 0

        # first_name = line.split(maxsplit=1)[0]
        # for Python 2.7
        first_name = line.split(None, 1)[0]
        if first_name in block_definers:
            ident_direction_for_next = 1
        elif first_name in ("end", "end;"):
            ident_direction_for_next = -1
            ident_this_line = -1
        elif first_name == "elseif":
            ident_direction_for_next = 0
            ident_this_line = -1

        lines_new.append((ident_level + ident_this_line) * ident + line)
        ident_level += ident_direction_for_next

    return lines_new


def modif_unwrap_if(code_lines):
    lines_new = []
    for line in code_lines:
        line = line.strip()
        if_starts = ("if (", "elseif (")

        if not any(line.startswith(s) for s in if_starts):
            lines_new.append(line)
            continue

        for s in if_starts:
            if line.startswith(s):
                index_begin = len(s) - 1

        index = get_index_closing_parenthesis(line, index_begin)
        if_statement = line[: index + 1]
        lines_new.append(if_statement)
        rest_line = line[index + 1 :]

        if len(rest_line) == 0:
            continue

        lines_new.append(rest_line)

    return lines_new


def modif_split_statements(code_lines):
    lines_new = []
    for line in code_lines:
        line = line.strip()

        if is_comment_line(line) or ";" not in line:
            lines_new.append(line)
            continue

        statements = [stat.strip() for stat in line.split(";")]

        for i, stat in enumerate(statements[:-1]):
            statements[i] = stat + ";"

        if statements[-1] == "":
            statements = statements[:-1]

        lines_new.extend(statements)

    return lines_new


def modif_split_comments_from_code(code_lines):
    lines_new = []
    for line in code_lines:
        line = line.strip()

        if is_comment_line(line) or "%" not in line:
            lines_new.append(line)
            continue

        parts = line.split("%")
        before_comment = ""
        for i, part in enumerate(parts):
            before_comment += part
            if not before_comment.endswith("\\"):
                break

            else:
                before_comment += "%"

        comment_parts = parts[i + 1 :]
        if len(comment_parts) == 0:
            # no comment in the line
            lines_new.append(line)
            continue

        comment = "%" + "%".join(comment_parts)

        if line.startswith("if "):
            lines_new.extend([before_comment, comment])
        else:
            lines_new.extend([comment, before_comment])

    return lines_new


def modif_spaces_around_operators(code_lines):
    lines_new = []
    for line in code_lines:

        if is_comment_line(line) or "=" not in line or "for " in line:
            lines_new.append(line)
            continue

        parts = line.split("=")

        new_line = ""

        for i, part in enumerate(parts[:-1]):
            new_line += part

            if part != "" and not part.endswith(" "):
                new_line += " "

            new_line += "="

            if parts[i + 1] != "" and not parts[i + 1].startswith(" "):
                new_line += " "

        new_line += parts[-1]
        lines_new.append(new_line)

    return lines_new


def modif_space_after_comma(code_lines):
    lines_new = []
    for line in code_lines:

        if is_comment_line(line):
            lines_new.append(line)
            continue

        parts = line.split(",")

        new_line = ""
        for i, part in enumerate(parts[:-1]):
            new_line += part + ","

            if not parts[i + 1].startswith(" "):
                new_line += " "

        new_line += parts[-1]
        lines_new.append(new_line)

    return lines_new


def modif_code(path_file):

    with open(path_file) as f:
        code_lines = f.readlines()

    modif_functions = [
        modif_split_comments_from_code,
        modif_split_statements,
        modif_unwrap_if,
        modif_spaces_around_operators,
        modif_space_after_comma,
        modif_identation,
    ]

    for func in modif_functions:
        code_lines = func(code_lines)

    new_code = "\n".join(code_lines)
    return new_code


def treat_matlab_directory(path_dir):

    path_cleaner = path_dir + "_cleaner"

    if not os.path.exists(path_cleaner):
        os.mkdir(path_cleaner)

    for root, subdirs, nfiles in os.walk(path_dir):
        relative_path = root[len(path_dir) :]

        new_dir = path_cleaner + relative_path

        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        matlab_nfiles = [nfile for nfile in nfiles if nfile.endswith(".m")]

        for nfile in matlab_nfiles:
            path_file = os.path.join(root, nfile)
            path_file_new = os.path.join(new_dir, nfile)

            print((path_file, path_file_new))

            new_code = modif_code(path_file)

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
