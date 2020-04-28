# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import re
import shutil

import glob
from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand
from pkg_resources import parse_version
import pip

if parse_version(pip.__version__) < parse_version('19.3.0'):
    raise ValueError('Pip should be version 19.3.0 or higher')

from pip._internal import main as pip_main

PLUGIN_NAME = 'ftrack-location-compatibility-{0}'

ROOT_PATH = os.path.dirname(
    os.path.realpath(__file__)
)

SOURCE_PATH = os.path.join(
    ROOT_PATH, 'source'
)

README_PATH = os.path.join(os.path.dirname(__file__), 'README.rst')

PACKAGES_PATH = os.path.join(os.path.dirname(__file__), 'source')


HOOK_PATH = os.path.join(
    ROOT_PATH, 'hook'
)

BUILD_PATH = os.path.join(
    ROOT_PATH, 'build'
)

STAGING_PATH = os.path.join(
    BUILD_PATH, PLUGIN_NAME
)

# Read version from source.
with open(os.path.join(
    SOURCE_PATH, 'ftrack_location_compatibility', '_version.py'
)) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)

# Update staging path with the plugin version
STAGING_PATH = STAGING_PATH.format(VERSION)


class BuildPlugin(Command):
    '''Build plugin.'''

    description = 'Download dependencies and build plugin .'

    user_options = []

    def initialize_options(self):
        '''Initialize options.'''
        pass

    def finalize_options(self):
        '''Finalize options.'''
        pass

    def run(self):
        '''Run the build step.'''

        # Clean staging path
        shutil.rmtree(STAGING_PATH, ignore_errors=True)

        # Copy plugin files
        shutil.copytree(
            HOOK_PATH,
            os.path.join(STAGING_PATH, 'hook')
        )

        pip_main.main(
            [
                'install',
                '.',
                '--target',
                os.path.join(STAGING_PATH, 'dependencies')
            ]
        )

        shutil.make_archive(
            os.path.join(
                BUILD_PATH,
                'ftrack-location-compatibilty-{0}'.format(VERSION)
            ),
            'zip',
            STAGING_PATH
        )


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
        (
            'lowdown @ https://bitbucket.org/ftrack/lowdown/get/0.1.0.zip'
            '#egg=lowdown-0.1.0'
        )
    ],
    tests_require=[
        'pytest >= 2.3.5, < 3',
        'ftrack-python-api >= 1, < 2',
    ],
    cmdclass={
        'test': PyTest,
        'build_plugin': BuildPlugin
    },

    options={},
    zip_safe=False,
    data_files=[
        (
            'ftrack_location_compatibility/hook',
            glob.glob(os.path.join(HOOK_PATH, '*.py'))
        )
    ]
)


# Call main setup.
setup(**configuration)
