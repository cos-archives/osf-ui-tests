"""
Selenium test suite for account profile manipulation and access
Author: Harry Rybacki
Date: 29May13
"""

import time
import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Project imports
import util
import config


class AccountProfileTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        
        # Start WebDriver
        cls.driver = util.launch_driver()
        
        # Create test user
        cls.user_data = util.create_user(cls.driver)
        
        # Login to test account
        util.login(
            cls.driver,
            cls.user_data['username'],
            cls.user_data['password']
        )
    
    @classmethod
    def tearDownClass(cls):
        
        # Close WebDriver
        cls.driver.close()

    def setUp(self):

        # Browse to profile
        util.goto_profile(self.driver)

    def test_access_profile(self):
        """
        tests user ability to access page and verifies name on profile page
        matches expected test data
        """
        profile_name = self.driver.find_element_by_id('profile-fullname').text
        self.assertTrue(
            self.user_data['fullname'] in profile_name
        )

    def test_change_name(self):
        """
        tests user ability to change username and asserts the change is made
        before changing it back to the original
        """
        # select and click the username edit field
        self.driver.find_element_by_id('profile-fullname').click()

        # select the name field on the new popup
        edit_profile_name_field = self.driver.find_element_by_xpath(
            '//div[@class="popover-content"]//input[@class="span2"]'
        )

        # delete the current name
        edit_profile_name_field.clear()

        # enter the reverse name
        edit_profile_name_field.send_keys(self.user_data['fullname'][::-1])

        # find and click submit new name
        self.driver.find_element_by_xpath(
            '//div[@class="popover-content"]//button[@class="btn btn-primary"]'
        ).click()
        
        # refresh page and assert change was made
        self.driver.refresh()
        profile_name = self.driver.find_element_by_id('profile-fullname').text
        self.assertTrue(self.user_data['fullname'][::-1] in profile_name)

        # return the username back to its original -- same as above
        self.driver.find_element_by_id(
            'profile-fullname'
        ).click()
        edit_profile_name_field = self.driver.find_element_by_xpath(
            '//div[@class="popover-content"]//input[@class="span2"]'
        )
        edit_profile_name_field.clear()
        edit_profile_name_field.send_keys(self.user_data['fullname'])
        self.driver.find_element_by_xpath(
            '//div[@class="popover-content"]//button[@class="btn btn-primary"]'
        ).click()

        # refresh page and assert username is back to the original
        self.driver.refresh()
        profile_name = self.driver.find_element_by_id('profile-fullname').text
        self.assertTrue(self.user_data['fullname'] in profile_name)

    @unittest.skip("not an implemented feature in OSF codebase")
    def test_change_location(self):
        pass

    def test_click_public_shortlink(self):
        """
        tests user ability to click profile short link and be direted to their
        profile.

        Note: We are checking against the name because Selenium
        doesn't currently have the ability to monitor redirects or check
        HTTP status codes.
        """
        # find and click user's profile shortlink
        self.driver.find_element_by_xpath(
            '//div[@class="span4"]//a'
        ).click()
        # assert name still matches username
        profile_name = self.driver.find_element_by_id(
            'profile-fullname'
        ).text
        self.assertTrue(self.user_data['fullname'] in profile_name)

    @unittest.skip("not implemented")
    def test_check_public_project_updates(self):
        pass

# Run tests
if __name__ == '__main__':
    unittest.main()
