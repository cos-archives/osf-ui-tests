"""
Tests for creating projects.
"""

import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

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

    def test_privacy_settings(self):
        """ Test creating a project and then making it public. """

        # Create a new project
        project_url = util.create_project(
            driver=self.driver,
            project_title=config.project_title
        )

        # Navigate to the project
        util.goto_project(self.driver, project_title=config.project_title)

        # Click the "Make public" button
        wait(
            driver=self.driver,
            timeout=10
        ).until(
            method=ec.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.btn-toolbar > div.btn-group:first-child > a')
            )
        ).click()

        # Confirm modal popup
        wait(
            driver=self.driver,
            timeout=10,
        ).until(
            method=ec.element_to_be_clickable(
                locator=(By.CSS_SELECTOR, 'div#modal_0 button.modal-confirm')
            )
        ).click()

        util.logout(self.driver)

        # Confirm access be comparing project's title to the expected value
        self.driver.get(project_url)
        self.assertEqual(
            config.project_title,
            wait(
                driver=self.driver,
                timeout=10
            ).until(
                method=ec.visibility_of_element_located(
                    (By.ID, 'node-title-editable')
                )
            ).text
        )

        util.login(
            driver=self.driver,
            username=self.user_data['username'],
            password=self.user_data['password'],
        )

        # Make the project private
        self.driver.get(project_url)
        self.driver.find_element_by_css_selector(
            "div.btn-toolbar > div.btn-group:first-child > a"
        ).click()

        # Confirm modal popup
        wait(
            driver=self.driver,
            timeout=10,
        ).until(
            method=ec.element_to_be_clickable(
                locator=(By.CSS_SELECTOR, 'div#modal_0 button.modal-confirm')
            )
        ).click()

        util.logout(self.driver)

        self.driver.get(project_url)

        self.assertEqual(
            len(util.get_alert_boxes(self.driver, 'not authorized')),
            1
        )


# Generate tests
util.generate_tests(ProjectCreationTests)

# Run tests
if __name__ == '__main__':
    unittest.main()
