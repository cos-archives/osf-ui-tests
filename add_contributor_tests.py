import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Project imports
import util
import config
import time

class AddContributorTests(unittest.TestCase):

    def setUp(self):

        # Start WebDriver
        self.driver = util.launch_driver()

        # Create test user
        self.user_data = util.create_user(self.driver)

        self.second_user_data = util.create_user(self.driver)

        # Login to test account
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )

        # create a project
        util.create_project(self.driver)

    def test_add_contributor(self):

        #go to the project
        self.url = util.goto_project(self.driver)

        self.driver.find_element_by_link_text("add").click()
        time.sleep(3)
        self.user_email = self.second_user_data['username']
        username_box = self.driver.find_element_by_xpath(
            '//input[@id="ember204"]')
        username_box.send_keys(self.user_email)
        self.driver.find_element_by_xpath('//button[@id="ember234"]').click()
        self.driver.find_element_by_xpath('//input[@id="ember385"]').click()
        self.user_name = self.driver.find_element_by_xpath('//div[@id="ember178"]').text.replace("Search\n", "")
        self.driver.find_element_by_xpath('//button[@class="btn primary"]').click()
        time.sleep(3)
        contribs = self.driver.find_element_by_id('contributors').text
        self.assertTrue(self.user_name in contribs)
#        contribs = self.driver.find_elements_by_xpath('//a[@class="user-quickedit"]')
#        self.assertTrue(all([self.user_name in contrib.text for contrib in contribs]))
        #for contributor in contribs:
        #    if self.user_name in contributor.text:
        #        self.assertTrue(True == True)

    def tearDown(self):

        # Close WebDriver
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
