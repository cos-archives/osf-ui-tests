"""
sample usage of selenium in OSF context

Note: As of version 2 Selenium does not have native ability to
grab HTTP response codes. So, we have a few options:

1. Ignore them, and either
    a) look at the final page user is redirected to
    b) look for specific ids in the redirected page (like below)
2. Use an odd NetCaptcher hack with Firefox. But, this limits us
to using Firefox. Terrible.
3. Setup a proxy server to handle the get requests and inject the info we want
    "BrowserMob Proxy" is recommended. Seems hackish.
    Base package:   https://github.com/lightbody/browsermob-proxy
    Python wrapper: https://github.com/AutomatedTester/browsermob-proxy-py
4. Alter actual OSF pages to place 'web responses' in the page source
    custom meta-tags or something else. Seems hackish.
"""
import unittest

from selenium import webdriver
from pymongo import MongoClient

from util import login, create_project, clear_project

client = MongoClient("localhost:20771")
database = client["test"]


class projectCreationTest(unittest.TestCase):

    # initialize a Firefox webdriver

    def setUp(self):
        username = "samson@gmail.com"
        password = "jeans123"
        self.driver = webdriver.Firefox()
        login(self.driver, username, password)

    def test_create_project(self):
        """
        test to make sure that creating a project works correctly
        """
        self.project_title = "Sam's Great Project"
        self.project_description = "This is a great project"
        create_project(
            self.driver, self.project_title, self.project_description)
        #assert that the title and description above the same
        #as the webpage
        redirect_title = self.driver.find_element_by_xpath(
            '//h1[@id="node-title-editable"]').text
        redirect_description_all = self.driver.find_element_by_xpath(
            '//p[@id="contributors"]').text
        #theres a lot of text in this p element, so have to find
        #where the description starts
        index = redirect_description_all.find(self.project_description)
        self.assertEqual(
            redirect_description_all[index:], self.project_description)
        self.assertEqual(redirect_title, self.project_title)
        self.project_url = self.driver.current_url

    # close the Firefox webdriver
    def tearDown(self):
        self.driver.close()
        clear_project(self.project_title)


if __name__ == '__main__':
    unittest.main()
