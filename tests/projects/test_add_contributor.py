from nose.tools import *

from pages.project import ProjectPage, NodePage
from tests.fixtures import ProjectFixture, SubprojectFixture, ComplexProjectFixture
from tests.components.fixtures import ComponentOfProjectFixture, ComponentOfSubprojectFixture
from tests.projects.fixtures import AddContributorFixture, AddContributorAccessFixture, AddMultiContributorFixture, \
    AddMultiContributorDeleteFixture, AddContributorChildrenFixture , AddContributorImportFromParentFixture
import datetime as dt


class AddContributorTests(AddContributorFixture):
    def test_contributor_added(self):
        assert_equal(2, len(self.page.contributors))

    def test_contributor_present(self):
        assert_equal(self.users[-1].full_name, self.page.contributors[-1].full_name)

    def test_logged(self):
        assert_equal(
            u'{} added {} to {} {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.type,
                self.page.title,
            ),
            self.page.logs[0].text,
        )

    def test_project_links(self):
        assert_equal(
            self.page.driver.current_url,
            self.page.logs[0].links[2].url
        )

    def test_user_links(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url
        )
        assert_in(
            self.page.log_user_link(self.users[-1]),
            self.page.logs[0].links[1].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )


class ProjectTestCase(AddContributorTests, ProjectFixture):
    """Test that a contributor was added to a project"""
    pass


class SubprojectTestCase(AddContributorTests, SubprojectFixture):
    """Test that a contributor was added to a subproject"""
    pass


class ComponentOfProjectTestCase(AddContributorTests, ComponentOfProjectFixture):
    """Test that a contributor was added to a project component"""
    pass


class ComponentOfSubprojectTestCase(AddContributorTests, ComponentOfSubprojectFixture):
    """Test that a contributor was added to a subproject component"""
    pass


class AddContributorAccessTests(AddContributorAccessFixture):
    def test_contributor_access(self):
        assert_is_instance(self.page, ProjectPage)

    def test_contributor_present(self):
        assert_equal(self.users[1].full_name, self.page.contributors[1].full_name)


class ProjectAddContributorAccessTestCase(AddContributorAccessTests, ProjectFixture):
    pass


class SubprojectAddContributorAccessTestCase(AddContributorAccessTests, SubprojectFixture):
    pass


class ComponentOfProjectAddContributorAccessTestCase(AddContributorAccessTests, ComponentOfProjectFixture):
    pass


class ComponentOfSubprojectAddContributorAccessTestCase(AddContributorAccessTests, ComponentOfSubprojectFixture):
    pass


class AddMultiContributorTests(AddMultiContributorFixture):
    def test_contributor_added(self):
        assert_equal(3, len(self.page.contributors))

    def test_contributor_present(self):
        assert_equal(self.users[1].full_name, self.page.contributors[1].full_name)
        assert_equal(self.users[2].full_name, self.page.contributors[2].full_name)

    def test_logged(self):
        assert_equal(
            u'{} added {} and {} to {} {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.users[2].full_name,
                self.page.type,
                self.page.title,
            ),
            self.page.logs[0].text,
        )

    def test_project_links(self):
        assert_equal(
            self.page.driver.current_url,
            self.page.logs[0].links[3].url
        )

    def test_user_links(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url
        )
        assert_in(
            self.page.log_user_link(self.users[1]),
            self.page.logs[0].links[1].url
        )
        assert_in(
            self.page.log_user_link(self.users[2]),
            self.page.logs[0].links[2].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )


class ProjectAddMultiContributorTestCase(AddMultiContributorTests, ProjectFixture):
    """Test that multiple contributors were added to a project"""
    pass


class SubprojectAddMultiContributorTestCase(AddMultiContributorTests, SubprojectFixture):
    """Test that multiple contributors were added to a subproject"""
    pass


class ComponentOfProjectAddMultiContributorTestCase(AddMultiContributorTests, ComponentOfProjectFixture):
    """Test that multiple contributors were added to a project component"""
    pass


class ComponentOfSubprojectAddMultiContributorTestCase(AddMultiContributorTests, ComponentOfSubprojectFixture):
    """Test that multiple contributors were added to a subproject component"""
    pass


class AddMultiContributorDeleteTests(AddMultiContributorDeleteFixture):
    def test_contributor_added(self):
        assert_equal(2, len(self.page.contributors))

    def test_contributor_present(self):
        assert_equal(self.users[2].full_name, self.page.contributors[1].full_name)

    def test_logged(self):
        assert_equal(
            u'{} added {} to {} {}'.format(
                self.users[0].full_name,
                self.users[2].full_name,
                self.page.type,
                self.page.title,
            ),
            self.page.logs[0].text,
        )

    def test_project_links(self):
        assert_equal(
            self.page.driver.current_url,
            self.page.logs[0].links[2].url
        )

    def test_user_links(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url
        )
        assert_in(
            self.page.log_user_link(self.users[2]),
            self.page.logs[0].links[1].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.now(),
            delta=dt.timedelta(minutes=2)
        )


class ProjectAddMultiContributorDelete(AddMultiContributorDeleteTests, ProjectFixture):
    """Test that contributor deleted from "Add Contributors" page of project is not added"""
    pass


class SubprojectAddMultiContributorDelete(AddMultiContributorDeleteTests, SubprojectFixture):
    """Test that contributor deleted from "Add Contributors" page of subproject is not added"""
    pass


class ComponentOfProjectAddMultiContributorDelete(AddMultiContributorDeleteTests, ComponentOfProjectFixture):
    """Test that contributor deleted from "Add Contributors" page of project component is not added"""
    pass


class ComponentOfSubprojectAddMultiContributorDelete(AddMultiContributorDeleteTests, ComponentOfSubprojectFixture):
    """Test that contributor deleted from "Add Contributors" page of subproject component is not added"""
    pass


class AddContributorChildrenTests(AddContributorChildrenFixture):
    def test_contributor_in_subproject(self):
        self.page = self.page.node(self.subproject_id, self.old_id)
        assert_equal(self.users[-1].full_name, self.page.contributors[-1].full_name)

    def test_contributor_in_component(self):
        self.page = self.page.node(self.component_id, self.old_id)
        assert_equal(self.users[-1].full_name, self.page.contributors[-1].full_name)


class AddContributorChildrenProjectTestCase(AddContributorChildrenTests, ProjectFixture):
    pass


class AddContributorChildrenSubprojectTestCase(AddContributorChildrenTests, SubprojectFixture):
    pass


class AddContributorImportFromParentTests(AddContributorImportFromParentFixture):
    def test_contributor_added(self):
        assert_equal(3, len(self.page.contributors))

    def test_contributor_present(self):
        assert_equal(self.users[1].full_name, self.page.contributors[1].full_name)
        assert_equal(self.users[2].full_name, self.page.contributors[2].full_name)

    def test_logged(self):
        assert_equal(
            u'{} added {} and {} to {} {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.users[2].full_name,
                self.page.type,
                self.page.title,
            ),
            self.page.logs[0].text,
        )

    def test_project_links(self):
        assert_equal(
            self.page.driver.current_url,
            self.page.logs[0].links[3].url
        )

    def test_user_links(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url
        )
        assert_in(
            self.page.log_user_link(self.users[1]),
            self.page.logs[0].links[1].url
        )
        assert_in(
            self.page.log_user_link(self.users[2]),
            self.page.logs[0].links[2].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.now(),
            delta=dt.timedelta(minutes=2)
        )


class AddContributorImportFromParentSubprojectTestCase(
    AddContributorImportFromParentTests,
    SubprojectFixture
):
    pass


class AddContributorImportFromParentComponentTestCase(
    AddContributorImportFromParentTests,
    ComponentOfProjectFixture
):
    pass