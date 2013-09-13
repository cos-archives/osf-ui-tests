import unittest

import requests

from base import ProjectSmokeTest
import config
from pages import helpers


class RegressionTests2(unittest.TestCase):
    def test_username_injection_account_creation(self):
        """ Account creation should not allow < or > in fullname fields """
        r = requests.post(
            url='/'.join((config.osf_home.strip('/'), 'register')),
            data={
                'register-fullname':  'Bad <script>alert("xss");</script>Guy',
                'register-username': 'heinz@doofenshmirtz.com',
                'register-username2': 'heinz@doofenshmirtz.com',
                'register-password': 'password',
                'register-password2': 'password',
            },
            verify=False,
        )

        self.assertIn("Illegal characters in field", r.content)

    def test_node_title_injection(self):
        """A node's title should allow < and >, but should HTML encode them.

        This test verifies that when a project is renamed, the title is properly
        encoded."""

        page = helpers.get_new_project()
        page.title = 'Bad <script>alert("xss");</script>Project'

        self.assertEqual(
            page.driver.find_element_by_id(
                'node-title-editable'
            ).get_attribute('innerHTML'),
            'Bad &lt;script&gt;alert("xss");&lt;/script&gt;Project',
        )

        page.close()

    def test_node_title_injection_creation(self):
        """A node's title should allow < and >, but should HTML encode them.

        This test verifies that when a project is created, the title is properly
        encoded."""
        page = helpers.get_new_project(
            title='Bad <script>alert("xss");</script>Project'
        )

        self.assertEqual(
            page.driver.find_element_by_id(
                'node-title-editable'
            ).get_attribute('innerHTML'),
            'Bad &lt;script&gt;alert("xss");&lt;/script&gt;Project',
        )

        page.close()

    def test_node_description_injection_creation(self):
        """A node's description should allow < and >, but should HTML encode
        them.

        This test verifies that when a project is created, the description is
        properly encoded."""
        page = helpers.get_new_project(
            description='Bad <script>alert("xss");</script>Project'
        )

        self.assertIn(
            'Bad &lt;script&gt;alert("xss");&lt;/script&gt;Project',
            page.driver.find_element_by_id(
                'contributors'
            ).get_attribute('innerHTML'),
        )

        page.close()


class RegressionTests(ProjectSmokeTest):
    def test_private_component_of_public_project_not_forked(self):
        """Test that a private components of a public project that is then
         forked are not present on registrations of that fork.
        """

        # make the project public
        self.make_public()

        # create a private component
        private_component_title = "Private-Component"
        private_component_url = self.add_component(
            'hypothesis',
            private_component_title,
        )

        # verify that the component is private
        if self.is_public(private_component_url):
            self.make_private(private_component_url)

        # create a public component
        public_component_title = "Public-Component"
        public_component_url = self.add_component(
            'hypothesis',
            public_component_title
        )

        # verify that the component is public
        if not self.is_public(public_component_url):
            self.make_public(public_component_url)

        # Log out and make a new user
        self.log_out()
        self.second_user = self.create_user()
        self.log_in(self.second_user)

        # go to the project
        self.goto('dashboard')

        fork_url = self.create_fork()

        registration_url = self.create_registration(node_url=fork_url)

        self.driver.get(registration_url)

        # Public component should be there
        self.assertIn(
            public_component_title,
            self.get_element('#Nodes').text
        )

        # Private component should not be there
        self.assertNotIn(
            private_component_title,
            self.get_element('#Nodes').text
        )

        # delete the forked project.
        self.goto('settings', node_url=fork_url)
        self.get_element('button[type="submit"]').click()

        # log back in as the first user so teardown will work.
        self.log_out()
        self.log_in()