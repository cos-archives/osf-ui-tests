import time
from collections import namedtuple

import util


def create_user():
    """ Create a new OSF user
    """
    User = namedtuple('User', ['full_name', 'email', 'password'])

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

    user = create_user()
    page = LoginPage()
    page = page.log_in(
        username=user.email,
        password=user.password,
    )

    # create the project
    return page.new_project(title=title, description=description)


class WaitForPageReload(object):
    def __enter__(self):
        self.body = self.driver.find_element_by_css_selector('body')

    def __init__(self, driver):
        self.driver = driver

    def __exit__(self, *args, **kwargs):
        while(True):
            if self.body == self.driver.find_element_by_css_selector('body'):
                time.sleep(.1)
            else:
                break