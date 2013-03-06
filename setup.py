#! /usr/bin/env python

import sys
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] in ('submit', 'publish'):
    os.system('python setup.py sdist upload')
    sys.exit()

__version__ = ''
with open('collectr/__init__.py', 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

packages = ['collectr']

setup(
    name='collectr',
    version=__version__,
    description='Static file management for everyone.',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst'),
    author='Cory Benfield',
    author_email='cory@lukasa.co.uk',
    url='http://www.lukasa.co.uk/',
    scripts=['scripts/collect_static'],
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
