"""
IO for HDF5 files (:mod:`fluiddyn.io.hdf5`)
===========================================

.. autoclass:: H5File
   :members:

.. autofunction:: save_variables_h5

.. autofunction:: load_variables_h5

"""

import numbers

import h5py
import numpy as np


class H5File(h5py.File):
    """HDF5 file."""

    def save_dict(self, keydict, dicttosave):
        """Save the dictionnary `dicttosave` in the file."""
        group_params = self.create_group(keydict)
        if len(dicttosave) > 0:
            for k, v in list(dicttosave.items()):
                group_params.create_dataset(k, data=v)

    def load_dict(self, keydict):
        """Load a group as a dictionnary."""
        group_params = self[keydict]
        params = {}
        for k, v_in_file in list(group_params.items()):
            v = v_in_file[...]
            if not isinstance(v, (float, int)) and v.ndim == 0:
                v = v.item()
            params[k] = v
        return params

    def update_dict(self, keydict, dicttosave):
        group_params = self[keydict]
        for k, v in list(dicttosave.items()):
            group_params.create_dataset(k, data=v)

    def save_dict_of_ndarrays(self, dicttosave, dtype=np.float32):
        """Save ndarrays in the file."""

        dicttosave1 = {}
        for k, v in list(dicttosave.items()):
            if isinstance(v, numbers.Number):
                v = [v]
            a = np.array(v, dtype=dtype)
            dicttosave1[k] = a[None, ...]

        if k not in list(self.keys()):
            for k, v in list(dicttosave1.items()):
                self.create_dataset(k, data=v, maxshape=(None,) + v.shape[1:])
        else:
            nb_saved_times = self[k].shape[0]
            for k, v in list(dicttosave1.items()):
                dset_p = self[k]
                dset_p.resize((nb_saved_times + 1,) + v.shape[1:])
                dset_p[nb_saved_times] = v

    def load(self, times_slice=None):
        """Load data."""
        dict_return = {}
        for k in list(self.attrs.keys()):
            dict_return[k] = self.attrs[k]

        for k in list(self.keys()):
            dict_return[k] = self[k][...]

        if times_slice is not None:
            try:
                times = dict_return["times"]
            except KeyError:
                raise ValueError("No array times in the file.")

            tstart = times_slice[0]

            if tstart is None:
                tstart = times[0]
            itstart = abs(times - tstart).argmin()

            if len(times_slice) > 1 and times_slice[1] is not None:
                tend = times_slice[1]
            else:
                tend = times[-1]
            itend = abs(times - tend).argmin()

            if len(times_slice) > 2 and times_slice[2] is not None:
                tstep = times_slice[2]
            else:
                tstep = 0.0

            its = [itstart]
            for it in range(itstart + 1, itend):
                if times[it] >= times[its[-1]] + tstep:
                    its.append(it)
            its = list(its)

            for k in list(self.keys()):
                dict_return[k] = dict_return[k][its]

        return dict_return


def save_variables_h5(path, variables, names=None):
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

       save_variables_h5('myfile.h5', locals(), ('a', 'b', 'c'))

    or from a dictionary::

       d = {'a': 1, 'b': 'str', 'c': np.ones(2)}
       save_variables_h5('myfile.h5', d)

    """
    if names is not None:
        variables_all = variables
        variables = {}
        for name in names:
            variables[name] = variables_all[name]

    with h5py.File(path, "w") as file:
        for key, value in variables.items():
            file.create_dataset(key, data=value)


def load_variables_h5(path):
    """Load files created with the function `save_variables_h5`.

    Parameters
    ----------

    path : str

      Path towards a hdf5 file saved with `save_variables_h5`.

    """

    variables = {}

    with h5py.File(path, "r") as file:
        for key, dataset in file.items():
            value = dataset[()]
            if isinstance(value, bytes):
                value = value.decode()
            variables[key] = value

    return variables


# if __name__ == '__main__':

#     pass
