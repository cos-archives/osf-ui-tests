from nose.tools import *

from pages.helpers import create_user
from tests.fixtures import ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture, ComponentOfSubprojectFixture


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