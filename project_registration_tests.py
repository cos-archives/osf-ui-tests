"""
Tests for creating project registrations.
"""

# Project imports
import base
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class RegistrationTests(base.ProjectSmokeTest):

    def test_create_open_ended_registration(self):
        """ Create an Open-Ended Registration. """

        registration_url = self.create_registration('Open-Ended Registration')

        self.assertIn(
            'This node is a registration of',
            self.get_element('span.label.label-important').text,
        )

    def test_create_osf_standard_registration(self):
        """ Create an OSF Standard registration """
        registration_url = self.create_registration(
            'OSF-Standard Pre-Data Collection Registration'
        )

        self.assertIn(
            'This node is a registration of',
            self.get_element('span.label.label-important').text
        )

    def test_registration_link_to_parent_project(self):
        """
            Test that a link is created in the registration notice that points
            to the project from which it was created.
        """
        registration_url = self.create_registration()

        self.assertEqual(
            self.get_element(
                'span.label.label-important a'
            ).get_attribute('href').strip('/'),
            self.project_url.strip('/'),
        )


    def test_registration_add_files(self):
        """Test that a user cannot add files to a registration"""
        # TODO: This test should work, but the functionality is

        self.project_url = self.create_registration()

        self.goto('files', node_url=self.project_url)

        self.assertIn(
            'disabled',
            self.driver.find_element_by_css_selector("div.span7 span")
            .get_attribute("class")
        )

        self.assertIn(
            'disabled',
            self.driver.find_element_by_css_selector("div.span7 button")
            .get_attribute("class")
        )

    def test_registration_delete_files(self):
        """Test that files cannot be deleted from registrations"""

        # add a file to the project
        self.add_file(self.image_files['jpg']['path'])

        # create the registration
        registration_url = self.create_registration()

        # go to the files page
        self.goto(
            'files',
            node_url=registration_url
        )

        # click delete on a file
        self.get_element('table#filesTable button.btn.btn-danger').click()

        self.driver.get(self.driver.current_url)

        self.assertIn(
            self.image_files['jpg']['filename'],
            self.get_element('table#filesTable').text
        )

    def test_registration_add_contributor(self):
        second_user = self.create_user()
        registration_url = self.create_registration()

        # add a contributor
        self.driver.get(registration_url)

        # with self.assertRaises(TimeoutException):
        self.assertTrue(
            len(
                self.get_element('#contributors')
                .find_elements_by_link_text("add")
            ) == 0
        )

        # refresh the page
        self.driver.get(registration_url)

        # make sure the added user isn't there.
        self.assertNotIn(
            second_user['fullname'],
            self.get_element('#contributors').text,
        )

    def test_registration_remove_contributor(self):
        """ Attempts to remove a contributor from a registration """

        # create a user
        second_user = self.create_user()

        # add them to the project
        self.goto('dashboard')
        self.add_contributor(second_user)

        # register it.
        registration_url = self.create_registration()

        # remove them from the registration
        self.driver.get(registration_url)
        element_to_hover_over = self.get_element('#contributors')\
            .find_element_by_link_text(second_user["fullname"])
        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()

        self.assertTrue(
            len(element_to_hover_over.find_elements_by_css_selector("i")) == 0
        )

        # make sure they're still there
        self.driver.get(registration_url)
        self.assertIn(
            second_user['fullname'],
            self.get_element('#contributors').text
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

