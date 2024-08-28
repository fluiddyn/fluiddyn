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


class PyFluidfftFftw(PythonPackage):
    """Fluidfft plugin using fftw."""

    pypi = "fluidfft_fftw/fluidfft_fftw-0.0.1.tar.gz"

    maintainers("paugier")
    license("CECILL-B", checked_by="paugier")

    # fmt: off
    version("0.0.1", sha256="59967846e1d976508db30ff65987e9c1e6c024ec9c095849608ee8913b96d3ff")
    # fmt: on

    with default_args(type=("build", "run")):
        extends("python@3.9:")
        depends_on("fftw")

    with default_args(type="build"):
        # Required to use --config-settings
        depends_on("py-pip@23.1:")
        depends_on("py-meson-python")
        depends_on("py-transonic")
        depends_on("py-fluidfft-builder")

    depends_on("py-fluidfft", type="run")

    def config_settings(self, spec, prefix):
        settings = {}
        return settings
