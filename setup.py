#!/usr/bin/env python

from setuptools import setup, find_packages

import bdd

#with open('README.rst', 'r'):
#    pass

setup(
    name='bdd',
    description='Library to convert BDD features into TestCase classes',
    version=bdd.__version__,
    author='Windel Bouwman',
    packages=find_packages(),
    url='https://github.com/windelbouwman/bdd',
    classifiers=[
        'Topic :: Software Development :: Testing'
    ]
)
