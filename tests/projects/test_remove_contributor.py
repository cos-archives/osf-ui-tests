import httplib as http

from nose.tools import *

from pages.exceptions import HttpError
from pages.helpers import create_user
from tests.fixtures import ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture
from tests.components.fixtures import ComponentOfSubprojectFixture
import datetime as dt


class RemoveContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(RemoveContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())

        cls.page.add_multi_contributor(cls.users[1], cls.users[2])

        cls.page.remove_contributor(cls.users[1])
        cls.old_id = cls.page.id

class RemoveContributorTests(RemoveContributorFixture):
    def test_contributor_removed(self):
        assert_equal(2, len(self.page.contributors))

    def test_logged(self):
        assert_equal(
            u'{} removed {} as a contributor from project {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
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
            dt.datetime.utcnow(),
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

    def test_logged(self):
        assert_equal(
            u'{} removed {} as a contributor from component {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class ComponentOfSubprojectRemoveContributorTest(
    RemoveContributorTests,
    ComponentOfSubprojectFixture
):

    def test_logged(self):
        assert_equal(
            u'{} removed {} as a contributor from component {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class RemoveContributorAccessFixture(RemoveContributorFixture):
    @classmethod
    def setUpClass(cls):
        super(RemoveContributorAccessFixture, cls).setUpClass()
        cls.page.log_out()
        cls.log_in(cls.users[1])
        with assert_raises(HttpError) as cls.cm:
            page = cls.page.node(cls.old_id, cls.project_id)


class RemoveContributorAccessTests(RemoveContributorAccessFixture):
    def test_removed_contributor_access(self):
        assert_equal(http.FORBIDDEN, self.cm.exception.code)


class ProjectRemoveContributorAccess(RemoveContributorAccessTests, ProjectFixture):
    pass


class SubprojectRemoveContributorAccess(RemoveContributorAccessTests, SubprojectFixture):
    pass


class ComponentOfProjectRemoveContributorAccess(RemoveContributorAccessTests, ComponentOfProjectFixture):
    pass


class ComponentOfSubprojectRemoveContributorAccess(RemoveContributorAccessTests, ComponentOfSubprojectFixture):
    pass