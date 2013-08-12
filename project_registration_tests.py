"""
Tests for creating project registrations.
"""

# Project imports
import base
from config import osf_home

from selenium.common.exceptions import TimeoutException


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
        """Test that a link is created in the registration notice that points to
         the project from which it was created.
        """
        registration_url = self.create_registration()

        self.assertEqual(
            self.get_element(
                'span.label.label-important a'
            ).get_attribute('href').strip('/'),
            self.project_url.strip('/'),
        )

    @base.not_implemented
    def test_registration_add_files(self):
        """Test that a user cannot add files to a registration"""
        # TODO: This test should work, but the functionality is

        self.project_url = self.create_registration()

        self.add_file(self.image_files['jpg']['path'])

        self.assertFalse(
            self._file_exists_in_project(
                self.image_files['jpg']['filename']
            )
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

        # A javascript alert() should be thrown
        alert = self.driver.switch_to_alert()
        self.assertEquals(
            alert.text,
            'Error!'
        )

        # dismiss the alert
        alert.dismiss()

    def test_registration_add_contributor(self):
        second_user = self.create_user()
        registration_url = self.create_registration()

        # add a contributor
        self.driver.get(registration_url)
        # with self.assertRaises(TimeoutException):
        self.add_contributor(second_user)

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
        self.remove_contributor(second_user)

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

        # click "Edit"
        self.get_element(
            '.subnav ul.nav > li:first-child > a[href$="edit"]'
        ).click()

        # should have been redirected to the homepage
        self.assertEqual(
            self.driver.current_url.strip('/'),
            registration_url.strip('/'),
        )

        self.assertIn(
            'Registrations are read-only',
            self.get_element('#alert-container').text,
        )