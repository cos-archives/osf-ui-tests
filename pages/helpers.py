from collections import namedtuple

import util
from pages import LoginPage


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


def get_new_project(title=None, description=None):
    """ Create a new project; return its page.
    """

    # Log in
    user = create_user()
    page = LoginPage()
    page = page.log_in(
        username=user.email,
        password=user.password,
    )

    # create the project
    return page.new_project(title=title, description=description)