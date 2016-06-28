import os
import numpy as np
from PIL import Image
try:
    from scipy.ndimage import imread
except ImportError:
    from scipy.misc import imread

from .hdf5 import H5File


__all__ = ['imread', 'imsave', 'imread_h5', 'imsave_h5']


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
        if mode == 'F':
            format = 'TIFF'
        else:
            format = 'PNG'

    im.save(path, format)


def imread_h5(path):
    """Read image(s) stored in a HDF5 file."""

    with ImageH5File(h5path, 'r') as f:
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

        images = f[group]
        nb_images = len(images)
        if nb_images == 1:
            dset = images.items()[0][1]
            return dset[...]
        else:
            dico = {}
            for k, v in images.iteritems():
                dico[k] = v[...]

            return dico

    def save_attrs(self, dictattrs):
        """Save the `dictattrs` as attributes."""

        for k, v in dictattrs.items():
            self.attrs[k] = v

    def save_dict(self, keydict, dicttosave, **kwargs):
        """Save the dictionary `dicttosave` in the file."""

        group = self.create_group(keydict)
        print(kwargs)
        if len(dicttosave) > 0:
            for k, v in dicttosave.items():
                group.create_dataset(k, data=v, **kwargs)
