import os

from pathlib import Path
from shutil import rmtree

import nox

os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1"})


@nox.session
def test(session):
    session.run_always("pdm", "install", "-G", "test", "-G", "mpi", external=True)

    path_coverage = Path(".coverage")
    rmtree(path_coverage, ignore_errors=True)
    path_coverage.mkdir(exist_ok=True)

    command = "coverage run -p -m pytest --junitxml=.coverage/as_junit.xml"
    session.run(*command.split(), external=True)

    command = "mpirun -np 2 --oversubscribe coverage run -p -m unittest discover fluiddyn.util.test -p test_mpi.py"
    session.run(*command.split(), external=True)
