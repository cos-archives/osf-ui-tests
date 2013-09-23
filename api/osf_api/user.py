import datetime as dt
import json
import requests

from . import endpoints
from . import exceptions
from .common import ApiKey


class OsfUser(object):
    def __init__(self, user_id, http_auth):
        self.http_auth = http_auth
        self._call_summary_api(user_id)

    @property
    def activity_points(self):
        return self._api_summary['activity_points'] or 0

    @property
    def api_keys(self):
        try:
            return self._api_keys
        except AttributeError:
            r = requests.get(
                endpoints.get_user_api_keys(),
                auth=self.http_auth,
            )

            exceptions.assert_auth_passed(r)

            self._api_keys = [
                ApiKey(
                    key=x['key'],
                    label=x['label'],
                ) for x in json.loads(r.content)
            ]

            return self._api_keys

    @property
    def date_registered(self):
        return dt.datetime.strptime(
            self._api_summary['date_registered'],
            '%Y-%m-%d',
        ).date()

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

    @property
    def public_projects(self):
        try:
            return self._public_projects
        except AttributeError:
            r = requests.get(
                endpoints.get_user_public_projects(self.id),
                auth=self.http_auth,
            )

            exceptions.assert_auth_passed(r)

            self._public_projects = json.loads(r.content)

            return self._public_projects

    @property
    def public_components(self):
        try:
            return self._public_components
        except AttributeError:
            r = requests.get(
                endpoints.get_user_public_projects(self.id),
                auth=self.http_auth,
            )

            exceptions.assert_auth_passed(r)

            self._public_components = json.loads(r.content)

            return self._public_components

    def add_api_key(self, label=None):
        old_keys = self.api_keys

        r = requests.post(
            endpoints.add_user_api_key(),
            auth=self.http_auth,
            data={
                'label': label or 'Generated via API'
            }
        )

        exceptions.assert_auth_passed(r)

        del self._api_keys
        new_keys = self.api_keys

        return [x for x in new_keys if x not in old_keys][0]

    def revoke_api_key(self, key):
        old_keys = self.api_keys

        r = requests.post(
            endpoints.revoke_user_api_key(),
            auth=self.http_auth,
            data={
                'key': key.key
            }
        )

        exceptions.assert_auth_passed(r)

        del self._api_keys

        return True

    def _call_summary_api(self, user_id):
        r = requests.get(
            endpoints.get_user(user_id),
            auth=self.http_auth
        )

        exceptions.assert_auth_passed(r)

        self._api_summary = json.loads(r.content)