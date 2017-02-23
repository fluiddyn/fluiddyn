from __future__ import print_function
import os
import numpy as np

try:
    from PIL import Image
except ImportError:
    pass
try:
    from cv2 import imread as _imread, IMREAD_ANYDEPTH
    use_opencv = True
except ImportError:
    use_opencv = False
    try:
        from scipy.ndimage import imread as _imread
    except ImportError:
        from scipy.misc import imread as _imread

from .hdf5 import H5File


__all__ = ['imread', 'imsave', 'imread_h5', 'imsave_h5']


def imread(path, *args, **kwargs):
    """Wrapper for OpenCV/SciPy imread functions."""
    if use_opencv:
        return _imread(path, IMREAD_ANYDEPTH)
    else:
        return _imread(path, *args, **kwargs)


def imsave(path, array, format=None, as_int=False):
    """
    Alternative implementation of `scipy.misc.imsave` function.
    Detects a compatible format based on the array dtype, rather than relying
    on the file extension.

    .. WARNING: setting `as_int=True` might lead to loss of precision.

    """
    if as_int:
        if array.max() < 256:
            mode = 'L'
            dtype = np.uint8
        else:
            mode = 'I'
            dtype = np.uint32

        array = array.astype(dtype)
    else:
        dtype = array.dtype
        if np.issubdtype(dtype, np.floating):
            mode = 'F'
        elif np.issubdtype(dtype, np.uint8):
            mode = 'L'
        elif np.issubdtype(dtype, np.integer):
            mode = 'I'
        else:
            raise NotImplementedError('Unexpected dtype %s' % dtype)

    # im = toimage(arr=array, mode=mode, channel_axis=2)

    im = Image.fromarray(array, mode)

    if format is None:
        if mode == 'F' or \
           any([path.endswith(ext) for ext in ('.tif', '.tiff')]):
            format = 'TIFF'
        else:
            format = 'PNG'

    if format == 'TIFF':
        if not any([path.endswith(ext) for ext in ('.tif', '.tiff')]):
            path += '.tiff'
    elif format == 'PNG':
        if not any([path.endswith(ext) for ext in ('.png', '.PNG')]):
            if path.endswith('.tif'):
                path = path[:-len('.tif')]
            if path.endswith('.tiff'):
                path = path[:-len('.tiff')]
            path += '.png'

    im.save(path, format)


def imread_h5(path):
    """Read image(s) stored in a HDF5 file."""

    with ImageH5File(path, 'r') as f:
        return f.load(group='images')


def imsave_h5(path, array, params=None, attrs={}, compression='gzip',
              as_int=False):
    """Saves an image as a compressed HDF5 file."""

    fname = os.path.basename(path)
    root, ext = os.path.splitext(path)
    h5path = root + '.h5'

    if as_int:
        if array.max() < 256:
            dtype = np.uint8
        else:
            dtype = np.uint32

        array = array.astype(dtype)

    with ImageH5File(h5path, 'w') as f:
        f.save_dict('images', {fname: array},
                    compression=compression, shuffle=True)
        f.save_attrs(attrs)
        if params is not None:
            params._save_as_hdf5(hdf5_parent=f)


class ImageH5File(H5File):

    def __init__(self, *args, **kwargs):
        super(ImageH5File, self).__init__(*args, **kwargs)

    def load(self, group):
        """Load images in the HDF5 file."""

        images = self[group]
        nb_images = len(images)
        if nb_images == 1:
            dset = list(images.items())[0][1]
            return dset[...]
        else:
            dico = {}
            for k, v in images.items():
                dico[k] = v[...]

            return dico

    def save_attrs(self, dictattrs):
        """Save the `dictattrs` as attributes."""

        for k, v in list(dictattrs.items()):
            self.attrs[k] = v

    def save_dict(self, keydict, dicttosave, **kwargs):
        """Save the dictionary `dicttosave` in the file."""

        group = self.create_group(keydict)

        if len(dicttosave) > 0:
            for k, v in list(dicttosave.items()):
                group.create_dataset(k, data=v, **kwargs)
