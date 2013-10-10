import time
import unittest
import config
from pages import helpers, LoginPage
from pages.generic import OsfPage


__doc__ = """IMPORTANT!

Classes in this module may be interdependent.
---------------------------------------------

When modifying an existing fixture, be sure to check that other fixtures which
inherit it are not broken.

As a rule, you should verify that all tests pass for the object you're modifying
and all object which inherit from it before committing.
"""


class OsfBaseFixture(unittest.TestCase):
    page = None
    users = []

    @classmethod
    def setUpClass(cls):
        cls.page = OsfPage(url=config.osf_home)
        cls._start_time = time.time()

    @classmethod
    def tearDownClass(cls):
        cls.page.close()
        print('{} ran in {} seconds'.format(
            cls.__name__,
            round(time.time() - cls._start_time, 2),
        ))

    @classmethod
    def create_user(cls):
        cls.users.append(helpers.create_user())
        return cls

    @classmethod
    def log_in(cls, user=None):
        cls.page.driver.get(LoginPage.default_url)
        cls.page = LoginPage(
            driver=cls.page.driver
        ).log_in(
            user=user or cls.users[-1]
        )

        return cls


class UserFixture(OsfBaseFixture):
    """User Dashboard for a freshly created user"""
    @classmethod
    def setUpClass(cls):
        super(UserFixture, cls).setUpClass()
        cls.create_user().log_in()


class ProjectFixture(UserFixture):

    @classmethod
    def setUpClass(cls):
        super(ProjectFixture, cls).setUpClass()
        cls.page = cls.page.new_project(
            title='Test Project',
            description='Test Project Description',
        )

        cls.project_id = cls.page.id


class SubprojectFixture(ProjectFixture):

    @classmethod
    def setUpClass(cls):
        super(SubprojectFixture, cls).setUpClass()
        cls.page = cls.page.add_component(
            title='Test Subproject',
            component_type='Project',
        )


class ComplexFixture(object):

    @classmethod
    def setUpClass(cls):
        super(ComplexFixture, cls).setUpClass()

        # Add a couple of components
        cls.page = cls.page.add_component(
            title='Hypothesis Component',
            component_type='Hypothesis'
        )
        cls.page = cls.page.parent_project()
        cls.page = cls.page.add_component(
            title='Data Component',
            component_type='Data',
        )
        cls.page = cls.page.parent_project()

        cls.page.set_wiki_content('Test Wiki Content')


class ComplexProjectFixture(ComplexFixture, ProjectFixture):
    pass


class ComplexSubprojectFixture(ComplexFixture, SubprojectFixture):
    pass