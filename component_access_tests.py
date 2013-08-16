import time

from selenium.webdriver import ActionChains

from base import ProjectSmokeTest


class ComponentAccessCase(ProjectSmokeTest):
    def test_add_component(self):
        """Add a component and make sure its name appears in the dashboard"""
        component_name = 'Test Hypothesis'

        self.add_component('hypothesis', component_name)

        self.assertTrue(
            # name is the same as one of the components in the dashboard list.
            component_name in [
                x.text
                for x
                in self.driver.find_elements_by_css_selector(
                    '#Nodes li.project h3'
                )
            ]
        )

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

    def test_public_component_of_private_project(self):
        """ Test that a public component or a private project is accessible"""
        title = 'Public Hypothesis'

        component_url = self.add_component('hypothesis', title)

        self.make_public(component_url)
        self.log_out()

        # navigate to the component as a non-logged-in user.
        self.driver.get(component_url)

        self.assertEqual(
            self.get_element('#node-title-editable').text,
            title
        )

        # log back in so the teardown works.
        self.log_in()

    def test_private_component_of_public_project(self):
        """Test that a private component of a public project is not accessible
        """

        # make the project public
        self.make_public()

        # create a component
        title = "Private Hypothesis"
        component_url = self.add_component('hypothesis', title)

        # verify that the component is private
        if self.is_public(component_url):
            self.make_private(component_url)

        # test that the component is not accessible to an anonymous user

        self.log_out()

        self.assert_not_authorized(component_url)

        # test that the component is not accessible to a non-contributor

        self.second_user = self.create_user()
        self.log_in(self.second_user)

        self.assert_not_authorized(component_url)

        # log back in so teardown doesn't fail.
        self.log_out()
        self.log_in()

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
        self.get_element('button[type="submit"]').click()

        # log back in as the first user so teardown will work.
        self.log_out()
        self.log_in()

    def test_files_of_private_component_of_public_project(self):
        """Test that a private component of a public project is not accessible
        """

        # make the project public
        self.make_public()

        # create a component
        title = "Private Hypothesis"
        component_url = self.add_component('hypothesis', title)

        # verify that the component is private
        if self.is_public(component_url):
            self.make_private(component_url)

        # upload a file to the component
        self.add_file(self.image_files['jpg']['path'])

        # test that the component is not accessible to an anonymous user

        self.log_out()

        self.goto(
            'file',
            self.image_files['jpg']['filename'],
            node_url=component_url,
        )

        self.assert_not_authorized()

        # test that the component is not accessible to a non-contributor

        self.second_user = self.create_user()
        self.log_in(self.second_user)

        self.goto(
            'file',
            self.image_files['jpg']['filename'],
            node_url=component_url,
        )

        self.assert_not_authorized()

        # log back in so teardown doesn't fail.
        self.log_out()
        self.log_in()
