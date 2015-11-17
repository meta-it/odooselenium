# Reference card for usual actions in development environment.
#
# For standard installation, see INSTALL.
# For details about development environment, see CONTRIBUTING.rst.
#
PIP ?= pip
TOX ?= tox
PROJECT := $(shell python -c "import setup; print setup.NAME")


#: help - Display callable targets.
.PHONY: 
help:
	@echo "Reference card for usual actions in development environment."
	@echo "Here are available targets:"
	@egrep -o "^#: (.+)" [Mm]akefile  | sed 's/#: /* /'


#: develop - Install minimal development utilities.
.PHONY: develop
develop:
	$(PIP) install -e .[test]


#: clean - Basic cleanup, mostly temporary files.
.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete


#: distclean - Remove local builds, such as *.egg-info.
.PHONY: distclean
distclean: clean
	rm -rf *.egg
	rm -rf *.egg-info


#: maintainer-clean - Remove almost everything that can be re-generated.
.PHONY: maintainer-clean
maintainer-clean: distclean
	rm -rf build/
	rm -rf dist/
	rm -rf .tox/


#: test - Run test suites.
.PHONY: test
test:
	$(TOX)


#: documentation - Build documentation (Sphinx, README, ...)
.PHONY: documentation
documentation: readme


#: readme - Build standalone documentation files (README, CONTRIBUTING...).
.PHONY: readme
readme:
	$(TOX) -e readme


#: release - Tag and push to PyPI.
.PHONY: release
release:
	$(TOX) -e release
