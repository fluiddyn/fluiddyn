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


class PyFluidsim(PythonPackage):
    """Framework for studying fluid dynamics with simulations."""

    pypi = "fluidsim/fluidsim-0.8.2.tar.gz"

    maintainers("paugier")
    license("CECILL", checked_by="paugier")

    # fmt: off
    version("0.8.2", sha256="eb36c2d7d588fbb088af026683a12bb14aa126bbbc91b999009130d6cb7920f9")
    version("0.8.1", sha256="44c70f388c429856f5df24705cddb2e024d7d1376d2153e113ef111af90b857b")
    version("0.8.0", sha256="01f6d489ce44fe4dc47357506ba227ae0e87b346758d8f067c13f319d0a9a881")
    version("0.7.4", sha256="c04e232f68faafee93fa922bb86fd8d313bb7d3c84c98aa095285121d5e17ece")
    version("0.7.3", sha256="199853fc0211001299b6cdad02d2c21452af5162c2dd4305afa1e1674e294edc")
    version("0.7.2", sha256="ab85dfacd8edec9c3f1934b16df4783a212cb52373d0e75f0cfecb5e928e075a")
    version("0.7.1", sha256="371faeecdfbe9b89cb9bc19fbca35266e0b24175f9caf6fff2d69504c68de3e4")
    version("0.7.0", sha256="b349a0070c40b2bed6983672d8e269a7b8874c0ab6979f5ef03ad0760e66e804")
    # fmt: on

    with default_args(type=("build", "run")):
        extends("python@3.9:")
        depends_on("py-transonic")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-pythran")

    with default_args(type="run"):
        depends_on("py-fluidsim-core")
        depends_on("py-xarray")
        depends_on("py-rich")
        depends_on("py-scipy")

    def config_settings(self, spec, prefix):
        settings = {}
        return settings
