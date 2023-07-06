"""Handle ipython notebooks (:mod:`fluiddoc.ipynb_maker`)
=========================================================

.. autofunction:: execute_notebooks

.. autofunction:: ipynb_to_rst

"""

import os
import subprocess
from datetime import datetime
from glob import glob
from pathlib import Path


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


def call_bash(commands):
    subprocess.call(["/bin/bash", "-c", commands])


def execute_notebooks(path_dir):
    """Execute notebooks in a directory"""
    paths_ipynb = Path(path_dir).glob("*.ipynb")
    paths_ipynb = [
        path for path in paths_ipynb if not path.name.endswith(".executed.ipynb")
    ]
    for path in paths_ipynb:
        path_executed = path.with_suffix(".executed.ipynb")
        if not os.path.exists(path_executed) or modification_date(
            path
        ) > modification_date(path_executed):
            call_bash(
                "jupyter-nbconvert --ExecutePreprocessor.timeout=200 "
                + f"--to notebook --execute {path} --output={path_executed.name}"
            )


def ipynb_to_rst(path="ipynb", executed=None):
    """Convert notebooks to rst files

    If the user does not specify that the notebooks have already been executed,
    they are executed with jupyter-nbconvert before the conversion to rst
    files.

    """

    paths_ipynb = glob(path + "/*.ipynb")
    paths_ipynb = [
        path for path in paths_ipynb if not path.endswith(".nbconvert.ipynb")
    ]

    paths_ipynb_executed = []

    for filepath in paths_ipynb:
        if executed:
            try:
                executed[0]
            except TypeError:
                paths_ipynb_executed.append(filepath)
                continue

            else:
                nfile = os.path.split(filepath)[-1]
                if nfile in executed:
                    paths_ipynb_executed.append(filepath)
                    continue

        basename = os.path.splitext(filepath)[0]
        ipynb_executed = basename + ".nbconvert.ipynb"
        paths_ipynb_executed.append(ipynb_executed)

        if not os.path.exists(ipynb_executed) or modification_date(
            filepath
        ) > modification_date(ipynb_executed):
            call_bash(
                "jupyter-nbconvert --ExecutePreprocessor.timeout=200 "
                "--to notebook --execute " + filepath
            )

    for filepath in paths_ipynb_executed:
        basename = os.path.splitext(os.path.splitext(filepath)[0])[0]
        rstpath = basename + ".rst"
        rstname = os.path.split(rstpath)[-1]

        if not os.path.exists(rstpath):
            has_to_be_compiled = True
        else:
            d_ipynb = modification_date(filepath)
            d_rst = modification_date(rstpath)
            if d_ipynb > d_rst:
                has_to_be_compiled = True
            else:
                has_to_be_compiled = False

        if has_to_be_compiled:
            call_bash(
                "jupyter-nbconvert --to rst " + filepath + " --output " + rstname
            )
