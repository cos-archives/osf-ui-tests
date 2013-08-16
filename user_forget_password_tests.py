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


class UserForgetPasswordTests(base.SmokeTest):

    def setUp(self):

        # Call parent setUp
        super(UserForgetPasswordTests, self).setUp()




    def test_no_email(self):

        # use forgetpassword with no email address
        util.forget_password(self.driver, '')


        # check for alert
        alerts = util.get_alert_boxes(self.driver, 'Email address is required')
        self.assertEqual(len(alerts), 1)


    def test_too_short_email(self):
        #forgetpassowrd with too short and wrong email
        util.forget_password(self.driver, 'Alpha')

        # check for alert
        alertstooshort = util.get_alert_boxes(self.driver, 'Email address is too short')
        self.assertEqual(len(alertstooshort), 1)
        alertsinvalid = util.get_alert_boxes(self.driver, 'Email address is invalid')
        self.assertEqual(len(alertsinvalid), 1)


    def test_invalid_email(self):
        #forgetpassowrd with invalid email
        util.forget_password(self.driver, 'AlphaOmega')

        # check for alert
        alerts = util.get_alert_boxes(self.driver, 'Email address is invalid')
        self.assertEqual(len(alerts), 1)


    def test_not_registered_email(self):
        #forgetpassowrd with not registered email
        util.forget_password(self.driver, 'bad@email.addr')

        # check for alert
        alerts = util.get_alert_boxes(self.driver, 'Email bad@email.addr not found')
        self.assertEqual(len(alerts), 1)


    def test_registered_email(self):
        # Create user data
        self.user_data = util.create_user(self.driver)

        #forgetpassowrd with registered email
        util.forget_password(self.driver, self.user_data['username'])

        # check for alert
        alerts = util.get_alert_boxes(self.driver, 'Reset email sent')
        self.assertEqual(len(alerts), 1)