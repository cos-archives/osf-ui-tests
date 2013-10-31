from nose.tools import *

from pages.helpers import create_user
from tests.fixtures import ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture
from tests.components.fixtures import ComponentOfSubprojectFixture
import datetime as dt


class AddContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddContributorFixture, cls).setUpClass()

        cls.users.append(create_user())

        cls.page.add_contributor(cls.users[-1])

    def test_contributor_added(self):
        assert_equal(2, len(self.page.contributors))

    def test_logged(self):
        assert_equal(
            u'{} added {} to project {}'.format(
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


class ProjectAddContributor(AddContributorFixture, ProjectFixture):
    pass


class SubprojectAddContributor(AddContributorFixture, SubprojectFixture):
    pass


class ComponentOfProjectAddContributorTest(
    AddContributorFixture,
    ComponentOfProjectFixture
):

    def test_logged(self):
        assert_equal(
            u'{} added {} to component {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class ComponentOfSubprojectAddContributorTest(
    AddContributorFixture,
    ComponentOfSubprojectFixture
):

    def test_logged(self):
        assert_equal(
            u'{} added {} to component {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class AddMultiContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddMultiContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())

        cls.page.add_multi_contributor(cls.users[1], cls.users[2])

    def test_contributor_added(self):
        assert_equal(3, len(self.page.contributors))

    def test_logged(self):
        assert_equal(
            u'{} added {}, and {} to project {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.users[2].full_name,
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


class ProjectAddMultiContributor(AddMultiContributorFixture, ProjectFixture):
    pass


class SubprojectAddMultiContributor(AddMultiContributorFixture, SubprojectFixture):
    pass


class ComponentOfProjectAddMultiContributorTest(
    AddMultiContributorFixture,
    ComponentOfProjectFixture
):

    def test_logged(self):
        assert_equal(
            u'{} added {}, and {} to component {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.users[2].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class ComponentOfSubprojectAddMultiContributorTest(
    AddMultiContributorFixture,
    ComponentOfSubprojectFixture
):

    def test_logged(self):
        assert_equal(
            u'{} added {}, and {} to component {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.users[2].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class AddMultiContributorDeleteFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddMultiContributorDeleteFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())

        cls.page.add_multi_contributor_delete(cls.users[1], cls.users[2])

    def test_contributor_added(self):
        assert_equal(2, len(self.page.contributors))

    def test_logged(self):
        assert_equal(
            u'{} added {} to project {}'.format(
                self.users[0].full_name,
                self.users[2].full_name,
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
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )


class ProjectAddMultiContributorDelete(
    AddMultiContributorDeleteFixture,
    ProjectFixture
):
    pass


class SubprojectAddMultiContributorDelete(
    AddMultiContributorDeleteFixture,
    SubprojectFixture
):
    pass


class ComponentOfProjectAddMultiContributorDeleteTest(
    AddMultiContributorDeleteFixture,
    ComponentOfProjectFixture
):

    def test_logged(self):
        assert_equal(
            u'{} added {} to component {}'.format(
                self.users[0].full_name,
                self.users[2].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class ComponentOfSubprojectAddMultiContributorDeleteTest(
    AddMultiContributorDeleteFixture,
    ComponentOfSubprojectFixture
):

    def test_logged(self):
        assert_equal(
            u'{} added {} to component {}'.format(
                self.users[0].full_name,
                self.users[2].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )