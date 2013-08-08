"""

"""

import time
import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Project imports
import base
import util
import config

class AddContributorTests(base.ProjectSmokeTest):
    
    def setUp(self):
        
        # Call parent setUp
        super(AddContributorTests, self).setUp()
        
        # Log out
        util.logout(self.driver)
        
        # Create second user
        self.second_user_data = util.create_user(self.driver)
        
        # Login to first user account
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )

    def test_add_contributor(self):

        #add the contributor
        self.add_contributor(self.second_user_data)

        #check the contributor
        contribs = self.driver.find_element_by_id('contributors').text
        self.assertTrue(self.second_user_data['fullname'] in contribs)

        #logout the first user
        util.logout(self.driver)

        #log in as the second user
        util.login(
            self.driver,
            self.second_user_data['username'],
            self.second_user_data['password']
        )

        #find created project in dashboard
        title=self.driver.find_element_by_link_text(config.project_title)
        self.assertTrue(title)


# Generate tests
util.generate_tests(AddContributorTests)

# Run tests
if __name__ == '__main__':
    unittest.main()
