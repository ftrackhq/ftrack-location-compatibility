..
    :copyright: Copyright (c) 2017 ftrack

#############################
ftrack-location-compatibility
#############################

This event plugin is built for the ftrack-python-api and is meant to act as a
bridge between the ftrack legacy and the ftrack-python-api. It allows users to
use fthe ftrack-python-api with location plugins that are only defined for the
legacy ftrack api.

Setup is automatic and works by automatically proxying method calls. It is
applied to ftrack-python-api locations that are not configured with an accessor,
but does have an accessor configured in the legacy api.

.. toctree::
    :maxdepth: 1

    release/index

Installation
============

Checkout and/or install this repository and put the hook directory on the
FTRACK_EVENT_PLUGIN_PATH or as a plugin to ftrack Connect.

.. note::

    Custom legacy api location plugins must be available on the
    `FTRACK_LOCATION_PLUGIN_PATH`.

.. note::

    The ftrack legacy api must be available for import.
