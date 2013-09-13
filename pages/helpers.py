import time
from collections import namedtuple

import util

User = namedtuple('User', ['full_name', 'email', 'password'])


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