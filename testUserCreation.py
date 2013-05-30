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
    
    def _clear_users(self):
        """Clear all users from test database. Otherwise account creation
        test will fail after running once.

        """
        
        database['user'].remove()

    def setUp(self):
        
        # Browse to account creation page
        self.driver.get('http://localhost:5000/account')

        util.clear_users()

    def tearDown(self):
        
        util.clear_users()

    def _fill_form(self, form_data):
        """Fill out form fields in registration page.

        Args:
            form_data : Dictionary mapping input IDs to values
            
        """
        
        # Enter form data into fields
        for field in form_data:
            xpath = '//form[@name="registration"]//*[@id="%s"]' % (field)
            self.driver.find_element_by_xpath(xpath).send_keys(form_data[field])
        
        # Find submit button
        submit_button = self.driver.find_element_by_xpath('//form[@name="registration"]//button')
        
        # Submit form
        submit_button.click()
    
    def _submit_and_check(self, form_data, alert_text):
        """Submit form data and check for appropriate alert box. Asserts
        that there is exactly one matching alert box.

        Args:
            form_data : Dictionary of field values (see _fill_form)
            alert_text : Text to search for in alert box

        """
        
        # Submit form
        self._fill_form(form_data)
        
        # Find alerts
        alerts = self.driver.find_elements_by_xpath('//div[contains(@class, "alert")]')
        alerts = [alert for alert in alerts if alert_text.lower() in alert.text.lower()]
        
        # Must be exactly one matching alert
        self.assertEquals(len(alerts), 1)
    
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
    
    def testValidAccount(self):
        
        # Submit original form data
        self._submit_and_check(self.form_data, 'you may now login')
        
        # Make sure we can log in
        util.login(self.driver, self.form_data['username'], self.form_data['password'])
        self.assertTrue('dashboard' in self.driver.current_url)

# Run tests
if __name__ == '__main__':
    unittest.main()
