"""
IO for binary files (:mod:`fluiddyn.io.binary`)
===============================================

.. currentmodule:: fluiddyn.io.binary

Provides the class :class:`BinFile`.

.. autoclass:: BinFile
   :members:


"""

from __future__ import division, print_function


import struct
import zlib
import io as _io


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def _code_byte_order_from_str(byteorder=None):
    if byteorder is None:
        return '='  # native
    elif byteorder.startswith('little'):
        return '<'  # little-endian
    elif byteorder.startswith('big'):
        return '>'  # big-endian
    else:
        raise ValueError('byteorder should start with little or big.')


class BinFile(_io.FileIO):

    dcodetypes = {
        's': 's',
        'B': 'B',
        'uint8': 'B',
        'H': 'H',
        'uint16': 'H',
        'I': 'I',
        'uint32': 'I',
        'f': 'f',
        'float32': 'f',
        'd': 'd',
        'float64': 'd',
        'q': 'q',
        'int64': 'q'}

    keys_types = dcodetypes.keys()

    def __init__(self, file_path, mode='rb', byteorder=None):
        if 'b' not in mode:
            mode += 'b'
        super(BinFile, self).__init__(file_path, mode)

        self.code_byte_order = _code_byte_order_from_str(byteorder)

    def readt(self, nb_values, codetype, byteorder=None):
        """Read some values coded in a particular type."""
        if codetype == 's':
            fmt = '{0:d}s'.format(nb_values)
            return struct.unpack(fmt, self.read(nb_values))[0].rstrip()
        elif codetype in self.keys_types:
            if byteorder is None:
                code_byte_order = self.code_byte_order
            else:
                code_byte_order = _code_byte_order_from_str(byteorder)

            fmt = (code_byte_order + '{0:d}'.format(nb_values)
                   + self.dcodetypes[codetype])
            nb_bytes = struct.calcsize(fmt)
            raw = self.read(nb_bytes)
            if len(raw) != nb_bytes:
                return 'eof'  # end of file
            else:
                t_result = struct.unpack(fmt, raw)
                if len(t_result) == 1:
                    return t_result[0]
                else:
                    return t_result
        else:
            raise ValueError('Value of codetype not yet implemented')

    def readt_zlib(self, nb_bytes, nb_values, codetype):
        """Read some value encoded with zlib."""
        if codetype in self.keys_types:
            fmt = '={0:d}'.format(nb_values)+self.dcodetypes[codetype]
            nb_bytes_decompressed = struct.calcsize(fmt)
            raw = self.read(nb_bytes)
            raw_decompressed = zlib.decompress(raw)
            if len(raw_decompressed) != nb_bytes_decompressed:
                return 'eof'  # end of file
            else:
                t_result = struct.unpack(fmt, raw_decompressed)
                if len(t_result) == 1:
                    return t_result[0]
                else:
                    return t_result
        else:
            raise ValueError('Value of codetype not yet implemented')

    def write_as(self, to_be_saved, codetype='s', byteorder=None, 
                 buffersize=1000):

        if codetype == 's':
            self.write(to_be_saved)
        elif codetype in self.keys_types:
            if byteorder is None:
                code_byte_order = self.code_byte_order
            else:
                code_byte_order = _code_byte_order_from_str(byteorder)

            if not hasattr(to_be_saved, '__len__'):
                fmt = (code_byte_order + self.dcodetypes[codetype])
                raw = struct.pack(fmt, to_be_saved)
                self.write(raw)
            else:
                fmt_to_be_formated = (code_byte_order + '{0:d}'
                                      + self.dcodetypes[codetype])
                self._write_ndarray_with_buffer(
                    to_be_saved, fmt_to_be_formated, buffersize=buffersize)

                # raw = struct.pack(fmt, *to_be_saved)

    def _write_ndarray_with_buffer(self, to_be_saved, fmt_to_be_formated,
                                   buffersize=1000):
        nb_values = len(to_be_saved)
        if nb_values < buffersize:
            fmt = fmt_to_be_formated.format(nb_values)
            raw = struct.pack(fmt, *to_be_saved)
            self.write(raw)
        else:
            for small_arr in chunks(to_be_saved, buffersize):
                fmt = fmt_to_be_formated.format(len(small_arr))
                raw = struct.pack(fmt, *small_arr)
                self.write(raw)


if __name__ == '__main__':
    import os
    import numpy as np
    path_test_file = os.path.expanduser('/tmp/test_file.bin')

    with BinFile(path_test_file, 'w') as f:
        f.write_as('poum', buffersize=1)
        f.write_as([1, 3.55], 'I', buffersize=1)
        f.write_as(np.array([1., 1.5]), 'float64', buffersize=1)

    with BinFile(path_test_file) as f:
        s = f.readt(4, 's')
        l = f.readt(2, 'I')
        a = f.readt(2, 'float64')

    print(s, l, a)
