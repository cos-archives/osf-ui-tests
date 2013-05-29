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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class sampleOSFUITests(unittest.TestCase):

    # initialize a Firefox webdriver
    def setUp(self):
        self.driver = webdriver.Firefox()

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

if __name__ == '__main__':
    unittest.main()


