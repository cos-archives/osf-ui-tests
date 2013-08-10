import config
import util

from base import ProjectSmokeTest, not_implemented


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

    @not_implemented
    def test_fork_with_private_components(self):
        raise NotImplementedError