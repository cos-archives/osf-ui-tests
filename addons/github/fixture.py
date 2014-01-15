from pages import FILES
from pages.helpers import create_user
from tests.fixtures import UserFixture, ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentFixture, ComponentOfProjectFixture, ComponentOfSubprojectFixture


class GithubaddonFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(GithubaddonFixture, cls).setUpClass()

        _url = cls.page.driver.current_url
        cls.page.settings.addon_selection("GitHub")
        cls.page.settings.set_repo()


