# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# pylint: disable=W0622,E0401

from spack.package import (
    PythonPackage,
    default_args,
    depends_on,
    extends,
    license,
    maintainers,
    version,
)


class PyFluidimage(PythonPackage):
    """Fluid image processing with Python."""

    pypi = "fluidimage/fluidimage-0.5.3.tar.gz"

    maintainers("paugier")
    license("CECILL", checked_by="paugier")

    # fmt: off
    version("0.5.3", sha256="f5333804748d35fae0a4b4c7b7346171b99f4c22e1c21620dc822af34145cb49")
    version("0.5.2", sha256="56aa8a0b987da0a5a39994671ab1c976c26c7092d818a2a82e6184a455c2b275")
    version("0.5.1", sha256="648d24d1c046b105de5ebcc2e8d1c1f6e418152a3c4b945cfa35e4255495295b")
    version("0.5.0", sha256="c683a9229ae44c04afcc1040057f0a658bfb1e5912954f54d913bcee117fec4a")
    version("0.4.6", sha256="9285146497a820ac94b37f0260f9731b2955f9a246ce196bfa644f09982c97e9")
    # fmt: on

    with default_args(type=("build", "run")):
        extends("python@3.9:")
        depends_on("py-transonic")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-pythran")

    with default_args(type="run"):
        depends_on("py-fluiddyn")
        depends_on("py-scipy")
        depends_on("py-scikit-image")
        depends_on("py-imageio")
        depends_on("py-trio")
        depends_on("py-rich")
        depends_on("py-textual")
        depends_on("py-dask")

    def config_settings(self, spec, prefix):
        settings = {}
        return settings
