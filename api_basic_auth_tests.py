import httplib as http
import unittest
import requests

import config
from pages import helpers, LoginPage
from pages.auth import ApiKey


class ApiAuthTestCase(unittest.TestCase):
    def test_user_key_creation(self):
        user = helpers.create_user()
        page = LoginPage().log_in(user)
        key = page.settings.add_api_key()
        page.close()
        self.assertIsInstance(key, ApiKey)

    @unittest.skip('not yet implemented')
    def test_change_user_fullname(self):
        user = helpers.create_user()
        page = LoginPage().log_in(user)
        profile_page = page.driver.find_element_by_link_text(
            'My Public Profile'
        ).get_attribute('href')
        key = page.settings.add_api_key()
        page.close()

        r = requests.post(
            profile_page,
            auth=(
                key.key,
                ''
            ),
            data={
                'name': 'fullname',
                'value': 'praC auhsoJ'
            }
        )

        self.assertEqual(r.status_code, http.OK)

