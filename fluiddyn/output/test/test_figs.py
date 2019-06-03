import os
import unittest
from shutil import rmtree

from .. import figs
from ...io.redirect_stdout import stdout_redirected
from ..figs import Figures, show
from ..util import gradient_colors


def do_nothing(*args):
    pass


figs.plt.show = do_nothing
figs.plt.ion = do_nothing
figs.plt.ioff = do_nothing


class TestFigs(unittest.TestCase):
    """Test fluiddyn.output.figs module."""

    def setUp(self):
        self._work_dir = "test_fluiddyn_output_figs"
        if not os.path.exists(self._work_dir):
            os.mkdir(self._work_dir)

        self.figures = Figures(self._work_dir, hastosave=True, for_article=False)

    def tearDown(self):
        rmtree(self._work_dir)

    def test_gradient_colors(self):
        gradient_colors(4)
        gradient_colors(5)

    def test_save(self):

        fig = self.figures.new_figure(
            "figure0.png", fig_width_mm=40, fig_height_mm=40
        )
        with stdout_redirected():
            fig.saveifhasto()
        show()


if __name__ == "__main__":
    unittest.main(exit=True)
