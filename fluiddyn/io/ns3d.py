"""
IO for NS3D files (:mod:`fluiddyn.io.ns3d`)
===================================================

.. currentmodule:: fluiddyn.io.ns3d

Provides the classes :class:`NS3DFieldFile`.

.. autoclass:: NS3DFieldFile
   :members:

"""

from __future__ import division, print_function

import sys

import numpy as np

from fluiddyn.io.binary import BinFile


def print_with_emptyend(s):
    print(s, end='')
    sys.stdout.flush()


class NS3DFile(object):
    """Fields in a NS3D binary file."""

    def __init__(self, path_file=None):

        if path_file is not None:
            self.path_file = path_file
            self.byteorder = self._get_byte_order()
            self._read_header()

    def _get_byte_order(self):
        with BinFile(self.path_file, byteorder='little') as f:
            trash, flag = f.readt(2, 'I')
        if flag == 1:
            return 'little'

        with BinFile(self.path_file, byteorder='big') as f:
            trash, flag = f.readt(2, 'I')
        if flag == 1:
            return 'big'
        else:
            raise ValueError('This file does not look like a ns3d file.')


class NS3DFieldFile(NS3DFile):
    """Fields in a NS3D binary file."""
    nb_bytes_header = 148

    def _read_header(self):
        """Read the header of the file."""

        with BinFile(self.path_file, byteorder=self.byteorder) as f:
            trash, flag, self.nx, self.ny, self.nz = f.readt(5, 'uint32')
            self.lx, self.ly, self.lz, self.dt = f.readt(4, 'float64')

            self.truncate, self.type_trunc = f.readt(2, 'uint32')
            (self.rtrunc_x, self.rtrunc_y, self.rtrunc_z,
             self.nu) = f.readt(4, 'float64')

            self.stratification = f.readt(1, 'uint32')
            self.N, self.schm, self.omega2 = f.readt(3, 'float64')

            self.perturb, self.lin, trash, trash = f.readt(4, 'uint32')

            self.time = f.readt(1, 'float64')

        self.shape = (self.nx, self.ny, self.nz)
        if not self.stratification:
            self.N == 0

        self.Re = np.round(1./self.nu, decimals=2)
        self.Fh = np.round(1./self.N, decimals=4)

    def read_field(self, ifield=0):
        nb_pts_one_field = self.nx*self.ny*self.nz
        field = np.empty([self.nz, self.ny, self.nx])
        with BinFile(self.path_file, byteorder=self.byteorder) as f:
            f.seek(self.nb_bytes_header + ifield*(nb_pts_one_field+1)*8 + 4)
            for iz in range(self.nz):
                field[iz] = np.array(
                    f.readt(self.nx*self.ny, 'float64')).reshape(
                        [self.ny, self.nx])
        return field

    def read_xy(self, ifield=0, iz=0):

        nb_pts_one_field = self.nx*self.ny*self.nz

        with BinFile(self.path_file, byteorder=self.byteorder) as f:
            f.seek(self.nb_bytes_header + ifield*(nb_pts_one_field+1)*8
                   + 4 + self.nx*self.ny*iz*8)
            field = np.array(f.readt(self.nx*self.ny, 'float64'))

        return field.reshape([self.ny, self.nx])

    def save_with_byteorder_changed(self):

        if self.byteorder.startswith('little'):
            newbyteorder = 'big'
        elif self.byteorder.startswith('big'):
            newbyteorder = 'little'
        else:
            raise ValueError('byteorder should start with little or big.')

        new_path = self.path_file + '_' + newbyteorder + '-endian'

        nb_pts = self.nx*self.ny*self.nz

        with BinFile(new_path, 'w', byteorder=newbyteorder) as f:
            # write the header
            f.write_as([124, 1, self.nx, self.ny, self.nz], 'uint32')
            f.write_as([self.lx, self.ly, self.lz, self.dt], 'float64')
            f.write_as([self.truncate, self.type_trunc], 'uint32')
            f.write_as([self.rtrunc_x, self.rtrunc_y, self.rtrunc_z, self.nu],
                       'float64')
            f.write_as(self.stratification, 'uint32')
            f.write_as([self.N, self.schm, self.omega2], 'float64')
            f.write_as([self.perturb, self.lin, 124], 'uint32')
            # write the time
            f.write_as(8, 'uint32')
            f.write_as(self.time, 'float64')
            f.write_as(8, 'uint32')
            # write the 6 fields
            for ifield in range(7):
                field = self.read_field(ifield)
                f.write_as(nb_pts, 'uint32')
                f.write_as(field.flatten(), 'float64')
                f.write_as(nb_pts, 'uint32')

        print('New file saved:\n' + new_path)

    def save_with_resol_changed(self, nx_new, ny_new, nz_new):

        from fluiddyn.simul.operators.fft import easypyfft
        print_with_emptyend('init. FFTW3DReal2Complex for input file...')
        op = easypyfft.FFTW3DReal2Complex(self.nx, self.ny, self.nz)
        print(' Done.')
        print_with_emptyend('init. FFTW3DReal2Complex for output file...')
        op_new = easypyfft.FFTW3DReal2Complex(nx_new, ny_new, nz_new)
        print(' Done.')

        new_path = self.path_file + '_{}x{}x{}'.format(nx_new, ny_new, nz_new)

        nb_pts = nx_new*ny_new*nz_new

        with BinFile(new_path, 'w', byteorder=self.byteorder) as f:
            # write the header
            f.write_as([124, 1, nx_new, ny_new, nz_new], 'uint32')
            f.write_as([self.lx, self.ly, self.lz, self.dt], 'float64')
            f.write_as([self.truncate, self.type_trunc], 'uint32')
            f.write_as([self.rtrunc_x, self.rtrunc_y, self.rtrunc_z, self.nu],
                       'float64')
            f.write_as(self.stratification, 'uint32')
            f.write_as([self.N, self.schm, self.omega2], 'float64')
            f.write_as([self.perturb, self.lin, 124], 'uint32')
            # write the time
            f.write_as(8, 'uint32')
            f.write_as(self.time, 'float64')
            f.write_as(8, 'uint32')
            # write the 4 fields
            for ifield in range(4):
                print('treat field {} (over 4)'.format(ifield))
                print_with_emptyend('    read_field...')
                field = self.read_field(ifield)
                print_with_emptyend(' Done.\n    _compute_field_new_resol...')
                field_new = self._compute_field_new_resol(
                    field, op, op_new)
                del(field)
                print_with_emptyend(
                    ' Done.\n    write the array in the new file...')
                f.write_as(nb_pts, 'uint32')
                f.write_as(field_new.flat, 'float64')
                del(field_new)
                print(' Done.')
                f.write_as(nb_pts, 'uint32')

        print('New file saved:\n' + new_path)

    def _compute_field_new_resol(self, field, op, op_new):

        nz_new, ny_new, nx_new = op_new.shapeK

        nx_min = min(self.nx, nx_new)
        ny_min = min(self.ny, ny_new)
        nz_min = min(self.nz, nz_new)

        f_Fourier = op.fft3d(field)
        f_Fourier_new = np.zeros(op_new.shapeK, dtype=np.complex128)

        nkx = nx_min//2+1
        # for z and y, we take advantage of the "from the end" Python
        # index notation:
        for iz in [0, nz_min//2]:
            for iy in [0, ny_min//2]:
                for ix in range(nkx):
                    f_Fourier_new[iz, iy, ix] = f_Fourier[iz, iy, ix]
            for iy in range(1, ny_min//2):
                for ix in range(nkx):
                    f_Fourier_new[iz, iy, ix] = f_Fourier[iz, iy, ix]
                    f_Fourier_new[iz, -iy, ix] = f_Fourier[iz, -iy, ix]
        for iz in range(1, nz_min//2):
            for iy in [0, ny_min//2]:
                for ix in range(nkx):
                    f_Fourier_new[iz, iy, ix] = f_Fourier[iz, iy, ix]
                    f_Fourier_new[-iz, iy, ix] = f_Fourier[-iz, iy, ix]
            for iy in range(1, ny_min//2):
                for ix in range(nkx):
                    f_Fourier_new[iz, iy, ix] = f_Fourier[iz, iy, ix]
                    f_Fourier_new[iz, -iy, ix] = f_Fourier[iz, -iy, ix]
                    f_Fourier_new[-iz, iy, ix] = f_Fourier[-iz, iy, ix]
                    f_Fourier_new[-iz, -iy, ix] = f_Fourier[-iz, -iy, ix]

        return op_new.ifft3d(f_Fourier_new)


class NS3DForcingInfoFile(NS3DFile):
    """Information on forcing NS3D binary file."""

    def _read_header(self):
        """Read the header of the file."""

        with BinFile(self.path_file, byteorder=self.byteorder) as f:
            trash, flag = f.readt(2, 'uint32')
            self.lx, self.ly, self.Delta_t = f.readt(3, 'float64')
            (self.nb_fields, self.nb_Delta_t, self.nkx, self.nky,
             trash, trash2) = f.readt(6, 'uint32')
            self.vec_ind_field = f.readt(self.nb_Delta_t, 'uint32')

    def save_with_byteorder_changed(self):

        if self.byteorder.startswith('little'):
            newbyteorder = 'big'
        elif self.byteorder.startswith('big'):
            newbyteorder = 'little'
        else:
            raise ValueError('byteorder should start with little or big.')

        new_path = self.path_file + '_' + newbyteorder + '-endian'

        with BinFile(new_path, 'w', byteorder=newbyteorder) as f:
            f.write_as([44, 1], 'uint32')
            f.write_as([self.lx, self.ly, self.Delta_t], 'float64')
            f.write_as([self.nb_fields, self.nb_Delta_t, self.nkx, self.nky,
                        44, self.nb_Delta_t*4], 'uint32')
            f.write_as(self.vec_ind_field, 'uint32')
            f.write_as(self.nb_Delta_t*4, 'uint32')

        print('New file saved:\n' + new_path)


class NS3DForcingSpectralFile(object):
    """Fields in a NS3D binary file."""

    def __init__(self, path_file):
        if 'forcing_2D_spectral.in' not in path_file:
            raise ValueError(
                '"forcing_2D_spectral.in" should be in path_file.')

        base, suffix = tuple(path_file.split('forcing_2D_spectral.in'))
        path_file_info = base + 'forcing_2D_info.in' + suffix
        f_info = NS3DForcingInfoFile(path_file_info)

        self.path_file = path_file
        self.byteorder = f_info.byteorder
        self.nkx = f_info.nkx
        self.nky = f_info.nky
        self.nb_fields = f_info.nb_fields

    def read_one_forcing_field(self, iforcing):

        if iforcing < 0 or iforcing > self.nb_fields-1:
            raise ValueError('iforcing should be >=0 and <self.nb_fields-1.')

        with BinFile(self.path_file, byteorder=self.byteorder) as f:
            f.seek(3*iforcing*2*self.nkx*self.nky*8)
            tdata = f.readt(3*2*self.nkx*self.nky, 'float64')

        return tdata

    def save_with_byteorder_changed(self):

        if self.byteorder.startswith('little'):
            newbyteorder = 'big'
        elif self.byteorder.startswith('big'):
            newbyteorder = 'little'
        else:
            raise ValueError('byteorder should start with little or big.')

        new_path = self.path_file + '_' + newbyteorder + '-endian'

        with BinFile(new_path, 'w', byteorder=newbyteorder) as f:

            for iforcing in range(self.nb_fields):
                tdata = self.read_one_forcing_field(iforcing)
                f.write_as(tdata, 'float64')

        print('New file saved:\n' + new_path)


if __name__ == '__main__':

    path_dir = (
        '/home/users/augier3pi/useful/project/14LADHYX/NS3D_results_froggy/'
        'ns3d_exp_HYPER_288x288x96_L=30x30x10_'
        'nu=0.0001266_N=2.0_Tend=400_2015-01-09_19-18-52'
    )

    ff0 = NS3DFieldFile(path_file=path_dir
                        + '/velo_rho_vort.t=0400.045')

    ff1 = NS3DFieldFile(path_file=path_dir
                        + '/velo_rho_vort.t=0400.045_64x64x32')

#     ff2 = NS3DFieldFile(path_file=path_dir
#                         + '/velo_rho_vort.t=0005.010_128x128x32')

