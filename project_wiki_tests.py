"""
Selenium tests for user account creation. Tests valid account creation,
as well as various ways to do it wrong (mismatched passwords, invalid
email addresses, etc.).
"""

import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Project imports
import base
import util
import config


class ProjectWikiTests(base.ProjectSmokeTest):
    
    # Utility functions

    def _edit_wiki_setup(self):
        """
        """
        
        # Browse to wiki page
        self.driver.find_element_by_link_text('Wiki').click()
        
        # Get original version and text
        orig_version = util.get_wiki_version(self.driver)
        orig_text = util.get_wiki_text(self.driver) if orig_version else ''
        
        # Click edit button
        util.edit_wiki(self.driver)
        
        return orig_version, orig_text
        
    def _edit_wiki_teardown(self, expected_version, expected_text):
        """
        """
        
        # Test preview text
        preview_text = util.get_wiki_preview(self.driver)
        self.assertEqual(preview_text, expected_text)
        
        # Click submit button
        util.submit_wiki_text(self.driver)

        # Get updated version and text
        new_version = util.get_wiki_version(self.driver)
        new_text = util.get_wiki_text(self.driver) if new_version else ''
        
        # Test version and text
        self.assertEqual(new_version, expected_version)
        self.assertEqual(new_text, expected_text)
        
        # Check version on dashboard
        self._check_dashboard(expected_version)
    
    def _test_wiki_delete(self):
        
        # Get original values and open edit box
        orig_version, orig_text = self._edit_wiki_setup()

        # Clear text
        util.clear_wiki_text(self.driver)
        
        # Update expected version and text
        expected_version = orig_version + 1
        expected_text = ''
        
        # Submit changes and check results
        self._edit_wiki_teardown(expected_version, expected_text)
        
    def _test_wiki_edit(self, new_text):
        
        # Get original values and open edit box
        orig_version, orig_text = self._edit_wiki_setup()

        # Enter text
        util.add_wiki_text(self.driver, new_text)
        
        # Update expected version and text
        expected_version = orig_version + 1
        expected_text = orig_text + new_text
        
        # Submit changes and check results
        self._edit_wiki_teardown(expected_version, expected_text)
    
    def _check_dashboard(self, expected_version):
        
        # Browse to project page
        util.goto_project(self.driver)
        
       # Get latest version update
        version = self.driver.find_element_by_css_selector(
            'span[data-bind="text: params.version"]'
        ).text

        # Assert that expected version is in version string
        self.assertIn(str(expected_version), version)

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
            util.add_wiki_text(self.driver, new_text)
        
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
            util.get_wiki_input(self.driver).get_attribute('value'),
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
        wiki_par = util.get_wiki_par(self.driver)
        bold_elements = wiki_par.find_elements_by_tag_name('strong')
        self.assertTrue(strong_fun(len(bold_elements)))
    
    def test_wiki_format_batch(self):
        """ Test bold / unbold functions. """
        
        self._test_wiki_format('make this bold', 'make this bold', 'bold')
        self._test_wiki_format('', 'make this bold', 'unbold')