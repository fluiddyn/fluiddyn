"""Container for parameters (:mod:`fluiddyn.util.paramcontainer`)
=================================================================

.. currentmodule:: fluiddyn.util.paramcontainer

Provides:

.. autoclass:: ParamContainer
   :members:
   :private-members:

"""

from __future__ import division, print_function

import os

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from ast import literal_eval

import six

import re

from fluiddyn.io.hdf5 import H5File
import h5py

from fluiddyn.util.xmltotext import produce_text_element


def _as_str(value):
    if not isinstance(value, six.string_types):
        return repr(value)
    else:
        return value


def _as_value(value):
    if value.startswith('array('):
        return eval(value)
    try:
        return literal_eval(value)
    except (SyntaxError, ValueError):
        return value


class ParamContainer(object):
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
    def __init__(self, tag=None, attribs=None,
                 path_file=None, elemxml=None, hdf5_object=None):

        self._set_internal_attr('_attribs', set())
        self._set_internal_attr('_tag_children', set())

        if path_file is not None:
            self._set_internal_attr('_path_file', path_file)
            if path_file.endswith('.xml'):
                self._load_from_xml_file(path_file)
            elif path_file.endswith('.h5'):
                self._load_from_hdf5_file(path_file)
        elif elemxml is not None:
            self._load_from_elemxml(elemxml)
        elif hdf5_object is not None:
            self._load_from_hdf5_objet(hdf5_object)
        elif tag is not None:
            self._set_internal_attr('_tag', tag)
        else:
            raise ValueError(
                'To create an empty ParamContainer, '
                'a tag has to be provided.')

        if attribs is not None:
            self._set_attribs(attribs)

    def __setattr__(self, key, value):
        if key in self._attribs:
            self._set_internal_attr(key, value)
        elif key in self._tag_children:
            if not isinstance(value, ParamContainer):
                raise AttributeError(
                    key + ' is a tag of a child.')
        else:
            raise AttributeError(
                key + ' is not already set in ' + self._tag +
                '.\nThe attributes are: ' + str(self._attribs) +
                '\nTo set a new attribute, use _set_attrib or _set_attribs.')

    def __getattr__(self, attr):
        if attr.startswith('_'):
            raise AttributeError(
                '{} object has no attribute {}'.format(self.__class__, attr))
        else:
            raise AttributeError(
                attr + ' is not an attribute of ' + self._tag +
                '.\nThe attributes are: ' + str(list(self._attribs)))

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def _set_internal_attr(self, key, value):
        self.__dict__[key] = value

    def _set_attrib(self, key, value):
        """Add an attribute to the container."""
        self.__dict__[key] = value
        self._attribs.add(key)

    def _set_attribs(self, d):
        """Add the attributes to the container."""
        for k, v in d.items():
            self._set_attrib(k, v)

    def _set_child(self, tag, attribs=None):
        """Add a child (of the same class) to the container."""
        if tag in self.__dict__:
            raise ValueError('The tag "{}" is already used.'.format(tag))
        self.__dict__[tag] = self.__class__(tag=tag, attribs=attribs)
        self._tag_children.add(tag)

    def _set_as_child(self, child):
        """Associate a ParamContainer as a child."""
        if not isinstance(child, ParamContainer):
            raise ValueError('child should be a ParamContainer instance.')
        if child._tag in self.__dict__:
            raise ValueError(
                'The tag "{}" is already used.'.format(child._tag))
        self.__dict__[child._tag] = child
        self._tag_children.add(child._tag)

    def _make_dict(self):
        d = {'_tag': self._tag, '_attribs': self._attribs,
             '_tag_children': self._tag_children}

        for k in self._attribs.union(self._tag_children):
            d[k] = self.__dict__[k]

        return d

    def __eq__(self, other):
        return self._make_dict() == other._make_dict()

    def _make_element_xml(self, parentxml=None):
        if parentxml is None:
            elemxml = etree.Element(self._tag)
        else:
            elemxml = etree.SubElement(parentxml, self._tag)

        for key in self._attribs:
            elemxml.attrib[key] = _as_str(self.__dict__[key])

        for key in self._tag_children:
            child = self.__dict__[key]
            elemxml.append(child._make_element_xml(elemxml))

        return elemxml

    def _make_xml_text(self):
        """Produce and return a xml text representing the container."""
        elemxml = self._make_element_xml()
        return produce_text_element(elemxml)

    def _print_as_xml(self):
        """Print the xml text representing the container."""
        print(self._make_xml_text())

    def __repr__(self):
        return (super(ParamContainer, self).__repr__() +
                '\n\n'+self._make_xml_text())

    def _load_from_xml_file(self, path_file):
        tree = etree.parse(path_file)
        elemxml = tree.getroot()
        self._load_from_elemxml(elemxml)

    def _load_from_elemxml(self, elemxml):
        self._set_internal_attr('_tag', elemxml.tag)

        text = elemxml.text
        if text is not None:
            v = text.strip()
            if len(v) > 0:
                self._set_internal_attr('_value_text', _as_value(v))

        for k, v in elemxml.attrib.items():
            self._set_attrib(k, _as_value(v))

        for childxml in elemxml:
            self._set_internal_attr(
                childxml.tag, self.__class__(elemxml=childxml))
            self._tag_children.add(childxml.tag)

    def _save_as_xml(self, path_file=None, comment=None):
        """Save the xml text in a file."""
        if path_file is None:
            path_file = self._tag + '.xml'

        if os.path.exists(path_file):
            raise ValueError('The file already exists.')

        with open(path_file, 'w') as f:
            if comment is not None:
                f.write('<!--\n'+comment+'\n-->\n')
            f.write(self._make_xml_text())

    def _save_as_hdf5(self, path_file=None, hdf5_object=None,
                      hdf5_parent=None):
        """Save in a hdf5 file."""

        if hdf5_parent is not None:
            hdf5_object = hdf5_parent.create_group(self._tag)

        if hdf5_object is None:
            if path_file is None or not path_file.endswith('.h5'):
                path_file = os.path.join(path_file, self._tag + '.h5')
            with H5File(path_file, 'w') as f:
                f.attrs.create('_tag', self._tag)
                self._save_as_hdf5(hdf5_object=f)
        elif path_file is None:
            for key in self._attribs:
                hdf5_object.attrs.create(key, self.__dict__[key])
            for key in self._tag_children:
                group = hdf5_object.create_group(key)
                self.__dict__[key]._save_as_hdf5(hdf5_object=group)
        else:
            raise ValueError('If hdf5_object is not None,'
                             'path_file should be None.')

    def _load_from_hdf5_file(self, path_file):
        with H5File(path_file, 'r') as f:
            self._load_from_hdf5_objet(f)

    def _load_from_hdf5_objet(self, hdf5_object):

        attrs = dict(hdf5_object.attrs)

        tag = hdf5_object.name.split('/')[-1]
        if tag == '':
            try:
                tag = hdf5_object.attrs['_tag']
                attrs.pop('_tag')
            except KeyError:
                tag = 'root_file'

        self._set_internal_attr('_tag', tag)

        for key in attrs.keys():
            if ' ' in key:
                attrs[key.replace(' ', '_')] = attrs.pop(key)

        self._set_attribs(attrs)
        for tag in hdf5_object.keys():
            if isinstance(hdf5_object[tag], h5py.Dataset):
                value = hdf5_object[tag][...]
                self._set_attrib(tag, value)

            elif isinstance(hdf5_object[tag], h5py.Group):
                self.__dict__[tag] = self.__class__(
                    hdf5_object=hdf5_object[tag])
                self._tag_children.add(tag)


def tidy_container(cont):
    """Modify the names in a ParamContainer and its organization.

    """
    newtag = convert_capword_to_lowercaseunderscore(cont._tag)
    cont._tag = newtag

    for oldtag in cont._tag_children:
        newtag = convert_capword_to_lowercaseunderscore(oldtag)
        cont._tag_children.remove(oldtag)
        cont._tag_children.add(newtag)
        cont.__dict__[newtag] = cont.__dict__.pop(oldtag)
        tidy_container(cont.__dict__[newtag])

    for tag in cont._tag_children:
        child = cont.__dict__[tag]

        if len(child._tag_children) == 0 and len(child._attribs) == 0:
            value_text = child._value_text
            cont.__dict__.pop(tag)
            cont._set_attrib(tag, value_text)


def convert_capword_to_lowercaseunderscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


if __name__ == '__main__':
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

    params = ParamContainer(tag='params')
    params._set_attribs({'a0': 1, 'a1': 1})
    params._set_attrib('a2', 1)

    params._print_as_xml()

    params._set_child('child0', {'a0': 2, 'a1': 2})
    params.child0.a0 = 3

    params._print_as_xml()

    # params.a3 = 3

    # params.child0 = 3

    params._save_as_xml()

    params_loaded = ParamContainer(path_file=params._tag + '.xml')
    os.remove(params._tag + '.xml')

    assert params_loaded == params
