

import unittest
import os
from shutil import rmtree

from ..figs import Figures
from ..util import gradient_colors


class TestFigs(unittest.TestCase):
    """Test fluiddyn.output.figs module."""
    def setUp(self):
        self._work_dir = 'test_fluiddyn_output_figs'
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        self.figures = Figures(self._work_dir, hastosave=True,
                               for_article=False)

    def tearDown(self):
        rmtree(self._work_dir)

    def test_gradient_colors(self):
        gradient_colors(4)
        gradient_colors(5)

    def test_save(self):

        fig = self.figures.new_figure(
            'figure0.png', fig_width_mm=40, fig_height_mm=40)
        fig.saveifhasto()


if __name__ == '__main__':
    unittest.main(exit=True)
