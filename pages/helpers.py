import time
from collections import namedtuple

import requests
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as exc

import util
import config

User = namedtuple('User', ['full_name', 'email', 'password'])
Project = namedtuple('Project', ('title', 'url'))


def create_user():
    """ Create a new OSF user
    """

    u = util.create_user()
    return User(
        full_name=u['fullname'],
        email=u['username'],
        password=u['password'],
    )


def get_new_project(title='New Project', description=None):
    """ Create a new project; return its page.
    """

    # Log in
    from pages import LoginPage

    page = LoginPage()
    page = page.log_in(create_user())

    # create the project
    return page.new_project(title=title, description=description)


def get_new_subproject(title='Test Subproject'):
    """ Create and return a (sub)project which is the child of a project.

    The ``current_url`` of the driver is the subproject's overview.
    """
    return get_new_project().add_component(
        title=title,
        component_type='Project',
    )


def get_new_component(title='New Component', component_type='Other'):
    """ Create and return a (sub)project which is the child of a project.

    The ``current_url`` of the driver is the subproject's overview.
    """
    return get_new_project().add_component(
        title=title,
        component_type=component_type,
    )


def get_new_nested_component(title='New Component', component_type='Other'):
    """ Create and return a (sub)project which is the child of a project.

    The ``current_url`` of the driver is the subproject's overview.
    """
    return get_new_subproject().add_component(
        title=title,
        component_type=component_type,
    )


def convert_cookies(cookie_jar):
    """Converts a CookieJar from Requests into a list suitable for use by
    Selenium's WebDriver."""
    return [
        {
            'name': x.name,
            'value': x.value,
            'domain': (
                'localhost' if x.domain == 'localhost.local' else x.domain
            ),
            'path': x.path,
            'secure': x.secure,
            'expiry': x.expires,
        } for x in cookie_jar
    ]


def load_cookies(webdriver, cookie_jar):
    for c in cookie_jar:
        webdriver.add_cookie(c)
    return webdriver


class WaitForPageReload(object):
    def __enter__(self):
        self.body = self.driver.find_element_by_css_selector('body')

    def __init__(self, driver):
        self.driver = driver

    def __exit__(self, *args, **kwargs):
        WebDriverWait(self.driver, 3).until(
            EC.staleness_of(self.body)
        )


class WaitForFileUpload(object):
    def __enter__(self):
        pass

    def __init__(self, driver, wait=3, interval=0.1):
        self.driver = driver
        self.wait = wait
        self.interval = interval

        self.files = len(
            self.driver.find_elements_by_css_selector(
                'tbody.files tr.start'
            )
        )

        print(self.files)

    def __exit__(self, *args, **kwargs):
        entered = time.time()
        while time.time() - entered < self.wait:
            if len(
                self.driver.find_elements_by_css_selector(
                    'tbody.files td.start'
                )
            ) == self.files:
                time.sleep(self.interval)
            else:
                self.driver.get(self.driver.current_url)
                return
        raise exc.TimeoutException(
            '{} seconds passed without the upload completing'.format(self.wait)
        )