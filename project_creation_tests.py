"""
Tests for creating projects.
"""

import unittest

from selenium import webdriver

# Project imports
import base
import util
import config

class ProjectCreationTests(base.UserSmokeTest):

    def test_create_project(self):
        """
        test to make sure that creating a project works correctly
        """

        # Create project with default args
        util.create_project(self.driver)

        #assert that the title and description above the same
        #as the webpage
        redirect_title = self.driver.find_element_by_xpath(
            '//h1[@id="node-title-editable"]'
        ).text
        redirect_description_all = self.driver.find_element_by_xpath(
            '//p[@id="contributors"]'
        ).text
        #theres a lot of text in this p element, so have to find
        #where the description starts
        index = redirect_description_all.find(config.project_description)
        self.assertEqual(
            redirect_description_all[index:],
            config.project_description
        )
        self.assertEqual(redirect_title, config.project_title)

        # Delete project
        util.delete_project(self.driver)

    def test_create_project_no_title(self):
        #self.project_title = ''
        #self.project_description = "This is a great project"
        util.create_project(self.driver, '')
        #    self.driver, self.project_title, self.project_description)
        alert_msg = self.driver.find_element_by_xpath(
            '//div[@class="alert alert-block alert-warning fade in"]//p'
        ).text
        self.assertEqual(alert_msg, "Title is required")
        #assert that a title is needed

    def test_create_project_no_description(self):

        # 
        util.create_project(
            self.driver, 
            project_description=''
        )

        #assert that the title and description above the same
        #as the webpage
        redirect_title = self.driver.find_element_by_xpath(
            '//h1[@id="node-title-editable"]'
        ).text

        #theres a lot of text in this p element, so have to find
        #where the description starts
        self.assertEqual(redirect_title, config.project_title)
        util.delete_project(self.driver)
    
    def test_delete_project(self):
        """ Test creating and then deleting a project. """
            
        # Create a new project
        util.create_project(self.driver)
        
        # Delete the project
        util.delete_project(self.driver)
        
        # Get alert boxes
        alerts = util.get_alert_boxes(self.driver, 'component(s) deleted')
        
        # Must be exactly one matching alert
        self.assertEqual(len(alerts), 1)

# Generate tests
def test():
    util.generate_tests(ProjectCreationTests)

# Run tests
if __name__ == '__main__':
    unittest.main()
