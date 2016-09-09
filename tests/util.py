# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


def skip_not_selenium(driver_interface):
    if 'Selenium' not in driver_interface.__identifier__:
        pytest.skip()


def skip_not_splinter(driver_interface):
    if 'Splinter' not in driver_interface.__identifier__:
        pytest.skip()
