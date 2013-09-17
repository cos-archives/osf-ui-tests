import httplib as http

from bs4 import BeautifulSoup
import requests

from . import endpoints


class OsfClientException(Exception):
    pass


class OsfClient(object):
    def __init__(self, api_key=None):
        self.http_auth = (api_key, '')
        # TODO: This should be a lazy list of projects, not a dict.
        self.projects = dict()

    def add_component(self, title, parent, category=None):
        r = requests.post(
            endpoints.add_node(parent),
            auth=self.http_auth,
            data={
                'title': title,
                'category': category or 'Other'
            }
        )
        if r.status_code is not http.OK:
            raise OsfClientException('Component was not created')

        soup = BeautifulSoup(r.content)
        component_id = soup.select(
            '#Nodes li h3 a'
        )[0]['href'].strip('/').split('/')[-1]

        if category == 'Project':
            parent.components[component_id] = OsfProject(
                parent=parent,
                project_id=component_id,
            )
        else:
            parent.components[component_id] = OsfComponent(
                parent=parent,
                component_id=component_id,
            )

        return parent.components[component_id]

    def add_project(self, title, description='', parent=None):
        """Adds a project; returns its project ID

        """
        if parent:
            return self.add_component(
                title=title,
                parent=parent,
                category='Project'
            )

        r = requests.post(
            endpoints.add_project(parent),
            auth=self.http_auth,
            data={
                'title': title,
                'description': description,
            }
        )

        if r.status_code is not http.OK:
            raise OsfClientException('Project was not created')

        project_id = r.url.strip('/').split('/')[-1]
        self.projects[project_id] = OsfProject(
            # TODO: Refactor this once the API endpoint is done.
            project_id=project_id
        )
        return self.projects[project_id]


class OsfProject(object):
    def __init__(self, project_id, parent=None):
        self.id = project_id
        self.parent = parent
        # TODO: This should be a lazy list of components, not a dict.
        self.components = dict()

    @property
    def url(self):
        return '/project/' + self.id


class OsfComponent(object):
    def __init__(self, parent, component_id):
        self.parent = parent
        self.component_id = component_id