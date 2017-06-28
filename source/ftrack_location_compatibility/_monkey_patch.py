import logging
import functools

global _discoverd_plugins
_discovered_plugins = dict()

logger = logging.getLogger(
    'ftrack-location-compatibility-' + __name__
)

def patch_legacy_api():
    import ftrack

    functools.wraps(ftrack.EVENT_HUB.connect)
    def connect(*args, **kwargs):
        if ftrack.EVENT_HUB.connected:
            return

        try:
            return ftrack.EVENT_HUB._connect()

        except Exception as e:
            raise e

    # patch connect to not raise an exception if already connected
    ftrack.EVENT_HUB._connect = ftrack.EVENT_HUB.connect
    ftrack.EVENT_HUB.connect = connect

    def discover(register, **kwargs):
        global _discovered_plugins

        _discovered_plugins.setdefault(
            id(register), set()
        )

        register.paths = list(
            set(register.paths) - _discovered_plugins.get(id(register))
        )

        register._discover(**kwargs)

        _discovered_plugins[id(register)] = _discovered_plugins.get(id(register)).union(
            set(register.paths)
        )

    # patch discover for LOCATION_PLUGINS and EVENT_HANDLERS in order to
    # allow calling setup multiple times.
    for register in (ftrack.LOCATION_PLUGINS, ftrack.EVENT_HANDLERS):
        register._discover = register.discover

        register.discover = (
            lambda x=register, **kwargs: discover(x, **kwargs)
        )

    logger.warning(
        'Patched legacy setup function to allow multiple calls.'
    )