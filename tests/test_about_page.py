#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home_page import Home
from pages.link_crawler import LinkCrawler

from axe_selenium_python.test_accessibility_rules import report, rules
from axe_selenium_python import Axe


class TestAboutPage:

    @pytest.mark.nondestructive
    def test_about_page(self, base_url, selenium, pytestconfig):
        home_page = Home(base_url, selenium)
        about_mozillians_page = home_page.footer.click_about_link()

        # Run aXe against page and store results
        axe = Axe(selenium)
        pytestconfig.data = axe.execute()

        assert about_mozillians_page.is_privacy_section_present
        assert about_mozillians_page.is_get_involved_section_present

    @pytest.mark.parametrize("rule", rules)
    @pytest.mark.nondestructive
    def test_accessibility_rules(self, pytestconfig, rule):
        violations = dict((k['id'], k) for k in pytestconfig.data['violations'])
        if(rule in violations):
            TestAboutPage.test_accessibility_rules.__func__.__doc__ = violations[rule]['help']
        assert rule not in violations, report(violations[rule])

    @pytest.mark.nondestructive
    @pytest.mark.xfail
    def test_that_links_in_the_about_page_return_200_code(self, base_url):
        crawler = LinkCrawler(base_url)
        urls = crawler.collect_links('/about', id='main')
        bad_urls = []

        assert len(urls) > 0

        for url in urls:
            check_result = crawler.verify_status_code_is_ok(url)
            if check_result is not True:
                bad_urls.append(check_result)

        assert 0 == len(bad_urls), u'%s bad links found. ' % len(bad_urls) + ', '.join(bad_urls)
