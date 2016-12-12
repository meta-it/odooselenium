#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python packaging."""
import os
import sys

from setuptools import setup


#: Absolute path to directory containing setup.py file.
here = os.path.abspath(os.path.dirname(__file__))
#: Boolean, ``True`` if environment is running Python version 2.
IS_PYTHON2 = sys.version_info[0] == 2


# Data for use in setup.
NAME = 'odooselenium'
DESCRIPTION = 'Tools to interact with Odoo using Selenium'
README = open(os.path.join(here, 'README.rst')).read()
VERSION = open(os.path.join(here, 'VERSION')).read().strip()
AUTHOR = u'Meta IT'
EMAIL = 'technique@meta-it.fr'
LICENSE = 'GPLv2'
URL = 'https://pypi.python.org/pypi/{name}'.format(name=NAME)
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
]
KEYWORDS = [
    'odoo',
    'selenium==2.53.0',
]
PACKAGES = ['odooselenium']
REQUIREMENTS = [
    'selenium',
    'setuptools',
]
ENTRY_POINTS = {}
TEST_REQUIREMENTS = ['tox']
CMDCLASS = {}
EXTRA_REQUIREMENTS = {
    'test': TEST_REQUIREMENTS,
}


if __name__ == '__main__':  # Do not run setup() when we import this module.
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=README,
        classifiers=CLASSIFIERS,
        keywords=' '.join(KEYWORDS),
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        license=LICENSE,
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        install_requires=REQUIREMENTS,
        entry_points=ENTRY_POINTS,
        tests_require=TEST_REQUIREMENTS,
        cmdclass=CMDCLASS,
        extras_require=EXTRA_REQUIREMENTS,
    )
