"""
Selenium tests for user account creation. Tests valid account creation,
as well as various ways to do it wrong (mismatched passwords, invalid
email addresses, etc.).
"""

import re
import time
import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Project imports
import util
import config


class ProjectWikiTests(unittest.TestCase):

    # Setup / teardown functions

    @classmethod
    def setUpClass(cls):

        # Launch Selenium
        cls.driver = util.launch_driver()

        # Create test account
        util.create_user(cls.driver)

        # Login to test account
        util.login(cls.driver)

    @classmethod
    def tearDownClass(cls):

        # Delete test user
        util.clear_user()

        # Close Selenium
        cls.driver.close()

    def setUp(self):

        # Create test project
        self.project_url = util.create_project(self.driver)

        # Browse to project page
        util.goto_project(self.driver)

    def tearDown(self):

        # Delete test project
        util.delete_project(self.driver)

    # Utility functions

    def _edit_wiki(self):

        edit_button = self.driver.find_element_by_link_text('Edit')
        edit_button.click()

    def _get_wiki_input(self):

        return self.driver.find_element_by_id('wmd-input')

    def _add_wiki_text(self, text):

        self._get_wiki_input().send_keys(text)

    def _clear_wiki_text(self):

        util.clear_text(self._get_wiki_input())

    def _submit_wiki_text(self):
        """ Click submit button. """

        self.driver.find_element_by_xpath(
            '//div[@class="wmd-panel"]//input[@type="submit"]'
        ).click()

    def _get_wiki_version(self):
        """ Get current wiki version. """

        # Extract version text
        version = self.driver\
        .find_element_by_xpath('//dt[text()="Version"]/following-sibling::*')\
        .text

        # Strip (current) from version string
        version = re.sub('\s*\(current\)\s*', '', version, flags=re.I)

        # Return version number or 0
        try:
            return int(version)
        except ValueError:
            return 0

    def _get_wiki_par(self):
        """ Get <p> containing wiki text. """

        # Set implicitly_wait to short value: text may not
        # exist, so we don't want to wait too long to find it
        self.driver.implicitly_wait(0.1)

        # Extract wiki text
        # Hack: Wiki text element isn't uniquely labeled,
        # so find its sibling first
        try:
            wiki_par = self.driver.find_element_by_xpath(
                '//div[@id="addContributors"]/following-sibling::div//p'
            )
        except NoSuchElementException:
            wiki_par = None

        # Set implicitly_wait to original value
        self.driver.implicitly_wait(config.selenium_wait_time)

        # Return element
        return wiki_par

    def _get_wiki_text(self):
        """ Get text from wiki <p>. """

        # Get <p> containing wiki text
        wiki_par = self._get_wiki_par()

        # Extract text
        if wiki_par is not None:
            return wiki_par.text
        return ''

    def _get_wiki_preview(self):
        """
"""

        return self.driver\
        .find_element_by_id('wmd-preview')\
        .text

    def _edit_wiki_setup(self):
        """
"""

        # Browse to wiki page
        self.driver.find_element_by_link_text('Wiki').click()

        # Get original version and text
        orig_version = self._get_wiki_version()
        orig_text = self._get_wiki_text() if orig_version else ''

        # Click edit button
        self._edit_wiki()

        return orig_version, orig_text

    def _edit_wiki_teardown(self, expected_version, expected_text):
        """
"""

        # Test preview text
        preview_text = self._get_wiki_preview()
        self.assertEqual(preview_text, expected_text)

        # Click submit button
        self._submit_wiki_text()

        # Get updated version and text
        new_version = self._get_wiki_version()
        new_text = self._get_wiki_text() if new_version else ''

        # Test version and text
        self.assertEqual(new_version, expected_version)
        self.assertEqual(new_text, expected_text)

        # Check version on dashboard
        self._check_dashboard(expected_version)

    def _test_wiki_delete(self):

        # Get original values and open edit box
        orig_version, orig_text = self._edit_wiki_setup()

        # Clear text
        self._clear_wiki_text()

        # Update expected version and text
        expected_version = orig_version + 1
        expected_text = ''

        # Submit changes and check results
        self._edit_wiki_teardown(expected_version, expected_text)

    def _test_wiki_edit(self, new_text):

        # Get original values and open edit box
        orig_version, orig_text = self._edit_wiki_setup()

        # Enter text
        self._add_wiki_text(new_text)

        # Update expected version and text
        expected_version = orig_version + 1
        expected_text = orig_text + new_text

        # Submit changes and check results
        self._edit_wiki_teardown(expected_version, expected_text)

    def _check_dashboard(self, expected_version):

        # Browse to project page
        util.goto_project(self.driver)

        # Get latest version update
        version = self.driver.find_element_by_tag_name('dd').text

        # Assert that expected version is in version string
        self.assertTrue('version %d' % (expected_version) in version)

        # Browse to wiki page
        self.driver.find_element_by_link_text('Wiki').click()

    def test_wiki_batch(self):
        """ Test entering and deleting wiki text. """

        self._test_wiki_edit('entry 1')
        self._test_wiki_edit('entry 2')
        self._test_wiki_delete()
        self._test_wiki_edit('entry 3')

    def _test_wiki_format(self, new_text, expected_text, action):
        """Test bolding wiki text.

Args:
"""
        # Setup and get starting values
        orig_version, orig_text = self._edit_wiki_setup()

        # Enter text
        if new_text:
            self._add_wiki_text(new_text)

        # Set text to boldface
        if action == 'bold':
            self.driver.execute_script(
                '$("#wmd-input").select();'
            )
        else:
            util.select_partial(self.driver, 'wmd-input', 2, len(expected_text) + 2)

        # Click bold button
        self.driver.find_element_by_id('wmd-bold-button').click()

        # Get appropriate wrap string and bold counter function
        if action == 'bold':
            expected_wrap = '**%s**' % expected_text
            strong_fun = lambda x: x > 0
        else:
            expected_wrap = expected_text
            strong_fun = lambda x: x == 0

        # Assert that wiki text has been wrapped in **
        self.assertEqual(
            self._get_wiki_input().get_attribute('value'),
            expected_wrap
        )

        # Assert that there are <strong> elements in the preview
        preview_bold_elements = self.driver.find_elements_by_css_selector(
            '#wmd-preview strong'
        )
        self.assertTrue(strong_fun(len(preview_bold_elements)))

        # Submit and check results
        expected_version = orig_version + 1
        self._edit_wiki_teardown(expected_version, expected_text)

        # Assert that there are <strong> elements in the wiki text
        wiki_par = self._get_wiki_par()
        bold_elements = wiki_par.find_elements_by_tag_name('strong')
        self.assertTrue(strong_fun(len(bold_elements)))

    def test_wiki_format_batch(self):
        """ Test bold / unbold functions. """

        self._test_wiki_format('make this bold', 'make this bold', 'bold')
        self._test_wiki_format('', 'make this bold', 'unbold')

# Run tests
if __name__ == '__main__':
    unittest.main()