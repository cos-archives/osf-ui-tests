import unittest

from pages import helpers, LoginPage
from pages.generic import ApiKey


class ApiCreateKeysTestCase(unittest.TestCase):
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