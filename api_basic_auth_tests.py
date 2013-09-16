import httplib as http
import json
import unittest
import requests

from pages import helpers, LoginPage
from pages.auth import ApiKey


class ApiAuthTestCase(unittest.TestCase):
    def test_user_key_creation(self):
        user = helpers.create_user()
        page = LoginPage().log_in(user)
        key = page.settings.add_api_key()
        page.close()
        self.assertIsInstance(key, ApiKey)

    def test_project_key_creation(self):
        page = helpers.get_new_project()
        key = page.settings.add_api_key()
        page.close()

        self.assertIsInstance(key, ApiKey)

    def test_subproject_key_creation(self):
        page = helpers.get_new_subproject()
        key = page.settings.add_api_key()
        page.close()

        self.assertIsInstance(key, ApiKey)

    def test_component_key_creation(self):
        page = helpers.get_new_component()
        key = page.settings.add_api_key()
        page.close()

        self.assertIsInstance(key, ApiKey)

    def test_nested_component_key_creation(self):
        page = helpers.get_new_nested_component()
        key = page.settings.add_api_key()
        page.close()

        self.assertIsInstance(key, ApiKey)


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
    def test_change_user_fullname(self):
        user = helpers.create_user()
        page = LoginPage().log_in(user)
        profile_page = page.driver.find_element_by_link_text(
            'My Public Profile'
        ).get_attribute('href')
        key = page.settings.add_api_key()
        page.close()

        r = requests.post(
            profile_page + '/edit',
            auth=(
                key.key,
                '',
            ),
            data={
                'name': 'fullname',
                'value': 'praC auhsoJ'
            }
        )

        self.assertEqual(r.status_code, http.OK)
        self.assertEqual(
            json.loads(r.content).get('response'),
            'success',
        )

        page = LoginPage().log_in(user)
        self.assertEqual(
            page.profile.full_name,
            'praC auhsoJ'
        )
        page.close()
