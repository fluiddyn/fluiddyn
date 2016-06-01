
import unittest
import os

from fluiddyn.util.serieofarrays import SeriesOfArrays


class TestSeriesOfArrays(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = '/tmp/test_fluidimage/case0'
        if not os.path.exists(path):
            os.makedirs(path)
        for i in range(7):
            with open(os.path.join(path, 'file{}'.format(i)), 'w'):
                pass

    # @classmethod
    # def tearDownClass(cls):
    #     pass

    def test0(self):
        path = '/tmp/test_fluidimage/case0'
        series = SeriesOfArrays(
            path, 'i:i+4:2',
            ind_start=0, ind_stop=None, ind_step=2)

        self.assertEqual(len(series), 3)
        self.assertEqual(series.ind_stop, 6)


if __name__ == '__main__':
    unittest.main()
