.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: clean
# target: clean - Display callable targets
clean:
	@rm -rf build dist docs/_build
	@find . -name \*.py[co] -delete
	@find . -name *\__pycache__ -delete

.PHONY: upload
# target: upload - Upload module on PyPI
upload:
	@python setup.py sdist bdist_wheel upload || echo 'Upload already'

.PHONY: serve
# target: serve - server docs
serve:
	python3 -mhttp.server
