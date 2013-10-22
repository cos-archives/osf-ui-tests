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
        cls.page.type = 'component' if 'node' in cls.page.driver.current_url else 'project'


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