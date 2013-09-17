import httplib as http
import json
import unittest
import requests

import config
from pages import helpers, LoginPage
from osf_api import OsfClient
from osf_api.osf_api import OsfClientException


class ApiNodeKeyTestCase(unittest.TestCase):
    def _test_title(self, page):
        project_url = page.driver.current_url
        key = page.settings.add_api_key()

        r = requests.post(
            project_url + "edit",
            auth=(key.key, ''),
            data={
                'name': 'title',
                'value': 'Changed via API',
            }
        )

        self.assertEqual(r.status_code, http.OK)
        self.assertEqual(
            json.loads(r.content).get('response'),
            'success'
        )

        page.driver.get(project_url)
        self.assertEqual(
            page.title,
            'Changed via API',
        )
        page.close()

    def test_project_title(self):
        self._test_title(helpers.get_new_project())

    def test_subproject_title(self):
        self._test_title(helpers.get_new_subproject())

    def test_component_title(self):
        self._test_title(helpers.get_new_component())

    def test_nested_component_title(self):
        self._test_title(helpers.get_new_nested_component())


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
        subproject = self.client.add_project(title='Before', parent=project)

        subproject.title = 'After'

        self.assertEqual(
            subproject.title,
            'After',
        )

    def test_component_title(self):
        project = self.client.add_project(title='Parent Project')
        component = self.client.add_component(title='Before', parent=project)

        component.title = 'After'

        self.assertEqual(
            component.title,
            'After',
        )

    def test_nested_component_title(self):
        project = self.client.add_project(title='Parent Project')
        subproject = self.client.add_project(title='Subproject', parent=project)
        component = self.client.add_component(title='Before', parent=subproject)

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

    def _test_title_non_contrib(self, page, user):

        node_id = page.id
        parent_id = page.parent_id

        edit_url = '{}/project/{}/edit'.format(
            config.osf_home,
            '{}/node/{}'.format(
                parent_id,
                node_id
            ) if parent_id else node_id,
        )

        page = page.log_out()

        page = page.user_login.log_in(helpers.create_user())

        key = page.user_dashboard.settings.add_api_key()

        page = page.log_out()

        r = requests.post(
            edit_url,
            auth=(key.key, ''),
            data={
                'name': 'title',
                'value': 'Changed via API',
            }
        )

        self.assertEqual(r.status_code, http.FORBIDDEN)

        page = page.user_login.log_in(user)

        page = page.node(node_id, parent_id)

        self.assertEqual(
            page.title,
            'Unchanged',
        )

        page.close()

    def test_project_title_non_contrib(self):
        project = self.client.add_project('Test Project')

        with self.assertRaises(OsfClientException):
            p = self.non_contrib_client.project(project.id).title

    def test_subproject_title_non_contrib(self):
        project = self.client.add_project('Test Project')
        subproject = self.client.add_project('Subproject', parent=project)

        with self.assertRaises(OsfClientException):
            p = self.non_contrib_client.project(subproject.id).title

    def test_component_title_non_contrib(self):
        project = self.client.add_project('Test Project')
        component = self.client.add_component('Test Component', parent=project)

        with self.assertRaises(OsfClientException):
            p = self.non_contrib_client.component(
                project_id=project.id,
                component_id=component.id
            ).title

    def test_nested_component_title_non_contrib(self):
        project = self.client.add_project('Test Project')
        subproject = self.client.add_project('Subproject', parent=project)
        component = self.client.add_component(
            'Test Component',
            parent=subproject
        )

        with self.assertRaises(OsfClientException):
            p = self.non_contrib_client.component(
                project_id=subproject.id,
                component_id=component.id
            ).title