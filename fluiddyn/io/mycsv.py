"""
IO for csv files (:mod:`fluiddyn.io.csv`)
==========================================

Provides:

.. autoclass:: CSVFile
   :members:
   :private-members:

"""

import csv
import io as _io

import numpy as np


class CSVFile(_io.FileIO):

    def __init__(self, *args, **kargs):
        super(CSVFile, self).__init__(*args, **kargs)

        self.reader = csv.DictReader(self)
        self.fieldnames = self.reader.fieldnames

    def load_as_dict(self, keys=None, skiptimes=0):
        if keys is None:
            keys = self.fieldnames
        else:
            for key in keys:
                if key not in self.fieldnames:
                    raise ValueError('A key is not in self.fieldnames')

        usecols = []
        for key in keys:
            usecols.append(self.fieldnames.index(key))

        # find dtypes from first line
        dtypes = []
        try:
            row = self.reader.next()
        except StopIteration:
            ret = {}
            for key in keys:
                ret[key] = np.array([])
            return ret
        else:
            for ik, key in enumerate(keys):
                value = row[key]
                if '.' in value:
                    dtype = np.float64
                else:
                    dtype = np.int32
                dtypes.append(dtype)

        self.seek(0)
        arr = np.loadtxt(self, delimiter=',', skiprows=1+skiptimes,
                         usecols=usecols).T

        ret = {}
        for ik, key in enumerate(keys):
            ret[key] = np.array(arr[ik], dtype=dtypes[ik])

        return ret

    def get_fieldnames(self):
        return self.fieldnames
