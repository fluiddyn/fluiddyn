# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# pylint: disable=W0622,E0401

from spack.package import (
    PythonPackage,
    depends_on,
    extends,
    license,
    maintainers,
    version,
)


class PyFluidsimCore(PythonPackage):
    """Pure-Python core library for FluidSim framework."""

    pypi = "fluidsim-core/fluidsim_core-0.8.2.tar.gz"

    maintainers("paugier")
    license("CECILL", checked_by="paugier")

    # fmt: off
    version("0.8.2", sha256="62a8b43fc7ede8c6efc5cc109ae5caca2c1f54891dff547511c8fe94caf0bd7c")
    version("0.8.1", sha256="3dfb51d5db1a574089738a4b8e1c76e75da32b25dceb349207dcece73d1b1646")
    version("0.8.0", sha256="4b7a23649df9d10cde6510280fb8683550549d4cbbc1ebb0bc6adc6e559915f7")
    # fmt: on

    extends("python@3.9:", type=("build", "run"))
    depends_on("py-flit-core", type="build")
    depends_on("py-fluiddyn", type="run")
