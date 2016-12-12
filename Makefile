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


#: lib/odoo-addons/web_selenium - Clone repository of 'web_selenium' addon for Odoo.
lib/odoo-addons/web_selenium:
	mkdir -p lib/odoo-addons
	git clone -b 8.0 https://github.com/brain-tec/web_selenium.git ./web_selenium
	mv ./web_selenium lib/odoo-addons/web_selenium


#: develop - Install minimal development utilities.
.PHONY: develop
develop: lib/odoo-addons/web_selenium
	$(PIP) install -e .[test] erppeek


#: odoo-start - Run and setup Odoo development server using Docker.
.PHONY: odoo-start
odoo-start:
	python -c "import init_odoo;init_odoo.odoo_start();init_odoo.odoo_setup()"


#: odoo-stop - Stop Odoo development server using Docker.
.PHONY: odoo-stop
odoo-stop:
	python -c "import init_odoo;init_odoo.odoo_stop()"


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
