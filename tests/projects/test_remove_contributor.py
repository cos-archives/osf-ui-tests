from nose.tools import *

from pages.helpers import create_user
from tests.fixtures import ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture
from tests.components.fixtures import ComponentOfSubprojectFixture


class RemoveContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(RemoveContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())

        cls.page.add_multi_contributor(cls.users[1], cls.users[2])

        cls.page.remove_contributor(cls.users[1])

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


class ProjectRemoveContributor(RemoveContributorFixture, ProjectFixture):
    pass


class SubprojectRemoveContributor(RemoveContributorFixture, SubprojectFixture):
    pass


class ComponentOfProjectRemoveContributorTest(
    RemoveContributorFixture,
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
    RemoveContributorFixture,
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