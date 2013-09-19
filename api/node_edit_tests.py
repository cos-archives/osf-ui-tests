import unittest

from pages import helpers, LoginPage
from osf_api import OsfClient
from osf_api.exceptions import OsfClientException
from osf_api.common import ApiKey


class ApiNodeKeyTestCase(unittest.TestCase):
    def setUp(self):
        page = LoginPage().log_in(helpers.create_user())
        self.client = OsfClient(
            api_key=page.settings.add_api_key()
        )
        page.close()

    def test_project_add_api_key(self):
        project = self.client.add_project('Test Project')
        key = project.add_api_key()

        self.assertIsInstance(key, ApiKey)

    def test_project_edit_title(self):
        project = self.client.add_project('Test Project')
        key = project.add_api_key()

        node_id = project.id
        del project

        osf = OsfClient(api_key=key)
        project = osf.project(project_id=node_id)
        project.title = 'Title Changed'

        self.assertEqual(
            'Title Changed',
            project.title,
        )

    def test_subproject_edit_title(self):
        project = self.client.add_project('Test Project')
        subproject = self.client.add_project(
            'Subproject',
            parent_id=project.id
        )
        key = subproject.add_api_key()

        node_id = subproject.id

        osf = OsfClient(api_key=key)
        node = osf.project(project_id=node_id)
        node.title = 'Title Changed'

        self.assertEqual(
            'Title Changed',
            node.title,
        )

    def test_component_edit_title(self):
        project = self.client.add_project('Test Project')
        component = self.client.add_component(
            'Component',
            parent_id=project.id
        )
        key = component.add_api_key()

        node_id = component.id

        osf = OsfClient(api_key=key)
        node = osf.component(project_id=project.id, component_id=node_id)
        node.title = 'Title Changed'

        self.assertEqual(
            'Title Changed',
            node.title,
        )

    def test_nested_component_edit_title(self):
        project = self.client.add_project('Test Project')
        subproject = self.client.add_project(
            'Subproject',
            parent_id=project.id
        )
        component = self.client.add_component(
            'Component',
            parent_id=subproject.id,
        )
        key = component.add_api_key()

        node_id = component.id

        osf = OsfClient(api_key=key)
        node = osf.component(
            component_id=node_id,
            project_id=subproject.id,
        )
        node.title = 'Title Changed'

        self.assertEqual(
            'Title Changed',
            node.title,
        )


class ApiUserKeyTestCase(unittest.TestCase):
    def setUp(self):
        page = LoginPage().log_in(helpers.create_user())
        self.client = OsfClient(
            api_key=page.settings.add_api_key().key
        )
        page.log_out()
        page.close()

    def test_project_title(self):
        project = self.client.add_project(title='Before')

        project.title = 'After'

        self.assertEqual(
            project.title,
            'After',
        )

    def test_subproject_title(self):
        project = self.client.add_project(title='Parent Project')
        subproject = self.client.add_project(
            title='Before',
            parent_id=project.id
        )

        subproject.title = 'After'

        self.assertEqual(
            subproject.title,
            'After',
        )

    def test_component_title(self):
        project = self.client.add_project(title='Parent Project')
        component = self.client.add_component(
            title='Before',
            parent_id=project.id
        )

        component.title = 'After'

        self.assertEqual(
            component.title,
            'After',
        )

    def test_nested_component_title(self):
        project = self.client.add_project(title='Parent Project')
        subproject = self.client.add_project(
            title='Subproject',
            parent_id=project.id
        )
        component = self.client.add_component(
            title='Before',
            parent_id=subproject.id
        )

        component.title = 'After'

        self.assertEqual(
            component.title,
            'After',
        )


class ApiUserKeyNonContributorTestCase(unittest.TestCase):
    def setUp(self):
        page = LoginPage().log_in(helpers.create_user())
        self.client = OsfClient(
            api_key=page.settings.add_api_key().key
        )
        page.log_out()

        page = page.user_login.log_in(helpers.create_user())
        self.non_contrib_client = OsfClient(
            api_key=page.settings.add_api_key().key
        )
        page.close()

    def test_project_title_non_contrib(self):
        project = self.client.add_project('Test Project')

        with self.assertRaises(OsfClientException):
            p = self.non_contrib_client.project(project.id).title

    def test_subproject_title_non_contrib(self):
        project = self.client.add_project('Test Project')
        subproject = self.client.add_project('Subproject', parent_id=project.id)

        with self.assertRaises(OsfClientException):
            p = self.non_contrib_client.project(subproject.id).title

    def test_component_title_non_contrib(self):
        project = self.client.add_project('Test Project')
        component = self.client.add_component(
            'Test Component',
            parent_id=project.id
        )

        with self.assertRaises(OsfClientException):
            p = self.non_contrib_client.component(
                project_id=project.id,
                component_id=component.id
            ).title

    def test_nested_component_title_non_contrib(self):
        project = self.client.add_project('Test Project')
        subproject = self.client.add_project('Subproject', parent_id=project.id)
        component = self.client.add_component(
            'Test Component',
            parent_id=subproject.id
        )

        with self.assertRaises(OsfClientException):
            p = self.non_contrib_client.component(
                project_id=subproject.id,
                component_id=component.id
            ).title