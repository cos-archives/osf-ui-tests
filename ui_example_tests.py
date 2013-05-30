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
from selenium.common.exceptions import NoSuchElementException

client = MongoClient("localhost:20771")
database = client["test"]


class sampleOSFUITests(unittest.TestCase):

    # initialize a Firefox webdriver
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.user_email = 'samson@gmail.com'
        self.user_password = 'jeans123'
        self.user_name = 'Sam Portnow'
        self.driver.implicitly_wait(10)
        self.driver.get('http://localhost:5000')
        self.driver.find_element_by_xpath('//a[@href="/account"]').click()
        username_field = self.driver.find_elements_by_xpath(
            '//form[@name="signin"]//input[@id="username"]')
        password_field = self.driver.find_elements_by_xpath(
            '//form[@name="signin"]//input[@id="password"]')
        username_field[0].send_keys(self.user_email)
        password_field[0].send_keys(self.user_password)
        submit_buttons = self.driver.find_elements_by_xpath(
            '//button[@type="submit"]')
        submit_button = [b for b in submit_buttons if
                         b.text.lower() == 'sign in'][0]
        submit_button.click()
        database["node"].remove({"title": "Sam's Great Project"})

    # close the Firefox webdriver
    def tearDown(self):
        self.driver.close()

    def test_unauthorized_access_private_project(self):
        """
        test user attempt to access a private repo w/o permission
        checks alert message box text against expected alert message
        """
        driver = self.driver

        # point the browser at a private project
        driver.get('http://openscienceframework.org/project/xeAXJ/')

        # grab text from alert box presented to user
        try:
            alert_msg = driver.find_element_by_xpath(
                '//div[@class="alert alert-block alert-warning fade in"]//p'
            ).text
        # @TODO: How do we want to handle this?
        except NoSuchElementException:
            alert_msg = ''

        # assert alert text matches expected warning.
        self.assertTrue(
            'You are not authorized to perform that action for this node'
            in alert_msg)

    def test_attempted_access_nonexistent_project(self):
        """
        test user attempt to access a non-existent
        checks alert message box text against expected alert message
        """
        driver = self.driver

        # point the browser at a non-existent project
        driver.get(
            'http://openscienceframework.org/project/not_a_real_project/')

        # grab text from alert box presented to user
        try:
            alert_msg = driver.find_element_by_xpath(
                '//div[@class="alert alert-block alert-warning fade in"]//p'
            ).text
        # @TODO: How do we want to handle this?
        except NoSuchElementException:
            alert_msg = ''

        # assert alert text matches expected warning.
        self.assertTrue('Not a valid project' in alert_msg)

    def test_create_project(self):
        """
        test to make sure that creating a project works correctly
        """
        #go to the dashboard
        self.driver.get('http://localhost:5000/dashboard')
        #find the new project link and click it
        link = self.driver.find_element_by_link_text("New Project")
        link.click()
        # enter the title and description of your project
        # in the relevant fields and submit
        title_field = self.driver.find_element_by_xpath(
            '//form[@name="newProject"]//input[@id="title"]')
        description_field = self.driver.find_element_by_xpath(
            '//form[@name="newProject"]//textarea[@id="description"]')
        title = "Sam's Great Project"
        description = "This is my project"
        title_field.send_keys(title)
        description_field.send_keys(description)
        submit_button = self.driver.find_element_by_xpath(
            '//button[@class="btn primary"][@type="submit"]')
        submit_button.click()
        #assert that the title and description above the same
        #as the webpage
        redirect_title = self.driver.find_element_by_xpath(
            '//h1[@id="node-title-editable"]').text
        redirect_description_all = self.driver.find_element_by_xpath(
            '//p[@id="contributors"]').text
        #theres a lot of text in this p element, so have to find
        #where the description starts
        index = redirect_description_all.find(description)
        self.assertEqual(redirect_description_all[index:], description)
        self.assertEqual(redirect_title, title)

if __name__ == '__main__':
    unittest.main()
