import unittest
import os

from fluiddyn.util.paramcontainer import ParamContainer


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.params = ParamContainer(tag='params')
        params = self.params
        params._set_attrib('a0', 1)
        params._set_attribs({'a1': 1, 'a2': 1})

        params._set_child('child0', {'a0': 2, 'a1': 2})
        params.child0.a0 = []
        params.child0.a0.append(1)

        self.txt = params._make_xml_text()

    def test_save_load_xml(self):
        """Test save to and load from xml file."""
        params = self.params

        name_file_xml = 'params_test.xml'
        params._save_as_xml(name_file_xml)

        params2 = ParamContainer(path_file=name_file_xml)
        os.remove(name_file_xml)
        txt2 = params2._make_xml_text()

        self.assertEqual(self.txt, txt2)
        self.assertEqual(self.params, params2)

    def test_save_load_hdf5(self):
        """Test save to and load from hdf5 file."""
        params = self.params

        name_file_h5 = 'params_test.h5'
        params._save_as_hdf5(path_file=name_file_h5)

        params2 = ParamContainer(path_file=name_file_h5)
        os.remove(name_file_h5)

        self.assertEqual(self.params, params2)

    def test_raise(self):
        """Test raise errors."""
        params = self.params

        with self.assertRaises(AttributeError):
            params.does_not_exist = 1

        with self.assertRaises(AttributeError):
            print(params.child1.a0)

if __name__ == '__main__':
    unittest.main()
