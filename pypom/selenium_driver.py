# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from zope.interface import (
    implementer,
    Interface,
)

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import (
    Remote,
    Opera,
)

from .interfaces import IDriver
from .driver import registerDriver


class ISelenium(Interface):
    """ Marker interface for Selenium"""


@implementer(IDriver)
class Selenium(object):

    def __init__(self, driver):
        self.driver = driver

    def wait_factory(self, timeout):
        return WebDriverWait(self.driver, timeout)

    def open(self, url):
        """Open the page.
        Navigates to :py:attr:`url`
        """
        self.driver.get(url)

    def find_element(self, strategy, locator):
        """Finds an element on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: :py:class:`~selenium.webdriver.remote.webelement.WebElement` object.
        :rtype: selenium.webdriver.remote.webelement.WebElement

        """
        return self.driver.find_element(strategy, locator)

    def find_elements(self, strategy, locator):
        """Finds elements on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target elements.
        :type strategy: str
        :type locator: str
        :return: List of :py:class:`~selenium.webdriver.remote.webelement.WebElement` objects.
        :rtype: list

        """
        return self.driver.find_elements(strategy, locator)

    def is_element_present(self, strategy, locator):
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        try:
            return self.find_element(strategy, locator)
        except NoSuchElementException:
            return False

    def is_element_displayed(self, strategy, locator):
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        try:
            return self.find_element(strategy, locator).is_displayed()
        except NoSuchElementException:
            return False


def register():
    """ Register driver implementation"""
    registerDriver(
        ISelenium,
        Selenium,
        class_implements=[
            Remote,
            Opera,
        ])
