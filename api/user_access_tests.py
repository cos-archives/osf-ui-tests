import datetime as dt
import unittest

from pages import helpers, LoginPage
from osf_api import OsfClient


class ApiUserProfilesTestCase(unittest.TestCase):
    def setUp(self):
        self.user = helpers.create_user()
        page = LoginPage().log_in(self.user)
        key = page.settings.add_api_key()
        page.close()

        self.client = OsfClient(api_key=key)

    def test_own_profile(self):
        profile = self.client.user()

        self.assertEqual(
            self.user.full_name,
            profile.full_name,
        )

    def test_others_profile(self):
        own_profile = self.client.user()

        # Create another user, get their API key
        other_user = helpers.create_user()
        page = LoginPage().log_in(other_user)
        key = page.settings.add_api_key()
        page.close()

        other_client = OsfClient(api_key=key)
        other_profile = self.client.user(user_id=other_client.user().id)

        self.assertNotEqual(
            own_profile.id,
            other_profile.id,
        )

    def test_date_registered(self):
        self.assertEqual(
            dt.date.today(),
            self.client.user().date_registered,
        )

    def test_activity_points_increment(self):
        self.assertEqual(0, self.client.user().activity_points)

        self.client.add_project('Test Project')

        self.assertEqual(1, self.client.user().activity_points)

    @unittest.skip('Fails - public/private routes not yet implemented')
    def test_project_counts_private_project(self):
        self.assertEqual(0, self.client.user().total_project_count)

        project = self.client.add_project("Test Project")

        info = self.client.user()

        self.assertEqual(0, info.public_project_count)
        self.assertEqual(1, info.private_project_count)
        self.assertEqual(1, info.total_project_count)

        project.public = True

        info = self.client.user()

        self.assertEqual(1, info.public_project_count)
        self.assertEqual(0, info.private_project_count)
        self.assertEqual(1, info.total_project_count)

    @unittest.skip('Fails - public/private routes not yet implemented')
    def test_public_projects(self):
        self.assertEqual(0, len(self.client.user().public_projects))

        project = self.client.add_project('Test Project')
        project.public = True

        self.assertEqual(1, len(self.client.user().public_projects))

    @unittest.skip('Fails - public/private routes not yet implemented')
    def test_public_components(self):
        self.assertEqual(0, len(self.client.user().public_components))

        project = self.client.add_project('Test Project')
        component = self.client.add_component(
            title='Test Component',
            parent_id=project.id,
            category='Hypothesis',
        )

        component.public = True

        self.assertEqual(1, len(self.client.user().public_components))

