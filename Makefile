ENV=$(CURDIR)/.env

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

.PHONY: test
# target: test - Runs tests
test: clean
	$(PYTHON) setup.py test

.PHONY: env
# target: env - Setup development environment
env:
	virtualenv --no-site-packages $(ENV)
	$(ENV)/bin/pip install -r requirements-dev.txt

.PHONY: serve
# target: serve - server docs
serve:
	python3 -mhttp.server
