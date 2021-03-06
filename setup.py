"""
WOFpy
-------

WOFpy is a python library for serving CUAHSI's WaterOneflow  web services

CUAHSI is the Consortium of Universities for the
Advancement of Hydrologic Science, Inc.

"""
from __future__ import (absolute_import, division, print_function)

import codecs
import os
import re

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Dependencies.
with open('requirements.txt') as f:
    requirements = f.readlines()
install_requires = [t.strip() for t in requirements]

setup(
    name='WOFpy',
    version=find_version("wof", "__init__.py"),
    license='BSD',
    author='James Seppi',
    author_email='james.seppi@gmail.com',
    # note: maintainer gets listed as author in PKG-INFO, so leaving
    # this commented out for now
    maintainer='David Valentine',
    maintainer_email='david.valentine@gmail.com',
    description='a python library for serving WaterOneFlow web services',
    long_description=__doc__,
    keywords='cuahsi his wofpy water waterml cuahsi wateroneflow odm2 czodata',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    extras_require={
        'odm1': ['sqlalchemy', 'pyodbc'],
        'odm2': ['sqlalchemy', 'odm2api'],
        'sqlite': ['sqlalchemy'],
        'server': ['uwsgi'],
    },
    dependency_links=[
        'git+https://github.com/ODM2/ODM2PythonAPI@v0.1.0-alpha#egg=odm2api-0.1.0'  # noqa
    ],
    tests_require=['suds-jurko', 'requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points=dict(console_scripts=[
        'wofpy_config = wof.wofpy_config:main'
        ]
    ),
)
