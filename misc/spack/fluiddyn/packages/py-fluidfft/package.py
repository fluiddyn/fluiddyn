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


class PyFluidfft(PythonPackage):
    """Efficient and easy Fast Fourier Transform (FFT) for Python."""

    pypi = "fluidfft/fluidfft-0.4.1.tar.gz"

    maintainers("paugier")

    license("CECILL-B", checked_by="paugier")

    # fmt: off
    version("0.4.1", sha256="b17e64c7b2be47c61d6ac7b713e0e8992cf900d2367381288c93a56090e6c0c1")
    version("0.4.0.post1", sha256="70791c92f43d7611c5db89d069e745875fca9be02948156a6c1b184fbc87cb4d")
    version("0.3.5", sha256="56ba7213eb79af6afeb60fb19eb4a31b9f4d64f295683f9743790c71677ead87")
    # fmt: on

    with default_args(type=("build", "run")):
        extends("python@3.9:")
        depends_on("py-transonic")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-pythran")

    with default_args(type="run"):
        depends_on("py-fluiddyn")
        depends_on("py-pyfftw")

    def config_settings(self, spec, prefix):
        settings = {}
        return settings
