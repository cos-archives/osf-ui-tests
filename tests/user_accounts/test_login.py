from nose.tools import *

from tests.fixtures import UserTestCase


class CreateUserTestCase(UserTestCase):

    def test_login(self):
        assert_true(self.page.logged_in)