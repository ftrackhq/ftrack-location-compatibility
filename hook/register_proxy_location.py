# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import sys
import logging

import ftrack_api
import ftrack

try:
    import ftrack_location_compatibility
except ImportError:
    dependencies_path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), '..', 'package')
    )
    sys.path.append(dependencies_path)
    import ftrack_location_compatibility


logger = logging.getLogger('ftrack-location-compatibility-register')


def new_api_event_listener(event):
    '''Handle *event*.'''
    session = event['data']['session']

    # Store session on cached module.
    ftrack_location_compatibility.session = session

    if ftrack_location_compatibility.is_legacy_location_registered:
        logger.debug(
            'Called by legacy and new api, continue and register locations.'''
        )
        ftrack_location_compatibility.register_locations(session)


def legacy_location_registered():
    '''Handle legacy locations being registered.'''

    # Store legacy location registry information on cached module.
    ftrack_location_compatibility.is_legacy_location_registered = True

    if ftrack_location_compatibility.session is not None:
        logger.debug(
            'Called by legacy and new api, continue and register locations.'''
        )
        ftrack_location_compatibility.register_locations(
            ftrack_location_compatibility.session
        )


def register(api_object):
    '''Register to *session*.'''
    if isinstance(api_object, ftrack_api.Session):
        logger.debug('Register called for session.')
        session = api_object
        session.event_hub.subscribe(
            'topic=ftrack.api.session.configure-location',
            new_api_event_listener
        )

    if api_object is ftrack.EVENT_HANDLERS:
        logger.debug('Register called for legacy event handlers registry.')
        legacy_location_registered()
