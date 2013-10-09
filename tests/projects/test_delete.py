from nose.tools import *

from tests.fixtures import ProjectFixture


class DeleteTests(ProjectFixture):
    """This test case changes state"""
    def test_delete(self):
        self.page = self.page.settings.delete()

        assert_true(False)