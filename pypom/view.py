# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .interfaces import IDriver


class WebView(object):

    def __init__(self, driver, timeout):
        self.driver = driver
        self.driver_adapter = IDriver(driver)
        self.timeout = timeout
        self.wait = self.driver_adapter.wait_factory(self.timeout)

    def find_element(self, strategy, locator, root=None):
        """Finds an element on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: :py:class:`~selenium.webdriver.remote.webelement.WebElement` object.
        :rtype: selenium.webdriver.remote.webelement.WebElement

        """
        return self.driver_adapter.find_element(strategy, locator, root=root)

    def find_elements(self, strategy, locator, root=None):
        """Finds elements on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target elements.
        :type strategy: str
        :type locator: str
        :return: List of :py:class:`~selenium.webdriver.remote.webelement.WebElement` objects.
        :rtype: list

        """
        return self.driver_adapter.find_elements(strategy, locator, root=root)

    def is_element_present(self, strategy, locator, root=None):
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_present(strategy, locator, root=root)

    def is_element_displayed(self, strategy, locator, root=None):
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_displayed(strategy, locator, root=root)
