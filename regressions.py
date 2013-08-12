from base import ProjectSmokeTest


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