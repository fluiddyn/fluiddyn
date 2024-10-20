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


class PyTrio(PythonPackage):
    """Trio – a friendly Python library for async concurrency and I/O."""

    pypi = "trio/trio-0.26.2.tar.gz"

    maintainers("paugier")
    license("MIT", checked_by="paugier")

    # fmt: off
    version("0.26.2", sha256="0346c3852c15e5c7d40ea15972c4805689ef2cb8b5206f794c9c19450119f3a4")
    version("0.26.1", sha256="6d2fe7ee656146d598ec75128ff4a2386576801b42b691f4a91cc2c18508544a")
    version("0.26.0", sha256="67c5ec3265dd4abc7b1d1ab9ca4fe4c25b896f9c93dac73713778adab487f9c4")
    # fmt: on

    with default_args(type=("build", "run")):
        extends("python@3.11:")

    depends_on("py-setuptools", type="build")

    with default_args(type="run"):
        depends_on("py-attrs")
        depends_on("py-sortedcontainers")
        depends_on("py-idna")
        depends_on("py-outcome")
        depends_on("py-sniffio")
        # only on windows
        # depends_on("py-cffi")
