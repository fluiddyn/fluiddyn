import os
import unittest

from numpy.testing import assert_allclose

from ...io import stdout_redirected
from .. import sphericalharmo

try:
    import shtns
except ImportError:
    use_shtns = False
else:
    use_shtns = True


class TestSphericalHarmo(unittest.TestCase):
    """Test ``sphericalharmo`` module."""

    @unittest.skipUnless(use_shtns, "SHTns not installed or can not be imported.")
    def test_sht_random(self):
        """Test forward and inverse SHT on a random array."""
        with stdout_redirected():
            op = sphericalharmo.EasySHT(lmax=15)

        field_phys = op.create_array_spat("rand")
        field_spect = op.sht(field_phys)
        field_phys = op.isht(field_spect)

        field_spect = op.sht(field_phys)
        field_phys2 = op.isht(field_spect)

        assert_allclose(field_phys, field_phys2)


if __name__ == "__main__":
    unittest.main()
