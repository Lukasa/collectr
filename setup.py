#! /usr/bin/env python

import collectr
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] in ('submit', 'publish'):
    os.system('python setup.py sdist upload')
    sys.exit()

packages = ['collectr']

setup(
    name='collectr',
    version=collectr.__version__,
    description='Static file management for everyone.',
    long_description=open('README.rst').read(),
    author='Cory Benfield',
    author_email='cory@lukasa.co.uk',
    url='http://www.lukasa.co.uk/',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'collectr': 'collectr'},
    include_package_data=True,
    install_requires=['boto'],
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
        ),
    )
