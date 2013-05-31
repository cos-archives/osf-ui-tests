"""
Tests for creating projects.
"""

import unittest

from selenium import webdriver
from pymongo import MongoClient

# Project imports
import util
import config

class ProjectCreationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls.driver = webdriver.Firefox()
        
        # 
        cls.driver.implicitly_wait(30)
        
        # Create user account and login
        util.create_user(cls.driver)
        util.login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        
        # 
        util.clear_user()
    
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
        self.project_url = self.driver.current_url

        # Delete project
        util.delete_project(self.driver)

    def test_create_project_no_title(self):
        self.project_title = ''
        self.project_description = "This is a great project"
        util.create_project(
            self.driver, self.project_title, self.project_description)
        alert_msg = self.driver.find_element_by_xpath(
            '//div[@class="alert alert-block alert-warning fade in"]//p').text
        self.assertEqual(alert_msg, "Title is required")
        #assert that a title is needed

    def test_create_project_no_description(self):
            self.project_title = "My Great Project"
            self.project_description = ''
            util.create_project(
                self.driver, self.project_title, self.project_description)
            #assert that the title and description above the same
            #as the webpage
            redirect_title = self.driver.find_element_by_xpath(
                '//h1[@id="node-title-editable"]').text
            #theres a lot of text in this p element, so have to find
            #where the description starts
            self.assertEqual(redirect_title, self.project_title)
            util.delete_project("My Great Project")
    
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

if __name__ == '__main__':
    unittest.main()
