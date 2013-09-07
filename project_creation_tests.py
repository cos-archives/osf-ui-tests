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


class ProjectCreationTests2(unittest.TestCase):

    def test_date_created(self):

        page = get_new_project('Test Project')

        self.assertAlmostEqual(
            page.date_created,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )

        page.close()


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

        #navigate to dashboard
        util.goto_dashboard(self.driver)

        #find created project in dashboard
        title=self.driver.find_element_by_link_text(config.project_title)
        self.assertTrue(title)

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