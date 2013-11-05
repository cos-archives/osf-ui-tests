from pages.helpers import create_user
from tests.fixtures import UserFixture, ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture


class AddContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.page.add_contributor(cls.users[-1])
        cls.page.type = 'component' if 'node' in cls.page.driver.current_url else 'project'
        cls.old_id = cls.page.id


class AddContributorAccessFixture(AddContributorFixture):
    @classmethod
    def setUpClass(cls):
        super(AddContributorAccessFixture, cls).setUpClass()
        cls.page.log_out()
        cls.log_in(cls.users[1])
        cls.page = cls.page.node(cls.old_id, cls.project_id)


class AddMultiContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddMultiContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())
        cls.page.add_multi_contributor(cls.users[1], cls.users[2])
        cls.page.type = 'component' if 'node' in cls.page.driver.current_url else 'project'


class AddMultiContributorDeleteFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddMultiContributorDeleteFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())
        cls.page.add_multi_contributor_delete(cls.users[-2], cls.users[-1])
        cls.page.type = 'component' if 'node' in cls.page.driver.current_url else 'project'


class ProjectNoDescriptionFixture(UserFixture):

    @classmethod
    def setUpClass(cls):
        super(ProjectNoDescriptionFixture, cls).setUpClass()
        cls.page = cls.page.new_project(
            title='Test Project',
            description=None
        )


class DeleteProjectFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(DeleteProjectFixture, cls).setUpClass()
        cls.project_url = cls.page.driver.current_url
        cls.page = cls.page.settings.delete()


class DeleteProjectwithComponentFixture(ComponentOfProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(DeleteProjectwithComponentFixture, cls).setUpClass()
        cls.component_url = cls.page.driver.current_url
        cls.project_url = cls.page.parent_project().driver.current_url
        cls.page = cls.page.settings.delete()


class DeleteProjectwithSubprojectFixture(SubprojectFixture):
    @classmethod
    def setUpClass(cls):
        super(DeleteProjectwithSubprojectFixture, cls).setUpClass()
        cls.subproject_title = cls.page.title
        cls.subproject_url = cls.page.driver.current_url
        cls.project_url = cls.page.parent_project().driver.current_url
        cls.page = cls.page.settings.delete()