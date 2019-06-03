import os
import unittest
from shutil import rmtree

import numpy as np
from PIL import Image

from fluiddyn.util.serieofarrays import SerieOfArraysFromFiles, SeriesOfArrays


def create_image(path):
    im = Image.fromarray(np.ones((8, 8), dtype=np.int32))
    im.save(path)
    im.close()


class TestSeriesOfArrays(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        work_dir = cls.work_dir = "test_fluiddyn_util_serieofarrays"
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        for i in range(7):
            for j in range(2):
                create_image(os.path.join(work_dir, f"file{i}_{j}.png"))

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.work_dir)

    def test0(self):

        serie = SerieOfArraysFromFiles(self.work_dir, "1:1+3, :")
        serie.get_path_arrays()
        serie.get_name_path_arrays()
        serie.check_all_arrays_exist()

        serie = SerieOfArraysFromFiles(self.work_dir, "1:1+3:2, 1")
        assert len(serie.get_name_files()) == 2

        series = SeriesOfArrays(
            self.work_dir, "i:i+3:2, 1", ind_start=0, ind_stop=None, ind_step=2
        )

        series = SeriesOfArrays(
            self.work_dir, "i:i+3:2, 1", ind_start=0, ind_stop=8, ind_step=2
        )

        self.assertEqual(len(series), 4)
        self.assertEqual(series.ind_stop, 7)
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

        for path in serie.iter_path_files():
            pass

        serie.get_index_slices_all_files()
        serie.get_index_slices()
        serie.get_nb_files()
        serie.set_index_slices(0, 1)


if __name__ == "__main__":
    unittest.main()
