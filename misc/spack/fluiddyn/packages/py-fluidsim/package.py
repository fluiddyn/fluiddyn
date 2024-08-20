# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFluidsim(PythonPackage):
    """Framework for studying fluid dynamics with simulations."""

    pypi = "fluidsim/fluidsim-0.8.2.tar.gz"

    maintainers("paugier")
    license("CECILL", checked_by="paugier")

    version(
        "0.8.2",
        sha256="eb36c2d7d588fbb088af026683a12bb14aa126bbbc91b999009130d6cb7920f9",
    )
    version(
        "0.8.1",
        sha256="44c70f388c429856f5df24705cddb2e024d7d1376d2153e113ef111af90b857b",
    )
    version(
        "0.8.0",
        sha256="01f6d489ce44fe4dc47357506ba227ae0e87b346758d8f067c13f319d0a9a881",
    )
    version(
        "0.8.0rc3",
        sha256="1d90f0cffec919e04182319a134412e4df1d882c36499356ecca05017f7d9bc0",
    )
    version(
        "0.8.0rc2",
        sha256="8c714c0e8a44a5b7f1e1216e7afe7dc74be92d2f6df7e58f2202b3cbd95aa1e1",
    )
    version(
        "0.8.0rc0",
        sha256="8acd9c29c7225944d482f9bbe4e08cef6f8c7a1ede2715e45a533a5c87ba104e",
    )
    version(
        "0.7.4",
        sha256="c04e232f68faafee93fa922bb86fd8d313bb7d3c84c98aa095285121d5e17ece",
    )
    version(
        "0.7.3",
        sha256="199853fc0211001299b6cdad02d2c21452af5162c2dd4305afa1e1674e294edc",
    )
    version(
        "0.7.2",
        sha256="ab85dfacd8edec9c3f1934b16df4783a212cb52373d0e75f0cfecb5e928e075a",
    )
    version(
        "0.7.1",
        sha256="371faeecdfbe9b89cb9bc19fbca35266e0b24175f9caf6fff2d69504c68de3e4",
    )
    version(
        "0.7.0",
        sha256="b349a0070c40b2bed6983672d8e269a7b8874c0ab6979f5ef03ad0760e66e804",
    )
    version(
        "0.7.0rc1",
        sha256="d7dc7a525e0050e276f87992b4807abbf38a8161c6365c8079b42caed385b8a9",
    )
    version(
        "0.7.0rc0",
        sha256="bd6ff5d03bfdcc67b7f35619d9d2a41e3676f417f29eff94cfa1d21a47470503",
    )
    version(
        "0.6.1",
        sha256="619b94dbae322996929921c82545bfc561c3403eeabaafcafd74b3e8b29a7210",
    )
    version(
        "0.6.1rc1",
        sha256="1d584474a768fcbeaebef338c0531df81a84359024bc83f8b45e3fd3ee55a1ae",
    )
    version(
        "0.6.1rc0",
        sha256="631e08e5100550e45b55d479b5bb8312f1f7e42ee741d283badac208e91f6d79",
    )
    version(
        "0.6.0b0",
        sha256="521b23a40d98984c8c9ddb31ad1068203c133e0ca6231c3baba1564b9101a5d0",
    )
    version(
        "0.6.0",
        sha256="fcac85fc748a489c54f919eaaf27e64d132f66c8426bb8cc8e989376cd189c45",
    )
    version(
        "0.5.1",
        sha256="1e8cfdfd76dc0f7f9d7f4b1a0725b758b6155025104f6d1b3c21f87fac5cac3b",
    )
    version(
        "0.5.0.post0",
        sha256="508a3c33c34cbef9c28e871508bb005bda1ff91bc515ed826778c8e2ef728596",
    )
    version(
        "0.5.0",
        sha256="60420a6e437878276b5b4f48fa43861ea3bb52181073d33491443c408feadd11",
    )
    version(
        "0.4.1",
        sha256="afc33a656fdbbd0977c253480a9125616a719f04bddbf7f902b10e6744d3d3c8",
    )
    version(
        "0.4.0",
        sha256="660c3a9c10da95293f75facc7deebadf0afa1723447dac91e87e684414ef27bd",
    )
    version(
        "0.3.3",
        sha256="addb6c80e7321fb7a10a49cdfc6fcf31056e57347d548272bcebb8eca46ce311",
    )
    version(
        "0.3.2",
        sha256="82bdf16fc9b0a40cadd227d6ca5eef5857e409715e4fcc75448ee958ba218382",
    )
    version(
        "0.3.1",
        sha256="2959d2edfed940433980a780616db8846ad7ced2acd46dac7225196f0bab7eec",
    )
    version(
        "0.3.0",
        sha256="c81b150797069577861dbcf5ae57f7e949d351e31d4162d5ea2b1bc61604d249",
    )
    version(
        "0.2.2.post0",
        sha256="f193b16a46329f442cc1c3ada3ebc0976e1a25588eeba9ba53243e54fc1d4719",
    )
    version(
        "0.2.2",
        sha256="47714a7819479e0c285542e82cd2ff714f0769d0ec1843cace85a2feee843990",
    )
    version(
        "0.2.1",
        sha256="85d0b83acd2e86186a0def0ca9cc701af9d0958f1f291b849a36e18cfbd83102",
    )
    version(
        "0.2.0",
        sha256="b0487593bd8436c0ae262e7306435f25dc9b3eefead8868b56278893a94b9e2b",
    )
    version(
        "0.1.1",
        sha256="810747c228043d90f28756741f44e0e09857bff90a0ab5db8ad55ecbd3da60be",
    )
    version(
        "0.1.0.post2",
        sha256="5821ed59129a50402798667808d6dd1b1c4e945c953b65c0c68332407c050ae5",
    )
    version(
        "0.1.0.post1",
        sha256="209b8b4a69fbde7f7dee195c6d9230560c9ef3cd839ec0d74e7510678a39f33e",
    )
    version(
        "0.1.0",
        sha256="8d54f7036c2dfce79e735cce1c3e93d165f186f63a587cf1e5525cb932881283",
    )
    version(
        "0.0.4",
        sha256="13539ecf664c9bd10e686187549ce7794525bf7bedc510067b441f77ba0a6650",
    )
    version(
        "0.0.3a1",
        sha256="75d8aac8e67169751b906baa93c42e7718c2b02ea159a46c9c3ee1ff50201cd0",
    )
    version(
        "0.0.2a1",
        sha256="f36672ea1b0eeec7aef12ca344bdd24b4700b56dcf29598d78505a23ca72ddf6",
    )
    version(
        "0.0.1a0",
        sha256="788092749979f0edcb743544116e74dc7212a40a4ed3497e934b4003a2a103fd",
    )

    extends("python@3.9:", type=("build", "run"))
    depends_on("py-transonic", type=("build", "run"))

    depends_on("py-meson-python", type="build")
    depends_on("py-pythran", type="build")

    depends_on("py-fluidsim-core", type="run")
    depends_on("py-xarray", type="run")
    depends_on("py-rich", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-ipython", type="run")

    def config_settings(self, spec, prefix):
        settings = {}
        return settings
