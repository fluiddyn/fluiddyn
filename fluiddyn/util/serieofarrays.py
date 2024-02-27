"""
Serie of arrays
===============

Provides classes to iterate over numbered files in a directory:

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

import itertools
import os
from copy import copy, deepcopy
from functools import partial
from glob import escape, glob
from math import ceil, log10

from simpleeval import simple_eval

from fluiddyn.io import Path
from fluiddyn.io.image import extensions_movies, imread

try:
    import pims
except ImportError:
    pass


def get_nb_arrays_in_file(fname):
    with pims.open(fname) as images:
        return images.len()


def compute_slices(str_slices):
    """Return a tuple of slices"""
    slices = []
    parts = str_slices.split(",")

    for part in parts:
        try:
            index = simple_eval(part)
        except SyntaxError:
            parts_slice = []
            for p in part.split(":"):
                if p.strip() == "":
                    parts_slice.append(None)
                else:
                    parts_slice.append(simple_eval(p))

            slices.append(slice(*parts_slice))
        else:
            if not isinstance(index, int):
                raise ValueError
            slices.append(index)

    return tuple(slices)


class SerieOfArrays:
    """Serie of arrays used for post-processing.

    Parameters
    ----------

    path : str
        The path of the base directory or of a file example.

    Attributes
    ----------
    path : str
        The path of the base directory.

    """

    def __init__(self, path):
        path = os.path.expanduser(path)
        if os.path.isfile(path):
            self.path_dir, self.filename_given = os.path.split(path)
        elif os.path.isdir(path):
            self.path_dir = path
            sep = os.path.sep
            filelist = glob(path + sep + "*")
            filelist.sort()
            self.filename_given = filelist[0].split(sep)[-1]
        else:
            if len(path) == 0:
                raise ValueError(
                    "The provided (empty) string does not point on any "
                    "existing path."
                )

            filelist = glob(path)
            if len(filelist) == 0:
                raise ValueError(
                    "The provided string does not point on any existing path. "
                    "The string is:\n" + path
                )

            self.path_dir, self.filename_given = os.path.split(filelist[0])

        path = os.path.join(self.path_dir, self.filename_given)
        if not os.path.isfile(path):
            raise ValueError(
                "The path given does not point towards a file "
                "but towards:\n" + path
            )

        if "." in self.filename_given:
            # bad hack
            if "[" in self.filename_given:
                self.extension_file = self.filename_given.rsplit(".", 1)[-1]
            else:
                self.extension_file = ".".join(self.filename_given.split(".")[1:])
        else:
            self.extension_file = ""


class SerieOfArraysFromFiles(SerieOfArrays):
    """Serie of arrays saved in files (images, netcdf, etc.).

    Parameters
    ----------

    path : str
        The path of the base directory or of a file example.

    slicing_tuples : None or iterable of iterables or str

        Iterable of slides (start, stop, step).

        Can also be a string of the form "0:2:6, 1" (in this case for two
        indexes).

    Attributes
    ----------
    path_dir : str
        The path of the base directory.

    slicing_tuples : list of list
        Lists of slides "[start, stop, step]" (one for each index).
        This list can be changed to loop over different sets of files.

    Notes
    -----

    An instance of SerieOfArraysFromFiles is an iterable and provides
    other iterables.

    Use the function :func:`set_slicing_tuples` to specify the files
    over which iterate.

    """

    def __init__(self, path, slicing=None):
        super().__init__(path)

        self.base_name = "".join(
            itertools.takewhile(
                lambda c: not c.isdigit(),
                self.filename_given[: -(1 + len(self.extension_file))],
            )
        )

        if len(self.base_name) > 0 and not self.base_name[-1].isalpha():
            self.base_name = self.base_name[:-1]

        # remove base_name
        remains = str(self.filename_given[len(self.base_name) :])

        # remove extension
        if self.extension_file != "":
            remains = remains[: -(1 + len(self.extension_file))]

        # separator between base and index
        if len(remains) > 0 and not remains[0].isdigit():
            self._separator_base_index = remains[0]
            remains = remains[1:]
        else:
            self._separator_base_index = ""

        self._index_types = []
        self._index_lens = []
        self._index_separators = []
        while len(remains) != 0:
            if remains[0].isdigit():
                test_type = str.isdigit
                self._index_types.append("digit")
            elif remains[0].isalpha():
                test_type = str.isalpha
                self._index_types.append("alpha")
            str_index = "".join(itertools.takewhile(test_type, remains))
            self._index_lens.append(len(str_index))
            remains = remains[len(str_index) :]
            if len(remains) > 0:
                if not str.isalnum(remains[0]):
                    self._index_separators.append(remains[0])
                    remains = remains[1:]
                else:
                    self._index_separators.append("")

        if len(self._index_separators) < len(self._index_types):
            self._index_separators.append("")

        self.nb_indices_name_file = len(self._index_types)

        str_glob_indices = ""
        for separator in self._index_separators:
            str_glob_indices += "*" + escape(separator)

        str_glob = (
            self.base_name + escape(self._separator_base_index) + str_glob_indices
        )
        if self.extension_file != "":
            str_glob += "." + self.extension_file
        str_glob = os.path.join(self.path_dir, str_glob)
        paths = glob(str_glob)
        if not paths:
            raise ValueError(
                "There is no data in the provided path directory: " + str_glob
            )

        file_names = [os.path.basename(p) for p in paths]
        file_names.sort()

        # for files containing more than one image
        if self.extension_file in extensions_movies:
            self._from_movies = True
            self.nb_indices = self.nb_indices_name_file + 1
            if len(file_names) == 0:
                names = []
            else:
                self._nb_arrays_file = {}
                self._nb_arrays_file[paths[0]] = self.nb_arrays_in_one_file = (
                    get_nb_arrays_in_file(paths[0])
                )

                self._format_index = (
                    "[{"
                    + ":0{}d".format(int(ceil(log10(self.nb_arrays_in_one_file))))
                    + "}]"
                )
                str_internal_index = [
                    self._format_index.format(i)
                    for i in range(self.nb_arrays_in_one_file)
                ]
                names = []
                for fname in file_names:
                    names.extend(fname + s for s in str_internal_index)
        else:
            self._from_movies = False
            names = file_names
            self.nb_indices = self.nb_indices_name_file

        indices_all_files = [
            self.compute_indices_from_name(name) for name in names
        ]

        self._slicing_tuples_all_files = []
        tmp = list(zip(*indices_all_files))
        for i_ind in range(self.nb_indices):
            self._slicing_tuples_all_files.append(
                tuple([min(tmp[i_ind]), max(tmp[i_ind]) + 1, 1])
            )

        if isinstance(slicing, str):
            self.set_slicing_tuples_from_str(slicing)
        elif slicing is None:
            self._slicing_tuples = copy(self._slicing_tuples_all_files)
        else:
            self.set_slicing_tuples(*slicing)

    def set_slicing_tuples_from_str(self, str_slices):
        """Set slicing_tuples from a string."""
        slices = compute_slices(str_slices)
        slicing_tuples = []
        for slice_ in slices:
            if isinstance(slice_, slice):
                step = slice_.step or 1
                slicing_tuples.append((slice_.start, slice_.stop, step))
            else:
                slicing_tuples.append(slice_)
        self.set_slicing_tuples(*slicing_tuples)

    def get_arrays(self):
        """Get the arrays on the serie."""
        return tuple(a for a in self.iter_arrays())

    def get_name_files(self):
        """Get the names of the files of the serie."""
        return tuple(n for n in self.iter_name_files())

    def get_name_arrays(self):
        """Get the name of the arrays of the serie."""
        return tuple(n for n in self.iter_name_arrays())

    def get_array_from_name(self, name):
        """Get the array from its name."""
        return imread(os.path.join(self.path_dir, name))

    def get_array_from_indices(self, *indices):
        """Get an array from its indices.

        Parameters
        ----------

        *indices :

          As many indices as used in the serie. For example with names of the
          form 'im100a.png', 2 indices are needed.

        """
        return self.get_array_from_name(self.compute_name_from_indices(*indices))

    def get_tuples_indices(self):
        return [
            tuple(range(*start_stop_step))
            for start_stop_step in self._slicing_tuples
        ]

    def get_indices_from_index(self, index):
        """Get indices from a flatten index"""
        if self.nb_indices_name_file == 1:
            return tuple([range(*self._slicing_tuples[0])[index]])
        elif self.nb_indices_name_file == 2:
            n0, n1 = [len(range(*_slice)) for _slice in self._slicing_tuples]
            i0 = range(*self._slicing_tuples[0])[index // n1]
            i1 = range(*self._slicing_tuples[1])[index % n1]
            return tuple([i0, i1])
        # inefficient
        return tuple(self.iter_indices())[index]

    def get_array_from_index(self, index):
        """Get the ith array of the serie.

        Parameters
        ----------

        index: int

          Index of the array, for example 0 to get the first array.

        """
        indices = self.get_indices_from_index(index)
        return self.get_array_from_indices(*indices)

    def get_path_all_files(self):
        """Get all paths found from path_dir and base_name."""
        str_glob = os.path.join(self.path_dir, self.base_name + "*")
        paths = glob(str_glob)
        paths.sort()
        return paths

    def get_path_files(self):
        """Get all paths of the serie.

        If the serie is formed from arrays in one file, only one path is given.

        """
        return (
            os.path.join(self.path_dir, name) for name in self.get_name_files()
        )

    def get_path_arrays(self):
        """Get all paths of the arrays of the serie.

        If the serie is formed from arrays in one file, ``len(path) ==
        len(arrays)``.

        """
        return (
            os.path.join(self.path_dir, name) for name in self.get_name_arrays()
        )

    def get_name_path_arrays(self):
        return (
            (name, os.path.join(self.path_dir, name))
            for name in self.get_name_arrays()
        )

    def check_all_files_exist(self):
        """Check that all files exist."""
        name_files = self.get_name_files()
        return all([self.isfile(name) for name in name_files])

    def check_all_arrays_exist(self):
        """Check that all arrays exists."""
        if not self._from_movies:
            return self.check_all_files_exist()

        if not self.check_all_files_exist():
            return False

        for indices in self.iter_indices():
            internal_index = indices[-1]
            if internal_index >= self.nb_arrays_in_one_file:
                return False

        for path in self.get_path_files():
            if path not in self._nb_arrays_file:
                self._nb_arrays_file[path] = get_nb_arrays_in_file(path)

        if not all(
            self.nb_arrays_in_one_file == nb
            for nb in self._nb_arrays_file.values()
        ):
            return False

        return True

    def iter_indices(self):
        """Iterator on the indices.

        ``len(indices) == self.nb_indices``

        """
        ranges = [range(*s) for s in self._slicing_tuples]
        for indices in itertools.product(*ranges):
            yield indices

    def __len__(self):
        return sum(1 for _ in self.iter_indices())

    def iter_name_files(self):
        """Iterator on the file names."""
        names = []
        for name in self.iter_name_arrays():
            if name.endswith("]"):
                name = name.split("[")[0]
                if name not in names:
                    names.append(name)
                    yield name
            else:
                yield name

    def iter_name_arrays(self):
        """Iterator on the array names."""
        for indices in self.iter_indices():
            yield self.compute_name_from_indices(*indices)

    __iter__ = iter_name_arrays

    def iter_path_files(self):
        """Iterator on the file paths."""
        for name in self.iter_name_files():
            yield os.path.join(self.path_dir, name)

    def iter_arrays(self):
        """Iterator on the arrays of the serie."""
        for name in self.iter_name_arrays():
            yield self.get_array_from_name(name)

    def _compute_strindices_from_indices(self, *indices):
        """Compute the string corresponding to the indices.

        Parameters
        ----------

        indices: iterable of int.

        """
        if self._from_movies:
            indices = indices[:-1]

        nb_indices = len(indices)
        if nb_indices != self.nb_indices_name_file:
            raise ValueError("nb_indices != self.nb_indices")

        str_indices = ""
        for i in range(nb_indices):
            if self._index_types[i] == "digit":
                code_format = "{:0" + str(self._index_lens[i]) + "d}"
                str_index = code_format.format(indices[i])
            elif self._index_types[i] == "alpha":
                if indices[i] > 25:
                    raise ValueError('"alpha" index larger than 25.')

                str_index = chr(ord("a") + indices[i])
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
        name = (
            self.base_name
            + self._separator_base_index
            + self._compute_strindices_from_indices(*indices)
        )
        if self.extension_file != "":
            name += "." + self.extension_file

        if self._from_movies:
            name += self._format_index.format(indices[-1])

        return name

    def compute_indices_from_name(self, name):
        """Compute a list of indices from a file name.

        Parameters
        ----------

        name: str
           Name of the array.
        """
        str_indices = str(name[len(self.base_name) :])

        if self._separator_base_index != "":
            str_indices = str_indices[1:]

        if str_indices.endswith("]"):
            str_indices, internal_index = str_indices.split("[")
            internal_index = int(internal_index[:-1])
        else:
            internal_index = None

        if self.extension_file != "":
            str_indices = str_indices[: -(len(self.extension_file) + 1)]

        remains = str_indices
        indices = []
        for i_ind in range(self.nb_indices_name_file):
            if self._index_types[i_ind] == "digit":
                test_type = str.isdigit
            elif self._index_types[i_ind] == "alpha":
                test_type = str.isalpha
            else:
                raise Exception('The type should be "digit" or "alpha".')

            index = "".join(itertools.takewhile(test_type, remains))
            remains = remains[len(index) :]
            if self._index_separators[i_ind] != "":
                remains = remains[1:]

            if self._index_types[i_ind] == "digit":
                index = int(index)
            elif self._index_types[i_ind] == "alpha":
                index = ord(index) - ord("a")

            indices.append(index)

        if internal_index is not None:
            indices.append(internal_index)

        assert len(remains) == 0
        return indices

    def isfile(self, path):
        """Check whether a path or name corresponds to an existing file."""
        if not os.path.isabs(path):
            path = os.path.join(self.path_dir, path)
        return os.path.exists(path)

    def get_slicing_tuples_all_files(self):
        """Get nb_indices "slices" (to get all the arrays in the directory).

        The "slices" are tuples of size 1 (``(start,)``), 2 (``(start, stop)``)
        or 3 (``(start, stop, step)``).

        """
        return self._slicing_tuples_all_files

    def get_slicing_tuples(self):
        """Get nb_indices "slices" to get all the arrays of the serie.

        The "slices" are tuples of size 1 (``(start,)``), 2 (``(start, stop)``)
        or 3 (``(start, stop, step)``).
        """
        return self._slicing_tuples

    def set_slicing_tuples(self, *slicing_tuples):
        """Set the (nb_indices) "slicing tuples".

        The "slicing tuples" are tuples of size 1 (``(start,)``), 2 (``(start, stop)``)
        or 3 (``(start, stop, step)``).

        """
        slicing_lists = list(slicing_tuples)
        if len(slicing_lists) != self.nb_indices:
            raise ValueError(
                "len(slicing_tuples) != self.nb_indices\n"
                "filename_given = {}\n".format(self.filename_given)
                + f"path_dir = {self.path_dir}"
            )

        for i, islice in enumerate(slicing_lists):
            if isinstance(islice, tuple):
                slicing_lists[i] = list(islice)
            if isinstance(islice, int):
                slicing_lists[i] = [islice, islice + 1]
            elif len(islice) == 1:
                slicing_lists[i] = [islice[0], islice[0] + 1]

        for i, islice in enumerate(slicing_lists):
            for ii, index in enumerate(islice):
                if index is None:
                    slicing_lists[i][ii] = self._slicing_tuples_all_files[i][ii]

        self._slicing_tuples = [tuple(slicing) for slicing in slicing_lists]

    def get_nb_arrays(self):
        """Get the number of arrays in the serie."""
        return len([i for i in self.iter_indices()])

    def get_nb_files(self):
        """Get the number of files of the serie."""
        return len(self.get_name_files())


class SlicingTuplesFromIndexSerie:
    def __init__(self, str_slices):
        self.str_ranges = [s.strip() for s in str_slices.split(",")]

    def __call__(self, index):
        slicing_tuples = []
        for str_range in self.str_ranges:
            indslice = []
            slicing_tuples.append(indslice)
            for ii, s in enumerate(str_range.split(":")):
                if s.strip() == "":
                    if ii == 0:
                        indslice.append(0)
                    elif ii == 1:
                        indslice.append(None)
                    elif ii > 2:
                        raise ValueError

                else:
                    indslice.append(simple_eval(s, names={"i": index}))
        return slicing_tuples


class SeriesOfArrays:
    """Series of arrays.

    This class can be used to produce series of arrays from a
    :class:`SerieOfArrays`.

    Parameters
    ----------

    serie: SerieOfArrays or str

    slicing_tuples_from_indserie: str or function

      The function has to take an integer and to return an iterable of
      "slicing tuples" used to compute a file name.

    """

    def __init__(
        self,
        serie,
        slicing_tuples_from_indserie,
        ind_start="first",
        ind_stop=None,
        ind_step=1,
    ):
        serie_input = serie
        slicing_tuples_from_indserie_input = slicing_tuples_from_indserie

        if isinstance(serie, (str, Path)):
            serie = str(serie)
            serie = SerieOfArraysFromFiles(serie)
        if isinstance(serie, SerieOfArraysFromFiles):
            self.serie = serie = deepcopy(serie)
        else:
            raise ValueError("serie should be a str or a SerieOfArraysFromFiles.")

        if slicing_tuples_from_indserie is None:
            slicing_tuples_from_indserie = "i:i+1"
            for i in range(serie.nb_indices - 1):
                slicing_tuples_from_indserie += ",:"

        if isinstance(slicing_tuples_from_indserie, str):
            slicing_tuples_from_indserie = SlicingTuplesFromIndexSerie(
                slicing_tuples_from_indserie
            )

        if slicing_tuples_from_indserie(0) == slicing_tuples_from_indserie(1):
            raise ValueError(
                "It seems that the function slicing_tuples_from_indserie "
                "does not depend on the index."
            )

        self.slicing_tuples_from_indserie = slicing_tuples_from_indserie

        if ind_start == "first":
            ind_start = 0
            while not self.check_all_arrays_serie_exist(ind_start):
                ind_start += 1

        if ind_stop is None:
            iserie = ind_start
            while self.check_all_arrays_serie_exist(iserie):
                iserie += ind_step
            iserie -= 1
        else:
            if len(range(ind_start, ind_stop, ind_step)) == 0:
                raise ValueError("len(range(ind_start, ind_stop, ind_step)) == 0")

            for iserie in range(ind_start, ind_stop, ind_step):
                if not self.check_all_arrays_serie_exist(iserie):
                    break

        ind_stop = iserie + 1

        self.nb_series = len(list(range(ind_start, ind_stop, ind_step)))
        self.iserie = ind_start
        self.ind_start = ind_start
        self.ind_stop = ind_stop
        self.ind_step = ind_step

        serie.set_slicing_tuples(*self.slicing_tuples_from_indserie(self.iserie))
        _print_warning = False
        if not serie.check_all_arrays_exist():
            _print_warning = True
            print(
                "warning: this SeriesOfArrays has been initialized with "
                "parameters such that the first serie if not complete."
            )

        if self.nb_series == 0:
            _print_warning = True
            print(
                "warning: this SeriesOfArrays has been initialized with "
                "parameters such that no serie of images has been found."
            )

        if _print_warning:
            print(
                f"serie='{serie_input}',\n"
                f"slicing_tuples_from_indserie='{slicing_tuples_from_indserie_input}', "
                f"{ind_start=}, {ind_stop=}, {ind_step=}."
            )

    def check_all_arrays_serie_exist(self, index_serie):
        self.serie.set_slicing_tuples(
            *self.slicing_tuples_from_indserie(index_serie)
        )
        return self.serie.check_all_arrays_exist()

    def __iter__(self):
        if hasattr(self, "index_series"):
            index_series = self.index_series
        else:
            index_series = list(
                range(self.ind_start, self.ind_stop, self.ind_step)
            )

        for iserie in index_series:
            self.serie.set_slicing_tuples(
                *self.slicing_tuples_from_indserie(iserie)
            )
            yield self.serie

    def items(self):
        if hasattr(self, "index_series"):
            index_series = self.index_series
        else:
            index_series = list(
                range(self.ind_start, self.ind_stop, self.ind_step)
            )

        for iserie in index_series:
            self.serie.set_slicing_tuples(
                *self.slicing_tuples_from_indserie(iserie)
            )
            yield iserie, self.serie

    def __len__(self):
        return len([s for s in self])

    def set_index_series(self, index_series):
        """Set the indices corresponding to the series.

        Parameters
        ----------

        index_series : sequence of int

        """
        self.index_series = index_series

    def get_next_serie(self):
        """Get the next serie."""
        if self.iserie < self.ind_stop:
            self.serie.set_slicing_tuples(
                *self.slicing_tuples_from_indserie(self.iserie)
            )
            self.iserie += 1
            return self.serie

    def get_serie_from_index(self, index):
        """Get a serie from an index."""
        self.serie.set_slicing_tuples(*self.slicing_tuples_from_indserie(index))
        return self.serie

    def get_name_all_files(self):
        """Get all file names."""
        names_all = []
        for serie in self:
            names = serie.get_name_files()
            for name in names:
                if name not in names_all:
                    names_all.append(name)
        return names_all

    def get_name_all_arrays(self):
        """Get all array names."""
        names_all = []
        for serie in self:
            names = serie.get_name_arrays()
            for name in names:
                if name not in names_all:
                    names_all.append(name)
        return names_all
