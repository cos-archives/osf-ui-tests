"""

"""

import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Project imports
import base
import util
import config

class UserLoginTests(base.SmokeTest):

    def setUp(self):    
        
        # Call parent setUp
        super(UserLoginTests, self).setUp()
        
        # Create user data
        self.user_data = util.create_user(self.driver)


    def test_no_email_and_no_passowrd(self):

        # Login with incorrect password
        util.login(self.driver, '', '')

        # Check for alert
        alertsusername = util.get_alert_boxes(self.driver, 'Email address is required')
        self.assertEqual(len(alertsusername), 1)
        alertspassword = util.get_alert_boxes(self.driver, 'Password is required')
        self.assertEqual(len(alertspassword), 1)

    def test_no_email(self):

        # Login with incorrect password
        util.login(self.driver, '', 'badpassword')

        # Check for alert
        alerts = util.get_alert_boxes(self.driver, 'Email address is required')
        self.assertEqual(len(alerts), 1)

    def test_no_password(self):

        # Login with incorrect password
        util.login(self.driver, self.user_data['username'], '')

        # Check for alert
        alerts = util.get_alert_boxes(self.driver, 'Password is required')
        self.assertEqual(len(alerts), 1)


    def test_not_registered_email(self):

        # Login with incorrect password
        util.login(self.driver, 'bad@email.addr', self.user_data['password'])

        # Check for alert
        alerts = util.get_alert_boxes(self.driver, 'log-in failed')
        self.assertEqual(len(alerts), 1)

    def test_incorrect_password(self):

        # Login with incorrect password
        util.login(self.driver, self.user_data['username'], 'wrongpass')

        # Check for alert
        alerts = util.get_alert_boxes(self.driver, 'log-in failed')
        self.assertEqual(len(alerts), 1)


    def test_login(self):

        # Login
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )

        # Assert that browser is pointing to /dashboard
        self.assertTrue('/dashboard' in self.driver.current_url)


    def test_logout(self):

        # Login
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )

        #logout
        util.logout(self.driver)

        # Check for alert
        alerts = util.get_alert_boxes(self.driver, 'You have successfully logged out.')
        self.assertEqual(len(alerts), 1)
        #self.assertTrue('/dashboard' in self.driver.current_url)