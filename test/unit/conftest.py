
import os

import ftrack_api
import pytest

import ftrack_location_compatibility


@pytest.fixture(scope='session')
def resource_folder():
    '''Return absolute path to a temporary folder.'''
    return os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ),
        'resource'
    )


@pytest.fixture(scope='session')
def test_location_name():
    '''Return the name of the test location.'''
    return 'ftrack-compatibility-test-location'


@pytest.fixture(scope='session', autouse=True)
def setup_legacy_location(resource_folder, test_location_name):
    '''Setup and register the legacy location.'''
    import ftrack
    ftrack.ensureLocation(test_location_name)
    ftrack.LOCATION_PLUGINS.add(
        ftrack.Location(
            test_location_name,
            accessor=ftrack.DiskAccessor(prefix=resource_folder),
            structure=ftrack.IdStructure(),
            priority=150
        )
    )


@pytest.fixture(scope='session')
def legacy_location(test_location_name):
    '''Return legacy location.'''
    import ftrack
    return ftrack.Location(test_location_name)


@pytest.fixture
def session():
    '''Return session.'''
    session = ftrack_api.Session()
    ftrack_location_compatibility.register_locations(session)
    return session


@pytest.fixture
def proxy_location(session, test_location_name):
    '''Return proxy location.'''
    return session.query(
        'Location where name is {0}'.format(test_location_name)
    ).one()
