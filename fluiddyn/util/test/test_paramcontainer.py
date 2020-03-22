import json
import os
import unittest
from shutil import rmtree
from pathlib import Path

import numpy as np

from ...io.redirect_stdout import stdout_redirected
from ..paramcontainer import ParamContainer, tidy_container

xml_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "file.xml"))


class TestContainer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.params = ParamContainer(tag="params")
        params = cls.params
        params._set_attrib("a0", 1)
        params._set_attribs({"a1": 1, "a2": "a", "a_str_list": ["a", "b"]})

        params._set_child("child0", {"a0": 2, "a1": None})
        params.child0.a0 = []
        params.child0.a0.append(1)

        params.child0._set_child("cc", {})

        params.child0.cc._set_doc("Hello")

        with stdout_redirected():
            params._print_docs()

        params._get_key_attribs()

        cls.txt = params._make_xml_text()
        cls._work_dir = "test_fluiddyn_util_paramcontainer"
        if not os.path.exists(cls._work_dir):
            os.mkdir(cls._work_dir)

        os.chdir(cls._work_dir)

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        rmtree(cls._work_dir)

    def test_save_load_xml(self):
        """Test save to and load from xml file."""
        params = self.params

        name_file_xml = "params_test.xml"
        params._save_as_xml(name_file_xml)
        params._save_as_xml(comment="Hello")

        params2 = ParamContainer(path_file=name_file_xml)
        os.remove(name_file_xml)
        params2._make_xml_text()

        self.assertEqual(self.params, params2)

        params2["a1"]
        params2["a1"] = 2
        with stdout_redirected():
            params2._print_doc()
            params2._print_as_xml()
            repr(params2)

        params3 = ParamContainer(tag="params3")
        params3._set_attrib("a0", 1)
        params2._set_as_child(params3)

    def test_save_load_hdf5(self):
        """Test save to and load from hdf5 file."""
        params = self.params

        name_file_h5 = "params_test.h5"
        params._save_as_hdf5(path_file=name_file_h5)
        params._save_as_hdf5()

        params2 = ParamContainer(path_file=name_file_h5)
        os.remove(name_file_h5)

        try:
            self.assertEqual(self.params, params2)
        except AssertionError:
            print("params=\n", self.params)
            print("params2=\n", params2)
            raise

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

    def test_render_json(self):
        """Test JSON rendering (used in Jupyter)."""
        data, metadata = self.params._repr_json_()
        json.dumps(data)

    def test_as_code(self):
        def create_default_params():
            p = ParamContainer(tag="params")
            p._set_attribs(dict(a=0, b=2))
            p._set_child("c0", dict(a0="foo", a1=Path.home(), a2=np.arange(4)))
            return p

        p0 = create_default_params()
        p0.c0.a0 = "bar"
        code = p0._as_code()
        p1 = create_default_params()

        assert p1.c0.a0 == "foo"
        exec(code, {"params": p1})
        assert p1.c0.a0 == "bar"

        p1._print_as_code()


if __name__ == "__main__":
    unittest.main()
