"""
Multitiff
=========


"""
from __future__ import print_function

import sys
import time
import os
import glob
from math import ceil, log10

from PIL import Image

from fluiddyn.util.query import query_yes_no


def _should_we_stop():
    if query_yes_no('Some folders already exist\n Do you want to continue?'):
        return False
    return True


def _save_new_file(im, base_path, outputext, erase=False):
    path_save = base_path + '.' + outputext
    if not erase and os.path.exists(path_save):
        return
    if outputext == 'jp2':
        with im.convert(mode='L') as new_im:
            new_im.save(path_save,
                        quality_mode='rate', quality_layers=[8])
    else:
        with im.convert(mode='I') as new_im:
            new_im.save(path_save)


def reorganize_single_frame_3Dscannedpiv_data(files, nb_levels, outputdir='.',
                                              outputext='tif', erase=False):
    """
    Reorganize data from multi tiff to a hierarchy of folders for each level

    Parameters
    ----------

    - files : root of the names of files: example files = 'van_karman_flow*'
    - nb_levels: number of levels in the scanned PIV
    - outputdir = '.': output folder
    - outputext : the output files extension

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

    index_im = 0

    dir_exists = False
    
    for ind in range(nb_levels):
        if os.path.exists(outputdir + '/level{}'.format(ind)):
            dir_exists = True
        else:
            os.makedirs(outputdir + '/level{}'.format(ind))

    for path_tiff in files:
        t_start = time.time()
        print('Convert and save file\n' +
              path_tiff + '\nin directory\n' + outputdir)
        with Image.open(path_tiff) as im:
            index_im_in_tiff = 0
            while True:
                try:
                    im.seek(index_im_in_tiff)
                    print('\r file {}; in {:.2f} s'.format(
                        index_im, time.time() - t_start), end='')
                    sys.stdout.flush()
                    base_path = (outputdir + '/level{}/im{}').format(
                        index_im % nb_levels, index_im/nb_levels)
                    _save_new_file(im, base_path, outputext)
                    index_im += 1
                    index_im_in_tiff +=1
                except EOFError:
                    break


def reorganize_double_frame_3Dscannedpiv_data(
        files, nb_levels, outputdir='.', outputext='tif', erase=False):
    """
    Reorganize data from multi tiff to a hierarchy of folders for each level

    Parameters
    ----------

    - files : root of the names of files: example files = 'van_karman_flow*'
    - nb_levels: number of levels in the scanned PIV
    - outputdir = '.': output folder
    - outputext : the output files extension

    Notes
    -----

    Data is organize as:
    - outputdir/level1/im0a.tif,
      outputdir/level1/im0b.tif,
      outputdir/level1/im1a.tif ...
      outputdir/level2/im0a.tif,
      outputdir/level2/im0b.tif,
      outputdir/level2/im1a.tif ...

    """
    files = glob.glob(files)
    n = 0
    isfolder = 0

    for ind in range(nb_levels):
        try:
            os.stat(outputdir + '/level{}'.format(ind+1))
            isfolder += 1
        except:
            os.makedirs(outputdir + '/level{}'.format(ind+1))

    if not erase and isfolder:
        resp = raw_input(
            'Some folders already exist\n Do you want to continue? (y/n)')
        if resp == "y":
            pass
        else:
            return None

    for fic in files:
        im = Image.open(fic)
        nf = 0
        while True:
            try:
                im.seek(nf)
                if (n/nb_levels) % 2 == 0:
                    name = outputdir + '/level{}/im{}a'.format(
                        n % nb_levels + 1, n/(2*nb_levels))
                else:
                    name = outputdir + '/level{}/im{}b'.format(
                        n % nb_levels + 1, n/(2*nb_levels))
                im2 = im.convert(mode='I')
                im2.save(name + '.' + outputext)
                im2.close()
                nf +=1
                n += 1

            except:
                break
            im.close()


def reorganize_single_frame_2Dpiv_data(
        files, outputdir='.', outputext='tif', erase=False):
    """
    Reorganize data from multi tiff to a hierarchy of folders for each level

    Parameters
    ----------

    - files : root of the names of files: example files = 'van_karman_flow*'
    - outputdir = '.': output folder
    - outputext : the output files extension

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
    dir_exists = False
    if os.path.exists(outputdir):
        dir_exists = True
    else:
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
                    print('\r file {}; in {:.2f} s'.format(
                        index_im, time.time() - t_start), end='')
                    sys.stdout.flush()
                    base_path = (
                        outputdir +
                        ('/im{' + format_index + '}').format(index_im))
                    _save_new_file(im, base_path, outputext)
                    index_im += 1
                    index_im_in_tiff += 1
                except EOFError:
                    break
        print('\nEnd convert file {} in {} s'.format(
            os.path.split(path_tiff)[0], time.time() - t_start))
        sys.stdout.flush()

def reorganize_double_frame_2Dpiv_data(
        files, outputdir='.', outputext='tif', erase=False):
    """
    Reorganize data from multi tiff to a hierarchy of folders for each level

    Parameters
    ----------
    - files : root of the names of files: example files = 'van_karman_flow*'
    - outputdir = '.': output folder
    - outputext : the output files extension

    Notes
    -----

    Data is organize as:
    - outputdir/im0a.tif, outputdir/im0b.tif, outputdir/im1a.tif ...

    """
    files = glob.glob(files)
    n = 0
    isfolder = 0

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(
        files[0])
    t = time.gmtime(mtime)

    outputdir += ('_' + str(t.tm_year) + '-' + str(t.tm_mday) +
                  '-' + str(t.tm_hour))

    try:
        os.stat(outputdir)
        isfolder += 1
    except:
        os.makedirs(outputdir)

    if not erase and isfolder:
        resp = raw_input(
            'Some folders already exist\n Do you want to continue? (y/n)')
        if resp == 'y':
            pass
        else:
            return None

    for fic in files:
        im = Image.open(fic)
        nf = 0
        while True:
            try:
                im.seek(nf)
                if n % 2:
                    name = outputdir + '/im{}a'.format(n/2)
                else:
                    name = outputdir + '/im{}b'.format(n/2)
                im2 = im.convert(mode='I')
                im2.save(name + '.' + outputext)
                im2.close()
                n += 1
                nf +=1

            except:
                break
            im.close()
