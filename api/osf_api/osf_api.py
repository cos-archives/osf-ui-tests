from bs4 import BeautifulSoup
import requests

from . import endpoints, exceptions
from .node import OsfComponent, OsfProject
from .user import OsfUser


class OsfClient(object):
    def __init__(self, api_key=None):
        self.http_auth = (api_key.key, '')
        # TODO: This should be a lazy list of projects, not a dict.
        self.projects = dict()

    def add_component(self, title, parent_id, category=None):
        r = requests.post(
            endpoints.add_node(parent_id),
            auth=self.http_auth,
            data={
                'title': title,
                'category': category or 'Other'
            }
        )

        exceptions.assert_auth_passed(r)

        soup = BeautifulSoup(r.content)
        component_id = soup.select(
            '#Nodes li h3 a'
        )[0]['href'].strip('/').split('/')[-1]

        parent = OsfProject(parent_id)

        if category == 'Project':
            parent.components[component_id] = OsfProject(
                parent_id=parent_id,
                project_id=component_id,
                http_auth=self.http_auth,
            )
        else:
            parent.components[component_id] = OsfComponent(
                parent_id=parent_id,
                component_id=component_id,
                http_auth=self.http_auth,
            )

        return parent.components[component_id]

    def add_project(self, title, description='', parent_id=None):
        """Adds a project; returns its project ID

        """
        if parent_id:
            return self.add_component(
                title=title,
                parent_id=parent_id,
                category='Project'
            )

        r = requests.post(
            endpoints.add_node(parent_id),
            auth=self.http_auth,
            data={
                'title': title,
                'description': description,
            }
        )

        exceptions.assert_auth_passed(r)

        project_id = r.url.strip('/').split('/')[-1]
        self.projects[project_id] = OsfProject(
            # TODO: Refactor this once the API endpoint is done.
            project_id=project_id,
            http_auth=self.http_auth,
        )
        return self.projects[project_id]

    def project(self, project_id, parent_id=None):
        return OsfProject(
            project_id=project_id,
            parent_id=parent_id,
            http_auth=self.http_auth,
        )

    def component(self, component_id, project_id):
        return OsfComponent(
            component_id=component_id,
            parent_id=project_id,
            http_auth=self.http_auth,
        )

    def user(self, user_id=None):
        return OsfUser(user_id=user_id, http_auth=self.http_auth)
