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


class PyOutcome(PythonPackage):
    """Capture the outcome of Python function calls. Extracted from the Trio project."""

    pypi = "outcome/outcome-1.3.0.tar.gz"

    maintainers("paugier")
    license("MIT", checked_by="paugier")

    # fmt: off
    version("1.3.0.post0", sha256="9dcf02e65f2971b80047b377468e72a268e15c0af3cf1238e6ff14f7f91143b8")
    version("1.3.0", sha256="588ef4dc10b64e8df160d8d1310c44e1927129a66d6d2ef86845cef512c5f24c")
    version("1.2.0", sha256="6f82bd3de45da303cf1f771ecafa1633750a358436a8bb60e06a1ceb745d2672")
    version("1.1.0", sha256="e862f01d4e626e63e8f92c38d1f8d5546d3f9cce989263c521b2e7990d186967")
    version("1.0.1", sha256="fc7822068ba7dd0fc2532743611e8a73246708d3564e29a39f93d6ab3701b66f")
    version("1.0.0", sha256="9d58c05db36a900ce60c6da0167d76e28869f64b338d60fa3a61841cfa54ac71")
    # fmt: on

    extends("python@3.11:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-attrs", type="run")
