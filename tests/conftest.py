# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mock import Mock
import pytest
from pypom.selenium_driver import ISelenium
from pypom.splinter_driver import (
    ISplinter,
    ALLOWED_STRATEGIES,
)
from zope.interface import alsoProvides


@pytest.fixture
def base_url():
    return 'https://www.mozilla.org/'


@pytest.fixture
def element(selenium):
    element = Mock()
    selenium.find_element.return_value = element
    return element


@pytest.fixture
def page(selenium, base_url):
    from pypom import Page
    return Page(selenium, base_url)


@pytest.fixture(params=[ISelenium, ISplinter])
def driver_interface(request):
    return request.param


@pytest.fixture
def selenium(request, driver_interface):
    mock = Mock()
    alsoProvides(mock, driver_interface)
    return mock


@pytest.fixture(params=ALLOWED_STRATEGIES)
def splinter_strategy(request):
    return request.param
