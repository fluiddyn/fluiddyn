from __future__ import print_function
import unittest
import os
from shutil import rmtree

from ..paramcontainer import ParamContainer, tidy_container
from ...io.redirect_stdout import stdout_redirected

xml_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'file.xml'))


class TestContainer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.params = ParamContainer(tag='params')
        params = cls.params
        params._set_attrib('a0', 1)
        params._set_attribs({'a1': 1, 'a2': 1})

        params._set_child('child0', {'a0': 2, 'a1': None})
        params.child0.a0 = []
        params.child0.a0.append(1)

        cls.txt = params._make_xml_text()
        cls._work_dir = 'test_fluiddyn_util_paramcontainer'
        if not os.path.exists(cls._work_dir):
            os.mkdir(cls._work_dir)

        os.chdir(cls._work_dir)

    @classmethod
    def tearDownClass(cls):
        os.chdir('..')
        rmtree(cls._work_dir)

    def test_save_load_xml(self):
        """Test save to and load from xml file."""
        params = self.params

        name_file_xml = 'params_test.xml'
        params._save_as_xml(name_file_xml)
        params._save_as_xml(comment='Hello')

        params2 = ParamContainer(path_file=name_file_xml)
        os.remove(name_file_xml)
        params2._make_xml_text()

        self.assertEqual(self.params, params2)

        params2['a1']
        params2['a1'] = 2
        with stdout_redirected():
            params2._print_doc()
            params2._print_as_xml()
            repr(params2)

        params3 = ParamContainer(tag='params3')
        params3._set_attrib('a0', 1)
        params2._set_as_child(params3)

    def test_save_load_hdf5(self):
        """Test save to and load from hdf5 file."""
        params = self.params

        name_file_h5 = 'params_test.h5'
        params._save_as_hdf5(path_file=name_file_h5)
        params._save_as_hdf5()

        params2 = ParamContainer(path_file=name_file_h5)
        os.remove(name_file_h5)

        self.assertEqual(self.params, params2)

    def test_raise(self):
        """Test raise errors."""
        params = self.params

        with self.assertRaises(AttributeError):
            params.does_not_exist = 1

        with self.assertRaises(AttributeError):
            params._does_not_exist

        with self.assertRaises(AttributeError):
            print(params.child1.a0)

    def test_tidy(self):
        param = ParamContainer(path_file=xml_file)
        param._make_xml_text()
        tidy_container(param)


if __name__ == '__main__':
    unittest.main()
