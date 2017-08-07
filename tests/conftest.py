# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import uuid
import pytest
from datetime import datetime
from py.xml import html
from tests import restmail


@pytest.fixture(scope='session')
def session_capabilities(pytestconfig, session_capabilities):
    if pytestconfig.getoption('driver') == 'SauceLabs':
        session_capabilities.setdefault('tags', []).append('mozillians')
    return session_capabilities


@pytest.fixture
def capabilities(request, capabilities):
    driver = request.config.getoption('driver')
    if capabilities.get('browserName', driver).lower() == 'firefox':
        capabilities['marionette'] = True
    return capabilities


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium


@pytest.fixture
def new_email():
    return 'mozillians_{0}@restmail.net'.format(uuid.uuid1())


@pytest.fixture
def new_user(new_email):
    return {'email': new_email}


@pytest.fixture
def stored_users(variables):
    return variables['users']


@pytest.fixture
def vouched_user(stored_users):
    return stored_users['vouched']


@pytest.fixture
def private_user(stored_users):
    return stored_users['private']


@pytest.fixture
def unvouched_user(stored_users):
    return stored_users['unvouched']


@pytest.fixture
def login_link(username):
    mail = restmail.get_mail(username)
    mail_content = mail[0]['text'].replace('\n', ' ').replace('amp;', '').split(" ")
    for link in mail_content:
        if link.startswith("https://auth.mozilla.auth0.com/passwordless/verify_redirect"):
            return link

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(0, html.th('Time', class_='sortable time', col='time'))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # add docstring to 'description' column
    report.description = str(item.function.__doc__)
