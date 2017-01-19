import os

import ftrack


def register(registry):
    '''Register to *registry*.'''
    if not registry is ftrack.LOCATION_PLUGINS:
        return

    registry.add(
        ftrack.Location(
            'ftrack-location-compatibility-test',
            accessor=ftrack.DiskAccessor(
                prefix=os.path.normpath(
                    os.path.dirname(os.path.abspath(__file__))
                )
            ),
            structure=ftrack.IdStructure(),
            priority=150
        )
    )
