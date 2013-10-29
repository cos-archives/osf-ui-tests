from nose.tools import *

from tests.fixtures import UserFixture, OsfBaseFixture
from tests.user_accounts.fixtures import LoginUserFixture
import util


class UserLoginCorrect(LoginUserFixture):
    def test_login(self):
        self.log_in()
        assert_true(self.page.logged_in)


