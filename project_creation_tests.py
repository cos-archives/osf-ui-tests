"""
Tests for creating projects.
"""

# Project imports
import base
import util


class ProjectCreationTests(base.UserSmokeTest):

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