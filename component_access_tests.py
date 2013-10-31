import unittest

from selenium.webdriver import ActionChains

from base import ProjectSmokeTest


class ComponentAccessCase(ProjectSmokeTest):

    @unittest.skip('Fails due to Selenium troubles')
    def test_reorder_components(self):
        self.add_component('hypothesis', 'first')
        self.add_component('hypothesis', 'second')

        self.driver.get(self.project_url)

        # Second method: by element
        ac = ActionChains(self.driver)
        a = self.driver.find_element_by_css_selector('#Nodes li:first-child')
        b = self.driver.find_element_by_css_selector('#Nodes li:last-child')
        ac.drag_and_drop(a, b).perform()

        self.driver.get(self.project_url)
        self.assertEqual(
            self.get_element('#Nodes li:first-child').text,
            'second',
        )

    def test_private_component_of_public_project_not_forked(self):
        """Test that a private components of public projects are not forked
        when the project is forked
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

        self.driver.get(fork_url)

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
        self.get_element(
            'div.container button#delete-node.btn.btn-danger'
        ).click()

        # log back in as the first user so teardown will work.
        self.log_out()
        self.log_in()