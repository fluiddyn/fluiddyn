"""
IO for Dantec files (:mod:`fluiddyn.io.dantec`)
===============================================

.. currentmodule:: fluiddyn.io.dantec

Provides the classes :class:`LoadedElement`, :class:`LoadedXML`
:class:`DantecImageEnsemble` and :class:`DantecVectorEnsemble`.

Warning: no security at all. For example, it would fall in a loop
if there is a loop in the file. Do not use with untrusted xml
files.

.. autoclass:: LoadedElement
   :members:

.. autoclass:: LoadedXML
   :members:

.. autoclass:: DantecImageEnsemble
   :members:

.. autoclass:: DantecVectorEnsemble
   :members:


"""

from __future__ import division, print_function

import numpy as np
import os

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from ast import literal_eval
from glob import glob

from fluiddyn.io.binary import BinFile


class LoadedElement(object):
    """A loaded element of a xml file.

    Warning: no security at all. For example, it would fall in a loop
    if there is a loop in the file. Do not use with untrusted xml
    files.

    """
    def __init__(self, unloaded_element):
        self.tag = unloaded_element.tag
        attrib = unloaded_element.attrib
        if len(attrib) > 0:
            self.attrib = attrib
        try:
            value = literal_eval(unloaded_element.text)
            self.value = value
        except (SyntaxError, ValueError):
            pass
        for child in unloaded_element:
            key = child.tag.replace('.', '_')
            keyl = 'list_'+key
            # we hope there no tag in the file corresponding to keyl...
            # for Dantec files, it does not seem to be the case
            if key not in self.__dict__ and keyl not in self.__dict__:
                self.__dict__[key] = LoadedElement(child)
            else:
                if keyl not in self.__dict__:
                    self.__dict__[keyl] = []
                    self.__dict__[keyl].append(self.__dict__[key])
                    del self.__dict__[key]
                self.__dict__[keyl].append(LoadedElement(child))

    def __repr__(self):
        if hasattr(self, 'attrib'):
            return repr(self.attrib)
        elif hasattr(self, 'value'):
            return repr(self.value)
        else:
            return repr(self.__class__)

class LoadedXML(LoadedElement):
    """Initialize the loop on the file elements..."""
    def __init__(self, name_file):
        tree = etree.parse(name_file)
        root = tree.getroot()
        super(LoadedXML, self).__init__(root)



class DantecImageEnsemble(object):
    _offset_header = 0xC22
    def __init__(self, path_base):
        self.path_base = path_base
        self.xlm = LoadedXML(
            os.path.join(self.path_base, 'AcquiredImageEnsemble.xml'))
        self.name_files = glob(
            os.path.join(self.path_base, 'data/image*.image'))
        self.shape = np.array(
            self.xlm.Ensemble_CoordinateSummary.imageSize.value)

    def load_image(self, ind=-1):
        name_file = self.name_files[ind]
        with BinFile(name_file) as f:
            f.seek(0)
            f.seek(self._offset_header)
            data = f.readt(self.shape.prod(), 'B')
            return np.array(data, dtype=np.uint8).reshape(self.shape)



class DantecVectorEnsemble(object):
    def __init__(self):
        self.xlm = LoadedXML('AnalysisEnsemble_PIV.xml')




if __name__ == '__main__':

    path_base = r'/home/pa371/Data_reasons_pa371/Temp/Dantec_files/Run 11-00-21.3te2sz41/SpeedSence 1040.3te2sz4k'

    imensemble = DantecImageEnsemble(path_base)
    im = imensemble.load_image()


    # vectensemble = DantecVectorEnsemble('')

    # shape = np.array(imensemble.shape)
    # name_file = r'image#0.image'
    # f = BinFile(name_file)
    # offset = 0xC22
    # f.seek(offset)
    # im = np.array(f.readt(shape.prod(), 'B'), dtype=np.uint8).reshape(shape)
    # print(f.readt(1, 'B'))
    # print(f.readt(10, 'B'))


