import numpy as np
import pytest
from PIL import Image

from fluiddyn.util.serieofarrays import SerieOfArraysFromFiles, SeriesOfArrays

shape_image = (8, 8)


def create_image(path):
    im = Image.fromarray(np.ones(shape_image, dtype=np.uint16))
    im.save(path)
    im.close()


shape1d = (8,)
shape2d = (8, 2)


@pytest.fixture(scope="session")
def path_dir_images_1d(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("dir_images_1d")
    for idx in range(shape1d[0]):
        create_image(tmp_path / f"file{idx}.png")
    return tmp_path


@pytest.fixture(scope="session")
def path_dir_images_2d(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("dir_images_2d")
    for idx in range(shape2d[0]):
        for j in range(shape2d[1]):
            create_image(tmp_path / f"file{idx}_{j}.png")
    return tmp_path


@pytest.fixture(scope="session")
def path_dir_images_2d_jet(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("dir_images_2d_jet")
    for idx in range(60, 62):
        for letter in "ab":
            create_image(tmp_path / f"c{idx:03d}{letter}.png")
    return tmp_path


@pytest.fixture(scope="session")
def path_dir_images_2d_pairs_first_index(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("dir_images_2d_pairs_first_index")
    for i0 in (1, 2):
        for i1 in range(1, 9):
            create_image(tmp_path / f"c_{i0}_{i1}.png")
    return tmp_path


def _check_get_indices_from_index(serie):
    tuple_indices = tuple(serie.iter_indices())
    for idx in range(len(serie)):
        indices = serie.get_indices_from_index(idx)
        assert indices == tuple_indices[idx]


def check_all1by1(path_dir, size):
    series = SeriesOfArrays(path_dir, "all1by1")
    assert len(series) == size
    serie = series.get_serie_from_index(0)

    for index, serie in series.items():
        assert len(serie) == 1

    assert index == size - 1


def test_serie_1d(path_dir_images_1d):
    path_dir = path_dir_images_1d

    serie = SerieOfArraysFromFiles(path_dir, ":")
    serie.get_path_arrays()
    serie.get_name_path_arrays()
    serie.check_all_arrays_exist()
    repr(serie)
    _check_get_indices_from_index(serie)
    assert len(serie) == shape1d[0]
    assert serie.get_nb_arrays() == shape1d[0]

    assert serie.get_separator_base_index() == ""
    assert serie.get_index_separators() == [""]

    arr, name = serie.get_tuple_array_name_from_index(1)
    assert np.allclose(arr, np.ones(shape_image, dtype=np.uint16))
    assert name == "file1.png"

    assert serie.get_str_for_name_from_idim_idx(0, 1) == "1"


def test_series_1d(path_dir_images_1d):
    path_dir = path_dir_images_1d

    series = SeriesOfArrays(
        path_dir, "i:i+3", ind_start=0, ind_stop=None, ind_step=2
    )

    assert len(series) == 3
    assert series.ind_stop == 6
    series.get_next_serie()
    series.get_name_all_files()
    series.get_name_all_arrays()
    repr(series)

    series = SeriesOfArrays(path_dir, "pairs")
    assert len(series) == 7
    assert series.ind_stop == 7

    check_all1by1(path_dir, shape1d[0])

    series = SeriesOfArrays(
        series.serie, "i:i+3", ind_start=0, ind_stop=None, ind_step=2
    )
    assert len(series) == 3
    assert series.ind_stop == 6

    series = SeriesOfArrays(series.serie)
    series.set_index_series(range(2))


def test_serie_2d(path_dir_images_2d):
    path_dir = path_dir_images_2d

    serie = SerieOfArraysFromFiles(path_dir, "1:1+3, :")
    serie.get_path_arrays()
    serie.get_name_path_arrays()
    serie.check_all_arrays_exist()
    _check_get_indices_from_index(serie)

    serie = SerieOfArraysFromFiles(path_dir, "1:1+3:2, 1")
    assert len(serie.get_name_files()) == 2

    _check_get_indices_from_index(serie)

    indices = serie.get_indices_from_index(1)
    name = serie.compute_name_from_indices(*indices)
    assert name == "file3_1.png"

    serie.get_array_from_index(0)

    assert serie.get_separator_base_index() == ""
    assert serie.get_index_separators() == ["_", ""]

    arr, name = serie.get_tuple_array_name_from_index(1)
    assert np.allclose(arr, np.ones(shape_image, dtype=np.uint16))
    assert name == "file3_1.png"

    assert serie.get_str_for_name_from_idim_idx(0, 1) == "1"


def test_series_2d_pair_i0(path_dir_images_2d):
    path_dir = path_dir_images_2d
    series = SeriesOfArrays(
        path_dir, "i:i+3:2, 1", ind_start=0, ind_stop=None, ind_step=2
    )

    series = SeriesOfArrays(
        path_dir, "i:i+3:2, 1", ind_start=0, ind_stop=8, ind_step=2
    )

    assert len(series) == 4
    assert series.ind_stop == 7
    series.get_next_serie()
    series.get_name_all_files()
    series.get_name_all_arrays()

    tuple(series.items())

    serie = series.get_serie_from_index(0)
    serie.get_arrays()
    serie.get_array_from_index(0)
    serie.get_array_from_indices(0, 1)
    serie.get_name_files()
    serie.get_path_all_files()
    serie.get_path_files()

    _check_get_indices_from_index(serie)

    for path in serie.iter_path_files():
        pass

    serie.get_slicing_tuples_all_files()
    serie.get_slicing_tuples()
    serie.get_nb_files()
    serie.set_slicing_tuples(0, 1)

    check_all1by1(path_dir, shape2d[0] * shape2d[1])

    series = SeriesOfArrays(series.serie)


def test_series_2d_pair_i1(path_dir_images_2d):
    path_dir = path_dir_images_2d
    series = SeriesOfArrays(path_dir, "i, :")

    assert len(series) == 8
    assert series.ind_stop == 8
    series.get_next_serie()
    series.get_name_all_files()
    series.get_name_all_arrays()

    serie = series.get_serie_from_index(0)
    serie.get_arrays()
    serie.get_array_from_index(0)
    _check_get_indices_from_index(serie)


def test_series_jet(path_dir_images_2d_jet):

    path_dir = path_dir_images_2d_jet
    series = SeriesOfArrays(path_dir, "pairs")
    assert len(series) == 2
    serie = series.get_serie_from_index(0)
    assert len(serie) == 2

    check_all1by1(path_dir, 4)


def test_series_jet_bug(path_dir_images_2d_jet):
    path_dir = path_dir_images_2d_jet
    series = SeriesOfArrays(path_dir, ":,i")
    assert len(series) == 2
    serie = series.get_serie_from_index(0)
    assert len(serie) == 2


def test_series_pairs_first_index(path_dir_images_2d_pairs_first_index):

    path_dir = path_dir_images_2d_pairs_first_index

    series = SeriesOfArrays(path_dir, "pairs")
    assert len(series) == 8
    serie = series.get_serie_from_index(0)
    assert len(serie) == 2

    check_all1by1(path_dir, 16)
