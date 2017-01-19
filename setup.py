# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import re

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


ROOT_PATH = os.path.dirname(
    os.path.realpath(__file__)
)

SOURCE_PATH = os.path.join(
    ROOT_PATH, 'source'
)

README_PATH = os.path.join(os.path.dirname(__file__), 'README.rst')

PACKAGES_PATH = os.path.join(os.path.dirname(__file__), 'source')

# Read version from source.
with open(os.path.join(
    SOURCE_PATH, 'ftrack_location_compatibility', '_version.py'
)) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


class PyTest(TestCommand):
    '''Pytest command.'''

    def finalize_options(self):
        '''Finalize options to be used.'''
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        '''Import pytest and run.'''
        import pytest
        raise SystemExit(pytest.main(self.test_args))


# General configuration.
configuration = dict(
    name='ftrack-location-compatibility',
    version=VERSION,
    description='ftrack location compatibility layer.',
    long_description=open(README_PATH).read(),
    keywords='ftrack, location',
    url='https://bitbucket.org/ftrack/ftrack-location-compatibility',
    author='ftrack',
    author_email='support@ftrack.com',
    license='Apache License (2.0)',
    packages=find_packages(PACKAGES_PATH),
    package_dir={
        '': 'source'
    },
    setup_requires=[
        'sphinx >= 1.2.2, < 2',
        'sphinx_rtd_theme >= 0.1.6, < 2',
        'lowdown >= 0.1.0, < 1'
    ],
    tests_require=[
        'pytest >= 2.3.5, < 3',
        'ftrack-python-api'
    ],
    cmdclass={
        'test': PyTest
    },
    dependency_links=[
        (
            'https://bitbucket.org/ftrack/lowdown/get/0.1.0.zip'
            '#egg=lowdown-0.1.0'
        )
    ],
    options={},
    zip_safe=False
)


# Call main setup.
setup(**configuration)
