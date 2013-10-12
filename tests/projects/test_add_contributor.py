from nose.tools import *

from pages.helpers import create_user
from tests.fixtures import ProjectFixture


class AddContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddContributorFixture, cls).setUpClass()

        cls.users.append(create_user())

        cls.page.add_contributor(cls.users[-1])


class ProjectAddContributorFixture(AddContributorFixture, ProjectFixture):
    pass


class Project(ProjectAddContributorFixture):
    def test_contributor_added(self):
        assert_equal(2, len(self.page.contributors))

    def test_logged(self):
        assert_equal(
            u'{} added {} to node {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )