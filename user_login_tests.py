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
    
    def test_incorrect_password(self):
        
        # Login with incorrect password
        util.login(self.driver, 'bad@email.addr', 'wrongpass')
        
        # Check for alert
        alerts = util.get_alert_boxes(self.driver, 'log-in failed')
        self.assertEqual(len(alerts), 1)
    
    def test_login(self):
        
        util.login(
            self.driver, 
            self.user_data['username'],
            self.user_data['password']
        )
        
        # 
        self.assertTrue('/dashboard' in self.driver.current_url)

# Run tests
if __name__ == '__main__':
    unittest.main()
