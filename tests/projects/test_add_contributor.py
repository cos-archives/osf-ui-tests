from nose.tools import *

from pages import LoginPage
from pages.helpers import create_user
from pages.project import ProjectPage
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
        cls.page.type = 'component' if 'node' in cls.page.driver.current_url else 'project'
        cls.old_id = cls.page.id


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
            self.page.log_user_link(self.users[1]),
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


class AddContributorAccessFixture(AddContributorFixture):
    @classmethod
    def setUpClass(cls):
        super(AddContributorAccessFixture, cls).setUpClass()
        cls.page.log_out()
        cls.log_in(cls.users[1])
        cls.page = cls.page.node(cls.old_id, cls.project_id)


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
        assert_equal(self.users[1].full_name, self.page.contributors[1].full_name)
        assert_equal(self.users[2].full_name, self.page.contributors[2].full_name)

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



class AddMultiContributorDeleteFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddMultiContributorDeleteFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())
        cls.page.add_multi_contributor_delete(cls.users[-2], cls.users[-1])
        cls.page.type = 'component' if 'node' in cls.page.driver.current_url else 'project'


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
            dt.datetime.utcnow(),
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
