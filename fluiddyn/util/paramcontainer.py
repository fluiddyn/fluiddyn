"""Container for parameters (:mod:`fluiddyn.util.paramcontainer`)
=================================================================

.. currentmodule:: fluiddyn.util.paramcontainer

Provides:

.. autoclass:: ParamContainer
   :members:
   :private-members:

"""

import os
import re
from ast import literal_eval
from copy import deepcopy
from io import open
from typing import Any, Dict

import numpy as np

from fluiddyn.io import Path
from fluiddyn.util.xmltotext import produce_text_element

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree


try:
    import h5py

    from fluiddyn.io.hdf5 import H5File
except ImportError:
    from warnings import warn

    warn(
        "Cannot import h5py. Loading from and writing to HDF5 files will not"
        "work",
        ImportWarning,
    )


def _as_str(value):
    if isinstance(value, Path):
        return str(value)
    elif isinstance(value, str):
        return value
    else:
        return repr(value)


def _as_code(value):
    if isinstance(value, Path):
        return f'Path(r"{str(value)}")'
    elif isinstance(value, str):
        return f'"{value}"'
    else:
        return repr(value)


def _as_value(value):
    if value.startswith("array("):
        # -1 to remove the last ")"
        code = value.strip()[len("array(") : -1]
        dtype = None
        if "dtype=" in code:
            code, code_dtype = code.split("dtype=")
            code = code.strip()[:-1]
            try:
                dtype = np.dtype(code_dtype)
            except TypeError:
                pass
        obj = literal_eval(code)
        return np.array(obj, dtype=dtype)

    if "\t" in value:
        return value

    try:
        return literal_eval(value)

    except (SyntaxError, ValueError):
        return value


def sanitize_for_json(d: Dict[str, Any]) -> Dict[str, Any]:
    """JSON rendering requires values in the dictionary to be a basic type.

    That is the allowed types are ``{str, int, float, bool, None}``. If not,
    sanitize beforehand.

    """

    def is_not_allowed(value):
        allowed_types = (str, int, float, bool)
        return not (value is None or isinstance(value, allowed_types))

    for key, value in d.items():
        if isinstance(value, dict):
            d[key] = sanitize_for_json(value)  # recurse

        elif isinstance(value, (list, tuple)):
            d[key] = [_as_str(v) if is_not_allowed(v) else v for v in value]

        elif is_not_allowed(value):
            d[key] = _as_str(value)

    return d


class ParamContainer:
    """Structured container of values.

    The objects ParamContainer can be used as containers of
    parameters. They can be printed as xml text.

    They are used to contain parameters that can be modified by the
    user, for example in this way::

      >>> params = ParamContainer(tag='params')

      >>> params._set_attribs({'a0': 1, 'a1': 1})

      >>> params._set_attrib('a2', 1)

      >>> params._print_as_xml()
      <params a1="1" a0="1" a2="1"/>

      >>> params._set_child('child0', {'a0': 2, 'a1': 2})

      >>> params.child0.a0 = 3

      >>> params._print_as_xml()
      <params a1="1" a0="1" a2="1">
      <child0 a1="2" a0="3"/>
      </params>

    Here, ``params.child0`` is another ParamContainer.

    An interesting feature of the ParamContainer objects is that if one
    uses a non-existing parameter, an AttributeError is raised::

      >>> params.a3 = 3

      -------------------------------------------------------------------------
      AttributeError                          Traceback (most recent call last)
      <ipython-input-9-a91118d8b23e> in <module>()
      ----> 1 params.child1.a0 = 3

      AttributeError: a3 is not already set in params.
      The attributes are: set(['a1', 'a0', 'a2'])
      To set a new attribute, use _set_attrib or _set_attribs.

    Note that for a parameter container, it is much better to raise an
    error rather than just add an unused parameter!

    A ParamContainer object can be saved in xml and in hdf5 and then
    reloaded from the file::

      >>> params._save_as_xml()

      >>> params_loaded = ParamContainer(path_file=params._tag + '.xml')

      >>> assert params_loaded == params

    Parameters
    ----------
    (for the __init__ method)

    tag : (None) str
        A tag for the root container.

    attribs : (None) dict
        Some attributes.

    path_file : (None) str
        Path of a file (xml or hdf5).

    elemxml : (None) xml.etree.ElementTree.Element
        An xml element.

    hdf5_object : (None) file
        An open hdf5 file.

    """

    def __init__(
        self,
        tag=None,
        attribs=None,
        path_file=None,
        elemxml=None,
        hdf5_object=None,
        doc="",
        parent=None,
    ):
        self._set_internal_attr("_key_attribs", list())
        self._set_internal_attr("_tag_children", list())
        self._set_internal_attr("_parent", parent)
        self._set_doc(doc)

        if path_file is not None:
            path_file = str(path_file)
            self._set_internal_attr("_path_file", path_file)
            if path_file.endswith(".xml"):
                self._load_from_xml_file(path_file)
            elif path_file.endswith(".h5"):
                self._load_from_hdf5_file(path_file)
        elif elemxml is not None:
            self._load_from_elemxml(elemxml)
        elif hdf5_object is not None:
            self._load_from_hdf5_object(hdf5_object)
        elif tag is not None:
            self._set_internal_attr("_tag", tag)
        else:
            raise ValueError(
                "To create an empty ParamContainer, a tag has to be provided."
            )

        if attribs is not None:
            self._set_attribs(attribs)

    def __setattr__(self, key, value):
        if key in self._key_attribs:
            self._set_internal_attr(key, value)
        elif key in self._tag_children:
            if not isinstance(value, ParamContainer):
                raise AttributeError(key + " is a tag of a child.")

        else:
            raise AttributeError(
                key
                + " is not already set in "
                + self._tag
                + ".\nThe attributes are: "
                + str(self._key_attribs)
                + "\nTo set a new attribute, use _set_attrib or _set_attribs."
            )

    def __getattr__(self, attr):
        if attr.startswith("_"):
            raise AttributeError(
                f"{self.__class__} object has no attribute {attr}"
            )

        else:
            raise AttributeError(
                attr
                + " is not an attribute of "
                + self._tag
                + ".\nThe attributes are: "
                + str(self._key_attribs)
                + "\nThe children are: "
                + str(self._tag_children)
            )

    def __setitem__(self, key, value):
        if "." in key:
            first_part, second_part = key.split(".", 1)
            self[first_part].__setitem__(second_part, value)
        else:
            self.__setattr__(key, value)

    def __getitem__(self, key):
        if "." in key:
            first_part, second_part = key.split(".", 1)
            return self.__getitem__(first_part)[second_part]
        return self.__getattribute__(key)

    def _set_internal_attr(self, key, value):
        self.__dict__[key] = value

    def _set_doc(self, doc):
        self._set_internal_attr("_doc", doc)

    def _contains_doc(self):
        if len(self._doc) > 0:
            return True

        for tag in self._tag_children:
            if self[tag]._contains_doc():
                return True

        return False

    def _get_formatted_doc(self):
        full_tag = self._make_full_tag()
        txt = "Documentation for " + full_tag

        nb_points = full_tag.count(".")
        if nb_points == 0:
            char = "="
        elif nb_points == 1:
            char = "-"
        elif nb_points == 2:
            char = "~"
        else:
            char = "^"

        txt += "\n" + char * len(txt) + "\n"

        doc = self._doc.strip()

        if len(doc) == 0:
            return txt + "\n"

        if len(doc) > 0:
            txt += "\n"

        txt += doc

        if len(doc) > 0:
            txt += "\n"

        return txt

    def _print_doc(self):
        print(self._get_formatted_doc())

    def _get_formatted_docs(self):
        txt = self._get_formatted_doc()
        for tag in self._tag_children:
            if not txt.endswith("\n\n"):
                txt += "\n"
            txt += self[tag]._get_formatted_docs()

        return txt

    def _print_docs(self):
        print(self._get_formatted_docs())

    def _make_full_tag(self):
        if self._parent is None:
            return self._tag

        else:
            return self._parent._make_full_tag() + "." + self._tag

    def _set_attrib(self, key, value):
        """Add an attribute to the container."""
        self.__dict__[key] = value
        self._key_attribs.append(key)

    def _set_attribs(self, d):
        """Add the attributes to the container."""
        for k, v in list(d.items()):
            self._set_attrib(k, v)

    def _get_key_attribs(self):
        self._key_attribs.sort()
        return self._key_attribs

    def _set_child(self, tag, attribs=None, doc=None):
        """Add a child (of the same class) to the container."""
        if tag in self.__dict__:
            raise ValueError(f'The tag "{tag}" is already used.')

        self.__dict__[tag] = self.__class__(tag=tag, attribs=attribs, parent=self)
        self._tag_children.append(tag)

        child = getattr(self, tag)
        if doc is not None:
            child._set_doc(doc)
        return child

    def _set_as_child(self, child, change_parent=True):
        """Associate a ParamContainer as a child."""
        if not isinstance(child, ParamContainer):
            raise ValueError("child should be a ParamContainer instance.")

        if child._tag in self.__dict__:
            raise ValueError(f'The tag "{child._tag}" is already used.')

        self.__dict__[child._tag] = child
        if change_parent:
            child._set_internal_attr("_parent", self)
        self._tag_children.append(child._tag)

    def _make_dict_attribs(self):
        d = {}
        for k in self._key_attribs:
            d[k] = self.__dict__[k]
        return d

    def _make_dict(self):
        self._key_attribs.sort()
        d = {
            "tag": self._tag,
            "key_attribs": self._key_attribs,
            "tag_children": self._tag_children,
        }

        attribs = d["attribs"] = []
        for k in self._key_attribs:
            attribs.append(self.__dict__[k])

        children = d["children"] = []
        for k in self._tag_children:
            children.append(self.__dict__[k]._make_dict())

        return d

    def _make_dict_tree(self):
        """A tree-like nested dictionary, including attributes and children."""
        d = self._make_dict_attribs()
        for k in self._tag_children:
            d[k] = self.__dict__[k]._make_dict_tree()
        return d

    def __eq__(self, other):
        return self._make_dict_tree() == other._make_dict_tree()

    def __sub__(self, other):
        """Subtract and return an ParamContainer to understand differences."""
        if self == other:
            return None

        this = deepcopy(self)

        for k in self._key_attribs:
            if self.__dict__[k] == other.__dict__[k]:
                this.__dict__.pop(k)
                this._key_attribs.remove(k)

        for k in self._tag_children:
            this.__dict__[k] = self.__dict__[k] - other.__dict__[k]
            if this.__dict__[k] is None:
                this.__dict__.pop(k)
                this._tag_children.remove(k)

        return this

    def _make_element_xml(self, parentxml=None):
        if parentxml is None:
            elemxml = etree.Element(self._tag)
        else:
            elemxml = etree.SubElement(parentxml, self._tag)

        self._key_attribs.sort()
        for key in self._key_attribs:
            elemxml.attrib[key] = _as_str(self.__dict__[key])

        if hasattr(self, "_value_text"):
            elemxml.text = str(self._value_text)

        for key in self._tag_children:
            child = self.__dict__[key]
            child._make_element_xml(elemxml)

        return elemxml

    def _make_xml_text(self):
        """Produce and return a xml text representing the container."""
        elemxml = self._make_element_xml()
        return produce_text_element(elemxml)

    def _print_as_xml(self):
        """Print the xml text representing the container."""
        print(self._make_xml_text())

    def __repr__(self):
        return super().__repr__() + "\n\n" + self._make_xml_text()

    def _print_as_code(self):
        print(self._as_code())

    def _as_code(self):
        code = "\n".join(self.__make_lines_code())
        imports = None

        if " array(" in code:
            imports = "from numpy import array\n"

        if " Path(" in code:
            imports += "from pathlib import Path\n"

        if imports is not None:
            code = imports + "\n" + code

        return code

    def __make_lines_code(self):
        lines = []
        tag = self._tag

        self._key_attribs.sort()
        for key in self._key_attribs:
            attr = getattr(self, key)
            lines.append(f"{tag}.{key} = {_as_code(attr)}")

        for key in self._tag_children:
            child = getattr(self, key)
            lines_child = child.__make_lines_code()
            if lines_child:
                lines.extend(f"{tag}.{line}" for line in lines_child)

        return lines

    def _repr_json_(self):
        data = self._make_dict_tree()
        data = sanitize_for_json(data)

        this_id = hex(id(self))
        metadata = {
            "root": f"{self._tag} of {self.__class__} at {this_id}",
            "expanded": True,
        }
        return data, metadata

    def _load_from_xml_file(self, path_file):
        tree = etree.parse(path_file)
        elemxml = tree.getroot()
        self._load_from_elemxml(elemxml)

    def _load_from_elemxml(self, elemxml):
        self._set_internal_attr("_tag", elemxml.tag)

        text = elemxml.text
        if text is not None:
            v = text.strip()
            if len(v) > 0:
                self._set_internal_attr("_value_text", _as_value(v))

        for k, v in list(elemxml.attrib.items()):
            self._set_attrib(k, _as_value(v))

        self._key_attribs.sort()

        tags_multiple = []

        for childxml in elemxml:
            tag = childxml.tag

            children = [c for c in elemxml if c.tag == tag]

            if len(children) > 1 or tag in tags_multiple:
                if tag not in tags_multiple:
                    tags_multiple.append(tag)

                if len(childxml.attrib) == 1:
                    k = list(childxml.attrib.keys())[0]
                    tag += "_" + str(childxml.attrib.pop(k))
                    childxml.tag = tag

            self._set_internal_attr(
                tag, self.__class__(elemxml=childxml, parent=self)
            )
            self._tag_children.append(tag)

    def _save_as_xml(self, path_file=None, comment=None, find_new_name=False):
        """Save the xml text in a file."""
        if path_file is None:
            path_file = self._tag + ".xml"

        if os.path.exists(path_file):
            if not find_new_name:
                raise ValueError(f"The file {path_file} already exists.")

            else:
                base = path_file.split(".xml")[0]
                i = 1
                while os.path.exists(base + f"_{i}.xml"):
                    i += 1
                path_file = base + f"_{i}.xml"

        with open(path_file, "w", encoding="utf-8") as f:
            if comment is not None:
                try:
                    comment = comment.decode("utf-8")
                except (AttributeError, UnicodeEncodeError):
                    pass
                f.write("<!--\n" + comment + "\n-->\n")
            f.write(self._make_xml_text())
        return path_file

    def _save_as_hdf5(
        self,
        path_file=None,
        hdf5_object=None,
        hdf5_parent=None,
        invalid_netcdf=False,
    ):
        """Save in a hdf5 file."""

        if hdf5_parent is not None:
            hdf5_object = hdf5_parent.create_group(self._tag)

        if hdf5_object is None:
            if path_file is None:
                path_file = ""
            if not path_file.endswith(".h5"):
                path_file = os.path.join(path_file, self._tag + ".h5")
            with H5File(path_file, "w") as f:
                try:
                    tag = self._tag.encode("utf8")
                except AttributeError:
                    tag = self._tag
                f.attrs["_tag"] = tag
                self._save_as_hdf5(hdf5_object=f)
        elif path_file is None:
            for key in self._key_attribs:
                value = self.__dict__[key]
                if value is None:
                    value = "None"
                try:
                    value = value.encode("utf8")
                except (AttributeError, UnicodeDecodeError):
                    pass

                if isinstance(value, (list, tuple)):
                    value_tmp = []
                    for v in value:
                        try:
                            v_tmp = v.encode("utf8")
                        except AttributeError:
                            v_tmp = v
                        value_tmp.append(v_tmp)
                    if isinstance(value, tuple):
                        value = tuple(value_tmp)
                    else:
                        value = value_tmp

                if not invalid_netcdf and isinstance(value, bool):
                    value = int(value)

                if isinstance(value, Path):
                    value = str(value)

                try:
                    hdf5_object.attrs[key] = value
                except TypeError:
                    print(key, value, type(value))
                    raise

            for key in self._tag_children:
                group = hdf5_object.create_group(key)
                self.__dict__[key]._save_as_hdf5(hdf5_object=group)
        else:
            raise ValueError(
                "If hdf5_object is not None," "path_file should be None."
            )

    def _load_from_hdf5_file(self, path_file):
        with H5File(path_file, "r") as f:
            self._load_from_hdf5_object(f)

    def _load_from_hdf5_object(self, hdf5_object):
        attrs = dict(hdf5_object.attrs)

        for k, v in list(attrs.items()):
            if isinstance(v, np.integer):
                attrs[k] = int(v)
                continue

            try:
                attrs[k] = v.decode("utf8")
            except AttributeError:
                pass

            if isinstance(v, np.ndarray) and v.dtype.kind in ("S", "U", "O"):
                attrs[k] = list(v.astype(np.compat.unicode))

        tag = hdf5_object.name.split("/")[-1]

        if tag == "":
            try:
                tag = hdf5_object.attrs["_tag"]
                attrs.pop("_tag")
            except KeyError:
                tag = "root_file"

        try:
            tag = tag.decode("utf8")
        except AttributeError:
            pass

        self._set_internal_attr("_tag", tag)

        # detect None attributes
        for k, v in list(attrs.items()):
            if isinstance(v, str) and v == "None":
                attrs[k] = None

        for key in list(attrs.keys()):
            if " " in key:
                attrs[key.replace(" ", "_")] = attrs.pop(key)

        self._set_attribs(attrs)
        for tag in list(hdf5_object.keys()):
            if isinstance(hdf5_object[tag], h5py.Dataset):
                value = hdf5_object[tag][...]
                self._set_attrib(tag, value)

            elif isinstance(hdf5_object[tag], h5py.Group):
                self.__dict__[tag] = self.__class__(
                    hdf5_object=hdf5_object[tag], parent=self
                )
                self._tag_children.append(tag)

    def _modif_from_other_params(self, params):
        """Modify the object with another similar container."""
        for key in params._key_attribs:
            try:
                self[key] = params[key]
            except AttributeError:
                pass
        for tag_child in params._tag_children:
            try:
                self[tag_child]._modif_from_other_params(params[tag_child])
            except AttributeError:
                pass

    def _pop_attrib(self, name):
        self._key_attribs.remove(name)
        return self.__dict__.pop(name)


def tidy_container(cont):
    """Modify the names in a ParamContainer and its organization."""
    newtag = convert_capword_to_lowercaseunderscore(cont._tag)
    cont._set_internal_attr("_tag", newtag)

    for i, oldtag in enumerate(cont._tag_children):
        newtag = convert_capword_to_lowercaseunderscore(oldtag)
        cont._tag_children[i] = newtag
        cont.__dict__[newtag] = cont.__dict__.pop(oldtag)

        if isinstance(cont.__dict__[newtag], str):
            print(cont.__dict__[newtag])
        tidy_container(cont.__dict__[newtag])

    tag_child_to_remove = []
    for tag in cont._tag_children:
        child = cont.__dict__[tag]
        if len(child._tag_children) == 0 and len(child._key_attribs) == 0:
            try:
                value_text = child._value_text
            except AttributeError:
                value_text = ""
            cont.__dict__.pop(tag)
            tag_child_to_remove.append(tag)
            cont._set_attrib(tag, value_text)

    for tag in tag_child_to_remove:
        cont._tag_children.remove(tag)


def convert_capword_to_lowercaseunderscore(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


if __name__ == "__main__":
    # params = ParamContainer(tag='params')

    # params._set_attrib('a0', 1)
    # params._set_attribs({'a1': 1, 'a2': 1})

    # params._set_child('child0', {'a0': 2, 'a1': 2})

    # params2 = ParamContainer(tag='params')

    # params2._set_attribs({'a1': 1, 'a2': 1})
    # params2._set_attrib('a0', 1)

    # params2._set_child('child0', {'a0': 2, 'a1': 2})

    # assert params == params2

    # c1 = ParamContainer(tag='child1')
    # c1._set_attrib('a0', 10)

    # params._set_as_child(c1)

    # print(params)

    # assert params != params2

    params = ParamContainer(tag="params")
    params._set_attribs({"a0": 1, "a1": 1})
    params._set_attrib("a2", 1)

    params._print_as_xml()

    params._set_child("child0", {"a0": 2, "a1": 2})
    params.child0.a0 = 3

    params._print_as_xml()

    # params.a3 = 3

    # params.child0 = 3

    params._save_as_xml()

    params_loaded = ParamContainer(path_file=params._tag + ".xml")
    os.remove(params._tag + ".xml")

    assert params_loaded == params
