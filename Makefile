
clean_so:
	find fluiddyn -name "*.so" -delete

tests:
	python -m unittest discover

develop:
	python setup.py develop
