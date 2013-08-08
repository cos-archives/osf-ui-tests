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

# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Project imports
import base
import util
import config

class UITests(base.ProjectSmokeTest):
    
    def setUp(self):
        
        # Call parent setUp
        super(UITests, self).setUp()

        # Log out
        util.logout(self.driver)

    def tearDown(self):
        
        # Need to login again to delete project
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )

        # Call parent tearDown
        super(UITests, self).tearDown()

    def test_unauthorized_access_private_project(self):
        """
        test user attempt to access a private repo w/o permission
        checks alert message box text against expected alert message
        """

        # point the browser at test project
        self.driver.get(self.project_url)

        # grab text from alert box presented to user
        alerts = util.get_alert_boxes(self.driver, 'you are not authorized')
        self.assertEqual(len(alerts), 1)

    def test_attempted_access_nonexistent_project(self):
        """
        test user attempt to access a non-existent
        checks alert message box text against expected alert message
        """

        # point the browser at a non-existent project
        self.driver.get('%s/project/fakeproject/' % (config.osf_home))
        
        # Must be exactly one matching alert
        alerts = util.get_alert_boxes(self.driver, 'not a valid project')
        self.assertEqual(len(alerts), 1)