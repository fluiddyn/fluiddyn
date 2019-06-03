"""IO for python files containing data (:mod:`fluiddyn.io.in_py`)
=================================================================

.. autofunction:: save_in_py

"""

import sys

import numpy as np


def save_in_py(path, variables, names=None):
    """Save data in `variables` in the file `path`.

    Parameters
    ----------

    path : str

      Path of the file where the data are saved (has to end with '.py').

    variables : dict

      Contains the variables to be saved.

    names : None or sequence of str.

      If None, all variables in variables are saved, else, only the variables
      with name in names of the variables to be saved.

    Examples
    --------

    .. code::

       a = 1
       b = 'str'
       c = np.ones(2)

       save_in_py('myfile.py', locals(), ('a', 'b', 'c'))

    or from a dictionary::

       d = {'a': 1, 'b': 'str', 'c': np.ones(2)}
       save_in_py('myfile.py', d)

    """
    if not path.endswith(".py"):
        raise ValueError

    if names is not None:
        variables_all = variables
        variables = {}
        for name in names:
            variables[name] = variables_all[name]

    np.set_printoptions(threshold=sys.maxsize)
    with open(path, "w") as f:
        f.write("from numpy import array, nan\n")
        for key, value in variables.items():
            f.write(key + " = " + repr(value) + "\n")
