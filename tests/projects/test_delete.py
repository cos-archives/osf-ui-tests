from nose.tools import *

from pages.auth import UserDashboardPage
from tests.fixtures import ProjectFixture


class DeleteTests(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(DeleteTests, cls).setUpClass()
        cls.page = cls.page.settings.delete()

    def test_on_user_dashboard(self):
        assert_is_instance(self.page, UserDashboardPage)

    def test_deleted(self):
        assert_equal(0, len(self.page.projects))
