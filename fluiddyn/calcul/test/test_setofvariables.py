import unittest

from ..setofvariables import SetOfVariables


class TestSetofvariables(unittest.TestCase):
    def test_sov(self):
        sov = SetOfVariables(keys=("a", "b", "c"), shape_variable=(2, 2))
        b = sov.get_var("b")
        sov.set_var("a", b)
        sov.initialize(3)

        sov1 = SetOfVariables(like=sov)
