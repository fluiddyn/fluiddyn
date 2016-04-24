"""
Serie of arrays (:mod:`fluidlab.postproc.serieofarrays`)
========================================================

Provides classes to iterate over files.

Example::

  serie = SerieOfArraysFromFiles(path)

  def indslices_from_indserie(iserie):
      indslices = copy(serie._index_slices_all_files)
      indslices[0] = [iserie, iserie+1, 1]
      return indslices

  series = SeriesOfArrays(serie, indslices_from_indserie)

  for serie in series:
      print([name for name in serie])

API:

.. autoclass:: SerieOfArrays
   :members:
   :private-members:

.. autoclass:: SerieOfArraysFromFiles
   :members:
   :private-members:

.. autoclass:: SeriesOfArrays
   :members:
   :private-members:


"""

from __future__ import division, print_function

import os
from glob import glob

from copy import copy

import itertools

try:
    from scipy.ndimage import imread
except ImportError:
    from scipy.misc import imread


class SerieOfArrays(object):
    """Serie of arrays used for post-processing.

    Parameters
    ----------

    path : str
        The path of the base directory or of a file example.

    Attributes
    ----------
    path_dir : str
        The path of the base directory.

    """
    def __init__(self, path):
        if os.path.isfile(path):
            self.path_dir, self.filename_given = os.path.split(path)
        elif os.path.isdir(path):
            self.path_dir = path
            self.filename_given = glob(path + '/*')[0].split('/')[-1]
        else:
            l = glob(path)
            if len(l) == 0:
                raise ValueError('The provided path does not exist:\n'
                                 + path)

            self.path_dir, self.filename_given = os.path.split(l[0])

        if '.' in self.filename_given:
            self.extension_file = self.filename_given.split('.')[-1]
        else:
            self.extension_file = ''


class SerieOfArraysFromFiles(SerieOfArrays):
    """Serie of arrays saved in files (images, netcdf, etc.).

    Parameters
    ----------

    path : str
        The path of the base directory or of a file example.

    index_slices : None or iterable of iterables
        Series of slides (start, end, step).

    Attributes
    ----------
    path_dir : str
        The path of the base directory.

    index_slices : list of list
        Lists of slides "[start, end, step]" (one for each index).
        This list can be changed to loop over different sets of files.

    Notes
    -----

    An instance of SerieOfArraysFromFiles is an iterable and provides
    other iterables.

    Use the function :func:`set_index_slices` to specify the files
    over which iterate.

    """
    def __init__(self, path, index_slices=None):

        super(SerieOfArraysFromFiles, self).__init__(path)

        self.base_name = ''.join(
            itertools.takewhile(lambda c: not str.isdigit(c),
                                self.filename_given))

        if not str.isalpha(self.base_name[-1]):
            self.base_name = self.base_name[:-1]

        # remove base_name
        remains = self.filename_given[len(self.base_name):]

        # remove extension
        if self.extension_file != '':
            remains = remains[:-(1+len(self.extension_file))]

        # separator between base and index
        if not str.isdigit(remains[0]):
            self._separator_base_index = remains[0]
            remains = remains[1:]
        else:
            self._separator_base_index = ''

        self._index_types = []
        self._index_lens = []
        self._index_separators = []
        while len(remains) != 0:
            if str.isdigit(remains[0]):
                test_type = str.isdigit
                self._index_types.append('digit')
            elif str.isalpha(remains[0]):
                test_type = str.isalpha
                self._index_types.append('alpha')
            index = ''.join(itertools.takewhile(test_type, remains))
            self._index_lens.append(len(index))
            remains = remains[len(index):]
            if len(remains) > 0:
                if not str.isalnum(remains[0]):
                    self._index_separators.append(remains[0])
                    remains = remains[1:]
                else:
                    self._index_separators.append('')
        self._index_separators.append('')

        self.nb_indices = len(self._index_types)

        str_glob_indices = ''
        for separator in self._index_separators:
            str_glob_indices = str_glob_indices + '*' + separator

        str_glob = (self.base_name + self._separator_base_index +
                    str_glob_indices)
        if self.extension_file != '':
            str_glob = str_glob + '.' + self.extension_file
        str_glob = os.path.join(self.path_dir, str_glob)
        paths = glob(str_glob)
        if not paths:
            raise ValueError(
                'There is no data in the provided path directory: ' + str_glob)

        file_names = [os.path.basename(p) for p in paths]
        file_names.sort()

        indices_all_files = [
            self.compute_indices_from_filename(file_name)
            for file_name in file_names]

        indices_indices = zip(*indices_all_files)
        self._index_slices_all_files = []
        for i_ind in range(self.nb_indices):
            self._index_slices_all_files.append(
                [min(indices_indices[i_ind]),
                 max(indices_indices[i_ind])+1, 1])

        if index_slices is None:
            self._index_slices = copy(self._index_slices_all_files)
        else:
            self.set_index_slices(*index_slices)

    def get_arrays(self):
        return tuple(a for a in self.iter_arrays())

    def get_name_files(self):
        return tuple(n for n in self.iter_name_files())

    def get_array_from_name(self, name):
        return imread(os.path.join(self.path_dir, name))

    def get_array_from_indices(self, *indices):
        return self.get_array_from_name(
            self.compute_name_from_indices(*indices))

    def get_array_from_index(self, index):
        indices = [t for t in self.iter_indices()][index]
        return self.get_array_from_indices(*indices)

    def get_path_all_files(self):
        str_glob = os.path.join(self.path_dir, self.base_name + '*')
        paths = glob(str_glob)
        paths.sort()
        return paths

    def get_path_files(self):
        return [os.path.join(self.path_dir, name)
                for name in self.get_name_files()]

    def verify_all_fields_present(self):
        raise ValueError('Not yet implemented.')

    def iter_indices(self):
        islices = list(self._index_slices)
        for i, islice in enumerate(islices):
            if len(islice) == 1:
                islices[i] = [islice[0], islice[0]+1]
        lists = [range(*s) for s in islices]
        for l in itertools.product(*lists):
            yield l

    def iter_name_files(self):
        for l in self.iter_indices():
            yield self.compute_name_from_indices(*l)

    __iter__ = iter_name_files

    def iter_path_files(self):
        for name in self.iter_name_files():
            yield os.path.join(
                self.path_dir, name)

    def iter_arrays(self):
        for name in self.iter_name_files():
            yield self.get_array_from_name(name)

    def _compute_strindices_from_indices(self, *indices):
        """Compute the string corresponding to the indices.

        Parameters
        ----------

        indices: iterable of int.

        """
        nb_indices = len(indices)
        if nb_indices != self.nb_indices:
            raise ValueError('nb_indices != self.nb_indices')

        str_indices = ''
        for i in range(nb_indices):
            if self._index_types[i] == 'digit':
                code_format = '{:0' + str(self._index_lens[i]) + 'd}'
                str_index = code_format.format(indices[i])
            elif self._index_types[i] == 'alpha':
                if indices[i] > 25:
                    raise ValueError('"alpha" index larger than 25.')
                str_index = chr(ord('a') + indices[i])
            else:
                raise Exception('The type should be "digit" or "alpha".')

            str_indices += str_index + self._index_separators[i]
        return str_indices

    def compute_name_from_indices(self, *indices):
        """Compute a file name from a list of indices.

        Parameters
        ----------

        indices: iterable of int.
        """
        name_file = (self.base_name + self._separator_base_index
                     + self._compute_strindices_from_indices(*indices))
        if self.extension_file != '':
            name_file = name_file + '.' + self.extension_file

        return name_file

    def compute_indices_from_filename(self, file_name):
        """Compute a list of indices from a file name.

        Parameters
        ----------

        file_name: str
        """
        str_indices = file_name[len(self.base_name):]

        if self._separator_base_index != '':
            str_indices = str_indices[1:]

        if self.extension_file != '':
            str_indices = str_indices[:-(len(self.extension_file)+1)]

        remains = str_indices
        indices = []
        for i_ind in range(self.nb_indices):
            if self._index_types[i_ind] == 'digit':
                test_type = str.isdigit
            elif self._index_types[i_ind] == 'alpha':
                test_type = str.isalpha
            else:
                raise Exception('The type should be "digit" or "alpha".')

            index = ''.join(itertools.takewhile(test_type, remains))
            remains = remains[len(index):]
            if self._index_separators[i_ind] != '':
                remains = remains[1:]

            if self._index_types[i_ind] == 'digit':
                index = int(index)
            elif self._index_types[i_ind] == 'alpha':
                index = ord(index) - ord('a')

            indices.append(index)

        assert len(remains) == 0
        return indices

    def isfile(self, path):
        """Check whether a path or name corresponds to an existing file."""
        if not os.path.isabs(path):
            path = os.path.join(self.path_dir, path)
        return os.path.exists(path)

    def get_index_slices_all_files(self):
        return self._index_slices_all_files

    def get_index_slices(self):
        return self._index_slices

    def set_index_slices(self, *index_slices):
        if len(index_slices) != self.nb_indices:
            raise ValueError(
                'indices has to be similar to self._index_slices_all_files')

        self._index_slices = index_slices

    def get_nb_files(self):
        return len([i for i in self.iter_indices()])


class SeriesOfArrays(object):
    """Series of arrays.

    This class can be used to produce series of arrays from a
    :class:`SerieOfArrays`.

    Arguments
    ---------

    serie: SerieOfArrays or str

    indslices_from_indserie: str or function

      The function has to take an integer and to return an iterable of
      indices used to compute a file name.

    """
    def __init__(self, serie, indslices_from_indserie,
                 ind_stop=None):
        if isinstance(serie, str):
            serie = SerieOfArraysFromFiles(serie)
        if isinstance(serie, SerieOfArraysFromFiles):
            self.serie = serie
        else:
            raise ValueError(
                'serie should be a str or a SerieOfArraysFromFiles.')

        if isinstance(indslices_from_indserie, str):
            l_range = indslices_from_indserie.split(',')

            def indslices_from_indserie(i):
                return [
                    [eval(s) for s in s_range.split(':')]
                    for s_range in l_range]

        self.indslices_from_indserie = indslices_from_indserie

        if ind_stop is None:
            iserie = -1
            cond = True
            while cond:
                iserie += 1
                serie.set_index_slices(
                    *self.indslices_from_indserie(iserie))
                name_files = serie.get_name_files()
                cond = all([serie.isfile(name) for name in name_files])
            ind_stop = iserie
        else:
            for iserie in range(ind_stop):
                serie.set_index_slices(
                    *self.indslices_from_indserie(iserie))
                name_files = [name for name in serie.iter_name_files()]
                if not all([serie.isfile(name) for name in name_files]):
                    break

        self.iserie = 0
        self.ind_stop = ind_stop
        self.nb_series = iserie

    def __iter__(self):

        if hasattr(self, 'index_series'):
            index_series = self.index_series
        else:
            index_series = range(self.ind_stop)

        for iserie in index_series:
            self.serie.set_index_slices(
                *self.indslices_from_indserie(iserie))
            yield self.serie

    def __len__(self):
        return len([s for s in self])

    def set_index_series(self, index_series):
        self.index_series = index_series

    def get_next_serie(self):
        if self.iserie < self.ind_stop:
            self.serie.set_index_slices(
                *self.indslices_from_indserie(self.iserie))
            self.iserie += 1
            return self.serie

    def get_serie_from_index(self, index):
        self.serie.set_index_slices(
            *self.indslices_from_indserie(index))
        return self.serie

    def get_name_all_files(self):
        names_all = []
        for serie in self:
            names = serie.get_name_files()
            for name in names:
                if name not in names_all:
                    names_all.append(name)
        return names_all


if __name__ == '__main__':

    # path = (
    #     os.environ['HOME'] +
    #     '/Dev/Matlab/Demo/UVMAT_DEMO04_PIV_challenge_2005_CaseC/'
    #     'Images'
    #     '/c001a.png'
    # )

    # serie = SerieOfArraysFromFiles(path)

    # def indslices_from_indserie(iserie):
    #     indslices = copy(serie._index_slices_all_files)
    #     indslices[0] = [iserie, iserie+1]
    #     return indslices

    # series = SeriesOfArrays(serie, indslices_from_indserie)

    # for serie in series:
    #     print([name for name in serie])

    # print('\nOther test')

    # def indslices_from_indserie(iserie):
    #     indslices = copy(serie._index_slices_all_files)
    #     indslices[0] = [iserie, iserie+2, 1]
    #     indslices[1] = [1]
    #     return indslices

    # series = SeriesOfArrays(serie, indslices_from_indserie)

    # for serie in series:
    #     print([name for name in serie])

    path = (
        os.environ['HOME'] +
        '/Dev/howtopiv/samples/Karman'
    )

    serie = SerieOfArraysFromFiles(path, base_name='PIVlab_Karman')

    def indslices_from_indserie(iserie):
        indslices = copy(serie._index_slices_all_files)
        indslices[0] = [iserie+1, iserie+2]
        return indslices

    series = SeriesOfArrays(serie, indslices_from_indserie)

    for serie in series:
        print([name for name in serie])
