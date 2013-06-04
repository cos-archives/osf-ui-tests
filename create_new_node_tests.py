"""

"""

import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Project imports
import util
import config

class CreateNewNodeTests(unittest.TestCase):

    def setUp(self):
        
        # Start WebDriver
        self.driver = util.launch_driver()

        # Create test user
        self.user_data = util.create_user(self.driver)
        
        # Login to test account
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )

        # Create project and store URL
        self.url = util.create_project(self.driver)

    def tearDown(self):

        # Close WebDriver
        self.driver.close()

    def test_new_node(self):
        self.driver.get(self.url)
        create_node_btn = self.driver.find_element_by_link_text("New Node")
        create_node_btn.click()
        title_field = self.driver.find_element_by_xpath(
            '//form[@class="well form-inline"]//input[@name="title"]')
        title = "This is a node"
        title_field.send_keys(title)
        category_fields = self.driver.find_elements_by_xpath(
            '//form[@class="well form-inline"]//select[@id="select01"]')
        for field in category_fields:
            if field.text.find('Project'):
                field.click()
        submit_btn = self.driver.find_element_by_xpath(
            '//button[@class="btn"][@type="submit"]')
        submit_btn.click()
        self.assertEqual(self.driver.find_element_by_link_text(title).text, title)

# Run tests
if __name__ == '__main__':
    unittest.main()
