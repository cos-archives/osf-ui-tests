from base import ProjectSmokeTest
from util import generate_tests


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

generate_tests(ProjectSecurityTest)

if __name__ == '__main__':
    import unittest
    unittest.main()