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
import util
import config

class testUserCreation(unittest.TestCase):
    
    # Default form data
    form_data = {
        'fullname' : 'raymond occupant',
        'username' : 'raymond@occupant.com',
        'username2' : 'raymond@occupant.com',
        'password' : 'secret',
        'password2' : 'secret',
    }

    @classmethod
    def setUpClass(cls):
        
        # Launch Selenium
        cls.driver = webdriver.Chrome()

        # Wait for elements to load
        cls.driver.implicitly_wait(30)
    
    @classmethod
    def tearDownClass(cls):
        
        # Close Selenium
        cls.driver.close()
    
    def setUp(self):
        
        # Browse to account creation page
        self.driver.get('http://localhost:5000/account')
        
        # Delete users
        util.clear_user(self.form_data['username'])

    def tearDown(self):
        
        # Delete users
        util.clear_user(self.form_data['username'])

    def _check_alerts(self, alert_text):
        """Check page for alert boxes. Asserts that there is exactly
        one matching alert.

        Args:
            alert_text : Text to search for in alert box

        """
        
        # Find alerts
        alerts = self.driver.find_elements_by_xpath('//div[contains(@class, "alert")]')
        alerts = [alert for alert in alerts if alert_text.lower() in alert.text.lower()]
        
        # Must be exactly one matching alert
        self.assertEquals(len(alerts), 1)
        
    def _submit_and_check(self, form_data, alert_text):
        """Submit form data and check for appropriate alert box. Asserts
        that there is exactly one matching alert box.

        Args:
            form_data : Dictionary of field values (see util.fill_form)
            alert_text : Text to search for in alert box

        """
        
        # Submit form
        util.fill_form(self.driver, form_data)
        
        # Check alerts
        self._check_alerts(alert_text)
    
    def testNoPassword(self):
        
        # Alter form data
        form_data = self.form_data.copy()
        form_data['password'] = ''
    
        # Submit form
        self._submit_and_check(form_data, 'password is required')

    def testNoEmail(self):
        
        # Alter form data
        form_data = self.form_data.copy()
        form_data['username'] = ''
    
        # Submit form
        self._submit_and_check(form_data, 'email address is required')
    
    def testPasswordMismatch(self):
        
        # Alter form data
        form_data = self.form_data.copy()
        form_data['password2'] = form_data['password2'] + 'junk'

        # Submit form
        self._submit_and_check(form_data, 'passwords must match')
    
    def testEmailMismatch(self):
        
        # Alter form data
        form_data = self.form_data.copy()
        form_data['username2'] = form_data['username2'] + 'junk'

        # Submit form
        self._submit_and_check(form_data, 'email addresses must match')

    def testShortPassword(self):
        
        # Alter form data
        form_data = self.form_data.copy()
        form_data['password'] = 'short'

        # Submit form
        self._submit_and_check(form_data, 'password is too short')
    
    def testInvalidEmail(self):
        
        # Alter form data
        form_data = self.form_data.copy()
        form_data['username'] = 'invalidemail'

        # Submit form
        self._submit_and_check(form_data, 'email address is invalid')
    
    def testWrongPassword(self):
        
        util.login(self.driver, {
            'username' : 'bad@email.addr', 
            'password' : 'wrongpass'
        })
        
        # 
        self._check_alerts('log-in failed')

    def testValidAccount(self):
        
        # Submit original form data
        self._submit_and_check(self.form_data, 'you may now login')
        
        # Make sure we can log in
        util.login(self.driver, {
            'username' : self.form_data['username'], 
            'password' : self.form_data['password']
        })
        self.assertTrue('dashboard' in self.driver.current_url)

# Run tests
if __name__ == '__main__':
    unittest.main()
