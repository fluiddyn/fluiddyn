
develop:
	pip install -v -e .[dev] | grep -v link

help:
	@echo "targets: develop, clean_so and tests"

clean_pyc:
	find fluiddyn -name "*.pyc" -delete
	find fluiddyn -name "__pycache__" -type d | xargs rm -rf

clean: clean_pyc

black:
	black -l 82 fluiddyn fluiddoc

isort:
	isort -rc --atomic -tc fluiddyn fluiddoc

tests:
	pytest

tests_mpi:
	mpirun -np 2 --oversubscribe python -m unittest fluiddyn.util.test.test_mpi -v

tests_coverage:
	mkdir -p .coverage
	coverage run -p -m pytest
	mpirun -np 2 --oversubscribe coverage run -p -m unittest discover fluiddyn.util.test -p test_mpi.py

report_coverage:
	coverage combine
	coverage report
	coverage html
	coverage xml
	@echo "Code coverage analysis complete. View detailed report:"
	@echo "file://${PWD}/.coverage/index.html"

coverage: tests_coverage report_coverage
