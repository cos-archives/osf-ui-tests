import httplib as http
import json
import unittest
import requests

import config
from pages import helpers, LoginPage


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
    def _test_title(self, page):
        node_id = page.id
        parent_id = page.parent_id

        edit_url = '{}/project/{}/edit'.format(
            config.osf_home,
            '{}/node/{}'.format(
                parent_id,
                node_id
            ) if parent_id else node_id,
        )

        key = page.user_dashboard.settings.add_api_key()

        r = requests.post(
            edit_url,
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

        page = page.node(node_id, parent_id)

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
