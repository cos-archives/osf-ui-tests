import unittest
import time

import config
from pages import helpers
from pages import LoginPage
from pages.generic import OsfPage


__doc__ = """IMPORTANT!

Classes in this module may be interdependent.
---------------------------------------------

When modifying an existing fixture, be sure to check that other fixtures which
inherit it are not broken.

As a rule, you should verify that all tests pass for the object you're modifying
and all object which inherit from it before committing.
"""


class OsfTestCase(unittest.TestCase):
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


class UserTestCase(OsfTestCase):
    """User Dashboard for a freshly created user"""
    @classmethod
    def setUpClass(cls):
        super(UserTestCase, cls).setUpClass()
        cls.create_user().log_in()


class ProjectTestCase(UserTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectTestCase, cls).setUpClass()
        cls.page = cls.page.new_project(
            title='Test Project',
            description='Test Project Description',
        )

        cls.project_id = cls.page.id


class SubprojectTestCase(ProjectTestCase):

    @classmethod
    def setUpClass(cls):
        super(SubprojectTestCase, cls).setUpClass()
        cls.page = cls.page.add_component(
            title='Test Subproject',
            component_type='Project',
        )


#TODO: This should be a decorator.
def make_RegistrationTestCase(base_class):

    class RegistrationTestCase(base_class):

        registration_template = 'Open-Ended Registration'
        registration_meta = ('sample narrative', )

        @classmethod
        def setUpClass(cls):
            super(RegistrationTestCase, cls).setUpClass()

            cls.parent_values = {
                'title': cls.page.title,
                'component_names': cls.page.component_names,
                'contributors': cls.page.contributors,
                'date_created': cls.page.date_created,
                'last_updated': cls.page.last_updated,
                'logs': cls.page.logs,

            }

            cls.page = cls.page.add_registration(
                registration_type=cls.registration_template,
                meta=cls.registration_meta,
            )

    return RegistrationTestCase


class ProjectRegistrationTestCase(make_RegistrationTestCase(ProjectTestCase)):
    pass


class SubprojectRegistrationTestCase(make_RegistrationTestCase(SubprojectTestCase)):
    pass