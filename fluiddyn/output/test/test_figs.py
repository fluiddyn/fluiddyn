
import fluiddyn.output.figs as figs

import unittest


class SimpleTestCase(unittest.TestCase):
    def setUp(self):
        self.figures = figs.Figures(hastosave=True)

    # def test_create_figure(self):
    #     self.figures.new_figure()

    # def test_save(self):
    #     fig = self.figures.new_figure(name_file='testfig')
    #     fig.saveifhasto(verbose=False)
    #     nfiles = glob('testfig.*')
    #     for nfile in nfiles:
    #         os.remove(nfile)


if __name__ == '__main__':
    unittest.main(exit=False)
    figs.show()
