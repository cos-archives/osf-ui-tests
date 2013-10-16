"""Tests user access to private projects via the web.

NOTE: The order of tests in this file are significant!

While test ordering is a bad idea (generally speaking), these tests share much
of the same setup and teardown - they require the project be built and added.
The only difference between them is the session state of the user. Since the
tests themselves do not change the state of the application, strict ordering
is an acceptable compromise.

In the future, it might be better to strip session cookies from a requests
response object for each state, then inject them into the WebDriver object for
each test.
"""

import httplib as http

from nose.tools import *

from pages.auth import LoginPage
from pages.exceptions import HttpError
from pages.generic import OsfPage
from pages.helpers import create_user
from pages.project import ProjectPage

# Setup
# This could have been in a ``setup()`` method so that nose would see it as a
# module-level setup method, but then the variables would have to be declared
# with the global keyword. Given a choice between using ``global`` and doing it
# this way, this seemed the least hackish.


contributor = create_user()
noncontributor = create_user()

# log in
global_page = LoginPage().log_in(contributor)

# create a project
global_page = global_page.new_project(title='New Project')

driver = global_page.driver
driver.implicitly_wait(0)

url = global_page.driver.current_url


def teardown():
    """Close the browser"""
    driver.quit()


def test_contributor():
    """A contributor can access the project.

    The existing session is tied to the user who created the project, so no
    setup is needed
    """
    driver.get(url)

    page = ProjectPage(driver=global_page.driver)

    assert_is_instance(page, ProjectPage)


def test_anonymous():
    """An anonymous user cannot access the project.ProjectPage

    Setup consists of logging out of the existing user session (if any)
    """
    page = OsfPage(driver=global_page.driver).log_out()

    page.driver.get(url)

    with assert_raises(HttpError) as cm:
        ProjectPage(driver=page.driver)
    assert_equal(http.UNAUTHORIZED, cm.exception.code)


def test_non_contributor():
    """A registered user who is not a contributor cannot access the project.

    Setup consists of logging into the OSF as the non-contributor.
    """
    page = OsfPage(driver=global_page.driver)

    page = page.user_login.log_in(noncontributor)

    page.driver.get(url)

    with assert_raises(HttpError) as cm:
        ProjectPage(driver=page.driver)
    assert_equal(http.FORBIDDEN, cm.exception.code)