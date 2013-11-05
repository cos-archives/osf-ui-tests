import unittest

from base import ProjectSmokeTest, not_implemented
from pages import helpers
from pages.auth import LoginPage
from pages.project import NodePage, ProjectPage
from pages.exceptions import PageException
from pages.helpers import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class ProjectSecurityTest(ProjectSmokeTest):

    def setUp(self):
        super(ProjectSecurityTest, self).setUp()

        self.second_user = self.create_user()

    def test_public_non_contributor_modify(self):
        """ Users who are not contributors should not have access to the wiki
        edit page of a public project.
        """

        self.make_public()

        second_user = self.create_user()

        self.log_out()
        self.log_in(second_user)

        # Try to edit the wiki
        self.goto('wiki')
        self.driver.get('/'.join([
            self.driver.current_url.strip('/'),
            'edit',
        ]))

        # should have redirect the user elsewhere
        self.assert_forbidden()

        # try to add a node
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.add_component('hypothesis', 'foo')

        # try to delete the project
        self.goto('settings')
        self.assert_forbidden()

        # try to rename the project
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.edit_title('foo')

        # try to add a contributor
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.add_contributor(second_user)

        # try to remove a contributor
        self.goto('dashboard')
        # with self.assertRaises(TimeoutException):
        with self.assertRaises(TimeoutException):
            self.remove_contributor(self.user_data)

        self.goto('dashboard')
        self.assertIn(
            self.user_data['fullname'],
            self.get_element('#contributors').text,
        )

        # log back in so teardown works.
        self.log_out()
        self.log_in()

    @not_implemented
    def test_fork_with_private_components(self):
        raise NotImplementedError
