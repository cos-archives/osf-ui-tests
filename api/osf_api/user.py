import json
import requests

from . import endpoints
from . import exceptions


class OsfUser(object):
    def __init__(self, user_id, http_auth):
        self.http_auth = http_auth
        self._call_summary_api(user_id)

    @property
    def activity_points(self):
        return self._api_summary['activity_points']

    @property
    def full_name(self):
        return self._api_summary['fullname']

    @property
    def id(self):
        return self._api_summary['user_id']

    @property
    def private_project_count(self):
        return self.total_project_count - self.public_project_count

    @property
    def public_project_count(self):
        return self._api_summary['number_public_projects']

    @property
    def total_project_count(self):
        return self._api_summary['number_projects']

    def _call_summary_api(self, user_id):
        r = requests.get(
            endpoints.get_user(user_id),
            auth=self.http_auth
        )

        exceptions.assert_auth_passed(r)

        self._api_summary = json.loads(r.content)