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

        #go to the project
        self.url = util.goto_project(self.driver)

        self.driver.find_element_by_link_text("add").click()
        time.sleep(3)

        user_email = self.second_user_data['username']
        username_box = self.driver.find_element_by_xpath(
            '//input[@id="ember204"]'
        )
        username_box.send_keys(user_email)

        self.driver.find_element_by_xpath('//button[@id="ember234"]').click()
        self.driver.find_element_by_xpath('//input[@id="ember385"]').click()
        user_name = self.driver.find_element_by_xpath('//div[@id="ember178"]').text.replace("Search\n", "")
        self.driver.find_element_by_xpath('//button[@class="btn primary"]').click()
        time.sleep(3)
        contribs = self.driver.find_element_by_id('contributors').text
        self.assertTrue(user_name in contribs)

# Generate tests
def test():
    util.generate_tests(AddContributorTests)

# Run tests
if __name__ == '__main__':
    unittest.main()
