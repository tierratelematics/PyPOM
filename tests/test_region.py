# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from mock import (
    Mock,
    MagicMock,
    patch,
)
from pypom import Region
import pytest
from .util import (
    skip_not_selenium,
    skip_not_splinter,
)


class TestWaitForRegion:

    def test_wait_for_region(self, page):
        assert isinstance(Region(page).wait_for_region_to_load(), Region)

    def test_wait_for_region_timeout(self, page):
        class MyRegion(Region):
            def wait_for_region_to_load(self):
                self.wait.until(lambda s: False)
        page.timeout = 0
        from selenium.common.exceptions import TimeoutException
        with pytest.raises(TimeoutException):
            MyRegion(page)


class TestNoRoot:

    def test_root(self, page):
        assert Region(page).root is None

    def test_find_element(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        Region(page).find_element(*locator)
        selenium.find_element.assert_called_once_with(*locator)

    def test_find_elements(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        Region(page).find_elements(*locator)
        selenium.find_elements.assert_called_once_with(*locator)

    def test_is_element_displayed(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        assert Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed_not_present(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        selenium.find_element.side_effect = NoSuchElementException()
        assert not Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*locator)
        selenium.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden_selenium(self, page, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        locator = (str(random.random()), str(random.random()))
        hidden_element = selenium.find_element()
        hidden_element.is_displayed.return_value = False
        assert not Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_with(*locator)
        hidden_element.is_displayed.assert_called_once_with()


class TestNoRootSplinter:

    def test_is_element_displayed_hidden_splinter(self, page, selenium, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        locator = (splinter_strategy, str(random.random()))
        hidden_element = selenium.find_element()
        hidden_element.is_displayed.return_value = False
        region = Region(page)
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=Mock()) as mock_find_element:
            visible_mock = Mock().visible.return_value = False
            first_mock = Mock().first.return_value = visible_mock
            mock_find_element.return_value = first_mock
            assert not region.is_element_displayed(*locator)


class TestRootElement:

    def test_root(self, page, selenium):
        element = Mock()
        assert Region(page, root=element).root == element

    def test_find_element_selenium(self, page, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        Region(page, root=root_element).find_element(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_find_elements_selenium(self, page, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        Region(page, root=root_element).find_elements(*locator)
        root_element.find_elements.assert_called_once_with(*locator)
        selenium.find_elements.assert_not_called()

    def test_is_element_present_selenium(self, page, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        assert Region(page, root=root_element).is_element_present(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_present_not_preset_selenium(self, page, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        root_element.find_element.side_effect = NoSuchElementException()
        assert not Region(page, root=root_element).is_element_present(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_displayed_selenium(self, page, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        assert Region(page, root=root_element).is_element_displayed(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_displayed_not_present_selenium(self, page, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        root_element.find_element.side_effect = NoSuchElementException()
        region = Region(page, root=root_element)
        assert not region.is_element_displayed(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        root_element.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden_selenium(self, page, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        hidden_element = root_element.find_element()
        hidden_element.is_displayed.return_value = False
        region = Region(page, root=root_element)
        assert not region.is_element_displayed(*locator)
        root_element.find_element.assert_called_with(*locator)
        hidden_element.is_displayed.assert_called_once_with()


class TestRootElementSplinter:

    def test_find_element_splinter(self, page, selenium, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        root_element = MagicMock()
        root_element.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): Mock()})
        locator = (splinter_strategy, str(random.random()))
        Region(page, root=root_element).find_element(*locator)
        getattr(root_element, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_find_elements_splinter(self, page, selenium, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        root_element = MagicMock()
        root_element.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): Mock()})
        locator = (splinter_strategy, str(random.random()))
        Region(page, root=root_element).find_elements(*locator)
        getattr(root_element, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_is_element_present_splinter(self, page, selenium, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        root_element = Mock()
        locator = (splinter_strategy, str(random.random()))
        from splinter.element_list import ElementList
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=MagicMock()) as mock_find_element:
            mock_find_element.return_value = ElementList([Mock()])
            assert Region(page, root=root_element).is_element_present(*locator)
            mock_find_element.assert_called_once_with(*locator, root=root_element)

    def test_is_element_present_not_preset_splinter(self, page, selenium, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        root_element = MagicMock()
        from splinter.element_list import ElementList
        root_element.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([])})
        locator = (splinter_strategy, str(random.random()))
        assert not Region(page, root=root_element).is_element_present(*locator)

    def test_is_element_displayed_splinter(self, page, selenium, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        root_element = MagicMock()
        root_element.configure_mock(**{'find_by_{0}.return_value.first.visible.return_value'.format(splinter_strategy): True})
        locator = (splinter_strategy, str(random.random()))
        region = Region(page, root=root_element)
        assert region.is_element_displayed(*locator)

    def test_is_element_displayed_not_present_splinter(self, page, selenium, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        root_element = Mock()
        locator = (splinter_strategy, str(random.random()))
        region = Region(page, root=root_element)
        from splinter.element_list import ElementList
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=MagicMock()) as mock_find_element:
            mock_find_element.return_value = ElementList([])
            assert not region.is_element_displayed(*locator)

    def test_is_element_displayed_hidden_splinter(self, page, selenium, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        root_element = MagicMock()
        root_element.configure_mock(**{'find_by_{0}.return_value.first.visible.return_value'.format(splinter_strategy): False})
        locator = (splinter_strategy, str(random.random()))
        region = Region(page, root=root_element)
        assert not region.is_element_displayed(*locator)


class TestRootLocator:

    @pytest.fixture
    def region(self, page):
        class MyRegion(Region):
            _root_locator = (str(random.random()), str(random.random()))
        return MyRegion(page)

    def test_root_selenium(self, element, region, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        assert element == region.root
        selenium.find_element.assert_called_once_with(*region._root_locator)

    def test_find_element_selenium(self, element, region, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        locator = (str(random.random()), str(random.random()))
        region.find_element(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_find_elements_selenium(self, element, region, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        locator = (str(random.random()), str(random.random()))
        region.find_elements(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_elements.assert_called_once_with(*locator)

    def test_is_element_present_selenium(self, element, region, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        locator = (str(random.random()), str(random.random()))
        assert region.is_element_present(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_present_not_present_selenium(self, element, region, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        element.find_element.side_effect = NoSuchElementException()
        assert not region.is_element_present(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed_selenium(self, element, region, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        locator = (str(random.random()), str(random.random()))
        assert region.is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed_not_present_selenium(self, element, region, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        element.find_element.side_effect = NoSuchElementException()
        assert not region.is_element_displayed(*locator)
        element.find_element.assert_called_once_with(*locator)
        element.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden_selenium(self, element, region, selenium, driver_interface):
        skip_not_selenium(driver_interface)

        locator = (str(random.random()), str(random.random()))
        hidden_element = element.find_element()
        hidden_element.is_displayed.return_value = False
        assert not region.is_element_displayed(*locator)
        element.find_element.assert_called_with(*locator)
        hidden_element.is_displayed.assert_called_once_with()


class TestRootLocatorSplinter:

    @pytest.fixture
    def region(self, page, splinter_strategy):
        class MyRegion(Region):
            _root_locator = (splinter_strategy, str(random.random()))
        return MyRegion(page)

    def test_root_splinter(self, region, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        region.root
        getattr(region.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(region._root_locator[1])

    def test_find_element_splinter(self, region, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        locator = (splinter_strategy, str(random.random()))
        region.find_element(*locator)

        getattr(region.root, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_find_elements_splinter(self, region, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        locator = (splinter_strategy, str(random.random()))
        region.find_elements(*locator)

        getattr(region.root, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_is_element_present_splinter(self, region, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        assert region._root_locator[0] == splinter_strategy
        locator = (splinter_strategy, str(random.random()))

        assert region.is_element_present(*locator)
        getattr(region.root, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_is_element_present_not_present_splinter(self, region, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        from splinter.element_list import ElementList
        locator = (splinter_strategy, str(random.random()))
        with patch('pypom.splinter_driver.Splinter.find_elements', new_callable=MagicMock()) as mock_find_elements:
            mock_find_elements.return_value = ElementList([])
            assert not region.is_element_present(*locator)

    def test_is_element_displayed_splinter(self, region, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        locator = (splinter_strategy, str(random.random()))
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=MagicMock()) as mock_find_element:
            mock_find_element.return_value.first.visible.return_value = True
            assert region.is_element_displayed(*locator)

    def test_is_element_displayed_not_present_splinter(self, region, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        locator = (splinter_strategy, str(random.random()))
        from splinter.element_list import ElementList
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=Mock()) as mock_find_element:
            mock_find_element.return_value = ElementList([])
            assert not region.is_element_displayed(*locator)

    def test_is_element_displayed_hidden_splinter(self, region, driver_interface, splinter_strategy):
        skip_not_splinter(driver_interface)

        locator = (splinter_strategy, str(random.random()))
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=Mock()) as mock_find_element:
            visible_mock = Mock().visible.return_value = False
            first_mock = Mock().first.return_value = visible_mock
            mock_find_element.return_value = first_mock
            assert not region.is_element_displayed(*locator)
