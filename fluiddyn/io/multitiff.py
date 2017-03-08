"""
Multitiff
=========

.. autofunction:: reorganize_single_frame_3Dscannedpiv_data
.. autofunction:: reorganize_double_frame_3Dscannedpiv_data
.. autofunction:: reorganize_single_frame_2Dpiv_data
.. autofunction:: reorganize_double_frame_2Dpiv_data

"""
from __future__ import print_function, division

from builtins import range
import sys
import time
import os
import glob
from math import ceil, log10

try:
    from PIL import Image
except ImportError:
    pass

from fluiddyn.util.query import query_yes_no


def _should_we_stop():
    if query_yes_no('Some folders already exist\n Do you want to continue?'):
        return False
    return True


def _save_new_file(im, base_path, outputext, erase=False):
    path_save = base_path + '.' + outputext
    if not erase and os.path.exists(path_save):
        return False
    if outputext == 'jp2':
        with im.convert(mode='L') as new_im:
            new_im.save(path_save,
                        quality_mode='rate', quality_layers=[8])
    else:
        with im.convert(mode='I') as new_im:
            new_im.save(path_save)
    return True


def reorganize_single_frame_3Dscannedpiv_data(files, nb_levels, outputdir='.',
                                              outputext='tif', erase=False):
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

    files = glob.glob(files)

    # wrong ! to be improved
    nb_images = int(round(len(files) * 200. / nb_levels))
    if nb_images == 0:
        return
    format_index = ':0{}d'.format(int(ceil(log10(nb_images))))
    format_level = ':0{}d'.format(int(ceil(log10(nb_levels))))

    index_im = 0

    for ind in range(nb_levels):
        dir_lev = (outputdir + '/level{' + format_level + '}').format(ind)
        if not os.path.exists(dir_lev):
            os.makedirs(dir_lev)

    for path_tiff in files:
        t_start = time.time()
        print('Convert and save file\n' +
              path_tiff + '\nin directory\n' + outputdir)
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                except EOFError:
                    break
                else:
                    base_path = (
                        outputdir + '/level{' + format_level +
                        '}/im{' + format_index + '}').format(
                            index_im % nb_levels, index_im//nb_levels)
                    if _save_new_file(im, base_path, outputext, erase):
                        print('\r file {}; in {:.2f} s'.format(
                            index_im, time.time() - t_start), end='')
                        sys.stdout.flush()

                    index_im += 1
                    index_im_in_tiff += 1


def reorganize_double_frame_3Dscannedpiv_data(
        files, nb_levels, outputdir='.', outputext='tif', erase=False):
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

    files = glob.glob(files)

    # wrong ! to be improved
    nb_images = int(round(len(files) * 200. / nb_levels))
    if nb_images == 0:
        return
    format_index = ':0{}d'.format(int(ceil(log10(nb_images))))
    format_level = ':0{}d'.format(int(ceil(log10(nb_levels))))

    index_im = 0

    for ind in range(nb_levels):
        dir_lev = (outputdir + '/level{' + format_level + '}').format(ind)
        if not os.path.exists(dir_lev):
            os.makedirs(dir_lev)

    for path_tiff in files:
        t_start = time.time()
        print('Convert and save file\n' +
              path_tiff + '\nin directory\n' + outputdir)
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                except EOFError:
                    break
                else:
                    index_time = index_im // nb_levels
                    if index_time % 2 == 0:
                        letter = 'a'
                    else:
                        letter = 'b'
                    base_path = (
                        outputdir + '/level{' + format_level + '}/im{' +
                        format_index + '}' + letter).format(
                            index_im % nb_levels, index_time // 2)
                    if _save_new_file(im, base_path, outputext, erase):
                        print('\r file {}; in {:.2f} s'.format(
                            index_im, time.time() - t_start), end='')
                        sys.stdout.flush()

                    index_im += 1
                    index_im_in_tiff += 1


def reorganize_single_frame_2Dpiv_data(
        files, outputdir='.', outputext='tif', erase=False):
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
    files = glob.glob(files)

    # wrong ! to be improved
    nb_images = len(files) * 200
    if nb_images == 0:
        return
    format_index = ':0{}d'.format(int(ceil(log10(nb_images))))

    index_im = 0
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    for path_tiff in files:
        t_start = time.time()
        print('Convert and save file\n' +
              path_tiff + '\nin directory\n' + outputdir)
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                except EOFError:
                    break
                else:
                    base_path = (
                        outputdir +
                        ('/im{' + format_index + '}').format(index_im))
                    if _save_new_file(im, base_path, outputext, erase):
                        print('\r file {}; in {:.2f} s'.format(
                            index_im, time.time() - t_start), end='')
                        sys.stdout.flush()
                    index_im += 1
                    index_im_in_tiff += 1

        print('\nEnd convert file {} in {} s'.format(
            os.path.split(path_tiff)[0], time.time() - t_start))
        sys.stdout.flush()


def reorganize_double_frame_2Dpiv_data(
        files, outputdir='.', outputext='tif', erase=False):
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
    files = glob.glob(files)

    # wrong ! to be improved
    nb_images = len(files) * 200
    if nb_images == 0:
        return
    format_index = ':0{}d'.format(int(ceil(log10(nb_images))))

    index_im = 0
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    for path_tiff in files:
        t_start = time.time()
        print('Convert and save file\n' +
              path_tiff + '\nin directory\n' + outputdir)
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                except EOFError:
                    break
                else:
                    if index_im % 2 == 0:
                        letter = 'a'
                    else:
                        letter = 'b'
                    base_path = (
                        outputdir +
                        ('/im{' + format_index + '}').format(index_im//2) +
                        letter)
                    if _save_new_file(im, base_path, outputext, erase):
                        print('\r file {}; in {:.2f} s'.format(
                            index_im, time.time() - t_start), end='')
                        sys.stdout.flush()
                    index_im += 1
                    index_im_in_tiff += 1

        print('\nEnd convert file {} in {} s'.format(
            os.path.split(path_tiff)[0], time.time() - t_start))
        sys.stdout.flush()
