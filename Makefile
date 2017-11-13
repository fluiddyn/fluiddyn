
develop:
	python setup.py develop

help:
	@echo "targets: develop, clean_so and tests"

clean_so:
	find fluiddyn -name "*.so" -delete

tests:
	python -m unittest discover

tests_mpi:
	mpirun -np 2 python -m unittest fluiddyn.util.test.test_mpi

tests_coverage:
	mkdir -p .coverage
	coverage run -p -m unittest discover
	mpirun -np 2 coverage run -p -m unittest discover fluiddyn.util.test -p test_mpi.py

report_coverage:
	coverage combine
	coverage report
	coverage html
	coverage xml
	@echo "Code coverage analysis complete. View detailed report:"
	@echo "file://${PWD}/.coverage/index.html"

coverage: tests_coverage report_coverage
