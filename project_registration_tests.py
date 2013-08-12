"""
Tests for creating project registrations.
"""

#
import unittest

# Project imports
import base
import util
import config


class RegistrationTests(base.ProjectSmokeTest):
    
    ###########
    # Helpers #
    ###########

    def _test_registration(
            self,
            registration_type,
            registration_data):
        """Create a new registration, then assert that it was created.

        Args:
            registration_type : Type of registration
            registration_data : Data for registration form

        """
        # Create the registration
        util.create_registration(
            self.driver,
            registration_type,
            registration_data
        )
        
        # Find node label
        label = self.driver.find_element_by_css_selector(
            'span.label-important'
        )
        
        # Label must be a node label
        self.assertTrue('This node is a registration' in label.text)
        
        # Find link to original project
        link = label.find_element_by_tag_name('a')
        
        # Link must point to original project
        self.assertEqual(
            link.get_attribute('href').strip('/'),
            self.project_url.strip('/')
        )
    
    #########
    # Tests #
    #########

    def test_create_open_ended_registration(self):
        """ Create an Open-Ended Registration. """
        
        self._test_registration(
            'Open-Ended Registration',
            config.open_ended_registration_data
        )

    def test_create_osf_standard_registration(self):
        """ Create an OSF Standard Registration. """

        self._test_registration(
            'OSF-Standard Pre-Data Collection Registration',
            config.osf_standard_registration_data
        )

    def test_add_node_to_registration(self):
        """ Attempt to add a node to a registration. """
        
        # Create a registration
        registration_url = util.create_registration(
            self.driver,
            'Open-Ended Registration',
            config.open_ended_registration_data
        )
        
        # Attempt to create a new node
        util.create_node(
            self.driver,
            project_url=registration_url
        )
        
        # Get alert boxes
        alerts = util.get_alert_boxes(
            self.driver,
            'registrations are read-only'
        )
        
        # Must be exactly one alert
        self.assertEqual(
            len(alerts),
            1
        )