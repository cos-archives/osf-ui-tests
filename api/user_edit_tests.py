import httplib as http
import json
import requests
import unittest

from pages import helpers, LoginPage


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