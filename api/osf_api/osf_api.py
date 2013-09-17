import httplib as http

from bs4 import BeautifulSoup
import requests

from . import endpoints


class OsfClientException(Exception):
    def __init__(self, *args, **kwargs):
        self.http_status_code = kwargs.get('http_status_code')
        super(OsfClientException, self).__init__(*args)


class OsfClient(object):
    def __init__(self, api_key=None):
        self.http_auth = (api_key, '')
        # TODO: This should be a lazy list of projects, not a dict.
        self.projects = dict()

    def add_component(self, title, parent, category=None):
        r = requests.post(
            endpoints.add_component(parent),
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
                http_auth=self.http_auth,
            )
        else:
            parent.components[component_id] = OsfComponent(
                parent=parent,
                component_id=component_id,
                http_auth=self.http_auth,
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
            project_id=project_id,
            http_auth=self.http_auth,
        )
        return self.projects[project_id]

    def project(self, project_id):
        return OsfProject(
            project_id=project_id,
            http_auth=self.http_auth
        )

    def component(self, project_id, component_id):
        return OsfComponent(
            component_id=component_id,
            parent=self.project(project_id),
            http_auth=self.http_auth,
        )


class OsfNode(object):
    def __init__(self, http_auth=None):
        self.http_auth = http_auth

    @property
    def title(self):
        r = requests.get(
            self.url,
            auth=self.http_auth,
        )

        if r.status_code == http.FORBIDDEN:
            raise OsfClientException(
                'Access Denied',
                http_status_code=int(r.status_code)
            )
        elif r.status_code != http.OK:
            raise OsfClientException(http_status_code=r.status_code)
        soup = BeautifulSoup(r.content)

        return soup.find(id='node-title-editable').text

    @title.setter
    def title(self, value):
        r = requests.post(
            self._edit_endpoint,
            auth=self.http_auth,
            data={
                'name': 'title',
                'value': value,
            },
        )

        if r.status_code is not http.OK:
            raise OsfClientException('Title update failed')


class OsfProject(OsfNode):
    def __init__(self, project_id, *args, **kwargs):
        self.id = project_id
        self.parent = kwargs.get('parent')
        if self.parent:
            del kwargs['parent']

        # TODO: This should be a lazy list of components, not a dict.
        self.components = dict()

        self._edit_endpoint = endpoints.edit_project(project_id)

        super(OsfProject, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return '{}/project/{}'.format(endpoints.root, self.id)


class OsfComponent(OsfNode):
    def __init__(self, parent, component_id, *args, **kwargs):
        self.parent = parent
        self.id = component_id

        self._edit_endpoint = endpoints.edit_component(
            component_id=component_id,
            project_id=parent.id if parent else None,
        )

        super(OsfComponent, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return '{}/project/{}/node/{}'.format(
            endpoints.root,
            self.parent.id,
            self.id,
        )