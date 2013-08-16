import config
import util

from base import ProjectSmokeTest, not_implemented

from selenium.common.exceptions import TimeoutException


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
        """Test that public and private states work as intended.

        TODO: While this test tests security fine, it doesn't test the pop-up
        modals at all. This is because we ran into complex issues with selenium,
        trying to get it to fully load the GET requests after dismissing the
        confirmation modal.

        This should be fixed once we understand selenium better.
        """

        self.make_public()

        self.log_out()

        # Confirm access be comparing project's title to the expected value
        self.goto('dashboard')
        self.assertEqual(
            config.project_title,
            self.get_element('#node-title-editable').text
        )

        self.log_in()

        self.make_private()

        self.log_out()

        self.goto('dashboard')

        self.assertEqual(
            len(util.get_alert_boxes(self.driver, 'not authorized')),
            1
        )

        self.log_in()

    def test_public_non_contributor_modify(self):
        """ Users who are not contributors should not have access to the wiki
        edit page of a public project.
        """

        self.make_public()

        second_user = self.create_user()

        self.log_out()
        self.log_in(second_user)

        # Try to edit the wiki
        self.goto('wiki')
        self.driver.get('/'.join([
            self.driver.current_url.strip('/'),
            'edit',
        ]))

        # should have redirect the user elsewhere
        self.assertNotIn(
            'edit',
            self.driver.current_url
        )

        # try to add a node
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.add_component('hypothesis', 'foo')

        # try to delete the project
        self.goto('settings')
        self.assertNotIn(
            'settings',
            self.driver.current_url
        )

        # try to rename the project
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.edit_title('foo')

        # try to add a contributor
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.add_contributor(second_user)

        # try to remove a contributor
        self.goto('dashboard')
        # with self.assertRaises(TimeoutException):
        self.remove_contributor(self.user_data)
        self.goto('dashboard')
        self.assertIn(
            self.user_data['fullname'],
            self.get_element('#contributors').text,
        )

        # log back in so teardown works.
        self.log_out()
        self.log_in()

    @not_implemented
    def test_fork_with_private_components(self):
        raise NotImplementedError
