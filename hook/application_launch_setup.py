# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import logging
import ftrack

import ftrack_location_compatibility
import ftrack_connect.application

logger = logging.getLogger(
    'ftrack-location-compatibility-application-launch-setup'
)


def setup(event):
    '''Add FTRACK_EVENT_PLUGIN_PATH back to envs when application start.'''
    if 'options' not in event['data']:
        event['data']['options'] = {'env': {}}

    environment = event['data']['options']['env']

    _location_compatibility_hook_path = os.path.normpath(
        os.path.join(
            ftrack_location_compatibility.__file__,
            '..',
            '..',
            '..',
            'hook'
        )
    )

    ftrack_location_compatibility_path = os.path.dirname(
        os.path.join(
            ftrack_location_compatibility.__file__,
            '..',
            'dependencies'
        )
    )

    ftrack.application.appendPath(
        ftrack_location_compatibility_path,
        'PYTHONPATH',
        environment
    )

    location_compatibility_hook_path = os.environ.get(
        'FTRACK_LOCATION_COMPATIBILITY_PLUGIN_PATH',
        _location_compatibility_hook_path
    )

    ftrack_connect.application.appendPath(
        location_compatibility_hook_path,
        'FTRACK_EVENT_PLUGIN_PATH',
        environment
    )

    print 'ENV', environment


def register(registry, **kw):
    '''Register hooks.'''
    logger.debug('Registering application launch setup.')
    # Run when application are launched
    ftrack.EVENT_HUB.subscribe(
        'topic=ftrack.connect.application.launch',
        setup
    )
