"""
IO for Digiflow files (:mod:`fluiddyn.io.digiflow`)
===================================================

.. currentmodule:: fluiddyn.io.digiflow

Provides the classes :class:`DigiflowImage` and :class:`DigiflowMovie`.

.. autoclass:: DigiflowImage
   :members:

.. autoclass:: DigiflowMovie
   :members:

"""

from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt

from fluiddyn.io.binary import BinFile
from fluiddyn.util import Params

ddatatypes = {
    0x1001: '8 bit image',
    0x11001: '8 bit multi-plane image',
    0x12001: 'Compressed 8 bit image',
    0x1004: '32 bit image',
    0x11004: '32 bit multi-plane image',
    0x12004: 'Compressed 32 bit image',
    0x1008: '64 bit image',
    0x11008: '64 bit multi-plane image',
    0x12008: 'Compressed 64 bit image',
    0x1014: '32 bit range',
    0x1018: '64 bit range',
    0x1100: 'Rescale image',
    0x1101: 'Rescale image rectangle',
    0x2000: 'Colour scheme',
    0x2001: 'Colour scheme name',
    0x2003: 'Colour scheme name variable',
    0x3000: 'Description',
    0x3001: 'User comments',
    0x3002: 'Creating process',
    0x3003: 'Creator details',
    0x3018: 'Image time',
    0x4008: 'Image coordinates',
    0x4108: 'Image plane details'}

keys_image = [
    '8 bit image',
    '8 bit multi-plane image',
    'Compressed 8 bit image',
    '32 bit image',
    '32 bit multi-plane image',
    'Compressed 32 bit image',
    '64 bit image',
    '64 bit multi-plane image',
    'Compressed 64 bit image']


class DigiflowImage(object):
    """A digiflow image (.dfi, "image" containing 3 scalar fields).


    """
    def __init__(self, path_file=None):

        if path_file is not None:
            self.path_file = path_file
            self._load()

    def _load(self):
        """Loads the file."""

        with BinFile(self.path_file) as f:
            # header of the file:
            id_format = f.readt(32, 's')
            version = f.readt(1, 'I')

            if id_format != 'Tagged floating point image file':
                raise ValueError(
                    'This file does not seem to be a valid dfi file.')

            self.dict_infos = {}
            self._datatype_codes = []
            while self._read_one_field(f):
                pass

    def _read_one_field(self, f):
        """Read one field in the file `f`."""
        # tag for one field
        datatype_code = f.readt(1, 'uint32')
        if datatype_code == 'eof':
            # All the file has been read.
            return False
        self._datatype_codes.append(datatype_code)
        nbytes = f.readt(1, 'uint32')

        datatype = ddatatypes[datatype_code]
        # print(datatype)

        if datatype in keys_image:
            self._read_one_image(datatype, nbytes, f)

        elif datatype == '32 bit range':
            assert nbytes == 8
            r_black, r_white = f.readt(2, 'float32')
            self.range_data = np.array([r_black, r_white])

        elif datatype == '64 bit range':
            assert nbytes == 16
            r_black, r_white = f.readt(2, 'float64')
            self.range_data = np.array([r_black, r_white])

        elif datatype == 'Rescale image':
            print(datatype, 'not yet written')

        elif datatype == 'Rescale image rectangle':
            assert nbytes == 32
            self.rectangle_rescaleim = Params()
            r = self.rectangle_rescaleim
            (r.nxwant, r.nywant, r.method, r.userectangle,
             r.xmin, r.ymin, r.xmax, r.ymax) = f.readt(8, 'uint32')

        elif datatype == 'Colour scheme':
            assert nbytes == 3*256*1
            self.colours = np.array(f.readt(3*256, 'uint8')).reshape([3, 256])

        elif datatype == 'Colour scheme name':
            print(datatype, 'not yet written')

        elif datatype == 'Colour scheme name variable':
            print(datatype, 'not yet written')

        elif datatype == 'Description':
            assert nbytes == 512
            self.dict_infos[datatype] = f.readt(512, 's')

        elif datatype in ['User comments', 'Creating process']:
            nb_bytes_descrition = f.readt(1, 'uint32')
            assert nbytes == nb_bytes_descrition+4
            self.dict_infos[datatype] = f.readt(nb_bytes_descrition, 's')

        elif datatype == 'Creator details':
            assert nbytes == 64+48+32*5+16*2
            self.dict_infos['DigiFlow'] = f.readt(32, 's')
            self.dict_infos['buildDate'] = f.readt(16, 's')
            self.dict_infos['licenceType'] = f.readt(16, 's')
            self.dict_infos['nameUser'] = f.readt(32, 's')
            self.dict_infos['nameComputer'] = f.readt(32, 's')
            self.dict_infos['nameDomain'] = f.readt(32, 's')
            self.dict_infos['guidUser'] = f.readt(32, 's')
            self.dict_infos['macAddress'] = f.readt(48, 's')
            self.dict_infos['ipAddress'] = f.readt(64, 's')

        elif datatype == 'Image time':
            assert nbytes == 32
            self.times = Params()
            t = self.times
            t.iframe, t.reserved = f.readt(2, 'uint32')
            t.time, t.tstep, t.tfirst = f.readt(3, 'float64')

        elif datatype == 'Image coordinates':
            assert nbytes == 132
            self.coordinates = Params()
            c = self.coordinates
            c.kind = f.readt(1, 'uint32')
            xworldperpixel, yworldperpixel, xoriginworld, yoriginworld = \
                f.readt(4, 'float64')
            c.worldsperpixel = np.array([xworldperpixel, yworldperpixel])
            c.origins_world = np.array([xoriginworld, yoriginworld])
            c.xunits = f.readt(16, 's')
            c.yunits = f.readt(16, 's')
            c.original_name = f.readt(64, 's')

        elif datatype == 'Image plane details':
            nplanes = f.readt(1, 'uint32')
            assert nbytes == 100*nplanes+4
            self.infos_planes = Params()
            infop = self.infos_planes
            infop.codes = []
            infop.keys = []
            infop.params = []
            infop.dunno = []
            for ip in xrange(nplanes):
                infop.codes.append(int(
                    '{0:x}'.format(f.readt(1, 'uint32'))))
                infop.keys.append(f.readt(32, 's'))
                infop.params.append(list(f.readt(4, 'float64')))
                infop.dunno.append(f.readt(32, 's'))

        return True

    def _read_one_image(self, datatype, nbytes, f):
        """Reads one image."""

        nx, ny = f.readt(2, 'uint32')
        if datatype == '8 bit image':
            assert nbytes == nx*ny+8
            self.data = np.array(f.readt(nx*ny, 'uint8')
                                 ).reshape([1, ny, nx])

        elif datatype == '8 bit multi-plane image':
            nz = f.readt(1, 'uint32')
            assert nbytes == nx*ny*nz+12
            self.data = np.array(f.readt(nx*ny*nz, 'uint8')
                                 ).reshape([nz, ny, nx])

        elif datatype == 'Compressed 8 bit image':
            nz, size_compressed = f.readt(2, 'uint32')
            assert nbytes == size_compressed+16
            self.data = np.array(
                f.readt_zlib(size_compressed, nx*ny*nz, 'uint8')
                ).reshape([nz, ny, nx])

        elif datatype == '32 bit image':
            assert nbytes == 4*nx*ny+8
            self.data = np.array(f.readt(nx*ny, 'float32')
                                 ).reshape([1, ny, nx])

        elif datatype == '32 bit multi-plane image':
            nz = f.readt(1, 'uint32')
            assert nbytes == 4*nx*ny*nz+12
            self.data = np.array(f.readt(nx*ny*nz, 'float32')
                                 ).reshape([nz, ny, nx])

        elif datatype == 'Compressed 32 bit image':
            nz, size_compressed = f.readt(2, 'uint32')
            assert nbytes == size_compressed+16
            self.data = np.array(
                f.readt_zlib(size_compressed, nx*ny*nz, 'float32')
                ).reshape([nz, ny, nx])

        elif datatype == '64 bit image':
            assert nbytes == 8*nx*ny+8
            self.data = np.array(f.readt(nx*ny, 'float64')
                                 ).reshape([1, ny, nx])

        elif datatype == '64 bit multi-plane image':
            nz = f.readt(1, 'uint32')
            assert nbytes == 8*nx*ny*nz+12
            self.data = np.array(f.readt(nx*ny*nz, 'float64')
                                 ).reshape([nz, ny, nx])

        elif datatype == 'Compressed 64 bit image':
            nz, size_compressed = f.readt(2, 'uint32')
            assert nbytes == size_compressed+16
            self.data = np.array(
                f.readt_zlib(size_compressed, nx*ny*nz, 'float64')
                ).reshape([nz, ny, nx])

    # def save(self):
    #     print('Not yet implemented...')

    def __getitem__(self, key):
        if key not in self.infos_planes.keys:
            raise KeyError('correct keys:', self.infos_planes.keys)
        return self.data[self.infos_planes.keys.index(key)]


class DigiflowMovie(object):
    """A digiflow movie (.dfm, "movies", set of images).

    """
    def __init__(self, path_file=None):
        if path_file is not None:
            self.path_file = path_file
            self._load_info()

            self.deltat = self.movie_header['dtSampleSpacing']

    def _load_info(self):
        """Loads the file."""

        with BinFile(self.path_file) as f:
            # do not change the order of these lines!
            # do not comment one of these lines!
            self._read_file_header(f)
            self._read_hist_info(f)
            self._read_movie_header(f)

            nMovieFrames = self.movie_header['nMovieFrames']
            temp = f.readt(2*nMovieFrames, 'int64')
            temp = np.array(temp).reshape([nMovieFrames, 2])
            self.iFrameNumber = temp[:, 0]
            self.iPtrFrame = temp[:, 1]

            self.nb_frames = len(self.iFrameNumber)

    def _read_file_header(self, f):
        # header of the file:
        fileowner = f.readt(8, 's')
        version = f.readt(8, 's')
        iPtrHistory = f.readt(1, 'I')
        filetype = f.readt(16, 's')
        comments = f.readt(220, 's')
        d = locals()
        del(d['f'], d['self'])
        self.file_header = d

    def _read_hist_info(self, f):
        # History Header Information
        iPtrPrivateHeader = f.readt(1, 'I')
        iDummy = f.readt(1, 'I')
        CreatedBy = f.readt(8, 's')
        Hversion = f.readt(8, 's')
        CreatedUser = f.readt(16, 's')
        CreatedName = f.readt(64, 's')
        CreatedDate = f.readt(8, 's')
        CreatedTime = f.readt(8, 's')
        ModifiedUser = f.readt(16, 's')
        ModifiedName = f.readt(64, 's')
        ModifiedDate = f.readt(8, 's')
        ModifiedTime = f.readt(8, 's')
        UnUsed = f.readt(40, 's')
        del(UnUsed)
        d = locals()
        del(d['f'], d['self'])
        self.hist_info = d

    def _read_movie_header(self, f):
        # Movie Header Information

        (iFormatType, iFrameRate) = f.readt(2, 'uint16')
        (iSampleSpacing, iMovieDuration, iPtrFrameTable, nMovieFrames
         ) = f.readt(4, 'uint32')
        (iw0, iw1, jw0, jw1, idi, jdj) = f.readt(6, 'uint16')

        self.shape_im = [iw1-iw0+1, jw1-jw0+1]
        self.size_im = self.shape_im[0]*self.shape_im[1]

        nSize = f.readt(1, 'uint32')
        AspectRatio = f.readt(1, 'float32')

        nBits = f.readt(1, 'uint16')

        iOLUTRed = np.array(f.readt(256, 'uint8'))
        iOLUTGreen = np.array(f.readt(256, 'uint8'))
        iOLUTBlue = np.array(f.readt(256, 'uint8'))
        nFrameTableLength = f.readt(1, 'uint32')
        RecordAtFieldSpacing = f.readt(1, 'uint16')

        dtSampleSpacing = f.readt(1, 'float32')
        UnUsed = f.readt(204, 'uint8')
        del(UnUsed)

        d = locals()
        del(d['f'], d['self'])
        self.movie_header = d

    def __getitem__(self, arg):

        itstart = 0
        itstop = self.nb_frames-1
        itstep = 1

        # iystart = 0
        # iystop = self.shape_im[0]
        # iystep = 1

        # ixstart = 0
        # ixstop = self.shape_im[1]
        # ixstep = 1

        if isinstance(arg, int):
            with open(self.path_file) as f:
                f.seek(self.iPtrFrame[arg])
                return np.fromfile(
                    f, dtype=np.uint8,
                    count=self.size_im).reshape(self.shape_im)

        elif isinstance(arg, slice):
            raise NotImplementedError
            # itstart = arg.start
            # itstop = arg.stop
            # itstep = arg.step

        elif isinstance(arg, tuple):
            raise NotImplementedError
            # itstart = arg[0].start
            # itstop = arg[0].stop
            # itstep = arg[0].step

        # nb_values_between_frames = self.iPtrFrame[1] - self.iPtrFrame[0]

        # shape_ret = [nb_frames] + list(self.shape_im)
        # size_im = self.size_im
        # nb_values_to_jump_startim = 0
        # nb_values_to_jump_endim = nb_values_between_frames - size_im

        # ret = np.empty(shape_ret)

        # with BinFile(self.path_file) as f:
        #     f.seek(self.iPtrFrame[iframe_start])
        #     for iframe in xrange(nb_frames):
        #         # temp = np.array(f.readt(self.size_im, 'uint8'))
        #         # ret[iframe].flat = temp#.reshape(self.shape_im)
        #         f.seek(nb_values_to_jump_startim, 1)
        #         ret[iframe].flat = f.readt(size_im, 'uint8')
        #         f.seek(nb_values_to_jump_endim, 1)

        # if nb_frames == 1:
        #     return ret[0]
        # else:
        #     return ret

    # def load_contiguous_frames2(self, iframe_start, nb_frames=1):

    #     if iframe_start+1 > self.nb_frames:
    #         raise ValueError('A non excisting frame has been asked.')

    #     if iframe_start+nb_frames > self.nb_frames:
    #         print('too many frames asked...')
    #         nb_frames = self.nb_frames - iframe_start

    #     ret = np.empty([nb_frames]+list(self.shape_im))

    #     if self.nb_frames > 1:
    #         nb_values_between_frames = self.iPtrFrame[1] - self.iPtrFrame[0]
    #     else:
    #         nb_values_between_frames = self.size_im

    #     with BinFile(self.path_file) as f:
    #         f.seek(self.iPtrFrame[iframe_start])
    #         temp = f.readt(nb_frames*nb_values_between_frames, 'uint8')

    #     for iframe in xrange(nb_frames):
    #         istart = iframe*nb_values_between_frames
    #         temp2 = np.array(temp[istart:istart+self.size_im])
    #         ret[iframe] = temp2.reshape(self.shape_im)

    #     if nb_frames == 1:
    #         return ret[0]
    #     else:
    #         return ret

    def load_contiguous_frames(self, iframe_start, nb_frames=1):

        if iframe_start+1 > self.nb_frames:
            raise ValueError('A non-existing frame has been asked.')

        if iframe_start+nb_frames > self.nb_frames:
            print('too many frames asked...')
            nb_frames = self.nb_frames - iframe_start

        ret = np.empty([nb_frames] + list(self.shape_im))

        if self.nb_frames > 1:
            nb_values_to_jump = (
                self.iPtrFrame[1] - self.iPtrFrame[0] - self.size_im)
        else:
            nb_values_to_jump = 0

        # with BinFile(self.path_file) as f:
        #     f.seek(self.iPtrFrame[iframe_start])
        #     for iframe in xrange(nb_frames):
        #         # ret[iframe].flat = f.readt(self.size_im, 'uint8')
        #         ret[iframe].flat = np.fromfile(
        #             f, dtype=np.uint8, count=self.size_im)
        #         f.seek(nb_values_to_jump, 1)

        with open(self.path_file, 'rb') as f:
            f.seek(self.iPtrFrame[iframe_start])
            for iframe in xrange(nb_frames):
                # ret[iframe].flat = f.readt(self.size_im, 'uint8')
                ret[iframe].flat = np.fromfile(
                    f, dtype=np.uint8, count=self.size_im)
                f.seek(nb_values_to_jump, 1)


        if nb_frames == 1:
            return ret[0]
        else:
            return ret

    def _test_end_of_file(self, i):
        "Seems to reach eof if i > 275 but why ?"
        with BinFile(self.path_file) as f:
            f.seek(self.iPtrFrame[-1])
            im = f.readt(self.size_im, 'uint8')

            print('last values in last image:\n', im[-10:])
            print('after the last values:\n', f.readt(i, 'uint8'))

    def show_movie(self, i_start, i_stop, i_step=1, fps=4, decimate=4):
        plt.ion()
        fig = plt.figure()
        ax = plt.gca()

        data = self[i_start]
        if decimate > 1:
            data = data[::decimate, ::decimate]

        quadmesh = ax.pcolormesh(data)
        quadmesh.set_clim([0., 255.])

        ax.set_xlim([0, data.shape[1]])
        ax.set_ylim([0, data.shape[0]])

        for i in range(i_start+i_step, i_stop, i_step):
            with open(self.path_file) as f:
                f.seek(self.iPtrFrame[i])
                data = np.fromfile(
                    f, dtype=np.uint8,
                    count=self.size_im).reshape(self.shape_im)

                if decimate > 1:
                    data = data[::decimate, ::decimate]

            quadmesh.set_array(data.ravel())
            fig.canvas.draw()

    def plot_image(self, i_image, decimate=1, clim=None, cmap=None):
        plt.ion()
        plt.figure()
        ax = plt.gca()

        data = self[i_image]
        if decimate > 1:
            data = data[::decimate, ::decimate]

        # if cmap is None:
        #     cmap = plt.cm.hsv

        quadmesh = ax.pcolormesh(data, cmap=cmap, shading='flat')

        if clim is not None:
            quadmesh.set_clim(clim)

        ax.set_xlim([0, data.shape[1]])
        ax.set_ylim([0, data.shape[0]])

        plt.show()

    def make_time_serie(self, i_start, i_stop, i_x, i_step=1,
                        has_to_plot=True, cmap=None):

        if i_stop > self.nb_frames - 1:
            i_stop = self.nb_frames - 1

        inds_t = range(i_start, i_stop+1, i_step)

        time_serie = np.zeros([self.shape_im[0], len(inds_t)])

        for it in inds_t:
            a = self[it]
            time_serie[:, it] = a[:, i_x]

        if has_to_plot:
            plt.ion()
            plt.figure()
            ax = plt.gca()
            ax.pcolormesh(time_serie, cmap=cmap, shading='flat')
            plt.show()

        return time_serie


    # def save(self):
    #     pass


def plot_im(im):
    import fluiddyn.figs as figs

    import matplotlib.pyplot as plt

    figures = figs.Figures(
        hastosave=False, for_beamer=False, fontsize=20)
    size_axe = [0.15, 0.12, 0.8, 0.76]

    fig = figures.new_figure(
        name_file='fig_im',
        fig_width_mm=170, fig_height_mm=220,
        size_axe=size_axe)

    ax1 = fig.gca()

    ax1.set_xlabel(r'$x$ (pixels)')
    ax1.set_ylabel(r'$z$ (pixels)')

    pc = ax1.pcolormesh(im, cmap=plt.cm.hsv, shading='flat')

    fig.colorbar(pc)

    ax1.set_xlim([0, im.shape[1]])
    ax1.set_ylim([0, im.shape[0]])

    figs.show()


if __name__ == '__main__':

    path_file = (
        '/home/pa371/Data_reasons_pa371/Dropbox'
        '/Strat_inclined_duct/Decomposition/Data_exp/Exp_m7'
        '/clean_m7_lif3_0036.dfi'
        )

    print(path_file)
    dfi = DigiflowImage(path_file)

    plot_im(dfi.data[0])

    # dfm = DigiflowMovie(path_file)
    # im = dfm.load_contiguous_frames(10, nb_frames=3)
