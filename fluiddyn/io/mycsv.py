"""
IO for csv files (:mod:`fluiddyn.io.mycsv`)
===========================================

Provides:

.. autoclass:: CSVFile
   :members:
   :private-members:

"""

import csv

import numpy as np


class CSVFile:
    def __init__(self, *args, **kargs):
        self._textio = open(*args, **kargs)
        self.reader = csv.DictReader(self._textio)
        self.fieldnames = self.reader.fieldnames

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._textio.close()

    def load_as_dict(self, keys=None, skiptimes=0):
        if keys is None:
            keys = self.fieldnames
        else:
            for key in keys:
                if key not in self.fieldnames:
                    raise ValueError("A key is not in self.fieldnames")

        usecols = []
        for key in keys:
            usecols.append(self.fieldnames.index(key))

        # find dtypes from first line
        dtypes = []
        try:
            row = next(self.reader)
        except StopIteration:
            ret = {}
            for key in keys:
                ret[key] = np.array([])
            return ret

        else:
            for ik, key in enumerate(keys):
                value = row[key]
                if "." in value:
                    dtype = np.float64
                else:
                    dtype = np.int32
                dtypes.append(dtype)

        self._textio.seek(0)
        arr = np.loadtxt(
            self._textio, delimiter=",", skiprows=1 + skiptimes, usecols=usecols
        ).T

        ret = {}
        for ik, key in enumerate(keys):
            ret[key] = np.array(arr[ik], dtype=dtypes[ik])

        return ret

    def get_fieldnames(self):
        return self.fieldnames
