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


class PyPytestAllclose(PythonPackage):
    """Pytest fixture extending Numpy's allclose function."""

    pypi = "pytest-allclose/pytest-allclose-1.0.0.tar.gz"

    maintainers("paugier")

    license("MIT", checked_by="paugier")

    version(
        "1.0.0",
        sha256="b2f0c521fa652281400d4a105c84454db3c50b993bcfee9861380be69cc6b041",
    )

    extends("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
