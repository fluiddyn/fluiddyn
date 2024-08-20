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


class PyTransonic(PythonPackage):
    """Make your Python code fly at transonic speeds!"""

    pypi = "transonic/transonic-0.7.1.tar.gz"

    maintainers("paugier")

    license("BSD-3-Clause", checked_by="paugier")

    version(
        "0.7.1",
        sha256="dcc59f1936d09129c800629cd4e6812571a74afe40dadd8193940b545e6ef03e",
    )

    extends("python@3.9:", type=("build", "run"))
    depends_on("py-pdm-backend", type="build")

    depends_on("py-numpy", type="run")
    depends_on("py-beniget", type="run")
    depends_on("py-gast", type="run")
    depends_on("py-autopep8", type="run")
