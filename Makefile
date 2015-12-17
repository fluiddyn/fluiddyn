
help:
	@echo "targets: develop, clean_so and tests"

develop:
	python setup.py develop

clean_so:
	find fluiddyn -name "*.so" -delete

tests:
	python -m unittest discover


