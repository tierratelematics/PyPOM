from .page import Page  # noqa
from .region import Region  # noqa

try:
    import selenium  # noqa
except ImportError:
    pass
else:
    from .selenium_driver import register
    register()
