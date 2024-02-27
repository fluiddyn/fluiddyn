import pytest

import numpy as np
from PIL import Image

from fluiddyn.util.serieofarrays import SerieOfArraysFromFiles, SeriesOfArrays


def create_image(path):
    im = Image.fromarray(np.ones((8, 8), dtype=np.int32))
    im.save(path)
    im.close()


shape2d = (8, 2)
shape1d = (8,)


@pytest.fixture(scope="session")
def path_dir_images_2d(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("dir_images_2d")
    for i in range(shape2d[0]):
        for j in range(shape2d[1]):
            create_image(tmp_path / f"file{i}_{j}.png")
    return tmp_path


@pytest.fixture(scope="session")
def path_dir_images_1d(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("dir_images_1d")
    for i in range(shape1d[0]):
        create_image(tmp_path / f"file{i}.png")
    return tmp_path


def _check_get_indices_from_index(serie):
    tuple_indices = tuple(serie.iter_indices())
    for idx in range(len(serie)):
        indices = serie.get_indices_from_index(idx)
        assert indices == tuple_indices[idx]


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

    serie.get_index_slices_all_files()
    serie.get_index_slices()
    serie.get_nb_files()
    serie.set_index_slices(0, 1)


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


def test_serie_1d(path_dir_images_1d):
    path_dir = path_dir_images_1d

    serie = SerieOfArraysFromFiles(path_dir, ":")
    serie.get_path_arrays()
    serie.get_name_path_arrays()
    serie.check_all_arrays_exist()
    _check_get_indices_from_index(serie)
    assert len(serie) == shape1d[0]


def test_series_1d(path_dir_images_1d):
    path_dir = path_dir_images_1d

    series = SeriesOfArrays(
        path_dir, "i:i+3:2", ind_start=0, ind_stop=None, ind_step=2
    )

    assert len(series) == 3
    assert series.ind_stop == 6
    series.get_next_serie()
    series.get_name_all_files()
    series.get_name_all_arrays()
