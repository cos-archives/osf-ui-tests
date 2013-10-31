from nose.tools import *

from tests.fixtures import ProjectFixture, SubprojectFixture

from tests.components.fixtures import ComponentOfProjectFixture, ComponentOfSubprojectFixture
import datetime as dt


class Rename(object):

    @classmethod
    def setUpClass(cls):
        super(Rename, cls).setUpClass()
        cls.old_title = cls.page.title
        cls.page.title = 'Renamed Project'

    def test_title(self):
        assert_equal('Renamed Project', self.page.title)

    def test_log_text(self):
        assert_equal(
            u'{} changed the title from {} to {}'.format(
                self.users[0].full_name,
                self.old_title,
                self.page.title,
            ),
            self.page.logs[0].text,
        )

    def test_log_link_to_project(self):
        assert_equal(
            self.page.driver.current_url,
            self.page.logs[0].links[1].url,
        )

    def test_log_link_to_user_profile(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url,
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )

class ProjectTest(Rename, ProjectFixture):
    pass


class SubprojectTest(Rename, SubprojectFixture):
    pass


class ComponentOfProjectTest(Rename, ComponentOfProjectFixture):
    pass


class ComponentOfSubprojectTest(Rename, ComponentOfSubprojectFixture):
    pass