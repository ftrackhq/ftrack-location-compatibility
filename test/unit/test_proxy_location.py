# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import datetime
import os
import platform
import uuid

import pytest
import ftrack
import ftrack_api

import ftrack_location_compatibility.plugin


def test_proxy_location(proxy_location):
    '''Verify that location is really a proxied legacy location.'''
    assert isinstance(
        proxy_location.accessor,
        ftrack_location_compatibility.plugin.ProxyAccessor
    )


@pytest.mark.parametrize(
    'method, resource_name, expected_result',
    (
        ('is_container', 'foo', True),
        ('is_container', 'foo/test_file.foo', False),
        ('get_container', 'foo/test_file.foo', 'foo'),
        ('get_container', 'foo', ''),
        ('is_file', 'foo/test_file.foo', True),
        ('is_file', 'foo', False),
        ('exists', 'foo/test_file.foo', True),
        ('exists', 'foo/bar', False),
    )
)
def test_accessor(
    method, resource_name, expected_result, proxy_location, resource_folder
):
    '''Test accessor methods.'''
    argument = os.path.join(
        resource_folder, resource_name
    )
    result = getattr(proxy_location.accessor, method)(argument)
    assert result == expected_result


def test_accessor_list(proxy_location, resource_folder):
    '''Test listing files using proxy location.'''
    files = set(
        proxy_location.accessor.list(
            os.path.join(resource_folder, 'foo')
        )
    )
    for file_name in (
        'test_sequence.0001.bar', 'test_sequence.0002.bar',
        'test_sequence.0003.bar', 'test_file.foo'
    ):
        assert os.path.join(resource_folder, 'foo', file_name) in files


def test_make_and_remove_container(proxy_location, resource_folder):
    '''Test make and remove container functions on proxy location.'''
    folder_name = str(uuid.uuid1())
    folder_path = os.path.join(resource_folder, folder_name)
    assert os.path.isdir(folder_path) is False

    proxy_location.accessor.make_container(folder_name)
    assert os.path.isdir(folder_path) is True

    proxy_location.accessor.remove_container(folder_name)
    assert os.path.isdir(folder_path) is False


def test_open(proxy_location):
    '''Test open function on accessor.'''
    file_handle = proxy_location.accessor.open(
        os.path.join('foo', 'test_file.foo'), 'r'
    )
    assert file_handle.read() == 'bar'


def test_remove(proxy_location, resource_folder):
    '''Test removing a file.'''
    new_file_path = os.path.join(resource_folder, 'foo', 'new_file.foo')
    file_handle = proxy_location.accessor.open(
        new_file_path, 'w'
    )
    file_handle.close()
    assert os.path.exists(new_file_path) is True

    proxy_location.accessor.remove(new_file_path)
    assert os.path.exists(new_file_path) is False


def test_get_filesystem_path(proxy_location, resource_folder):
    '''Test getting a file system path from proxy location.'''
    file_name = os.path.join('foo', 'test_file.foo')
    assert proxy_location.accessor.get_filesystem_path(
        file_name
    ) == os.path.join(resource_folder, file_name)


def test_structure_file_component(proxy_location):
    '''Test proxied structure plugin with a file component.'''
    session = proxy_location.session
    file_component = session.create(
        'FileComponent', {'name': 'foo', 'file_type': '.bar'}
    )
    session.commit()
    resource_identifier = (
        os.path.sep.join(list(file_component['id'][:5])) +
        file_component['id'][5:] + '.bar'
    )
    assert (
        resource_identifier ==
        proxy_location.structure.get_resource_identifier(file_component)
    )


def test_structure_sequence_component(proxy_location):
    '''Test proxied structure plugin with a sequence component.'''
    session = proxy_location.session
    sequence_component = session.create(
        'SequenceComponent', {'name': 'foo', 'file_type': '.bar', 'padding': 4}
    )
    session.commit()
    resource_identifier = (
        os.path.sep.join(list(sequence_component['id'][:5])) +
        sequence_component['id'][5:] + os.path.sep + 'file.%04d.bar'
    )
    assert (
        resource_identifier ==
        proxy_location.structure.get_resource_identifier(sequence_component)
    )


def test_plugin_setup():
    '''Test that the setup is stable and works as expected.'''
    location_name = 'ftrack-location-compatibility-test'

    compatibility_plugin_path = os.path.normpath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            '..',
            'hook'
        )
    )
    resource_test_path = os.path.normpath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'resource',
            'legacy_location_plugin'
        )
    )
    session = ftrack_api.Session(
        plugin_paths=[compatibility_plugin_path]
    )
    session.ensure(
        'Location', {'name': location_name}, ['name']
    )
    ftrack.LOCATION_PLUGINS.paths.append(
        resource_test_path
    )
    ftrack.EVENT_HANDLERS.paths.append(
        compatibility_plugin_path
    )
    ftrack.setup()

    location = session.query(
        'Location where name is "{0}"'.format(location_name)
    ).one()

    assert isinstance(
        location.accessor,
        ftrack_location_compatibility.plugin.ProxyAccessor
    )


def test_origin_location(session):
    '''Test that origin location is not proxied.'''
    origin = session.query(
        'Location where name is "ftrack.origin"'
    ).one()

    assert not isinstance(
        origin.accessor,
        ftrack_location_compatibility.plugin.ProxyAccessor
    )


def test_unamanged_location(session):
    '''Test that the un-managed location is proxied.'''
    location = session.query(
        'Location where name is "ftrack.unmanaged"'
    ).one()

    assert isinstance(
        location.accessor,
        ftrack_location_compatibility.plugin.ProxyAccessor
    )

    test_disk = None
    for disk in session.query('select unix, windows from Disk'):
        if disk['unix'] and disk['windows'] and disk['unix'] != disk['windows']:
            test_disk = disk
            break

    assert test_disk

    name = 'test-location-compatibility-' + str(uuid.uuid1())

    project = session.create('Project', {
        'full_name': name,
        'name': name,
        'start': datetime.date.today(),
        'end': datetime.date.today() + datetime.timedelta(days=1)
    })

    asset = session.create('Asset', {
        'context_id': project['id'],
        'name': name,
        'type': session.query('AssetType').first()
    })
    version = session.create('AssetVersion', {'asset': asset})

    session.commit()

    # Allow testing on both windows and mac/linux platforms.
    if platform.system() == 'Windows':
        from_prefix = test_disk['unix']
        to_prefix = test_disk['windows']
    else:
        from_prefix = test_disk['windows']
        to_prefix = test_disk['unix']

    path = os.path.normpath(
        '{0}\\path\\to\\a\\file.png'.format(from_prefix)
    )

    component = session.create_component(
        path=path,
        data={'version': version},
        location=location
    )

    translated_path = location.get_filesystem_path(component)
    assert translated_path.startswith(to_prefix)
