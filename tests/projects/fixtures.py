from tests.fixtures import UserFixture, ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture


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