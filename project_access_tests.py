import time

from base import ProjectSmokeTest
from util import generate_tests, get_alert_boxes


class ProjectSecurityTest(ProjectSmokeTest):

    def setUp(self):
        super(ProjectSecurityTest, self).setUp()

        self.second_user = self.create_user()

    def test_add_contributor(self):

        # Add a contributor
        self.goto('dashboard')
        self.add_contributor(self.second_user)

        # Make sure they're in the contributors list
        self.assertTrue(
            self.second_user['fullname'] in
            self.get_element('#contributors').text
        )

        # get the project's title
        project_title = self.get_element('h1#node-title-editable').text

        # log in as the second user
        self.log_out()
        self.log_in(self.second_user)

        # go the project dashboard.
        self.goto('dashboard')

        # check to make sure we're on the project page, not redirected home.
        self.assertEqual(
            self.get_element('h1#node-title-editable').text,
            project_title,
        )

    def test_remove_contributor(self):

        # Add a contributor
        self.goto('dashboard')
        self.add_contributor(self.second_user)

        # refresh the page
        self.goto('dashboard')

        # remove the contributor
        self.remove_contributor(self.second_user)

        # log out and back in as the second user
        self.log_out()
        self.log_in(self.second_user)

        self.goto('dashboard')

        # There should be no project list, so just make sure the project title
        # isn't on the page.
        self.assertTrue(
            'not authorized' in self.get_element('div.alert').text
        )

        # log out and back in as the first user, so teardown will work
        self.log_out()
        self.log_in(self.user_data)

    def test_public_private(self):
        import util
        import config
        """ Test creating a project and then making it public. """

        # Navigate to the project
        util.goto_project(self.driver, project_title=config.project_title)

        # Click the "Make public" button
        self.get_element(
            'div.btn-toolbar > div.btn-group:first-child > a'
        ).click()

        # Confirm modal popup
        self.get_element('div#modal_0 button.modal-confirm').click()

        time.sleep(3)

        self.log_out()

        # Confirm access be comparing project's title to the expected value
        self.goto('dashboard')
        self.assertEqual(
            config.project_title,
            self.get_element('#node-title-editable').text
        )

        util.login(
            driver=self.driver,
            username=self.user_data['username'],
            password=self.user_data['password'],
        )

        # Make the project private
        self.goto('dashboard')
        self.get_element(
            "div.btn-toolbar > div.btn-group:first-child > a"
        ).click()

        # Confirm modal popup
        self.get_element('div#modal_0 button.modal-confirm').click()

        self.log_out()

        time.sleep(3)
        self.goto('dashboard')

        self.assertEqual(
            len(util.get_alert_boxes(self.driver, 'not authorized')),
            1
        )

        self.log_in(self.user_data)


generate_tests(ProjectSecurityTest)

if __name__ == '__main__':
    import unittest
    unittest.main()