..
    :copyright: Copyright (c) 2017 ftrack

.. _release/release_notes:

*************
Release Notes
*************

.. release:: Upcoming

    ..change:: changed
        :tags: Setup

        Build resultant folder renamed with the plugin name + version

    ..change:: changed
        :tags: Setup

        Pip compatibility for version 19.3.0 or higher

    ..change:: fixed
        :tags: location, compatibility

        Remove warning for ftrack.connect location.

.. release:: 0.3.1
    :date: 2017-06-28
    .. change:: fixed
        :tags: location, compatibility

        If multiple `ftrack-python-api` sessions were created before
        setup was called from the `ftrack-python-legacy-api` they were not
        all updated with the proxied legacy locations.


    .. change:: fixed
        :tags: logging

        Incorrect logging output when setting up proxy for the unmanaged
        location.

.. release:: 0.3.0
    :date: 2017-04-03
    
    .. change:: new
        :tags: location, compatibility

        Proxy the unmanaged location using the legacy API, since the
        ftrack-python-api does not translate paths between operating systems
        using ftrack disks.

.. release:: 0.2.0
    :date: 2017-03-24

    .. change:: fixed
        :tags: performance

        Registering legacy locations are very slow.

    .. change:: new
        :tags: build

        Provide build_plugin command to produce redistributable builds.

.. release:: 0.1.0
    :date: 2017-01-19

    .. change:: new
        :tags: location, compatibility

        Initial release of ftrack location compatibility.
