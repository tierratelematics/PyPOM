from .page import Page  # noqa
from .region import Region  # noqa

try:
    import selenium  # noqa
except ImportError:  # noqa
    pass             # noqa
else:
    from .selenium_driver import register as registerSelenium
    registerSelenium()

try:
    import splinter  # noqa
except ImportError:  # noqa
    pass             # noqa
else:
    from .splinter_driver import register as registerSplinter
    registerSplinter()
