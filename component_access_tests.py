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