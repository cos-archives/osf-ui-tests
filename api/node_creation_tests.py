import unittest

from osf_api import OsfClient, OsfComponent, OsfProject
from pages import helpers, LoginPage


class ApiUserKeyCreateNodeTestCase(unittest.TestCase):
    def setUp(self):
        page = LoginPage().log_in(helpers.create_user())
        self.client = OsfClient(
            api_key=page.settings.add_api_key().key
        )
        page.close()

    def test_create_project(self):
        # A project should be returned
        self.assertIsInstance(
            self.client.add_project('New Project'),
            OsfProject,
        )

    def test_create_subproject(self):
        parent = self.client.add_project('New Project')

        subproject = self.client.add_project(
            'Subproject',
            parent=parent
        )

        # a project should be returned ...
        self.assertIsInstance(
            subproject,
            OsfProject,
        )

        # ... and its parent should be set
        self.assertEqual(
            subproject.parent,
            parent,
        )

    def test_create_component(self):
        parent = self.client.add_project('Parent Project')
        component = self.client.add_component(
            title='Test Component',
            parent=parent,
            category='Hypothesis'
        )

        # a component should be returned ...
        self.assertIsInstance(
            component,
            OsfComponent,
        )

        # ... and its parent should be set
        self.assertEqual(
            component.parent,
            parent
        )

    def test_create_nested_component(self):
        parent_project = self.client.add_project('New Project')

        subproject = self.client.add_project(
            'Subproject',
            parent=parent_project
        )

        component = self.client.add_component(
            title='Test Component',
            parent=subproject,
            category='Hypothesis'
        )

        # a component should be returned ...
        self.assertIsInstance(
            component,
            OsfComponent,
        )

        # ... and its parent should be set
        self.assertEqual(
            component.parent,
            subproject,
        )