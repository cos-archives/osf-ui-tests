"""
Tests for creating project registrations.
"""

# Project imports
import base


class RegistrationTests(base.ProjectSmokeTest):

    def test_create_osf_standard_registration(self):
        """ Create an OSF Standard registration """
        registration_url = self.create_registration(
            'OSF-Standard Pre-Data Collection Registration'
        )

        self.assertIn(
            'This node is a registration of',
            self.get_element('span.label.label-important').text
        )

    def test_registration_modify_wiki(self):
        registration_url = self.create_registration()

        # go to the registration's wiki
        self.goto('wiki', node_url=registration_url)

        # "Edit" should be disabled.
        self.assertEqual(
            len(
                self.driver.find_elements_by_css_selector(
                    '.subnav ul.nav > li:first-child > a.disabled'
                )
            ),
            1
        )

