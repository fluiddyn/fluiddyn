"""Read and convert .im7 files (Davis Lavision) (:mod:`fluiddyn.io.davis`)
==========================================================================

"""

import argparse
import os
from glob import glob
from multiprocessing import Pool, cpu_count

from .query import query_yes_no

try:
    import ReadIM

    _readim_ok = True
except ImportError as error:
    _error_readim = error
    _readim_ok = False


try:
    import png

    _png_ok = True
except ImportError as error:
    _error_png = error
    _png_ok = False


def _import_error_readim():
    print(
        """ImportError ReadIM.
We need the package ReadIM to handle .im7 images. Please install it correctly
(see https://bitbucket.org/fleming79/readim)."""
    )
    raise ImportError(_error_readim)


def _import_error_png():
    print(
        """ImportError png.
We need the package pypng to handle png 'I;16'. Please install it correctly with
`pip install pypng` (see https://pypi.python.org/pypi/pypng)."""
    )
    raise ImportError(_error_png)


def readimages(path):

    if not _readim_ok:
        _import_error_readim()

    vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList(path)
    v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)

    images = []

    for iframe in range(vbuff.nf):
        images.append(v_array[iframe])

    return images


def parse_args():
    parser = argparse.ArgumentParser(
        description="""Convert .im7 files in a directory""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "path", nargs="?", default=os.getcwd(), help="Path of the directory."
    )

    parser.add_argument(
        "--sequential",
        help="Run sequencially, without multiprocessing.",
        action="store_true",
    )

    return parser.parse_args()


def convertim7(args):
    if not _readim_ok:
        _import_error_readim()

    if not _png_ok:
        _import_error_png()

    path = args.path

    if os.path.isdir(path):
        path = os.path.join(path, "*.im7")
    elif not path.endswith(".im7"):
        path += "*.im7"

    files = glob(path)
    files.sort()
    nb_files = len(files)

    if nb_files == 0:
        print("no file to treat.")
        return

    path_new_dir = os.path.dirname(files[0])
    path_new_dir += "_png"

    if nb_files == 1:
        plurial = ""
    else:
        plurial = "s"

    if not query_yes_no(
        "{} im7 file{} to be converted in the directory\n{}\n".format(
            nb_files, plurial, path_new_dir
        )
    ):
        return

    if not os.path.exists(path_new_dir):
        os.makedirs(path_new_dir)

    if args.sequential:
        for path in files:
            convert_1file(path, path_new_dir)
    else:
        pool = Pool(processes=min(cpu_count(), nb_files))
        pool.starmap(convert_1file, ((path, path_new_dir) for path in files))


def convert_1file(path, path_new_dir):

    name = os.path.split(path)[1]
    print("treat file " + name)
    name = os.path.splitext(name)[0]

    images = readimages(path)
    nb_images = len(images)

    if nb_images == 1:

        def get_new_name(i):
            return name + ".png"

    elif nb_images > 24:
        raise NotImplementedError

    else:
        isdecimal = name[-1].isdecimal()

        def get_new_name(i):
            if isdecimal:
                return name + chr(97 + i) + ".png"

            else:
                raise NotImplementedError

    for i, image in enumerate(images):
        new_name = get_new_name(i)
        print("save " + new_name)
        pathnew = os.path.join(path_new_dir, new_name)

        png_img = png.from_array(image, "L;16")
        png_img.save(pathnew)
