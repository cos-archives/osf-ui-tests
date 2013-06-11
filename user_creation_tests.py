"""
Selenium tests for user account creation. Tests valid account creation,
as well as various ways to do it wrong (mismatched passwords, invalid
email addresses, etc.).
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

class UserCreationTests(base.SmokeTest):
    
    def setUp(self):
        
        # Call parent setUp
        super(UserCreationTests, self).setUp()
        
        # Generate user data
        self.user_data = util.gen_user_data()

        # Browse to account creation page
        self.driver.get('%s/account' % (config.osf_home))
        
    def _submit_and_check(self, form_data, alert_text):
        """Submit form data and check for appropriate alert box. Asserts
        that there is exactly one matching alert box.

        Args:
            form_data : Dictionary of field values (see util.fill_form)
            alert_text : Text to search for in alert box

        """
        
        # Prepend #'s to form keys
        id_form_data = {'#%s' % (k) : form_data[k] for k in form_data}

        # Submit form
        util.fill_form(self.driver, id_form_data)
        
        # Get alert boxes
        alerts = util.get_alert_boxes(self.driver, alert_text)

        # Must be exactly one matching alert
        self.assertEqual(len(alerts), 1)
    
    def test_no_password(self):
        
        # Alter form data
        form_data = util.gen_user_data()
        form_data['password'] = ''
    
        # Submit form
        self._submit_and_check(form_data, 'password is required')

    def test_no_email(self):
        
        # Alter form data
        form_data = util.gen_user_data()
        form_data['username'] = ''
    
        # Submit form
        self._submit_and_check(form_data, 'email address is required')
    
    def test_password_mismatch(self):
        
        # Alter form data
        form_data = util.gen_user_data()
        form_data['password2'] = form_data['password2'] + 'junk'

        # Submit form
        self._submit_and_check(form_data, 'passwords must match')
    
    def test_email_mismatch(self):
        
        # Alter form data
        form_data = util.gen_user_data()
        form_data['username2'] = form_data['username2'] + 'junk'

        # Submit form
        self._submit_and_check(form_data, 'email addresses must match')

    def test_short_password(self):
        
        # Alter form data
        form_data = util.gen_user_data()
        form_data['password'] = 'short'

        # Submit form
        self._submit_and_check(form_data, 'password is too short')
    
    def test_long_password(self):
        
        # Alter form data
        form_data = util.gen_user_data()
        password = 'toolong' * 50
        form_data['password'] = password
        form_data['password2'] = password
        
        # Submit form
        self._submit_and_check(form_data, 'password is too long')

    def test_invalid_email(self):
        
        # Alter form data
        form_data = util.gen_user_data()
        form_data['username'] = 'invalidemail'

        # Submit form
        self._submit_and_check(form_data, 'email address is invalid')
    
    def test_valid_account(self):
        
        # Submit original form data
        self._submit_and_check(self.user_data, 'you may now login')
        
        # Make sure we can log in
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )
        self.assertTrue('dashboard' in self.driver.current_url)

# Generate tests
def test():
    util.generate_tests(UserCreationTests)

# Run tests
if __name__ == '__main__':
    unittest.main()
