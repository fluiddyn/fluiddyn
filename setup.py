from setuptools import setup, find_packages

import os
from runpy import run_path
import sys

here = os.path.abspath(os.path.dirname(__file__))

f"In >=2018, you should use a Python supporting f-strings!"

# Get the long description from the relevant file
with open(os.path.join(here, "README.rst")) as f:
    long_description = f.read()
lines = long_description.splitlines(True)
long_description = "".join(lines[26:])

# Get the version from the relevant file
d = run_path("fluiddyn/_version.py")
__version__ = d["__version__"]

# Get the development status from the version string
if "a" in __version__:
    devstatus = "Development Status :: 3 - Alpha"
elif "b" in __version__:
    devstatus = "Development Status :: 4 - Beta"
else:
    devstatus = "Development Status :: 5 - Production/Stable"


install_requires = [
    "fluidpythran",
    "numpy",
    "matplotlib",
    "h5py",
    "h5netcdf",
    "psutil >= 5.2.1",
    "future",
    'distro; python_version>="3.8"',
    'cached_property; python_version < "3.8"',
]
# Even though we also use scipy, we don't require its installation
# because it can be heavy to install.


setup(
    name="fluiddyn",
    version=__version__,
    description=("framework for studying fluid dynamics."),
    long_description=long_description,
    keywords="Fluid dynamics, research",
    author="Pierre Augier",
    author_email="pierre.augier@legi.cnrs.fr",
    url="https://bitbucket.org/fluiddyn/fluiddyn",
    license="CeCILL-B",
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        devstatus,
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: BSD License",
        # actually CeCILL-B License (BSD compatible license for French laws)
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages(exclude=["doc"]),
    install_requires=install_requires,
    scripts=["bin/fluidconvertim7"],
    entry_points={
        "console_scripts": [
            "fluidinfo = fluiddyn.util.info:main",
            "fluidnbstripout = fluiddoc.fluidnbstripout:main",
            "fluiddocset = fluiddoc.fluiddocset:main",
            "fluiddump = fluiddyn.io.dump:main",
            "fluidmat2py = fluiddyn.util.matlab2py:main",
            "fluidcluster-help = fluiddyn.clusters:print_help_scheduler",
        ]
    },
    extras_require=dict(doc=["Sphinx>=1.1", "numpydoc"]),
)
