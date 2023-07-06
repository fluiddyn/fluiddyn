"""
IO for multitiff files (:mod:`fluiddyn.io.multitiff`)
=====================================================

.. autofunction:: reorganize_single_frame_3Dscannedpiv_data
.. autofunction:: reorganize_piv3dscanning_doubleframe
.. autofunction:: reorganize_piv2d_singleframe
.. autofunction:: reorganize_piv2d_doubleframe

"""

import glob
import io
import os
import sys
import time
from math import ceil, log10

from packaging import version

from .image import _image_from_array
from .query import query_yes_no

try:
    import PIL
    from PIL import Image
except ImportError:
    pass


def glob_sorted(s):
    l = glob.glob(s)
    l.sort()
    return l


def _should_we_stop():
    if query_yes_no("Some folders already exist\n Do you want to continue?"):
        return False

    return True


def _save_new_file(im, base_path, outputext, erase=False):
    """Convert and save file if destination path does not exist.

    FIXME: The `im.convert` function calls result in ResourceWarning
    in Python 3.x. Almost certainly a Pillow bug. Can be suppressed by
    adding the following lines.

    >>> import warnings
    >>> warnings.simplefilter('ignore', ResourceWarning)

    """
    path_save = base_path + "." + outputext
    if not erase and os.path.exists(path_save):
        return False

    if outputext == "jp2":
        with im.convert(mode="L") as new_im:
            new_im.save(path_save, quality_mode="rate", quality_layers=[8])
    else:
        with im.convert(mode="I") as new_im:
            new_im.save(path_save)

    return True


def imsave(path, arrays, as_int=False):
    """Save a multi-frame image sequence.

    Parameters
    ----------
    path : str
        Output file name or full path.
    arrays : array-like
        A iterable containing multiple 2D numpy arrays, representing frames.
    as_int : bool
        Convert to integer or not.

    """

    pil_version = version.parse(PIL.__version__)

    if pil_version < version.parse("3.4.0"):
        raise ImportError("imsave for multiframe TIFF not supported.")

    im_list = [_image_from_array(a, as_int) for a in arrays]

    if pil_version < version.parse("4.2.0"):
        from warnings import warn

        warn(
            "imsave for multiframe TIFF uses an intermediate GIF workaround.",
            DeprecationWarning,
        )
        gif = im_list.pop(0)

        with io.BytesIO() as output:
            gif.save(output, format="GIF", save_all=True, append_images=im_list)
            gif.close()

            with Image.open(output) as im:
                im.save(path, format="TIFF", save_all=True)
    else:
        im_list[0].save(
            path,
            compression="tiff_deflate",
            save_all=True,
            append_images=im_list[1:],
        )


def reorganize_single_frame_3Dscannedpiv_data(
    files, nb_levels, outputdir=".", outputext="tif", erase=False
):
    """
    Reorganize data from multi tiff into a folders (one for each level).

    Parameters
    ----------

    files : str
      Root of the names of files: example files = 'van_karman_flow*'

    nb_levels : int
      Number of levels in the scanned PIV

    outputdir : '.'
      Output folder.

    outputext : str
      The output files extension

    erase : {False, bool}
      If erase, the existing files are replaced.

    Notes
    -----

    Data is organize as:
    - outputdir/level1/im0.tif, outputdir/level1/im1.tif ...
    - outputdir/level2/im0.tif, outputdir/level2/im1.tif ...

    """

    path_files = glob_sorted(files)
    if len(path_files) == 0:
        return

    nb_images = get_approximate_number_images(path_files)
    if nb_images == 0:
        return

    format_index = ":0{}d".format(int(ceil(log10(nb_images))))
    format_level = ":0{}d".format(int(ceil(log10(nb_levels))))

    index_im = 0

    for ind in range(nb_levels):
        dir_lev = (outputdir + "/level{" + format_level + "}").format(ind)
        if not os.path.exists(dir_lev):
            os.makedirs(dir_lev)

    for path_tiff in path_files:
        t_start = time.time()
        print(
            "Convert and save file\n" + path_tiff + "\nin directory\n" + outputdir
        )
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                except EOFError:
                    break

                else:
                    base_path = (
                        outputdir
                        + "/level{"
                        + format_level
                        + "}/im{"
                        + format_index
                        + "}"
                    ).format(index_im % nb_levels, index_im // nb_levels)
                    if _save_new_file(im, base_path, outputext, erase):
                        print(
                            "\r file {}; in {:.2f} s".format(
                                index_im, time.time() - t_start
                            ),
                            end="",
                        )
                        sys.stdout.flush()

                    index_im += 1
                    index_im_in_tiff += 1
            print("")


def reorganize_piv3dscanning_doubleframe(
    files, nb_levels, outputdir=".", outputext="tif", erase=False
):
    """
    Reorganize data from multi tiff into a folders (one for each level).

    Parameters
    ----------

    files : str
      Root of the names of files: example files = 'van_karman_flow*'

    nb_levels : int
      Number of levels in the scanned PIV

    outputdir : '.'
      Output folder.

    outputext : str
      The output files extension

    erase : {False, bool}
      If erase, the existing files are replaced.

    Notes
    -----

    Data is organized as:
    - outputdir/level1/im0.tif, outputdir/level1/im1.tif ...
    - outputdir/level2/im0.tif, outputdir/level2/im1.tif ...

    """
    path_files = glob_sorted(files)
    if len(path_files) == 0:
        return

    nb_images = get_approximate_number_images(path_files)
    if nb_images == 0:
        return

    format_index = ":0{}d".format(int(ceil(log10(nb_images))))
    format_level = ":0{}d".format(int(ceil(log10(nb_levels))))

    index_im = 0

    for ind in range(nb_levels):
        dir_lev = (outputdir + "/level{" + format_level + "}").format(ind)
        if not os.path.exists(dir_lev):
            os.makedirs(dir_lev)

    for path_tiff in path_files:
        t_start = time.time()
        print(
            "Convert and save file\n" + path_tiff + "\nin directory\n" + outputdir
        )
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                except EOFError:
                    break

                except SyntaxError:
                    print(
                        "SyntaxError with file",
                        path_tiff,
                        "\nStop the conversion for this file.",
                    )
                    return

                else:
                    index_time = index_im // nb_levels
                    if index_time % 2 == 0:
                        letter = "a"
                    else:
                        letter = "b"
                    base_path = (
                        outputdir
                        + "/level{"
                        + format_level
                        + "}/im{"
                        + format_index
                        + "}"
                        + letter
                    ).format(index_im % nb_levels, index_time // 2)
                    if _save_new_file(im, base_path, outputext, erase):
                        print(
                            "\r file {}; in {:.2f} s".format(
                                index_im, time.time() - t_start
                            ),
                            end="",
                        )
                        sys.stdout.flush()

                    index_im += 1
                    index_im_in_tiff += 1
            print("")


def count_number_images(path_files):
    # warning: can be very slow
    nb_images = 0
    for path_tiff in path_files:
        with Image.open(path_tiff) as image:
            nb_images += image.n_frames
            print(
                "taking in account file {}, nb_images = {}".format(
                    path_tiff, nb_images
                )
            )

    return nb_images


def get_approximate_number_images(path_files):
    # can be much faster than count_number_images
    path = path_files[0]
    with Image.open(path) as image:
        nb_images = image.n_frames

    return len(path_files) * nb_images


def reorganize_piv2d_singleframe(
    files, outputdir=".", outputext="tif", erase=False
):
    """
    Reorganize data from multi tiff (single frame 2D).

    Parameters
    ----------

    files : str
      Root of the names of files: example files = 'van_karman_flow*'

    outputdir : '.'
      Output folder

    outputext : str
      The output files extension

    erase : {False, bool}
      If erase, the existing files are replaced.

    Notes
    -----

    Data is organize as:
    outputdir/im0.tif, outputdir/im1.tif ...

    """
    path_files = glob_sorted(files)
    if len(path_files) == 0:
        return

    nb_images = get_approximate_number_images(path_files)
    if nb_images == 0:
        return

    format_index = ":0{}d".format(int(ceil(log10(nb_images))))

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    index_im = 0
    for path_tiff in path_files:
        t_start = time.time()
        print(
            "Convert and save file\n" + path_tiff + "\nin directory\n" + outputdir
        )
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                except EOFError:
                    break

                else:
                    base_path = outputdir + ("/im{" + format_index + "}").format(
                        index_im
                    )
                    if _save_new_file(im, base_path, outputext, erase):
                        print(
                            "\r file {}; in {:.2f} s".format(
                                index_im, time.time() - t_start
                            ),
                            end="",
                        )
                        sys.stdout.flush()
                    index_im += 1
                    index_im_in_tiff += 1

            print("")

        print(
            "End convert file {} in {} s".format(
                os.path.split(path_tiff)[0], time.time() - t_start
            )
        )
        sys.stdout.flush()


def reorganize_piv2d_doubleframe(
    files, outputdir=".", outputext="tif", erase=False
):
    """
    Reorganize data from multi tiff (double frame 2D).

    Parameters
    ----------
    files : str
      Root of the names of files: example files = 'van_karman_flow*'

    outputdir : '.'
      Output folder

    outputext : str
      The output files extension

    erase : {False, bool}
      If erase, the existing files are replaced.

    Notes
    -----

    Data is organize as:
    - outputdir/im0a.tif, outputdir/im0b.tif, outputdir/im1a.tif ...

    """
    path_files = glob_sorted(files)
    if len(path_files) == 0:
        return

    nb_images = get_approximate_number_images(path_files)
    if nb_images == 0:
        return

    format_index = ":0{}d".format(int(ceil(log10(nb_images))))

    index_im = 0
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    for path_tiff in path_files:
        t_start = time.time()
        print(
            "Convert and save file\n" + path_tiff + "\nin directory\n" + outputdir
        )
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                except EOFError:
                    break

                else:
                    if index_im % 2 == 0:
                        letter = "a"
                    else:
                        letter = "b"
                    base_path = (
                        outputdir
                        + ("/im{" + format_index + "}").format(index_im // 2)
                        + letter
                    )
                    if _save_new_file(im, base_path, outputext, erase):
                        print(
                            "\r file {}; in {:.2f} s".format(
                                index_im, time.time() - t_start
                            ),
                            end="",
                        )
                        sys.stdout.flush()
                    index_im += 1
                    index_im_in_tiff += 1

            print("")

        print(
            "End convert file {} in {} s".format(
                os.path.split(path_tiff)[0], time.time() - t_start
            )
        )
        sys.stdout.flush()
