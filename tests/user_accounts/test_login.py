from nose.tools import *

from tests.fixtures import UserFixture


class LoginUserTestCase(UserFixture):

    def test_login(self):
        assert_true(self.page.logged_in)