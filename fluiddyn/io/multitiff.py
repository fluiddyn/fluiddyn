# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:25:20 2016

@author: campagne8a
"""
from PIL import Image
import time
import os
import glob

def reorganize_single_frame_3Dscannedpiv_data(
        files, Nlevel, outputdir = '.',
        outputext = 'tif', erase=False):
    """
    Reorganize data from multi tiff to a hierarchy of folders for each level

    INPUT:
        - files : root of the names of files: example files = 'van_karman_flow*'
        - Nlevel: number of levels in the scanned PIV
        - outputdir = '.': output folder
        - outputext : the output files extension

    Data is organize as:
        - outputdir/level1/im0.tif, outputdir/level1/im1.tif ...
        - outputdir/level2/im0.tif, outputdir/level2/im1.tif ...

    """


    files = glob.glob(files)
    n = 0

    isfolder = 0

    for ind in range(Nlevel):
        try:
            os.stat(outputdir + '/level{}'.format(ind+1))
            isfolder += 1
        except:
            os.makedirs(outputdir + '/level{}'.format(ind+1))

    if not erase and isfolder !=0:
        resp = raw_input("Some folders already exist\n Do you want to continue? (y/n)")
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
                name = outputdir + '/level{}/im{}'.format(n%Nlevel+1,n/Nlevel)
                im2 = im.convert(mode='I')
                im2.save(name + '.' + outputext)
                im2.close()
                n += 1
                nf +=1

            except:
                break
            im.close()

def reorganize_double_frame_3Dscannedpiv_data(files, Nlevel, outputdir = '.',
                                              outputext = 'tif', erase=False):
    """
    Reorganize data from multi tiff to a hierarchy of folders for each level

    INPUT:
        - files : root of the names of files: example files = 'van_karman_flow*'
        - Nlevel: number of levels in the scanned PIV
        - outputdir = '.': output folder
        - outputext : the output files extension

    Data is organize as:
        - outputdir/level1/im0a.tif, outputdir/level1/im0b.tif, outputdir/level1/im1a.tif ...
        - outputdir/level2/im0a.tif, outputdir/level2/im0b.tif, outputdir/level2/im1a.tif ...

    """
    files = glob.glob(files)
    n = 0
    isfolder = 0

    for ind in range(Nlevel):
        try:
            os.stat(outputdir + '/level{}'.format(ind+1))
            isfolder +=1
        except:
            os.makedirs(outputdir + '/level{}'.format(ind+1))

    if not erase and isfolder:
        resp = raw_input("Some folders already exist\n Do you want to continue? (y/n)")
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
                if (n/Nlevel)%2 == 0:
                    name = outputdir + '/level{}/im{}a'.format(n%Nlevel+1,n/(2*Nlevel))
                else:
                    name = outputdir + '/level{}/im{}b'.format(n%Nlevel+1,n/(2*Nlevel))
                im2 = im.convert(mode='I')
                im2.save(name + '.' + outputext)
                im2.close()
                nf +=1
                n += 1

            except:
                break
            im.close()

def reorganize_single_frame_2Dpiv_data(files,  outputdir = '.',
                                       outputext = 'tif', erase=False):
    """
    Reorganize data from multi tiff to a hierarchy of folders for each level

    INPUT:
        - files : root of the names of files: example files = 'van_karman_flow*'
        - outputdir = '.': output folder
        - outputext : the output files extension

    Data is organize as:
        - outputdir/im0.tif, outputdir/im1.tif ...

    """
    files = glob.glob(files)
    n = 0
    isfolder = 0

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(files[0])
    t = time.gmtime(mtime)

    outputdir += '_' + str(t.tm_year) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour)

    try:
        os.stat(outputdir)
        isfolder +=1
    except:
        os.makedirs(outputdir)

    if not erase and isfolder:
        resp = raw_input("Some folders already exist\n Do you want to continue? (y/n)")
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
                name = outputdir + '/im{}'.format(n)
                im2 = im.convert(mode='I')
                im2.save(name + '.' + outputext)
                im2.close()
                n += 1
                nf +=1

            except:
                break
            im.close()


def reorganize_double_frame_2Dpiv_data(files,  outputdir = '.',
                                     outputext = 'tif', erase=False):
    """
    Reorganize data from multi tiff to a hierarchy of folders for each level

    INPUT:
        - files : root of the names of files: example files = 'van_karman_flow*'
        - outputdir = '.': output folder
        - outputext : the output files extension

    Data is organize as:
        - outputdir/im0a.tif, outputdir/im0b.tif, outputdir/im1a.tif ...

    """
    files = glob.glob(files)
    n = 0
    isfolder = 0

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(files[0])
    t = time.gmtime(mtime)

    outputdir += '_' + str(t.tm_year) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour)

    try:
        os.stat(outputdir)
        isfolder +=1
    except:
        os.makedirs(outputdir)

    if not erase and isfolder:
        resp = raw_input("Some folders already exist\n Do you want to continue? (y/n)")
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
                if n%2:
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
