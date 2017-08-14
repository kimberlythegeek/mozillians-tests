#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import uuid
import pytest

from pages.home_page import Home

from axe_selenium_python.test_accessibility import report, rules

def set_docstring(rule, violations, function):
    if(rule in violations):
        # Set docstring to description of current rule
        function.__func__.__doc__ = violations[rule]['help']

_MAIN_CONTENT = '#main'


class TestAccessibility:

    def test_header_footer_run_axe(self, base_url, selenium, pytestconfig, axe):
        home_page = Home(base_url, selenium)    # NOQA

        # Run aXe and store data in pytestconfig
        pytestconfig.header = axe.run('header')
        pytestconfig.footer = axe.run('footer')

        assert pytestconfig.header is not None
        assert pytestconfig.footer is not None

    @pytest.mark.parametrize("rule", rules)
    def test_header_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.header
        set_docstring(rule, violations, TestAccessibility.test_header_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.parametrize("rule", rules)
    def test_footer_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.footer
        set_docstring(rule, violations, TestAccessibility.test_footer_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.credentials
    def test_header_footer_when_logged_in_run_axe(self, base_url, selenium, vouched_user, pytestconfig, axe):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        # Run aXe and store data in pytestconfig
        pytestconfig.header_logged_in = axe.run('header')
        pytestconfig.footer_logged_in = axe.run('footer')

        assert pytestconfig.header_logged_in is not None
        assert pytestconfig.footer_logged_in is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_header_when_logged_in_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.header_logged_in
        set_docstring(rule, violations, TestAccessibility.test_header_when_logged_in_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_footer_when_logged_in_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.footer_logged_in
        set_docstring(rule, violations, TestAccessibility.test_footer_when_logged_in_accessibility)
        assert rule not in violations, report(violations[rule])

    def test_home_page_run_axe(self, base_url, selenium, pytestconfig, axe):
        home_page = Home(base_url, selenium)    # NOQA

        # Run aXe and store data in pytestconfig
        pytestconfig.home_page = axe.run(_MAIN_CONTENT)

        assert pytestconfig.home_page is not None

    @pytest.mark.parametrize("rule", rules)
    def test_home_page_accessibility(self, pytestconfig, rule):

        violations = pytestconfig.home_page
        set_docstring(rule, violations, TestAccessibility.test_home_page_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.credentials
    def test_home_page_when_logged_in_run_axe(self, base_url, selenium, vouched_user, pytestconfig, axe):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        # Run aXe and store data in pytestconfig
        pytestconfig.home_page_logged_in = axe.run(_MAIN_CONTENT)

        assert pytestconfig.home_page_logged_in is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_home_page_when_logged_in_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.home_page_logged_in
        set_docstring(rule, violations, TestAccessibility.test_home_page_when_logged_in_accessibility)
        assert rule not in violations, report(violations[rule])

    def test_about_page_run_axe(self, base_url, selenium, pytestconfig, axe):
        home_page = Home(base_url, selenium)
        home_page.footer.click_about_link()

        # Run aXe and store data in pytestconfig
        pytestconfig.about_page = axe.run(_MAIN_CONTENT)

        assert pytestconfig.about_page is not None

    @pytest.mark.parametrize("rule", rules)
    def test_about_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.about_page
        set_docstring(rule, violations, TestAccessibility.test_about_page_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.credentials
    def test_settings_page_run_axe(self, base_url, selenium, vouched_user, axe, pytestconfig):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        home_page.header.click_settings_menu_item()

        # Run aXe and store data in pytestconfig
        pytestconfig.settings_page = axe.run(_MAIN_CONTENT)

        assert pytestconfig.settings_page is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_settings_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.settings_page
        set_docstring(rule, violations, TestAccessibility.test_settings_page_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.credentials
    def test_group_create_page_run_axe(self, base_url, selenium, vouched_user, axe, pytestconfig):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        # Create a new group
        group_name = str(uuid.uuid4())
        settings = home_page.header.click_settings_menu_item()
        group = settings.create_group(group_name)

        # Run aXe and store data in pytestconfig
        pytestconfig.group_create_page = axe.run(_MAIN_CONTENT)

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

        # Run aXe and store data in pytestconfig
        pytestconfig.group_search = axe.run(_MAIN_CONTENT)

        assert pytestconfig.group_create_page is not None
        assert pytestconfig.group_search is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_group_create_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.group_create_page
        set_docstring(rule, violations, TestAccessibility.test_group_create_page_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_group_search_when_logged_in_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.group_search
        set_docstring(rule, violations, TestAccessibility.test_group_search_when_logged_in_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.credentials
    def test_group_invitations_run_axe(self, base_url, selenium, vouched_user, axe, pytestconfig):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        # Create a new group
        group_name = str(uuid.uuid4())
        settings = home_page.header.click_settings_menu_item()
        group = settings.create_group(group_name)

        # Invite a new member
        invite = group.invitations.invite
        # Run aXe and store data in pytestconfig
        pytestconfig.group_invite = axe.run(_MAIN_CONTENT)
        new_member = "Test User"
        invite.invite_new_member(new_member)
        invite.click_invite()

        # Check if the pending invitation exists
        invitations = group.invitations.invitations_list
        # Run aXe and store data in pytestconfig
        pytestconfig.group_invitations = axe.run(_MAIN_CONTENT)

        assert pytestconfig.group_invite is not None
        assert pytestconfig.group_invitations is not None

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_group_invite_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.group_invite
        set_docstring(rule, violations, TestAccessibility.test_group_invite_page_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_group_invitations_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.group_invitations
        set_docstring(rule, violations, TestAccessibility.test_group_invitations_page_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.credentials
    def test_invite_page_run_axe(self, base_url, selenium, vouched_user, axe, pytestconfig):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        invite_page = home_page.header.click_invite_menu_item()

        # Run aXe and store data in pytestconfig
        pytestconfig.invite_page = axe.run(_MAIN_CONTENT)

        email_address = "user@example.com"
        invite_page.invite(email_address, 'Just a bot sending a test invite to a test account.')

        # Run aXe and store data in pytestconfig
        pytestconfig.invite_success_page = axe.run(_MAIN_CONTENT)

        assert pytestconfig.invite_page is not None
        assert pytestconfig.invite_success_page is not None


    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_invite_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.invite_page
        set_docstring(rule, violations, TestAccessibility.test_invite_page_accessibility)
        assert rule not in violations, report(violations[rule])

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.credentials
    def test_invite_success_page_accessibility(self, pytestconfig, rule):
        violations = pytestconfig.invite_success_page
        set_docstring(rule, violations, TestAccessibility.test_invite_success_page_accessibility)
        assert rule not in violations, report(violations[rule])
