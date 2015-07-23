"""
IO for HDF5 files (:mod:`fluiddyn.io.hdf5`)
===============================================

.. currentmodule:: fluiddyn.io.hdf5

Provides the class :class:`H5File`.

.. autoclass:: H5File
   :members:


"""


from __future__ import division, print_function

import numpy as np
import numbers
import h5py


class H5File(h5py.File):
    """HDF5 file."""

    def save_dict(self, keydict, dicttosave):
        """Save the dictionnary `dicttosave` in the file.

        """
        group_params = self.create_group(keydict)
        if len(dicttosave) > 0:
            for k, v in dicttosave.items():
                group_params.create_dataset(k, data=v)

    def load_dict(self, keydict):
        """Load a group as a dictionnary.

        """
        group_params = self[keydict]
        params = {}
        for k, v_in_file in group_params.items():
            v = v_in_file[...]
            if not isinstance(v, (float, int)) and v.ndim == 0:
                v = v.item()
            params[k] = v
        return params

    def update_dict(self, keydict, dicttosave):

        group_params = self[keydict]
        for k, v in dicttosave.items():
            group_params.create_dataset(k, data=v)

    def save_dict_of_ndarrays(self, dicttosave, dtype=np.float32):
        """Save ndarrays in the file."""

        for k, v in dicttosave.items():
            if isinstance(v, numbers.Number):
                v = [v]
            dicttosave[k] = np.array(v, dtype=dtype)

        if k not in self.keys():
            for k, v in dicttosave.items():
                self.create_dataset(k, data=v,
                                    maxshape=(None,)+v.shape[1:])
        else:
            nb_saved_times = self[k].shape[0]
            for k, v in dicttosave.items():
                dset_p = self[k]
                dset_p.resize((nb_saved_times+1,)+v.shape[1:])
                dset_p[nb_saved_times] = v

    def load(self, times_slice=None):
        """Load data."""
        dict_return = {}
        for k in self.attrs.keys():
            dict_return[k] = self.attrs[k]

        for k in self.keys():
            dict_return[k] = self[k][...]

        if times_slice is not None:
            try:
                times = dict_return['times']
            except KeyError:
                raise ValueError('No array times in the file.')

            tstart = times_slice[0]

            if tstart is None:
                tstart = times[0]
            itstart = abs(times-tstart).argmin()

            if len(times_slice) > 1 and times_slice[1] is not None:
                tend = times_slice[1]
            else:
                tend = times[-1]
            itend = abs(times-tend).argmin()

            if len(times_slice) > 2 and times_slice[2] is not None:
                tstep = times_slice[2]
            else:
                tstep = 0.

            its = [itstart]
            for it in range(itstart+1, itend):
                if times[it] >= times[its[-1]] + tstep:
                    its.append(it)
            its = list(its)

            for k in self.keys():
                dict_return[k] = dict_return[k][its]

        return dict_return


# if __name__ == '__main__':

#     pass
