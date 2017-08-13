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

    @pytest.mark.nondestructive
    @pytest.mark.credentials
    def test_settings_page_run_axe(self, base_url, selenium, vouched_user, axe, pytestconfig):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        home_page.header.click_settings_menu_item()
        pytestconfig.settings_page = axe.run()
        assert pytestconfig.settings_page is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.nondestructive
    def test_settings_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.settings_page
        if(rule in violations):
            # Set docstring to description of current rule
            TestAccessibility.test_settings_page_accessibility.__func__.__doc__ = violations[rule]['help']

        assert rule not in violations, report(violations[rule])

    @pytest.mark.nondestructive
    @pytest.mark.credentials
    def test_group_create_page_run_axe(self, base_url, selenium, vouched_user, axe, pytestconfig):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        # Create a new group
        group_name = str(uuid.uuid4())
        settings = home_page.header.click_settings_menu_item()
        settings.create_group(group_name)

        pytestconfig.group_create_page = axe.run()

        # New group data
        new_group_description = 'This is an automated group.'
        new_group_irc_channel = '#testgroup'

        # Update the group description fields
        group_description = group.description.description_info
        group_description.set_description(new_group_description)
        group_description.set_irc_channel(new_group_irc_channel)
        group_description.click_update()

        search_listings = home_page.header.search_for(group_name)
        search_listings.open_group(group_name)

        pytestconfig.group_search = axe.run()

        assert pytestconfig.group_create_page is not None
        assert pytestconfig.group_search is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.nondestructive
    def test_group_create_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.group_create_page
        if(rule in violations):
            # Set docstring to description of current rule
            TestAccessibility.test_group_create_page_accessibility.__func__.__doc__ = violations[rule]['help']

        assert rule not in violations, report(violations[rule])

    @pytest.mark.nondestructive
    @pytest.mark.credentials
    def test_group_search_when_logged_in_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.group_search
        if(rule in violations):
            # Set docstring to description of current rule
            TestAccessibility.test_group_create_page_accessibility.__func__.__doc__ = violations[rule]['help']

        assert rule not in violations, report(violations[rule])
