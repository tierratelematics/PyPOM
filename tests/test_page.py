# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

import pytest

from pypom import Page
from .util import (
    skip_not_selenium,
    skip_not_splinter,
)


def test_base_url(base_url, page):
    assert base_url == page.seed_url


def test_seed_url_absolute(base_url, driver):
    url_template = 'https://www.test.com/'

    class MyPage(Page):
        URL_TEMPLATE = url_template
    page = MyPage(driver, base_url)
    assert url_template == page.seed_url


def test_seed_url_absolute_keywords(base_url, driver):
    value = str(random.random())
    absolute_url = 'https://www.test.com/'

    class MyPage(Page):
        URL_TEMPLATE = absolute_url + '{key}'
    page = MyPage(driver, base_url, key=value)
    assert absolute_url + value == page.seed_url


def test_seed_url_empty(driver):
    page = Page(driver)
    assert page.seed_url is None


def test_seed_url_keywords(base_url, driver):
    value = str(random.random())

    class MyPage(Page):
        URL_TEMPLATE = '{key}'
    page = MyPage(driver, base_url, key=value)
    assert base_url + value == page.seed_url


def test_seed_url_prepend(base_url, driver):
    url_template = str(random.random())

    class MyPage(Page):
        URL_TEMPLATE = url_template
    page = MyPage(driver, base_url)
    assert base_url + url_template == page.seed_url


def test_open(page, driver):
    assert isinstance(page.open(), Page)


def test_open_seed_url_none(driver):
    from pypom.exception import UsageError
    page = Page(driver)
    with pytest.raises(UsageError):
        page.open()


def test_open_timeout(base_url, driver):

    class MyPage(Page):
        def wait_for_page_to_load(self):
            self.wait.until(lambda s: False)
    page = MyPage(driver, base_url, timeout=0)
    from selenium.common.exceptions import TimeoutException
    with pytest.raises(TimeoutException):
        page.open()


def test_wait_for_page(page, driver):
    assert isinstance(page.wait_for_page_to_load(), Page)


def test_wait_for_page_timeout(base_url, driver):

    class MyPage(Page):
        def wait_for_page_to_load(self):
            self.wait.until(lambda s: False)
    page = MyPage(driver, base_url, timeout=0)
    from selenium.common.exceptions import TimeoutException
    with pytest.raises(TimeoutException):
        page.wait_for_page_to_load()


def test_wait_for_page_empty_base_url(driver):
    assert isinstance(Page(driver).wait_for_page_to_load(), Page)


def test_find_element_selenium(page, driver, driver_interface):
    skip_not_selenium(driver_interface)

    locator = (str(random.random()), str(random.random()))
    page.find_element(*locator)
    driver.find_element.assert_called_once_with(*locator)


def test_find_element_splinter(page, driver, driver_interface, splinter_strategy):
    skip_not_splinter(driver_interface)

    locator = (splinter_strategy, str(random.random()))
    page.find_element(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_find_elements_selenium(page, driver, driver_interface):
    skip_not_selenium(driver_interface)

    locator = (str(random.random()), str(random.random()))
    page.find_elements(*locator)
    driver.find_elements.assert_called_once_with(*locator)


def test_find_elements_splinter(page, driver, driver_interface, splinter_strategy):
    skip_not_splinter(driver_interface)

    locator = (splinter_strategy, str(random.random()))
    page.find_elements(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_is_element_present_selenium(page, driver, driver_interface):
    skip_not_selenium(driver_interface)

    locator = (str(random.random()), str(random.random()))
    assert page.is_element_present(*locator)
    driver.find_element.assert_called_once_with(*locator)


def test_is_element_present_splinter(page, driver, driver_interface, splinter_strategy):
    skip_not_splinter(driver_interface)

    locator = (splinter_strategy, str(random.random()))
    from splinter.element_list import ElementList
    from mock import Mock
    page.driver.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([Mock()])})
    assert page.is_element_present(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_is_element_present_not_present_selenium(page, driver, driver_interface):
    skip_not_selenium(driver_interface)

    locator = (str(random.random()), str(random.random()))
    from selenium.common.exceptions import NoSuchElementException
    driver.find_element.side_effect = NoSuchElementException()
    assert not page.is_element_present(*locator)
    driver.find_element.assert_called_once_with(*locator)


def test_is_element_present_not_present_splinter(page, driver, driver_interface, splinter_strategy):
    skip_not_splinter(driver_interface)

    locator = (splinter_strategy, str(random.random()))
    from splinter.element_list import ElementList
    page.driver.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([])})
    assert not page.is_element_present(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_is_element_displayed_selenium(page, driver, driver_interface):
    skip_not_selenium(driver_interface)

    locator = (str(random.random()), str(random.random()))
    assert page.is_element_displayed(*locator)
    driver.find_element.assert_called_once_with(*locator)


def test_is_element_displayed_splinter(page, driver, driver_interface, splinter_strategy):
    skip_not_splinter(driver_interface)

    locator = (splinter_strategy, str(random.random()))

    from mock import PropertyMock
    visible_mock = PropertyMock(return_value=True)
    page.driver.configure_mock(**{'find_by_{0}.return_value.first.visible'.format(splinter_strategy): visible_mock})
    type(getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).return_value.first).visible = visible_mock
    assert page.is_element_displayed(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])
    visible_mock.assert_called_with()


def test_is_element_displayed_not_present_selenium(page, driver, driver_interface):
    skip_not_selenium(driver_interface)

    locator = (str(random.random()), str(random.random()))
    from selenium.common.exceptions import NoSuchElementException
    driver.find_element.side_effect = NoSuchElementException()
    assert not page.is_element_displayed(*locator)
    driver.find_element.assert_called_once_with(*locator)
    driver.find_element.is_displayed.assert_not_called()


def test_is_element_displayed_not_present_splinter(page, driver, driver_interface, splinter_strategy):
    skip_not_splinter(driver_interface)

    locator = (splinter_strategy, str(random.random()))
    from splinter.element_list import ElementList
    page.driver.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([])})
    assert not page.is_element_displayed(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_is_element_displayed_not_displayed_selenium(page, driver, driver_interface):
    skip_not_selenium(driver_interface)

    locator = (str(random.random()), str(random.random()))
    element = driver.find_element()
    element.is_displayed.return_value = False
    assert not page.is_element_displayed(*locator)
    driver.find_element.assert_called_with(*locator)
    element.is_displayed.assert_called_once_with()


def test_is_element_displayed_not_displayed_splinter(page, driver, driver_interface, splinter_strategy):
    skip_not_splinter(driver_interface)

    locator = (splinter_strategy, str(random.random()))

    from mock import PropertyMock
    visible_mock = PropertyMock(return_value=False)
    page.driver.configure_mock(**{'find_by_{0}.return_value.first.visible'.format(splinter_strategy): visible_mock})
    type(getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).return_value.first).visible = visible_mock
    assert not page.is_element_displayed(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])
    visible_mock.assert_called_with()


def test_bwc_selenium(page, driver_interface):
    """ Backwards compatibility with old selenium attribute """
    driver = page.selenium
    assert driver == page.driver
