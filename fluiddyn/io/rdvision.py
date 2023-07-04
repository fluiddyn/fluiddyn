"""Utilities to read RD Vision files
====================================

"""

import configparser
import os

import numpy as np

from fluiddyn.io.binary import BinFile
from fluiddyn.util.paramcontainer import ParamContainer, tidy_container

try:
    from PIL import Image
except ImportError:
    pass


def read_seq(name):
    if not name.endswith(".seq"):
        name += ".seq"
    config = configparser.ConfigParser()
    config.read([name])
    l = config.items(config.sections()[0])
    d = {k.replace(" ", "_"): v for k, v in l}
    return d


def read_xml(name):
    if not name.endswith(".xml"):
        name += ".xml"

    p = ParamContainer(path_file=name)
    tidy_container(p)
    return p


def read_sqb(name, nb_files=1):
    if not name.endswith(".sqb"):
        name += ".sqb"
    offsets = np.empty([nb_files], dtype=np.uint32)
    timestamps = np.empty([nb_files], dtype=np.float64)
    indices_files = np.empty([nb_files], dtype=np.uint32)

    with BinFile(name) as f:
        for i in range(nb_files):
            offsets[i] = f.readt(1, "uint32")
            f.readt(1, "uint32")
            timestamps[i] = f.readt(1, "float64")
            indices_files[i] = f.readt(1, "uint32")
            f.readt(1, "uint32")

    return offsets, timestamps, indices_files


class SetOfFiles:
    def __init__(self, name):
        self.d = d = read_seq(name)

        self.name = d["sequence_name"]
        self.name_short = name.split("_")[0]

        self.width = int(d["width"])
        self.height = int(d["height"])
        self.bytesperpixel = int(d["bytesperpixel"])
        self.bitsperpixel = int(d["bitsperpixel"])

        self.nb_files = int(d["number_of_files"])

        self.offsets, self.timestamps, self.indices_files = read_sqb(
            name + ".sqb", int(d["number_of_files"])
        )

    def read_im(self, index):
        path = (
            self.d["bin_repertoire"]
            + "/"
            + self.d["bin_file"]
            + "{:05d}.bin".format(self.indices_files[index])
        )

        assert os.path.exists(path)

        with BinFile(path) as f:
            f.seek(self.offsets[index])
            im = np.reshape(
                f.readt(
                    self.width * self.height,
                    "uint{}".format(self.bytesperpixel * 8),
                ),
                [self.height, self.width],
            ).astype(np.dtype("int32"))

        return im * 2 ** (16 - self.bitsperpixel)

    def convert_all_images(self):
        new_dir = self.name_short
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        for index in range(self.nb_files):
            im = self.read_im(index)
            path = os.path.join(new_dir, f"im_{index}.png")
            im_pil = Image.fromarray(im)
            im_pil.save(path)
