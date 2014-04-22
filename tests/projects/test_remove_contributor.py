import httplib as http

from nose.tools import *

from pages.exceptions import HttpError
from tests.fixtures import ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture
from tests.components.fixtures import ComponentOfSubprojectFixture
from tests.projects.fixtures import RemoveContributorFixture, RemoveContributorAccessFixture
import datetime as dt


class RemoveContributorTests(RemoveContributorFixture):
    def test_contributor_removed(self):
        assert_equal(2, len(self.page.contributors))

    def test_logged(self):
        assert_equal(
            u'{} removed {} as a contributor from {} {}'.format(
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
            self.page.log_user_link(self.users[1]),
            self.page.logs[0].links[1].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.now(),
            delta=dt.timedelta(minutes=2)
        )


class ProjectRemoveContributor(RemoveContributorTests, ProjectFixture):
    pass


class SubprojectRemoveContributor(RemoveContributorTests, SubprojectFixture):
    pass


class ComponentOfProjectRemoveContributorTest(
    RemoveContributorTests,
    ComponentOfProjectFixture
):
    pass


class ComponentOfSubprojectRemoveContributorTest(
    RemoveContributorTests,
    ComponentOfSubprojectFixture
):
    pass


class RemoveContributorAccessTests(RemoveContributorAccessFixture):
    def test_removed_contributor_access(self):
        with assert_raises(HttpError) as cm:
            page = self.page.node(self.old_id, self.project_id)
        assert_equal(http.FORBIDDEN, cm.exception.code)


class ProjectRemoveContributorAccess(RemoveContributorAccessTests, ProjectFixture):
    pass


class SubprojectRemoveContributorAccess(RemoveContributorAccessTests, SubprojectFixture):
    pass


class ComponentOfProjectRemoveContributorAccess(RemoveContributorAccessTests, ComponentOfProjectFixture):
    pass


class ComponentOfSubprojectRemoveContributorAccess(RemoveContributorAccessTests, ComponentOfSubprojectFixture):
    pass