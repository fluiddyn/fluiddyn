import unittest

from ..colorchart import make_colorchart


class TestColorchart(unittest.TestCase):
    """Test fluiddyn.output.colorchart module."""

    def test_colorchart(self):
        make_colorchart(nb_colors=4, darkest_gray=0.5, lightest_gray=0.85)


if __name__ == "__main__":
    unittest.main()
