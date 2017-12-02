"""
Read and save image files
=========================


"""



from __future__ import print_function
import os
import numpy as np

try:
    from PIL import Image
except ImportError:
    pass

try:
    from cv2 import imread as _imread_opencv, IMREAD_ANYDEPTH
    use_opencv = True
except ImportError:
    use_opencv = False
    try:
        from imageio import imread as _imread
    except ImportError:
        from matplotlib.pyplot import imread as _imread

try:
    from skimage.io import imread as _imread_ski
except ImportError:
    pass

try:
    import pims
except ImportError:
    pass

from .hdf5 import H5File


__all__ = ['imread', 'imsave', 'imread_h5', 'imsave_h5', 'extensions_movies']


extensions_movies = ['cine', 'im7']


def imread(path, *args, **kwargs):
    """Wrapper for OpenCV/SciPy imread functions."""
    if path.endswith(']'):
        path, internal_index = path.split('[')
        internal_index = int(internal_index[:-1])
        for ext in extensions_movies:
            if path.endswith('.' + ext):
                with pims.open(path) as images:
                    return images.get_frame(internal_index)

    if path.lower().endswith(('.tiff', '.tif')):
        try:
            return _imread_ski(path, *args, **kwargs)
        except NameError:
            pass

    if use_opencv:
        return _imread_opencv(path, IMREAD_ANYDEPTH)
    else:
        return _imread(path, *args, **kwargs)


def _image_from_array(array, as_int):
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
    return im


def imsave(path, array, format=None, as_int=False):
    """
    Alternative implementation of `scipy.misc.imsave` function.
    Detects a compatible format based on the array dtype, rather than relying
    on the file extension.

    .. WARNING: setting `as_int=True` might lead to loss of precision.

    """
    im = _image_from_array(array, as_int)

    if format is None:
        if im.mode == 'F' or \
           any([path.endswith(ext) for ext in ('.tif', '.tiff')]):
            format = 'TIFF'
        else:
            format = 'PNG'

    if format == 'TIFF':
        if any([path.endswith(ext) for ext in ('.png', '.PNG')]) and\
           np.issubdtype(array.dtype, np.floating):
            print('warning: can not save float image as png. '
                  'Using tif format.')

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
    im.close()


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
