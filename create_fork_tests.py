import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Project imports
import util
import config
import time

class CreateForkTests(unittest.TestCase):

    def setUp(self):

        # Start WebDriver
        self.driver = webdriver.Firefox()

        # Wait for elements to appear
        self.driver.implicitly_wait(30)

        # Create test user
        util.create_user(self.driver)

        # Login to test account
        util.login(self.driver)

        # create a project
        util.create_project(self.driver)

        #go to the project
        self.url = util.goto_project(self.driver)

        # Make the project public
        util.make_project_public(self.driver, self.url)

        #logout
        util.logout(self.driver)

        util.create_user(self.driver,config.second_user_registration_data)

        util.login(
            self.driver, username=config.second_user_registration_data['username'],
            password=config.second_user_registration_data['password'])


    def test_create_fork(self):

        #go to the project that is now public
        self.driver.get(self.url)
        link = self.driver.find_element_by_xpath(
            '//a[@class="btn"][@data-original-title="Number of times this node has been forked (copied)"]')
        link.click()
        title = self.driver.find_element_by_css_selector("h1#node-title-editable").text
        self.assertEqual(title,
            "Fork of test project")

    def tearDown(self):

        # Delete test project
        util.login(self.driver)
        util.delete_project(self.driver)
        util.logout(self.driver)

        util.login(
            self.driver, username=config.second_user_registration_data['username'],
            password=config.second_user_registration_data['password'])
        util.delete_project(self.driver, "Fork of test project")
        util.logout(self.driver)

        # Close WebDriver
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
