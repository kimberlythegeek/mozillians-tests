#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home_page import Home
from pages.link_crawler import LinkCrawler
# from axe_selenium_python.test_accessibility_rules import TestAccessibility
from axe_selenium_python import Axe

def report(rule):
    # return json.dumps(rule, indent=4, sort_keys=True)
    string = '\n\n\nRule Violated:\n' + rule['id'] + ' - ' + rule['description'] + \
        '\n\tURL: ' + rule['helpUrl'] + \
        '\n\tImpact Level: ' + rule['impact'] + \
        '\n\tTags:'
    for tag in rule['tags']:
        string += ' ' + tag
    string += '\n\tElements Affected:'
    i = 1
    for node in rule['nodes']:
        for target in node['target']:
            string += '\n\t' + str(i) + ') Target: ' + target
            i += 1
        for item in node['all']:
            string += '\n\t\t' + item['message']
        for item in node['any']:
            string += '\n\t\t' + item['message']
        for item in node['none']:
            string += '\n\t\t' + item['message']
    string += '\n\n\n'
    return string




class TestAboutPage:

    @pytest.mark.nondestructive
    def test_about_page(self, base_url, selenium, pytestconfig):
        home_page = Home(base_url, selenium)
        about_mozillians_page = home_page.footer.click_about_link()
        axe = Axe(selenium)
        pytestconfig.data = axe.execute()
        assert about_mozillians_page.is_privacy_section_present
        assert about_mozillians_page.is_get_involved_section_present


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

class TestAccessibility:

    # Acessibility Rule IDs used to generate a test for each rule
    # https://github.com/dequelabs/axe-core/blob/master/doc/rule-descriptions.md
    _rules = [
        'accesskeys',
        'area-alt',
        'aria-allowed-attr',
        'aria-hidden-body',
        'aria-required-attr',
        'aria-required-children',
        'aria-required-parent',
        'aria-roles',
        'aria-valid-attr-value',
        'aria-valid-attr',
        'audio-caption',
        'blink',
        'button-name',
        'bypass',
        'checkboxgroup',
        'color-contrast',
        'definition-list',
        'dlitem',
        'document-title',
        'duplicate-id',
        'empty-heading',
        'frame-title-unique',
        'frame-title',
        'heading-order',
        'hidden-content',
        'href-no-hash',
        'html-has-lang',
        'html-lang-valid',
        'image-alt',
        'image-redundant-alt',
        'input-image-alt',
        'label-title-only',
        'label',
        'layout-table',
        'link-in-text-block',
        'link-name',
        'list',
        'listitem',
        'marquee',
        'meta-refresh',
        'meta-viewport-large',
        'meta-viewport',
        'object-alt',
        'p-as-heading',
        'radiogroup',
        'region',
        'scope-attr-valid',
        'server-side-image-map',
        'skip-link',
        'tabindex',
        'table-duplicate-name',
        'table-fake-caption',
        'td-has-header',
        'td-headers-attr',
        'th-has-data-cells',
        'valid-lang',
        'video-caption',
        'video-description'
    ]

    @pytest.mark.parametrize("rule", _rules)
    @pytest.mark.nondestructive
    def test_accessibility_rules(self, pytestconfig, rule):
        violations = dict((k['id'], k) for k in pytestconfig.data['violations'])
        if(rule in violations):
            TestAccessibility.test_accessibility_rules.__func__.__doc__ = violations[rule]['help']
        assert rule not in violations, report(violations[rule])
