ENV=$(CURDIR)/.env
PYTHON=$(ENV)/bin/python
PYVERSION=$(shell pyversions --default)
SITE_PACKAGES=numpy scipy

RED=\033[0;31m
GREEN=\033[0;32m
NC=\033[0m

all: $(ENV)
	@echo "Virtualenv is installed"

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: clean
# target: clean - Display callable targets
clean:
	@rm -rf build dist docs/_build
	@rm -f *.py[co]
	@rm -f *.orig
	@rm -f *.prof
	@rm -f *.lprof
	@rm -f *.so
	@rm -f */*.py[co]
	@rm -f */*.orig
	@rm -f */*/*.py[co]

.PHONY: register
# target: register - Register module on PyPi
register:
	@python setup.py register

.PHONY: upload
# target: upload - Upload module on PyPi
upload:
	@python setup.py sdist upload || echo 'Upload already'

.PHONY: test
# target: test - Runs tests
test: clean
	$(PYTHON) setup.py test

$(ENV):
	virtualenv --no-site-packages .env
	$(ENV)/bin/pip install -r requirements.txt --use-mirrors
