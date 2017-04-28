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

    .. change:: fixed

        Registering legacy locations are very slow.

    .. change:: new

        Provide build_plugin command to produce redistributable builds.

.. release:: 0.1.0
    :date: 2017-01-19

    .. change:: new

        Initial release of ftrack location compatibility.
