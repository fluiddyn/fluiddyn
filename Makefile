
help:
	@echo "targets: develop, clean_so and tests"

develop:
	python setup.py develop

clean_so:
	find fluiddyn -name "*.so" -delete

tests:
	python -m unittest discover

tests_coverage:
	mkdir -p .coverage
	coverage run -m unittest discover
	coverage report
	coverage html
	@echo "Code coverage analysis complete. View detailed report:"
	@echo "file://${PWD}/.coverage/index.html"
