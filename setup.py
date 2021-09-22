from setuptools import setup, find_packages

import os
from runpy import run_path
import sys

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")

here = os.path.abspath(os.path.dirname(__file__))

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

setup(
    version=__version__,
    long_description=long_description,
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages(exclude=["doc"]),
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
)
