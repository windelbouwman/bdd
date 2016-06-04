#!/usr/bin/env python

from setuptools import setup

from bdd import __version__

#with open('README.rst', 'r'):
#    pass

setup(
    name='bdd',
    description='Library to convert BDD features into TestCase classes',
    version=__version__,
    author='Windel Bouwman',
    py_modules=['bdd'],
    url='https://github.com/windelbouwman/bdd',
)
