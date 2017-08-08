#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests


class TestRedirects:

    @pytest.mark.nondestructive
    def test_302_redirect_for_anonymous_users(self, base_url):
        paths = ['/es/country/us/',
                 '/sq/country/doesnotexist/',
                 '/hu/country/us/region/California/',
                 '/pl/country/in/city/Gulbarga/',
                 '/zh-TW/group/webqa/',
                 '/zh-CN/group/258/join/',
                 '/sl/group/doesnotexit/',
                 '/pt-BR/u/moz.mozillians.unvouched/',
                 '/ca/u/UserDoesNotExist/',
                 '/nl/logout/',
                 '/lt/user/edit/',
                 '/en-US/invite/',
                 '/fr/register/']
        urls = self.make_absolute_paths(base_url, paths)
        error_list = self.verify_http_response_codes(urls, 302)
        assert 0 == len(error_list), error_list

    @pytest.mark.nondestructive
    def test_200_for_anonymous_users(self, base_url):
        paths = ['/pl/opensearch.xml', '/nl/u/Mozillians.User/']
        urls = self.make_absolute_paths(base_url, paths)
        error_list = self.verify_http_response_codes(urls, 200)
        assert 0 == len(error_list), error_list

    def make_absolute_paths(self, url, paths):
        urls = []
        for path in paths:
            urls.append(url + path)
        return urls

    def verify_http_response_codes(self, urls, expected_http_value):
        error_list = []
        for url in urls:
            # prevent redirects, we only want the value of the 1st HTTP status
            response = requests.get(url, allow_redirects=False)
            http_status = response.status_code
            if http_status != expected_http_value:
                error_list.append('Expected %s but got %s. %s' %
                                  (expected_http_value, http_status, url))
        return error_list
