import httplib as http
import json
import requests
import unittest

from pages import helpers, LoginPage
from osf_api import OsfClient
from osf_api.user import OsfUser


class ApiUserKeyTestCase(unittest.TestCase):
    def setUp(self):
        self.user = helpers.create_user()
        page = LoginPage().log_in(self.user)
        key = page.settings.add_api_key()
        page.close()

        self.client = OsfClient(api_key=key)

    def test_get_user_self(self):
        self.assertIsInstance(
            self.client.user(),
            OsfUser
        )

    def test_user_full_name(self):
        self.assertEqual(
            self.client.user().full_name,
            self.user.full_name,
        )

    def test_user_id(self):
        self.assertTrue(
            5,
            len(self.client.user().id),
        )


    def test_change_user_fullname(self):
        user = helpers.create_user()
        page = LoginPage().log_in(user)
        profile_page = page.driver.find_element_by_link_text(
            'My Public Profile'
        ).get_attribute('href')
        key = page.settings.add_api_key()
        page.close()

        r = requests.post(
            profile_page + 'edit/',
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