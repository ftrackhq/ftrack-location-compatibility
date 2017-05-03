..
    :copyright: Copyright (c) 2017 ftrack

.. _release/release_notes:

*************
Release Notes
*************

.. release:: Upcoming
    
    .. change:: new

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
