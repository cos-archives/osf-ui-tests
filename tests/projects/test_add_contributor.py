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


class AddMultiContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddMultiContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())
        cls.page.add_multi_contributor(cls.users[1], cls.users[2])
        cls.page.type = 'component' if 'node' in cls.page.driver.current_url else 'project'


class AddMultiContributorTests(AddMultiContributorFixture):
    def test_contributor_added(self):
        assert_equal(3, len(self.page.contributors))

    def test_contributor_present(self):
        assert_equal(self.users[-1].full_name, self.page.contributors[-1].full_name)
        assert_equal(self.users[-2].full_name, self.page.contributors[-2].full_name)

    def test_logged(self):
        assert_equal(
            u'{} added {}, and {} to {} {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.users[2].full_name,
                self.page.type,
                self.page.title,
            ),
            self.page.logs[0].text,
        )


class ProjectAddMultiContributor(AddMultiContributorTests, ProjectFixture):
    """Test that multiple contributors were added to a project"""
    pass


class SubprojectAddMultiContributor(AddMultiContributorTests, SubprojectFixture):
    """Test that multiple contributors were added to a subproject"""
    pass


class ComponentOfProjectAddMultiContributorTest(AddMultiContributorTests, ComponentOfProjectFixture):
    """Test that multiple contributors were added to a project component"""
    pass


class ComponentOfSubprojectAddMultiContributorTest(AddMultiContributorTests, ComponentOfSubprojectFixture):
    """Test that multiple contributors were added to a subproject component"""
    pass


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