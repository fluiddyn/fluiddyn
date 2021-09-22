"""
Spherical harmonics operators (:mod:`fluiddyn.calcul.sphericalharmo`)
=====================================================================

This module requires the C library shtns. To install it, run something like::

  ./configure --enable-openmp --enable-python
  make && make install

.. autoclass:: EasySHT
   :members:
   :private-members:

"""


import sys
from time import time

import numpy as np

try:
    import shtns
except ImportError:
    pass
else:
    sht_orthonormal = shtns.sht_orthonormal
    sht_fourpi = shtns.sht_fourpi
    sht_schmidt = shtns.sht_schmidt

    # print('sht_norms', sht_orthonormal, sht_fourpi, sht_schmidt)

    sht_gauss = shtns.sht_gauss
    sht_auto = shtns.sht_auto
    sht_reg_fast = shtns.sht_reg_fast
    sht_reg_dct = shtns.sht_reg_dct
    sht_quick_init = shtns.sht_quick_init
    sht_reg_poles = shtns.sht_reg_poles
    sht_gauss_fly = shtns.sht_gauss_fly

    SHT_THETA_CONTIGUOUS = shtns.SHT_THETA_CONTIGUOUS

    SHT_PHI_CONTIGUOUS = shtns.SHT_PHI_CONTIGUOUS

    SHT_NO_CS_PHASE = shtns.SHT_NO_CS_PHASE
    SHT_REAL_NORM = shtns.SHT_REAL_NORM
    SHT_SCALAR_ONLY = shtns.SHT_SCALAR_ONLY
    SHT_SOUTH_POLE_FIRST = shtns.SHT_SOUTH_POLE_FIRST


"""
flags for normalization (norm = ...)
 sht_orthonormal = 0  # orthonormalized spherical harmonics (default).
 sht_fourpi      = 1  # Geodesy and spectral analysis : 4.pi normalization.
 sht_schmidt     = 2  # Schmidt semi-normalized : 4.pi/(2l+1)

flags for spatial data layouts and grids used by SHTns
use the bitwise operator OR "|" to separate the different flags
for example:
flags = (shtns.sht_quick_init | shtns.SHT_PHI_CONTIGUOUS |
         shtns.SHT_SOUTH_POLE_FIRST)
"""

radius_earth = 6367470.0  # earth radius (m)


def compute_lmax(nlat, nl_order=2):
    return int(2 * nlat / (nl_order + 1) - 1)


def compute_nlatnlon(lmax, nl_order=2):
    if lmax % 2 == 0:
        lmax += 1
    nlat = int((lmax + 1) * (nl_order + 1) / 2)
    if nlat % 2 == 1:
        nlat += 1
    return nlat, 2 * nlat


def _for_test(i):
    if i % 2 == 1:
        assert i == compute_lmax(compute_nlatnlon(i)[0])


def bin_int(n, width):
    return "".join(str((n >> i) & 1) for i in range(width - 1, -1, -1))


class EasySHT:
    """Simple possibilities of shtns.

    Less possibilities but very simple to use...  It has been written
    specially for atmospheric applications.

    Creation of a default instance::

      esh = EasySHT(lmax=15)

    Parameters
    ----------

    lmax : number {15}
        Truncation degree.

    mmax : {None, int}
        If is None, triangular truncation.

    mres : 1
        Azimutal symmetry coefficient (see shtns documentation).

    norm=shtns.sht_fourpi
        For SH with quadratic mean equal to unity.

    nlat : {None, int}
        If None, computed by shtns to avoid aliasing.

    nlon : {None, int}
        If None, computed by shtns to avoid aliasing.

    flags : {sht_quick_init|SHT_PHI_CONTIGUOUS|SHT_SOUTH_POLE_FIRST, int}
        Option flag for shtns.

    polar_opt : {1.0e-8, float}
        Polar optimization threshold.

    nl_order : {2, int}
        Nonlinear order of the equations (used to compute nlat and nlon).

    radius : {radius_earth, number}
        Radius of the sphere (in meters)

    Notes
    -----

    In contrast as with shtns, with easypysht the meridional unit
    vector points towards the North if shtns.SHT_SOUTH_POLE_FIRST is
    used (this is the default) and it points towards the South if
    shtns.SHT_SOUTH_POLE_FIRST is not given in flags (thus there is a
    change of sign in the meridional velocity).

    easypysht has been written for atmospheric applications thus some
    usual notations are used.

    Here are some definitions useful to understand the code:

    - l     denotes the degree of the spherical harmonic functions
    - m     denotes the order of the spherical harmonic functions
    - SH    denotes spherical harmonic (spectral array)
    - spat  denotes spatial array

    - lat   denotes latitude
    - lon   denotes longitude
    - kh    denotes horizontal wavenumber
    - u     denotes longitudinal velocity
    - v     denotes meridional velocity (the sign depends on the used base)

    - hdiv  denotes horizontal divergence
    - hrot  denotes vertical vorticity (curl on the sphere)
    - grad  denotes the horizontal gradient

    Variables and functions about spectral space array:
    lmax, mmax, mres, nlm, idx_lm(), l_idx, m_idx, l2_idx

    Variables about grid and real space array:
    nlat, nlon, lats, lons, sin_lats, LATS, LONS

    Variables for spectra:
    l2_l, kh_l

    self.sh is the instance of the class sht defined in shtns.py.
    All functions and variables of this class can be used directly
    from this instance, for example::

      esh.sh.sh_to_point(f_lm, cost, phi)

    where t is the colatitude and phi is the longitude.

    """

    def __init__(
        self,
        lmax=15,
        mmax=None,
        mres=1,
        norm=None,
        nlat=None,
        nlon=None,
        flags=None,
        polar_opt=1.0e-8,
        nl_order=2,
        radius=radius_earth,
    ):

        # to get a clear ImportError
        try:
            import shtns
        except ImportError:
            print(
                "ImportError shtns.\n\n"
                "To install shtns, you can run the following:\n"
                "    git clone https://gricad-gitlab.univ-grenoble-alpes.fr/schaeffn/shtns\n"
                "    cd shtns\n"
                "    ./configure --prefix=$VIRTUAL_ENV --enable-python\n"
                "    make\n"
                "    make install\n"
            )
            raise

        if norm is None:
            norm = sht_fourpi

        if flags is None:
            flags = (
                shtns.sht_quick_init
                | shtns.SHT_PHI_CONTIGUOUS
                | shtns.SHT_SOUTH_POLE_FIRST
            )

        # print(lmax,mmax,mres,nlat,nlon,flags,polar_opt,nl_order,radius)
        # print('flags', flags,
        #       shtns.sht_quick_init, shtns.SHT_PHI_CONTIGUOUS,
        #       shtns.SHT_SOUTH_POLE_FIRST)

        if lmax is None and nlat is None:
            raise ValueError("lmax or nlat should be given.")

        elif lmax is None:
            lmax = compute_lmax(nlat)

        # print('lmax', lmax)

        self.lmax = int(lmax)
        self.radius = float(radius)
        # print(self.radius, radius_earth)

        if mmax is None and mres == 1:
            # triangular truncation
            self.mmax = self.lmax
            self.mres = 1
        else:
            self.mmax = int(float(lmax) / mres)
            self.mres = mres

        print(
            "lmax={}, mmax={}, mres={}, norm={}".format(
                self.lmax, self.mmax, self.mres, norm
            )
        )

        self.sh = shtns.sht(self.lmax, self.mmax, self.mres, norm=norm)

        bin_flags = bin_int(flags, 14)
        # print(bin_flags, bin_flags[-14])
        if bin_flags[-14] == "1":
            self.order_lat = "south_to_north"
        else:
            self.order_lat = "north_to_south"

        # in shtns, 0 means None
        if nlat is None:
            nlat = 0
        if nlon is None:
            nlon = 0

        self.nlat, self.nlon = self.sh.set_grid(
            nlat=nlat,
            nphi=nlon,
            flags=flags,
            polar_opt=polar_opt,
            nl_order=nl_order,
        )
        # print('flags', flags)

        self.sin_lats = self.sh.cos_theta
        self.lons = np.arange(self.nlon) * 360.0 / (self.nlon * self.mres)
        self.lats = np.arcsin(self.sin_lats) / np.pi * 180.0

        # for fluidsim plotting
        self.x_seq = self.lons
        self.y_seq = self.lats

        # degree
        self.l_idx = self.sh.l
        self.l2_idx = self.l_idx * (self.l_idx + 1)
        # laplacian:=l(l+1)/r^2 and laplacian^2
        self.K2 = self.l2_idx / self.radius ** 2
        self.K4 = self.K2 ** 2
        self.K8 = self.K4 ** 2

        self.K2_not0 = self.K2[:]
        COND = self.l2_idx == 0
        self.K2_not0[COND] = 1e-15

        # print('l2_idx=', self.l2_idx)
        self.m_idx = self.sh.m
        self.nlm = self.sh.nlm

        self.deltax = 360.0 / (self.nlon * self.mres)
        # wrong but useful for fluidsim
        self.deltay = self.deltax

        # create arrays 2D lats et lons
        self.LONS, self.LATS = np.meshgrid(self.lons, self.lats)
        self.cosLATS = np.cos(self.LATS / 180 * np.pi)

        self.lrange = np.arange(self.lmax + 1)
        self.l2_l = self.lrange * (self.lrange + 1)
        self.kh_l = np.sqrt(self.l2_l) / self.radius

        self._complex64_save_netCFD = np.dtype(
            [("real", np.float32), ("imag", np.float32)]
        )

        # print(lmax,mmax,mres,nlat,nlon,flags,polar_opt,nl_order,radius)

        # no MPI decomposition
        self.shapeX = self.shapeX_loc = self.shapeX_seq = (self.nlat, self.nlon)
        self.shapeK = self.shapeK_loc = self.shapeK_seq = (self.nlm,)

        self.sht_as_arg = self.sh.spat_to_SH
        self.isht_as_arg = self.sh.SH_to_spat

        self._zeros_sh = self.create_array_sh(0.0)

    def vec_from_rotsh(self, rot_sh):
        return self.uv_from_hdivrotsh(self._zeros_sh, rot_sh)

    def vec_from_divsh(self, div_sh):
        return self.uv_from_hdivrotsh(div_sh, self._zeros_sh)

    def produce_str_describing_oper(self):
        """Produce a string describing the operator."""
        return f"lmax{self.lmax}_nlat{self.nlat}_nlon{self.nlon}"

    def produce_long_str_describing_oper(self):
        return "\n".join(
            (
                "Spherical harmonic transforms "
                "nlat = {} ; nlon = {}".format(self.nlat, self.nlon),
                "(1 point every {:6.2g} m for the current sphere of radius {})".format(
                    2 * np.pi * self.radius / self.nlon, self.radius
                ),
                "(1 point every {:6.2g} km for the earth)\n".format(
                    2 * np.pi * radius_earth / self.nlon / 1000
                ),
            )
        )

    def idx_lm(self, l, m):
        """idx_lm(self, l,m)"""
        if l >= 0 and 0 <= m <= l:
            return self.sh.idx(int(l), int(m))

        else:
            raise ValueError("not (l>=0 and m>=0 and m<=l)")

    # functions for initialisation of field

    def create_array_sh(self, value=None, dtype=complex):
        """Create an array representing a field in spectral space."""
        if value is None:
            field_lm = np.empty(self.nlm, dtype)
        elif value == "rand":
            field_lm = np.random.randn(self.nlm) + 1.0j * np.random.randn(
                self.nlm
            )
        elif value == 0:
            field_lm = np.zeros(self.nlm, dtype)
        else:
            field_lm = value * np.ones(self.nlm, dtype)
        return field_lm

    def create_array_spat(self, value=None):
        """Create an array representing a field in spatial space."""
        if value is None:
            field = np.empty(self.shapeX)
        elif value == "rand":
            field = np.random.randn(self.nlat, self.nlon)
        elif value == 0:
            field = np.zeros(self.shapeX)
        else:
            field = value * np.ones(self.shapeX)
        # a spatial array matching a grid build with SHT_PHI_CONTIGUOUS
        return field

    def convert2complex64_save_netCFD(self, f_lm):
        result = np.empty(f_lm.shape, self._complex64_save_netCFD)
        result["real"] = f_lm.real
        result["imag"] = f_lm.imag
        return result

    # functions for scalar spherical harmonic transforms (forward and backward)

    def sht(self, field):
        field_lm = self.create_array_sh()
        self.sh.spat_to_SH(field, field_lm)
        return field_lm

    def isht(self, field_lm):
        field = self.create_array_spat()
        self.sh.SH_to_spat(field_lm, field)
        return field

    def sh_from_spat(self, field, field_lm=None):
        """Spherical harmonic transform.

        examples:
        f_lm = sh_from_spat(f)

        or if f_lm already exists:
        sh_from_spat(f, f_lm)
        """
        if field.dtype != np.dtype("float"):
            field = np.array(field, float)
        if field_lm is None:
            field_lm = self.create_array_sh()

        self.sh.spat_to_SH(field, field_lm)
        return field_lm

    def spat_from_sh(self, field_lm, field=None):
        """Inverse spherical harmonic transform."""
        if field_lm.dtype != np.dtype("complex"):
            field_lm = np.array(field_lm, complex)
        if field is None:
            field = self.create_array_spat()
        self.sh.SH_to_spat(field_lm, field)
        return field

    def chrono_sht(self, nb_sht=10):
        """Microbenchmark forward and inverse SHT, and
        vorticity, divergence <-> u, v transformations.

        """
        f = np.random.rand(self.nlat, self.nlon)
        t1 = time()
        for i in range(nb_sht):
            f_lm = self.sh_from_spat(f)
        t2 = time()
        print(
            "    mean time for 1 forward SHT: {:3.6f} s".format(
                (t2 - t1) / nb_sht
            )
        )
        t1 = time()
        for i in range(nb_sht):
            f = self.spat_from_sh(f_lm)
        t2 = time()
        print(
            "    mean time for 1 inverse SHT: {:3.6f} s".format(
                (t2 - t1) / nb_sht
            )
        )
        uu = np.random.rand(self.nlat, self.nlon)
        vv = np.random.rand(self.nlat, self.nlon)
        t1 = time()
        for i in range(nb_sht):
            hdiv, hrot = self.hdivrotsh_from_uv(uu, vv)
        t2 = time()
        print(
            "    mean time for hdivrotsh_from_uuvv vectorial SHT: "
            "{:3.6f} s".format((t2 - t1) / nb_sht)
        )
        t1 = time()
        for i in range(nb_sht):
            uu, vv = self.uv_from_hdivrotsh(hdiv, hrot)
        t2 = time()
        print(
            "    mean time for uv_from_hdivrotsh vectorial SHT: "
            "{:3.6f} s".format((t2 - t1) / nb_sht)
        )

    # functions for 2D vectorial spherical harmonic transforms

    def uv_from_hdivrotsh(self, hdiv_lm, hrot_lm, uu=None, vv=None):
        """
        u, v from div, rot (u and v are overwritten)
        """
        if uu is None:
            uu = self.create_array_spat()
            vv = self.create_array_spat()
        uD_lm = self.create_array_sh(0.0)
        uR_lm = self.create_array_sh(0.0)
        COND = self.l2_idx > 0
        uD_lm[COND] = -hdiv_lm[COND] / self.l2_idx[COND] * self.radius
        uR_lm[COND] = -hrot_lm[COND] / self.l2_idx[COND] * self.radius
        self.sh.SHsphtor_to_spat(uD_lm, uR_lm, vv, uu)
        # if self.order_lat == 'south_to_north':
        #    vv[:] = -vv+0       # because SHTns uses colatitude basis
        return uu, vv

    def hdivrotsh_from_uv(self, uu, vv, hdiv_lm=None, hrot_lm=None):
        """Compute hdivrotsh from uuvv.

        (div_lm and rot_lm are overwritten)
        """
        if hdiv_lm is None:
            hdiv_lm = self.create_array_sh()
            hrot_lm = self.create_array_sh()

        # if self.order_lat == 'south_to_north':
        #     vv = -vv
        # print('order_lat',self.order_lat)
        self.sh.spat_to_SHsphtor(vv, uu, hdiv_lm, hrot_lm)
        # in fact there is uD_lm in hdiv_lm and
        #                  uR_lm in hrot_lm
        # we compute div_lm and rot_lm
        hdiv_lm[:] = -self.l2_idx * hdiv_lm[:] / self.radius
        # removed minus
        hrot_lm[:] = -self.l2_idx * hrot_lm[:] / self.radius
        return hdiv_lm, hrot_lm

    def uv_from_uDuRsh(self, uD_lm, uR_lm, uu=None, vv=None):
        """Compute velocities uu, vv from uD, uR (uu and vv are
        overwritten).

        """
        if uu is None:
            uu = self.create_array_spat()

        if vv is None:
            vv = self.create_array_spat()
        self.sh.SHsphtor_to_spat(uD_lm, uR_lm, vv, uu)

        # if self.order_lat == 'south_to_north':
        #    vv[:] = -vv+0       # because SHTns uses colatitude basis

        return uu, vv

    def uDuRsh_from_uv(self, uu, vv, uD_lm=None, uR_lm=None):
        """Compute helmholtz decomposition of the velocities from uu, vv.
        (uD_lm and uR_lm are overwritten).

        """
        if uD_lm is None:
            uD_lm = self.create_array_sh()

        if uR_lm is None:
            uR_lm = self.create_array_sh()

        # if self.order_lat == 'south_to_north':
        #     vv = -vv
        # print('order_lat', self.order_lat)
        self.sh.spat_to_SHsphtor(vv, uu, uD_lm, uR_lm)
        # removed minus
        uD_lm[:] = -uD_lm[:]
        uR_lm[:] = -uR_lm[:]
        # print(self.radius)
        return uD_lm, uR_lm

    def hdivrotsh_from_uDuRsh(self, uD_lm, uR_lm, hdiv_lm=None, hrot_lm=None):
        """Compute horizontal divergence and vertical vorticity spherical
        harmonics from velocity vector spherical harmonics (hdiv_lm and hrot_lm
        are overwritten).

        """
        if hdiv_lm is None:
            hdiv_lm = self.create_array_sh(0.0)  # TODO: Maybe can be empty?

        if hrot_lm is None:
            hrot_lm = self.create_array_sh(0.0)

        hdiv_lm[:] = -self.l2_idx * uD_lm / self.radius
        hrot_lm[:] = self.l2_idx * uR_lm / self.radius
        return hdiv_lm, hrot_lm

    def uDuRsh_from_hdivrotsh(self, hdiv_lm, hrot_lm, uD_lm=None, uR_lm=None):
        """Compute velocity vector spherical harmonics from horizontal
        divergence and vertical vorticity spherical harmonics (uD_lm and
        uR_lm are overwritten).

        """
        if uD_lm is None:
            uD_lm = self.create_array_sh(0.0)

        if uR_lm is None:
            uR_lm = self.create_array_sh(0.0)

        COND = self.l2_idx > 0
        uD_lm[COND] = -hdiv_lm[COND] / self.l2_idx[COND] * self.radius
        uR_lm[COND] = +hrot_lm[COND] / self.l2_idx[COND] * self.radius
        # print(self.radius)
        return uD_lm, uR_lm

    def gradf_from_fsh(self, f_lm, gradf_lon=None, gradf_lat=None):
        """gradf from fsh.

        Compute the gradient of a function f from its spherical
        harmonic coeff f_lm (gradf_lon and gradf_lat are overwritten)

        """
        if gradf_lon is None:
            gradf_lon = self.create_array_spat(0)
            gradf_lat = self.create_array_spat(0)  # becareful bug if not 0!!!
        #       We do not use SHsph_to_spat() because it seems that there is a
        #       problem
        # FIXME: av: What exactly is the problem and does it still exist? Issue link?
        ####    self.sh.SHsph_to_spat(f_lm, gradf_lat, gradf_lon)
        #       instead we use SHsphtor_to_spat(...) with tor_lm= zeros_lm
        # zeros_lm = self.create_array_sh(0.)
        self.sh.SHsphtor_to_spat(f_lm, self._zeros_sh, gradf_lat, gradf_lon)

        # if self.order_lat == 'south_to_north':
        #    sign_inv_vv = -1
        # else:
        #    sign_inv_vv = 1
        # sign_inv_vv = 1
        gradf_lat[:] = +gradf_lat / self.radius  # *sign_inv_vv
        gradf_lon[:] = +gradf_lon / self.radius
        # print('radius', self.radius)
        return gradf_lon, gradf_lat

    def spat3d_from_sh3d(self, f_lm_3d, f3d=None, dtype=np.float64):
        nvert = f_lm_3d.shape[0]
        if f3d is None:
            f3d = np.empty([nvert, self.nlat, self.nlon], dtype)
        for iz in range(nvert):
            f2D = self.spat_from_sh(f_lm_3d[iz])
            f3d[iz] = f2D
        return f3d

    def sh3d_from_spat3d(self, f3d, f_lm3d=None, dtype=np.complex128):
        nvert = f3d.shape[0]
        if f_lm3d is None:
            f_lm3d = np.empty([nvert, self.nlm], dtype)
        for iz in range(nvert):
            f_lm3d[iz] = self.sh_from_spat(f3d[iz])
        return f_lm3d

    # print functions...

    def print_info(self):
        print(self.produce_str_describing_oper())
        self.sh.print_info()
        print("")

    def print_array_sh(self, field_lm, name_field_lm, lmax_print=10):
        lmax_print = np.min([lmax_print, self.lmax])
        print(name_field_lm, "= ")
        for n in range(lmax_print + 1):
            print(f"n={n:2d} ", end="")
            for m in range(n + 1):
                temp_idx = m * self.lmax - (m + 1) * m / 2 + m + n
                sys.stdout.write("{:8.3g} ".format(np.abs(field_lm[temp_idx])))
            print("")

    # functions for the computation of spectra and co-spectra

    def sum_wavenumbers(self, field_lm):
        """Convenient function to look more like a pseudo-spectral Operators"""
        return field_lm.sum()

    def _spectrum_from_array_desh(self, array_desh):
        """Compute spectrum(l) from array_desh(ilm)"""
        spectrum = np.zeros(self.lmax + 1)
        for ilm in range(0, self.nlm):
            spectrum[self.l_idx[ilm]] += array_desh[ilm]
        return spectrum

    def _array_desh_from_sh(self, field_lm, key_field):
        """Compute the array_desh (density of energy) from an field_lm"""
        if key_field[:1] == "u" or key_field[:1] == "v":
            array_desh = abs(field_lm) ** 2 / 2.0
        elif (
            key_field[:1] == "T" or key_field[:2] == "ps" or key_field[:1] == "o"
        ):
            array_desh = abs(field_lm) ** 2 / 2.0
        elif key_field[:4] == "beta":
            array_desh = self.create_array_sh(0.0, float)
            array_desh = abs(field_lm) ** 2
        elif key_field[:2] == "uD" or key_field[:2] == "uR":
            array_desh = self.l2_idx * (abs(field_lm) ** 2) / 2
        elif key_field[:4] == "hdiv" or key_field[:4] == "hrot":
            array_desh = self.create_array_sh(0.0, float)
            COND = self.l2_idx > 0
            array_desh[COND] = (
                self.radius ** 2
                / self.l2_idx[COND]
                * abs(field_lm[COND]) ** 2
                / 2
            )
        else:
            raise ValueError("key_field is not correct")

        array_desh[self.m_idx > 0] = 2 * array_desh[self.m_idx > 0]
        return array_desh

    def spectrum_from_sh(self, field_lm, key_field):
        """compute spectrum from field_lm"""
        array_desh = self._array_desh_from_sh(field_lm, key_field)
        spectrum = self._spectrum_from_array_desh(array_desh)
        return spectrum

    def cospectrum_from_2fieldssh(self, f_lm, g_lm):
        """compute cospectrum(l) from f_lm(ilm) and g_lm(ilm)"""
        cospectrum = np.zeros(self.lmax + 1)

        array_desh = f_lm.conjugate() * g_lm + f_lm * g_lm.conjugate()
        array_desh = array_desh.real
        array_desh[self.m_idx == 0] = array_desh[self.m_idx == 0] / 2

        for ilm in range(self.nlm):
            cospectrum[self.l_idx[ilm]] += array_desh[ilm]
        return cospectrum

    def cospectrum_from_2vectorssh(self, f_lon_lm, f_lat_lm, g_lon_lm, g_lat_lm):
        """compute cospectrum(l)..."""
        cospectrum = np.zeros(self.lmax + 1)

        array_desh = (
            f_lon_lm.conjugate() * g_lon_lm
            + f_lon_lm * g_lon_lm.conjugate()
            + f_lat_lm.conjugate() * g_lat_lm
            + f_lat_lm * g_lat_lm.conjugate()
        )
        array_desh = array_desh.real
        array_desh[self.m_idx == 0] = array_desh[self.m_idx == 0] / 2

        for ilm in range(self.nlm):
            cospectrum[self.l_idx[ilm]] += array_desh[ilm]
        return cospectrum

    def cospectrum_from_2fieldssh2(self, f_lm, g_lm):

        """compute cospectrum(l)..."""
        cospectrum = np.zeros(self.lmax + 1)

        array_desh = f_lm.conjugate() * g_lm + f_lm * g_lm.conjugate()
        array_desh = array_desh.real
        array_desh[self.m_idx == 0] = array_desh[self.m_idx == 0] / 2

        array_desh2 = self.create_array_sh(0.0, float)
        COND = self.l2_idx > 0
        array_desh2[COND] = (
            self.radius ** 2 / self.l2_idx[COND] * array_desh[COND]
        )

        for ilm in range(self.nlm):
            cospectrum[self.l_idx[ilm]] += array_desh2[ilm]
        return cospectrum

    def cospectrum_from_2divrotsh(self, hdiva_lm, hrota_lm, hdivb_lm, hrotb_lm):
        """compute cospectrum(l)..."""
        cospectrum = np.zeros(self.lmax + 1)

        array_desh = (
            hrota_lm.conjugate() * hrotb_lm + hdiva_lm.conjugate() * hdivb_lm
        )
        array_desh = array_desh.real
        array_desh[self.m_idx == 0] = array_desh[self.m_idx == 0] / 2

        array_desh2 = self.create_array_sh(0.0, float)
        COND = self.l2_idx > 0
        array_desh2[COND] = (
            self.radius ** 2 / self.l2_idx[COND] * array_desh[COND]
        )

        for ilm in range(self.nlm):
            cospectrum[self.l_idx[ilm]] += array_desh2[ilm]
        # print('cospe',cospectrum.shape)
        return cospectrum

    def dealiasing(self, field_lm):
        """Convenient function for fluidsim"""
        return field_lm


if __name__ == "__main__":
    obj = EasySHT()
