import unittest

from osf_api import OsfClient, OsfComponent, OsfProject

from config import osf_home
from pages import helpers, LoginPage


class NodeAccessTests(object):#unittest.TestCase):
    def setUp(self):
        page = LoginPage().log_in(helpers.create_user())
        self.client = OsfClient(
            api_key=page.settings.add_api_key()
        )
        page.close()

    def test_project_api_summary(self):
        project = self.client.add_project('Project')

        self.assertEqual(
            project.title,
            'Project',
        )

        self.assertEqual(
            '{}/project/{}/'.format(osf_home, project.id),
            project.url,
        )

    def test_subproject_api_summary(self):
        project = self.client.add_project('Project')
        subproject = self.client.add_project('Subproject', project.id)

        self.assertEqual(
            subproject.title,
            'Subproject',
        )

    def test_component_api_summary(self):
        project = self.client.add_project('Project')
        component = self.client.add_component('Component', project.id)

        self.assertEqual(
            component.title,
            'Component',
        )

    def test_nested_component_api_summary(self):
        project = self.client.add_project('Project')
        subproject = self.client.add_project('Subproject', project.id)
        component = self.client.add_component('Component', subproject.id)

        self.assertEqual(
            component.title,
            'Component',
        )

