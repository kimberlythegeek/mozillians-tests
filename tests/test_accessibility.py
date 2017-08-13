#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home_page import Home

from axe_selenium_python.test_accessibility import report, rules


class TestAccessibility:

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_home_page_run_axe(self, base_url, selenium, pytestconfig, axe):
        home_page = Home(base_url, selenium)    # NOQA

        pytestconfig.home_page = axe.run()
        assert pytestconfig.home_page is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_home_page_accessibility(self, pytestconfig, rule):

        violations = pytestconfig.home_page

        if(rule in violations):
            # Set docstring to description of current rule
            TestAccessibility.test_home_page_accessibility.__func__.__doc__ = violations[rule]['help']
        assert rule not in violations, report(violations[rule])

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_home_page_when_logged_in_run_axe(self, base_url, selenium, vouched_user, pytestconfig, axe):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        pytestconfig.home_page_logged_in = axe.run()
        assert pytestconfig.home_page_logged_in is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_home_page_when_logged_in_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.home_page_logged_in
        if(rule in violations):
            # Set docstring to description of current rule
            TestAccessibility.test_home_page_when_logged_in_accessibility.__func__.__doc__ = violations[rule]['help']
        assert rule not in violations, report(violations[rule])

    @pytest.mark.nondestructive
    def test_about_page_run_axe(self, base_url, selenium, pytestconfig, axe):
        home_page = Home(base_url, selenium)
        home_page.footer.click_about_link()
        pytestconfig.about_page = axe.run()

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.nondestructive
    def test_about_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.about_page
        if(rule in violations):
            # Set docstring to description of current rule
            TestAccessibility.test_about_page_accessibility.__func__.__doc__ = violations[rule]['help']

        assert rule not in violations, report(violations[rule])
