from nose.tools import *

from pages.auth import UserDashboardPage
from tests.fixtures import ProjectFixture
from tests.projects.fixtures import DeleteProjectwithComponentFixture
from tests.projects.fixtures import DeleteProjectwithSubprojectFixture
from tests.projects.fixtures import DeleteProjectFixture, ComponentDeleteFixture
from tests.projects.fixtures import SubprojectDeleteFixture, ComponentofSubprojectDeleteFixture

class Delete(object):
    def test_on_user_dashboard(self):
        assert_is_instance(self.page, UserDashboardPage)

    def test_deleted(self):
        assert_equal(0, len(self.page.projects))

    def test_on_project_not_found(self):
        self.page.driver.get(self.project_url)
        assert_in(
            "Resource deleted.",
            self.page.driver.find_element_by_css_selector(
                'div.row div.col-md-12 h2#error'
            ).text,
        )


class DeleteTests(Delete, DeleteProjectFixture):
    pass


class DeleteProjectwithComponent(Delete, DeleteProjectwithComponentFixture):
    def test_on_component_not_found(self):
        self.page.driver.get(self.component_url)
        assert_in(
            "Resource deleted.",
            self.page.driver.find_element_by_css_selector(
                'div.row div.col-md-12 h2#error'
            ).text,
        )


class DeleteProjectwithSubproject(Delete, DeleteProjectwithSubprojectFixture):
    def test_deleted(self):
        assert_equal(1, len(self.page.projects))


class Deletelog(object):
    def test_delete_node_log(self):
        assert_equal(
            u"{} removed {} {}".format(
                self.users[0].full_name,
                self.type,
                self.title
            ),
            self.page.logs[0].text
        )


class ComponentDeletelog(Deletelog, ComponentDeleteFixture):
    pass


class SubprojectDeletelog(Deletelog, SubprojectDeleteFixture):
    pass


class ComponentofSubprojectDeletelog(Deletelog, ComponentofSubprojectDeleteFixture):
    pass