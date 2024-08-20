# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import (
    PythonPackage,
    maintainers,
    license,
    version,
    depends_on,
    extends,
)


class PyFluidfft(PythonPackage):
    """Efficient and easy Fast Fourier Transform (FFT) for Python."""

    pypi = "fluidfft/fluidfft-0.4.1.tar.gz"

    maintainers("paugier")

    license("CECILL-B", checked_by="paugier")

    version("0.4.1", sha256="b17e64c7b2be47c61d6ac7b713e0e8992cf900d2367381288c93a56090e6c0c1")
    version("0.4.0.post1", sha256="70791c92f43d7611c5db89d069e745875fca9be02948156a6c1b184fbc87cb4d")
    version("0.3.5", sha256="56ba7213eb79af6afeb60fb19eb4a31b9f4d64f295683f9743790c71677ead87")

    extends("python@3.9:", type=("build", "run"))
    depends_on("py-transonic", type=("build", "run"))

    depends_on("py-meson-python", type="build")
    depends_on("py-pythran", type="build")

    depends_on("py-fluiddyn", type="run")
    depends_on("py-pyfftw", type="run")

    def config_settings(self, spec, prefix):
        settings = {}
        return settings
