"""Container for parameters using xml (:mod:`fluiddyn.util.containerxml`)
=========================================================================

.. currentmodule:: fluiddyn.util.containerxml

Provides:

.. autoclass:: ContainerXML
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

from fluiddyn.io.hdf5 import H5File
import h5py

from fluiddyn.util.xmltotext import produce_text_element


def _as_str(value):
    if not isinstance(value, six.string_types):
        return repr(value)
    else:
        return value


class ContainerXML(object):
    """Structured container of values associated with xml objects.

    The objects ContainerXML can be used as containers of
    parameters. They can be printed as xml text, and saved into and
    loaded from xml and hdf5 files.

    They are used to contain parameters that can be modified by the
    user, for example in this way::

      >>> params = ContainerXML(tag='params')

      >>> params.set_attribs({'a0': 1, 'a1': 1})

      >>> params.set_attrib('a2', 1)

      >>> params.xml_print()
      <params a1="1" a0="1" a2="1"/>

      >>> params.set_child('child0', {'a0': 2, 'a1': 2})

      >>> params.child0.a0 = 3

      >>> params.xml_print()
      <params a1="1" a0="1" a2="1">
      <child0 a1="2" a0="3"/>
      </params>

    Here, `params.child0` is another ContainerXML.

    An interesting feature of the ContainerXML objects is that if one
    uses a non-existing parameter, an AttributeError is raised::

      >>> params.a3 = 3

      -------------------------------------------------------------------------
      AttributeError                          Traceback (most recent call last)
      <ipython-input-9-a91118d8b23e> in <module>()
      ----> 1 params.child1.a0 = 3

      AttributeError: 'ContainerXML' object has no attribute 'child1'

    Note that for a parameter container, it is much better to raise an
    error rather than just add an unused parameter!

    Parameters
    ----------
    (for the __init__ method)

    path_file : (None) str
        Path of a file (xml, hdf5, ...)

    elemxml : (None) xml.etree.ElementTree.Element
        An xml element.

    hdf5_object : (None) file
        An open hdf5 file.

    tag : (None) str
        A tag for the root container.

    parentxml : (None) xml.etree.ElementTree.Element
        The parent element.

    attribs : (None) dict
        Some attributes.

    """
    def __init__(self, path_file=None, elemxml=None, hdf5_object=None,
                 tag=None, parentxml=None, attribs=None):

        self._set_attr('xml_tag_children', [])

        if path_file is not None:
            if path_file.endswith('.xml'):
                self._load_from_xml_file(path_file)
            elif path_file.endswith('.h5'):
                self._load_from_hdf5_file(path_file, parentxml)
        elif elemxml is not None:
            self._load_from_elemxml(elemxml)
        elif hdf5_object is not None:
            self._load_from_hdf5_objet(hdf5_object, parentxml)
        elif tag is not None:
            self._init_elemxml(tag, parentxml)

        if attribs is not None:
            self.set_attribs(attribs)

    def _init_elemxml(self, tag, parentxml):
        self._set_attr('xml_tag', tag)
        if parentxml is None:
            elemxml = etree.Element(tag)
        else:
            elemxml = etree.SubElement(parentxml, tag)
        self._set_attr('_elemxml', elemxml)
        self._set_attr('xml_attrib', elemxml.attrib)

    def _set_attr(self, key, value):
        self.__dict__[key] = value

    def _set_attr_xml(self, key, value):
        self._set_attr(key, value)
        self._elemxml.attrib[key] = _as_str(value)

    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            self._set_attr_xml(key, value)
        else:
            raise KeyError(key+' is not a proper key.')

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def set_attrib(self, key, value):
        """Add an attribute to the container."""
        if key in self.__dict__:
            raise ValueError(
                key+' is already used. If you know what you do,'
                ' you could use _set_attr_xml')
        self._set_attr_xml(key, value)

    def set_attribs(self, d):
        """Add the attributes in the dict d to the container."""
        for k, v in d.items():
            self.set_attrib(k, v)

    def set_child(self, tag, attribs=None):
        """Add a child (of the same class) to the container."""
        if tag in self.__dict__:
            raise ValueError('The tag "{}" is already used.'.format(tag))
        self.__dict__[tag] = self.__class__(tag=tag, attribs=attribs,
                                            parentxml=self._elemxml)
        self.xml_tag_children.append(tag)

    def set_as_child(self, child):
        """Associate a ContainerXML as a child."""
        if isinstance(child, ContainerXML):
            if child.xml_tag in self.__dict__:
                raise ValueError('The tag "{}" is already used.'.format(
                    child.xml_tag))
            self.__dict__[child.xml_tag] = child
            self.xml_tag_children.append(child.xml_tag)
            self._elemxml.append(child._elemxml)
        else:
            raise ValueError('child should be an ContainerXML instance.')

    def xml_produce_text(self):
        """Produce and return the xml text representing the container."""
        return produce_text_element(self._elemxml)

    def xml_print(self):
        """Print the xml text representing the container."""
        print(self.xml_produce_text())

    def __repr__(self):
        return (super(ContainerXML, self).__repr__()
                + '\n\n'+self.xml_produce_text())

    def xml_save(self, path_file, comment=None):
        """Save the xml text in a file."""
        # add verif if the file already exists?
        with open(path_file, 'w') as f:
            if comment is not None:
                f.write('<!--\n'+comment+'\n-->\n')
            f.write(self.xml_produce_text())

    def _load_from_xml_file(self, path_file):
        self._set_attr('xml_path_file', path_file)
        tree = etree.parse(path_file)
        elemxml = tree.getroot()
        self._set_attr('_elemxml', elemxml)
        self._set_attr('xml_attrib', elemxml.attrib)
        self._set_attr('xml_tag', elemxml.tag)

        link_to_his_elemxml(self)

    def xml_to_hdf5(self, hdf5_object=None, path_file=None, hdf5_parent=None):
        """Save in a hdf5 file."""
        if hdf5_parent is not None:
            hdf5_object = hdf5_parent.create_group(self.xml_tag)

        if hdf5_object is None:
            if path_file is None:
                path_file = ''
            if not path_file.endswith('.h5'):
                path_file = os.path.join(path_file, self.xml_tag+'.h5')
            with H5File(path_file, 'w') as f:
                f.attrs.create('xml_tag', self.xml_tag)
                self.xml_to_hdf5(hdf5_object=f)
        elif path_file is None:
            for key in self.xml_attrib.keys():
                hdf5_object.attrs.create(key, self[key])
            for key in self.xml_tag_children:
                group = hdf5_object.create_group(key)
                self[key].xml_to_hdf5(hdf5_object=group)
        else:
            raise ValueError('If hdf5_object is not None,'
                             'path_file should be None.')

    def _load_from_hdf5_file(self, path_file, parentxml):
        self._set_attr('xml_path_file', path_file)
        with H5File(path_file, 'r') as f:
            self._load_from_hdf5_objet(f, parentxml)

    def _load_from_hdf5_objet(self, hdf5_object, parentxml):

        attrs = dict(hdf5_object.attrs)

        tag = hdf5_object.name.split('/')[-1]
        if tag == '':
            try:
                tag = hdf5_object.attrs['xml_tag']
                attrs.pop('xml_tag')
            except KeyError:
                tag = 'root_file'
        self._init_elemxml(tag, parentxml)

        for key in attrs.keys():
            if ' ' in key:
                attrs[key.replace(' ', '_')] = attrs.pop(key)

        self.set_attribs(attrs)
        for tag in hdf5_object.keys():
            if isinstance(hdf5_object[tag], h5py.Dataset):
                value = hdf5_object[tag][...]
                self.set_attrib(tag, value)

            elif isinstance(hdf5_object[tag], h5py.Group):
                self.__dict__[tag] = self.__class__(
                    hdf5_object=hdf5_object[tag], parentxml=self._elemxml)
                self.xml_tag_children.append(tag)


def associate_with_containerxml(elemxml, parentcontxml):
    tag = elemxml.tag
    contxml = parentcontxml.__class__(tag=tag)
    contxml._set_attr('_elemxml', elemxml)

    parentcontxml._set_attr(tag, contxml)
    parentcontxml.xml_tag_children.append(tag)
    link_to_his_elemxml(contxml)


def link_to_his_elemxml(contxml):
    elemxml = contxml._elemxml

    text = elemxml.text
    if text is not None:
        v = text.strip()
        try:
            v = literal_eval(v)
        except (SyntaxError, ValueError):
            pass
        contxml._set_attr('xml_value_text', v)

    for k, v in elemxml.attrib.items():
        try:
            v = literal_eval(v)
        except (SyntaxError, ValueError):
            pass
        contxml._set_attr(k, v)

    for childxml in elemxml:
        associate_with_containerxml(childxml, parentcontxml=contxml)


import re


def tidy_containerxml(contxml):
    """Modify the names in a ContainerXML and its organisation.

    """
    tag = contxml.xml_tag
    newtag = convert_capword_to_lowercaseunderscore(tag)
    contxml._set_attr('xml_tag', newtag)
    elemxml = contxml._elemxml
    elemxml.tag = newtag

    for itag, tagchild in enumerate(contxml.xml_tag_children):
        newtag = convert_capword_to_lowercaseunderscore(tagchild)
        contxml.xml_tag_children[itag] = newtag
        contxml.__dict__[newtag] = contxml.__dict__.pop(tagchild)
        tidy_containerxml(contxml.__dict__[newtag])

    for tagchild in contxml.xml_tag_children:
        child = contxml.__dict__[tagchild]

        if len(child.xml_tag_children) == 0 and len(child.xml_attrib) == 0:
            contxml.__dict__[tagchild] = child.xml_value_text
            elemxml.remove(elemxml.find(tagchild))
            elemxml.attrib[tagchild] = str(child.xml_value_text)


def convert_capword_to_lowercaseunderscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
