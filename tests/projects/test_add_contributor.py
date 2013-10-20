import unittest

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


class ComponentOfProjectTest(AddContributorFixture, ComponentOfProjectFixture):

    def test_logged(self):
        assert_equal(
            u'{} added {} to component {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class ComponentOfSubprojectTest(AddContributorFixture, ComponentOfSubprojectFixture):

    def test_logged(self):
        assert_equal(
            u'{} added {} to component {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.title,
            ),
            self.page.logs[0].text,
        )