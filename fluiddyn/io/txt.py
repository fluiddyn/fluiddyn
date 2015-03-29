"""
IO for text files (:mod:`fluiddyn.io.txt`)
==========================================

.. currentmodule:: fluiddyn.io.txt

Provides the functions :func:`num_from_str`,
:func:`quantities_from_txt_file` and
:func:`save_quantities_in_txt_file`.


.. autofunction:: num_from_str

.. autofunction:: quantities_from_txt_file

.. autofunction:: save_quantities_in_txt_file

"""


from __future__ import division, print_function

import os
import numpy as np

from fluiddyn.util import query


def num_from_str(s):
    """Return a number from a string."""
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            raise ValueError(
                'Can not convert the string "'+s+'" into a numeric value.')



def quantities_from_txt_file(name_file):
    """Read a txt file and return the numerical data."""
    if os.path.isabs(name_file):
        path_file = name_file
    else:
        path_file = os.getcwd()+'/'+name_file

    if not os.path.exists(path_file):
        raise ValueError('file does not exist? path_file :\n'+path_file)

    f = open(path_file, 'r')
    lines = f.readlines()
    f.close()

    lines_with_num_data = []
    nb_nums_per_line = 0

    while len(lines) > 0:
        words = lines[0].split()
        del(lines[0])
        try:
            float(words[0])
            lines_with_num_data.append(words)
            if nb_nums_per_line < len(words):
                nb_nums_per_line = len(words)
        except (ValueError, IndexError):
            pass

    # create a list of lists
    lol = [[] for l in range(nb_nums_per_line)]

    for words in lines_with_num_data:
        for iw, word in enumerate(words):
            lol[iw].append(num_from_str(word))

    for iq in range(nb_nums_per_line):
        lol[iq] = np.array(lol[iq])

    return tuple(lol)




def save_quantities_in_txt_file(name_file, args, erase=False):
    """Save array_like objects in a text file."""
    try:
        args[0][0]
    except ValueError:
        raise ValueError('args has to be 2 times iterable...')

    nb_quantities = len(args)

    if nb_quantities < 1:
        raise ValueError('At least one quantity has to be given.')

    nb_values_1q = len(args[0])
    for iq in range(1, nb_quantities):
        if len(args[iq]) != nb_values_1q:
            raise ValueError('All quantities should have the same length.')

    if os.path.isfile(name_file) and not erase:
        answer = query.query(
            'The file '+name_file+' already exists. '+
            'What do you want to do?\n'+
            "[Don't save / erase file and save / modify name] ",
            default="Don't save"
            )
        if answer.lower().startswith('do'):
            print('The quantities have not been saved.')
            return
        elif answer.lower().startswith('e'):
            print('Existing file will be erased.')
        else:
            # need to be improved !
            print('Sorry. This option has to be implemented. '
                  'The quantities have not been saved.')
            return

    with open(name_file, 'w') as f:
        for iv in range(nb_values_1q):
            for iq in range(nb_quantities):
                f.write(repr(args[iq][iv]))
                f.write(' ')
            f.write('\n')











if __name__ == '__main__':

    t = quantities_from_txt_file('files.py')
    print(t)

    save_quantities_in_txt_file('test', t)


"""
zekfzlnfk

zklflzefk

1   3. 1

2   5. 4.
3  4  9
"""
