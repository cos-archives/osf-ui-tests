"""
Tests for creating projects.
"""

import datetime as dt
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

# Project imports
import base
import util
import config

from pages import LoginPage
from pages.helpers import get_new_project


class ProjectCreationTests(base.UserSmokeTest):

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